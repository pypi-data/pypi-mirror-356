import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path
from langchain_core.language_models.chat_models import BaseChatModel

# Import driver architecture
from .base_driver import BaseLLMDriver
from .openai_driver import OpenAIDriver
from .anthropic_driver import AnthropicDriver
from .gemini_driver import GoogleDriver

try:
    from langchain_core.messages import HumanMessage
    LANGCHAIN_CORE_AVAILABLE = True
except ImportError:
    LANGCHAIN_CORE_AVAILABLE = False

class LLMRouter:
    """
    Enhanced LLM Router that supports multiple providers and model policy configuration.
    Loads configuration from model_policy.yaml and routes to appropriate LLM providers.
    Uses driver architecture for provider-specific optimizations.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the router with model policy configuration and drivers."""
        self.config = self._load_model_policy(config_path)
        self._provider_cache = {}
        
        # Initialize drivers
        self._drivers = {
            "openai": OpenAIDriver(),
            "anthropic": AnthropicDriver(),
            "google": GoogleDriver()
        }
    
    def _load_model_policy(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load model policy from YAML configuration."""
        if config_path is None:
            # Default to project's model_policy.yaml
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            config_path = base_dir / "config" / "model_policy.yaml"
        
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"Warning: Model policy file not found at {config_path}. Using defaults.")
            return self._get_default_config()
        except yaml.YAMLError as e:
            print(f"Warning: Error parsing model policy YAML: {e}. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration when model_policy.yaml is not available."""
        return {
            "default": {
                "model": "gpt-4o-mini",
                "temperature": 0.0,
                "provider": "openai"
            },
            "models": {
                "gpt-4o-mini": {"provider": "openai", "api_key_env": "OPENAI_API_KEY"},
                "gpt-4o": {"provider": "openai", "api_key_env": "OPENAI_API_KEY"},
                "gpt-3.5-turbo": {"provider": "openai", "api_key_env": "OPENAI_API_KEY"}
            }
        }
    
    def _detect_provider(self, model_name: str) -> str:
        """Detect provider based on model name patterns."""
        model_lower = model_name.lower()
        
        if any(pattern in model_lower for pattern in ['gpt', 'openai']):
            return 'openai'
        elif any(pattern in model_lower for pattern in ['claude', 'anthropic']):
            return 'anthropic'
        elif any(pattern in model_lower for pattern in ['gemini', 'google']):
            return 'google'
        else:
            return 'openai'  # Default fallback
    
    def _check_api_key(self, provider: str) -> bool:
        """Check if required API key is available for the provider."""
        key_mapping = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY', 
            'google': 'GOOGLE_API_KEY'
        }
        
        required_key = key_mapping.get(provider)
        if required_key and not os.getenv(required_key):
            return False
        return True
    
    def get_llm_for_agent(self, agent_name: str) -> BaseChatModel:
        """
        Get an LLM instance configured for a specific agent.
        Uses agent-specific configuration from model_policy.yaml.
        """
        config = self._resolve_model_config(agent_name)
        
        # Check if API key is available for the provider
        if not self._check_api_key(config['provider']):
            raise ValueError(f"API key not found for provider: {config['provider']}")
        
        return self._create_llm_instance(config)
    
    def get_llm(self, model_name: str = None, temperature: float = None, agent_name: str = None) -> BaseChatModel:
        """
        Initializes and returns an LLM instance using model_policy.yaml configuration.
        Uses provided parameters or falls back to agent-specific or global defaults.
        """
        # If agent_name is provided but other params are None, use agent-specific config
        if agent_name and model_name is None and temperature is None:
            return self.get_llm_for_agent(agent_name)
        
        # Resolve model and temperature from policy configuration
        effective_model_name, effective_temperature = self._resolve_model_config_legacy(
            model_name, temperature, agent_name
        )
        
        # Detect provider for the model
        provider = self._detect_provider(effective_model_name)
        
        # Check API key availability
        if not self._check_api_key(provider):
            # Fallback to default provider if API key is missing
            fallback_config = self.config.get('default', {})
            effective_model_name = fallback_config.get('model', 'gpt-4o-mini')
            effective_temperature = fallback_config.get('temperature', 0.0)
            provider = fallback_config.get('provider', 'openai')
        
        # Create configuration dict
        config = {
            'model': effective_model_name,
            'temperature': effective_temperature,
            'provider': provider
        }
        
        # Create and return the appropriate LLM instance
        return self._create_llm_instance(config)
    
    def _resolve_model_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Resolve model configuration for a specific agent.
        Returns a dict with all config values, inheriting from defaults.
        """
        # Start with all default values
        default_config = self.config.get('default', {})
        config = default_config.copy()  # Copy all default values
        
        # Apply agent-specific configuration if available
        if agent_name:
            agent_config = self.config.get('agents', {}).get(agent_name, {})
            # Update config with any agent-specific overrides
            config.update(agent_config)
            
            # Auto-detect provider if not specified in either default or agent config
            if 'provider' not in config:
                config['provider'] = self._detect_provider(config.get('model', 'gpt-4o-mini'))
        
        return config
    
    def _resolve_model_config_legacy(self, model_name: str, temperature: float, agent_name: str) -> tuple[str, float]:
        """Resolve model name and temperature from configuration hierarchy (legacy method)."""
        # Start with defaults
        defaults = self.config.get('default', {})
        effective_model_name = defaults.get('model', 'gpt-4o-mini')
        effective_temperature = defaults.get('temperature', 0.0)
        
        # Apply agent-specific configuration if available
        if agent_name:
            agent_config = self.config.get('agents', {}).get(agent_name, {})
            if 'model' in agent_config:
                effective_model_name = agent_config['model']
            if 'temperature' in agent_config:
                effective_temperature = agent_config['temperature']
        
        # Override with explicit parameters
        if model_name is not None:
            effective_model_name = model_name
        if temperature is not None:
            effective_temperature = temperature
            
        return effective_model_name, effective_temperature
    
    def _create_llm_instance(self, config: Dict[str, Any]) -> BaseChatModel:
        """Create an LLM instance using the appropriate driver."""
        provider = config['provider']
        
        # Get the driver for this provider
        driver = self._drivers.get(provider)
        if not driver:
            raise ValueError(f"No driver available for provider: {provider}")
        
        # Use driver to create LLM instance
        return driver.create_llm(config)
    
    def get_supported_models(self, provider: str = None) -> Dict[str, List[str]]:
        """Get supported models for all providers or a specific provider."""
        if provider:
            driver = self._drivers.get(provider)
            if not driver:
                return {}
            return {provider: driver.get_supported_models()}
        
        # Return all supported models
        return {
            provider: driver.get_supported_models() 
            for provider, driver in self._drivers.items()
        }
    
    def get_model_capabilities(self, provider: str, model: str) -> Dict[str, Any]:
        """Get capabilities for a specific model."""
        driver = self._drivers.get(provider)
        if not driver:
            return {}
        return driver.get_model_capabilities(model)
    
    def estimate_cost(self, provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a specific model and token usage."""
        driver = self._drivers.get(provider)
        if not driver:
            return 0.0
        return driver.estimate_cost(model, input_tokens, output_tokens)
    
    def get_all_model_info(self) -> Dict[str, Dict[str, Any]]:
        """Get comprehensive information about all available models."""
        info = {}
        for provider, driver in self._drivers.items():
            info[provider] = {
                "models": driver.get_supported_models(),
                "capabilities": {
                    model: driver.get_model_capabilities(model)
                    for model in driver.get_supported_models()
                }
            }
        return info


# Create global router instance
_router_instance = None

def get_llm(model_name: str = None, temperature: float = None, agent_name: str = None) -> BaseChatModel:
    """
    Global function to get an LLM instance using the router.
    Provides backward compatibility with existing code.
    """
    global _router_instance
    if _router_instance is None:
        _router_instance = LLMRouter()
    return _router_instance.get_llm(model_name, temperature, agent_name)

# Example usage
if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY to be set for default gpt-4o-mini)
    try:
        print("Testing enhanced LLM Router with model_policy.yaml support")
        print("=" * 60)
        
        print("\n1. Testing get_llm with no parameters (should use defaults):")
        llm_default = get_llm()
        print(f"  ✓ LLM Type: {type(llm_default).__name__}")
        print(f"  ✓ Model: {llm_default.model_name}")
        print(f"  ✓ Temperature: {llm_default.temperature}")

        print("\n2. Testing get_llm with specified parameters:")
        llm_custom = get_llm(model_name="gpt-3.5-turbo", temperature=0.5)
        print(f"  ✓ LLM Type: {type(llm_custom).__name__}")
        print(f"  ✓ Model: {llm_custom.model_name}")
        print(f"  ✓ Temperature: {llm_custom.temperature}")

        print("\n3. Testing agent-specific configuration:")
        llm_codegen = get_llm(agent_name="codegen_agent")
        print(f"  ✓ LLM Type: {type(llm_codegen).__name__}")
        print(f"  ✓ Model: {llm_codegen.model_name}")
        print(f"  ✓ Temperature: {llm_codegen.temperature}")
        
        print("\n4. Testing agent with overrides:")
        llm_question = get_llm(agent_name="question_agent")
        print(f"  ✓ LLM Type: {type(llm_question).__name__}")
        print(f"  ✓ Model: {llm_question.model_name}")
        print(f"  ✓ Temperature: {llm_question.temperature}")

        print("\n5. Testing fallback behavior with non-existent model:")
        llm_fallback = get_llm(model_name="non-existent-model")
        print(f"  ✓ LLM Type: {type(llm_fallback).__name__}")
        print(f"  ✓ Model: {llm_fallback.model_name}")
        print(f"  ✓ Temperature: {llm_fallback.temperature}")

        # Test actual LLM invocation if API key is available
        if os.getenv("OPENAI_API_KEY") and LANGCHAIN_CORE_AVAILABLE:
            print("\n6. Testing actual LLM invocation:")
            response = llm_default.invoke([HumanMessage(content="Hello! Respond with just 'Working!'")])
            print(f"  ✓ LLM Response: {response.content}")
        else:
            print("\n6. Skipping LLM invocation test (OPENAI_API_KEY not set or langchain_core not available)")

    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during get_llm tests: {e}")
