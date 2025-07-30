# chuk_llm/api/providers.py
"""
Dynamic provider function generation - everything from YAML
==========================================================

Generates functions like ask_openai_gpt4o(), ask_claude_sync(), etc.
All models, aliases, and providers come from YAML configuration.
"""

import asyncio
import re
import logging
import warnings
from typing import Dict, Optional, List, AsyncIterator, Union
from pathlib import Path
import base64

from chuk_llm.configuration.unified_config import get_config, Feature

logger = logging.getLogger(__name__)

# Suppress specific asyncio cleanup warnings that don't affect functionality
warnings.filterwarnings("ignore", message=".*Event loop is closed.*", category=RuntimeWarning)
warnings.filterwarnings("ignore", message=".*Task exception was never retrieved.*", category=RuntimeWarning)


def _run_sync(coro):
    """Simple sync wrapper using event loop manager"""
    try:
        # Try to import the event loop manager
        from .event_loop_manager import run_sync
        return run_sync(coro)
    except ImportError:
        # Fallback to simple asyncio.run if event loop manager not available
        import asyncio
        import warnings
        
        # Suppress warnings
        warnings.filterwarnings("ignore", message=".*Event loop is closed.*", category=RuntimeWarning)
        warnings.filterwarnings("ignore", message=".*Task exception was never retrieved.*", category=RuntimeWarning)
        
        try:
            asyncio.get_running_loop()
            raise RuntimeError(
                "Cannot call sync functions from async context. "
                "Use the async version instead."
            )
        except RuntimeError as e:
            if "Cannot call sync functions" in str(e):
                raise e
        
        # Use asyncio.run - each call gets a fresh loop and fresh client connections
        return asyncio.run(coro)


def _sanitize_name(name: str) -> str:
    """Convert any name to valid Python identifier
    
    Single rule: Convert to lowercase, replace separators with underscores,
    remove special chars, and merge alphabetic parts with short numeric parts.
    """
    if not name:
        return ""
    
    # Single rule approach
    sanitized = name.lower()
    
    # Replace all separators (dots, dashes, slashes, spaces) with underscores
    sanitized = re.sub(r'[-./\s]+', '_', sanitized)
    
    # Remove all non-alphanumeric characters except underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '', sanitized)
    
    # Consolidate multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # Split and apply simple merging rule
    parts = [p for p in sanitized.split('_') if p]
    
    if not parts:
        return ""
    
    # Single merging rule: alphabetic + short alphanumeric = merge
    merged_parts = []
    i = 0
    
    while i < len(parts):
        current = parts[i]
        
        if (i + 1 < len(parts) and 
            current.isalpha() and 
            len(parts[i + 1]) <= 3 and 
            any(c.isdigit() for c in parts[i + 1])):
            # Merge current with next
            merged_parts.append(current + parts[i + 1])
            i += 2
        else:
            merged_parts.append(current)
            i += 1
    
    result = '_'.join(merged_parts)
    
    # Handle leading digits
    if result and result[0].isdigit():
        result = f"model_{result}"
    
    return result.strip('_')


def _prepare_vision_message(prompt: str, image: Union[str, Path, bytes], provider: str = None) -> Dict[str, any]:
    """Prepare a vision message with text and image, handling provider-specific formats"""
    
    # First, get the image data and determine format
    image_data = None
    image_url = None
    media_type = 'image/jpeg'  # default
    
    if isinstance(image, (str, Path)):
        image_path = Path(image) if not isinstance(image, str) or not image.startswith(('http://', 'https://')) else None
        
        if image_path and image_path.exists():
            # Local file
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
                # Determine media type from extension
                suffix = image_path.suffix.lower()
                media_type = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp'
                }.get(suffix, 'image/jpeg')
                image_url = f"data:{media_type};base64,{image_data}"
                
        elif isinstance(image, str) and image.startswith(('http://', 'https://')):
            # URL - handle provider differences
            image_url = image
            
            # For providers that need base64 (like Anthropic), download the image
            if provider and 'anthropic' in provider.lower():
                try:
                    import urllib.request
                    import urllib.parse
                    from io import BytesIO
                    
                    # Download the image
                    with urllib.request.urlopen(image) as response:
                        image_bytes = response.read()
                        
                    # Try to determine media type from headers
                    content_type = response.headers.get('Content-Type', 'image/jpeg')
                    if 'image/' in content_type:
                        media_type = content_type
                    
                    # Convert to base64
                    image_data = base64.b64encode(image_bytes).decode('utf-8')
                    
                except Exception as e:
                    raise ValueError(f"Failed to download image from URL for Anthropic: {e}")
        else:
            raise ValueError(f"Image file not found: {image}")
            
    elif isinstance(image, bytes):
        # Raw bytes
        image_data = base64.b64encode(image).decode('utf-8')
        media_type = 'image/png'  # Default to PNG for bytes
        image_url = f"data:{media_type};base64,{image_data}"
    else:
        raise TypeError(f"Unsupported image type: {type(image)}")
    
    # Now format based on provider
    if provider and 'anthropic' in provider.lower():
        # Anthropic format - always needs base64 data
        if image_data is None and image_url:
            # Extract base64 from data URL if needed
            if image_url.startswith('data:'):
                # Extract base64 part
                base64_part = image_url.split(',')[1] if ',' in image_url else image_url
                image_data = base64_part
                # Extract media type
                media_type_match = re.match(r'data:([^;]+);', image_url)
                media_type = media_type_match.group(1) if media_type_match else 'image/jpeg'
        
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                }
            ]
        }
    else:
        # OpenAI/Gemini/others format - can use URLs directly
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url}
                }
            ]
        }
    
def _create_provider_function(provider_name: str, model_name: Optional[str] = None, supports_vision: bool = False):
    """Create async provider function with optional vision support"""
    if model_name:
        if supports_vision:
            async def provider_model_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, **kwargs) -> str:
                from .core import ask
                if image is not None:
                    vision_message = _prepare_vision_message(prompt, image, provider_name)
                    kwargs['messages'] = [vision_message]
                return await ask(prompt, provider=provider_name, model=model_name, **kwargs)
        else:
            async def provider_model_func(prompt: str, **kwargs) -> str:
                from .core import ask
                return await ask(prompt, provider=provider_name, model=model_name, **kwargs)
        return provider_model_func
    else:
        if supports_vision:
            async def provider_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, model: Optional[str] = None, **kwargs) -> str:
                from .core import ask
                if image is not None:
                    vision_message = _prepare_vision_message(prompt, image, provider_name)
                    kwargs['messages'] = [vision_message]
                return await ask(prompt, provider=provider_name, model=model, **kwargs)
        else:
            async def provider_func(prompt: str, model: Optional[str] = None, **kwargs) -> str:
                from .core import ask
                return await ask(prompt, provider=provider_name, model=model, **kwargs)
        return provider_func


def _create_stream_function(provider_name: str, model_name: Optional[str] = None, supports_vision: bool = False):
    """Create async streaming function with optional vision support"""
    if model_name:
        if supports_vision:
            async def stream_model_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, **kwargs) -> AsyncIterator[str]:
                from .core import stream
                if image is not None:
                    vision_message = _prepare_vision_message(prompt, image, provider_name)
                    kwargs['messages'] = [vision_message]
                async for chunk in stream(prompt, provider=provider_name, model=model_name, **kwargs):
                    yield chunk
        else:
            async def stream_model_func(prompt: str, **kwargs) -> AsyncIterator[str]:
                from .core import stream
                async for chunk in stream(prompt, provider=provider_name, model=model_name, **kwargs):
                    yield chunk
        return stream_model_func
    else:
        if supports_vision:
            async def stream_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, model: Optional[str] = None, **kwargs) -> AsyncIterator[str]:
                from .core import stream
                if image is not None:
                    vision_message = _prepare_vision_message(prompt, image, provider_name)
                    kwargs['messages'] = [vision_message]
                async for chunk in stream(prompt, provider=provider_name, model=model, **kwargs):
                    yield chunk
        else:
            async def stream_func(prompt: str, model: Optional[str] = None, **kwargs) -> AsyncIterator[str]:
                from .core import stream
                async for chunk in stream(prompt, provider=provider_name, model=model, **kwargs):
                    yield chunk
        return stream_func


def _create_sync_function(provider_name: str, model_name: Optional[str] = None, supports_vision: bool = False):
    """Create sync provider function with optional vision support"""
    if model_name:
        if supports_vision:
            def sync_model_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, **kwargs) -> str:
                from .core import ask
                if image is not None:
                    vision_message = _prepare_vision_message(prompt, image, provider_name)
                    kwargs['messages'] = [vision_message]
                return _run_sync(ask(prompt, provider=provider_name, model=model_name, **kwargs))
        else:
            def sync_model_func(prompt: str, **kwargs) -> str:
                from .core import ask
                return _run_sync(ask(prompt, provider=provider_name, model=model_name, **kwargs))
        return sync_model_func
    else:
        if supports_vision:
            def sync_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, model: Optional[str] = None, **kwargs) -> str:
                from .core import ask
                if model is not None:
                    kwargs['model'] = model
                if image is not None:
                    vision_message = _prepare_vision_message(prompt, image, provider_name)
                    kwargs['messages'] = [vision_message]
                return _run_sync(ask(prompt, provider=provider_name, **kwargs))
        else:
            def sync_func(prompt: str, model: Optional[str] = None, **kwargs) -> str:
                from .core import ask
                if model is not None:
                    kwargs['model'] = model
                return _run_sync(ask(prompt, provider=provider_name, **kwargs))
        return sync_func


def _create_global_alias_function(alias_name: str, provider_model: str, supports_vision: bool = False):
    """Create global alias function with optional vision support"""
    if '/' not in provider_model:
        logger.warning(f"Invalid global alias: {provider_model} (expected 'provider/model')")
        return {}
    
    provider, model = provider_model.split('/', 1)
    
    if supports_vision:
        async def alias_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, **kwargs) -> str:
            from .core import ask
            if image is not None:
                vision_message = _prepare_vision_message(prompt, image, provider)
                kwargs['messages'] = [vision_message]
            return await ask(prompt, provider=provider, model=model, **kwargs)
        
        def alias_sync_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, **kwargs) -> str:
            return _run_sync(alias_func(prompt, image=image, **kwargs))
        
        async def alias_stream_func(prompt: str, image: Optional[Union[str, Path, bytes]] = None, **kwargs) -> AsyncIterator[str]:
            from .core import stream
            if image is not None:
                vision_message = _prepare_vision_message(prompt, image, provider)
                kwargs['messages'] = [vision_message]
            async for chunk in stream(prompt, provider=provider, model=model, **kwargs):
                yield chunk
    else:
        async def alias_func(prompt: str, **kwargs) -> str:
            from .core import ask
            return await ask(prompt, provider=provider, model=model, **kwargs)
        
        def alias_sync_func(prompt: str, **kwargs) -> str:
            return _run_sync(alias_func(prompt, **kwargs))
        
        async def alias_stream_func(prompt: str, **kwargs) -> AsyncIterator[str]:
            from .core import stream
            async for chunk in stream(prompt, provider=provider, model=model, **kwargs):
                yield chunk
    
    return {
        f"ask_{alias_name}": alias_func,
        f"ask_{alias_name}_sync": alias_sync_func,
        f"stream_{alias_name}": alias_stream_func,
    }


def _generate_functions():
    """Generate all provider functions from YAML config"""
    config_manager = get_config()
    functions = {}
    
    providers = config_manager.get_all_providers()
    logger.info(f"Generating functions for {len(providers)} providers")
    
    # Generate provider functions
    for provider_name in providers:
        try:
            provider_config = config_manager.get_provider(provider_name)
        except ValueError as e:
            logger.error(f"Error loading provider {provider_name}: {e}")
            continue
        
        # Check if provider supports vision at all
        provider_supports_vision = Feature.VISION in provider_config.features
        
        # Base provider functions: ask_openai(), stream_openai(), ask_openai_sync()
        functions[f"ask_{provider_name}"] = _create_provider_function(provider_name, supports_vision=provider_supports_vision)
        functions[f"stream_{provider_name}"] = _create_stream_function(provider_name, supports_vision=provider_supports_vision)
        functions[f"ask_{provider_name}_sync"] = _create_sync_function(provider_name, supports_vision=provider_supports_vision)
        
        # Model-specific functions from YAML models list
        for model in provider_config.models:
            model_suffix = _sanitize_name(model)
            if model_suffix:
                # Check if this specific model supports vision
                model_caps = provider_config.get_model_capabilities(model)
                model_supports_vision = Feature.VISION in model_caps.features
                
                functions[f"ask_{provider_name}_{model_suffix}"] = _create_provider_function(provider_name, model, model_supports_vision)
                functions[f"stream_{provider_name}_{model_suffix}"] = _create_stream_function(provider_name, model, model_supports_vision)
                functions[f"ask_{provider_name}_{model_suffix}_sync"] = _create_sync_function(provider_name, model, model_supports_vision)
        
        # Alias functions from YAML model_aliases
        for alias, actual_model in provider_config.model_aliases.items():
            alias_suffix = _sanitize_name(alias)
            if alias_suffix:
                # Check if the actual model supports vision
                model_caps = provider_config.get_model_capabilities(actual_model)
                model_supports_vision = Feature.VISION in model_caps.features
                
                functions[f"ask_{provider_name}_{alias_suffix}"] = _create_provider_function(provider_name, actual_model, model_supports_vision)
                functions[f"stream_{provider_name}_{alias_suffix}"] = _create_stream_function(provider_name, actual_model, model_supports_vision)
                functions[f"ask_{provider_name}_{alias_suffix}_sync"] = _create_sync_function(provider_name, actual_model, model_supports_vision)
    
    # Generate global alias functions from YAML
    global_aliases = config_manager.get_global_aliases()
    for alias_name, provider_model in global_aliases.items():
        # Check if the aliased model supports vision
        if '/' in provider_model:
            provider, model = provider_model.split('/', 1)
            try:
                provider_config = config_manager.get_provider(provider)
                model_caps = provider_config.get_model_capabilities(model)
                alias_supports_vision = Feature.VISION in model_caps.features
            except:
                alias_supports_vision = False
        else:
            alias_supports_vision = False
            
        alias_functions = _create_global_alias_function(alias_name, provider_model, alias_supports_vision)
        functions.update(alias_functions)
    
    # Set function names and docstrings
    for name, func in functions.items():
        func.__name__ = name
        
        # Check if this is a vision-capable function
        has_image_param = 'image' in func.__code__.co_varnames
        
        if name.endswith("_sync"):
            base = name[:-5].replace("_", " ")
            if has_image_param:
                func.__doc__ = f"Synchronous {base} call with optional image support."
            else:
                func.__doc__ = f"Synchronous {base} call."
        elif name.startswith("ask_"):
            base = name[4:].replace("_", " ")
            if has_image_param:
                func.__doc__ = f"Async {base} call with optional image support."
            else:
                func.__doc__ = f"Async {base} call."
        elif name.startswith("stream_"):
            base = name[7:].replace("_", " ")
            if has_image_param:
                func.__doc__ = f"Stream from {base} with optional image support."
            else:
                func.__doc__ = f"Stream from {base}."
    
    logger.info(f"Generated {len(functions)} provider functions")
    return functions


def _create_utility_functions():
    """Create utility functions"""
    config_manager = get_config()
    
    def quick_question(question: str, provider: str = None) -> str:
        """Quick one-off question using sync API"""
        if not provider:
            settings = config_manager.get_global_settings()
            provider = settings.get("active_provider", "openai")
        
        from .sync import ask_sync
        return ask_sync(question, provider=provider)
    
    def compare_providers(question: str, providers: List[str] = None) -> Dict[str, str]:
        """Compare responses from multiple providers"""
        if not providers:
            all_providers = config_manager.get_all_providers()
            providers = all_providers[:3] if len(all_providers) >= 3 else all_providers
        
        from .sync import ask_sync
        results = {}
        
        for provider in providers:
            try:
                results[provider] = ask_sync(question, provider=provider)
            except Exception as e:
                results[provider] = f"Error: {str(e)}"
        
        return results
    
    def show_config():
        """Show current configuration status"""
        from chuk_llm.configuration.unified_config import get_config
        config = get_config()
        
        print("🔧 ChukLLM Configuration")
        print("=" * 30)
        
        providers = config.get_all_providers()
        print(f"📦 Providers: {len(providers)}")
        for provider_name in providers:
            try:
                provider = config.get_provider(provider_name)
                has_key = "✅" if config.get_api_key(provider_name) else "❌"
                print(f"  {has_key} {provider_name:<12} | {len(provider.models):2d} models | {len(provider.model_aliases):2d} aliases")
            except Exception as e:
                print(f"  ❌ {provider_name:<12} | Error: {e}")
        
        aliases = config.get_global_aliases()
        if aliases:
            print(f"\n🌍 Global Aliases: {len(aliases)}")
            for alias, target in list(aliases.items())[:5]:
                print(f"  ask_{alias}() -> {target}")
            if len(aliases) > 5:
                print(f"  ... and {len(aliases) - 5} more")
    
    return {
        'quick_question': quick_question,
        'compare_providers': compare_providers,
        'show_config': show_config,
    }


# Generate all functions at module import
logger.info("Generating dynamic provider functions from YAML...")

try:
    # Generate provider functions
    _provider_functions = _generate_functions()
    
    # Generate utility functions
    _utility_functions = _create_utility_functions()
    
    # Combine all functions
    _all_functions = {}
    _all_functions.update(_provider_functions)
    _all_functions.update(_utility_functions)
    
    # Add to module namespace
    globals().update(_all_functions)
    
    # Export all function names
    __all__ = list(_all_functions.keys())
    
    logger.info(f"Generated {len(_all_functions)} total functions")
    
    # Log some examples
    examples = [name for name in __all__ 
               if any(x in name for x in ['gpt4', 'claude', 'llama']) 
               and not name.endswith('_sync')][:5]
    if examples:
        logger.info(f"Example functions: {', '.join(examples)}")

except Exception as e:
    logger.error(f"Error generating provider functions: {e}")
    # Fallback - at least provide utility functions
    __all__ = ['show_config']
    
    def show_config():
        print(f"❌ Error loading configuration: {e}")
        print("Create a providers.yaml file to use ChukLLM")
    
    globals()['show_config'] = show_config

# Export all generated functions for external access
def get_all_functions():
    """Get all generated provider functions"""
    return _all_functions.copy() if '_all_functions' in globals() else {}

def list_provider_functions():
    """List all available provider functions"""
    if '_all_functions' not in globals():
        return []
    
    functions = list(_all_functions.keys())
    functions.sort()
    return functions

def has_function(name):
    """Check if a provider function exists"""
    return '_all_functions' in globals() and name in _all_functions

# Make all generated functions available for getattr
def __getattr__(name):
    """Allow access to generated functions"""
    if '_all_functions' in globals() and name in _all_functions:
        return _all_functions[name]
    raise AttributeError(f"module 'providers' has no attribute '{name}'")