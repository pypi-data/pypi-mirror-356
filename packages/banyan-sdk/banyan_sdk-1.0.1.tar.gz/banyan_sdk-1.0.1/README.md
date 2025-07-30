# Banyan SDK v1.0

A Python client SDK for integrating with Banyan (Prompt Stack Manager) - the platform for managing, versioning, and A/B testing your LLM prompts in production.

## ✨ Key Features

**Intuitive Workflow**: The SDK provides a clean, three-step workflow for production LLM applications:

- **`get_prompt()`** - Fetch prompts with automatic experiment routing
- **Your Model** - Use the prompt content with any LLM (OpenAI, Anthropic, etc.)
- **`log_prompt()`** - Log real-world usage with experiment context

**Production-Ready Workflow**:
```python
# 1. Get the prompt (with automatic experiment routing)
prompt_data = banyan.get_prompt("my-prompt", sticky_context={"user_id": "123"})

# 2. Use the prompt content with your model
output = your_model_function(prompt_data.content, user_input)

# 3. Log the result (experiment context included automatically)
banyan.log_prompt(input=user_input, output=output, prompt_data=prompt_data)
```

## 🚀 Features

- ** Real-world Usage Logging**: Track how your prompts perform in production
- ** A/B Testing & Experiments**: Automatic experiment routing with sticky users/sessions
- ** Asynchronous Background Logging**: Non-blocking operation with retry logic
- ** Offline Resilience**: Local queue for when your backend is temporarily unavailable
- ** API Key Authentication**: Secure communication with your Prompt Stack Manager instance
- ** Project-level Organization**: Support for multi-project setups
- ** Built-in Analytics**: Track performance metrics and experiment results
- ** HTTPS Support**: Secure communication with production instances

## Installation

```bash
pip install banyan-sdk
```

## Production Configuration

The SDK is pre-configured to work with the production Prompt Stack Manager instance at `https://banyan-smpms.ondigitalocean.app`. 

For production use:

1. **Set your API key as an environment variable** (recommended):
   ```bash
   export BANYAN_API_KEY=psk_your_api_key_here
   ```

2. **Configure the SDK** (base_url defaults to production):
   ```python
   import banyan
   
   banyan.configure(
       api_key=os.getenv('BANYAN_API_KEY'),
   )
   ```

## 🛠️ Quick Start

### 1. Configure the SDK

```python
import banyan

# Configure once at application startup
banyan.configure(
    api_key="psk_your_api_key_here",
    project_id="project_id" #optional
)
```

### 2. Basic Usage

```python
import banyan

prompt_data = banyan.get_prompt(name="prompt_name")

if prompt_data:
    # 2. Use with your model
    user_input = "Hello, I'm a new user!"
    output = your_model_function(prompt_data.content, user_input)
    
    # 3. Log the result
    banyan.log_prompt(
        input=user_input,
        output=output,
        prompt_data=prompt_data,  # Contains all prompt info
        model="gpt-3.5-turbo",
        metadata={"user_type": "new"}
    )

    banyan.flush(timeout=30)

```

### 3. Usage with Experiments

```python
import banyan

# 1. Get prompt with sticky context for experiments
prompt_data = banyan.get_prompt(
    "marketing-email",
    sticky_context={"user_id": "user_123"}  # Enables automatic experiment routing
)

# Check if we got an experiment version
experiment_context = prompt_data.get_experiment_context()
if experiment_context:
    print(f"🧪 Using experiment version: {experiment_context['experiment_id']}")
else:
    print(f"📋 Using default version: {prompt_data.version}")

# 2. Use with your model
output = your_model_function(prompt_data.content, user_input)

# 3. Log (experiment context automatically included)
banyan.log_prompt(
    input=user_input,
    output=output,
    prompt_data=prompt_data,  # Experiment info automatically handled
    model="gpt-4",
    duration_ms=execution_time
)

banyan.flush(timeout=30)
```

## 🧪 Experiment Features

### Automatic Experiment Detection

The SDK automatically detects running experiments when you provide `sticky_context`:

```python
# Different sticky strategies
prompt_data = banyan.get_prompt(
    "my-prompt",
    sticky_context={
        "user_id": "user_123",      # User-based experiments
        # OR
        "session_id": "session_456",  # Session-based experiments  
        # OR
        "input_hash": "content_hash"  # Content-based experiments
    }
)
```

### Experiment Routing

The SDK handles experiment routing automatically based on:
- **Traffic percentages** defined in your experiments
- **Sticky context** for consistent user experience
- **Hash-based distribution** for deterministic routing

### Experiment Logging

When logging with a `PromptData` object from an experiment:
- Experiment ID and version are automatically included
- Sticky context is preserved for analytics
- All routing decisions are tracked

## 🎯 Sticky Context Strategies

### User-based Experiments
```python
sticky_context = {"user_id": "user_123"}
```
Each user consistently gets the same experiment version.

### Content-based Experiments
```python
sticky_context = {"input_hash": content_hash}
```
Same content always gets the same version.

### Custom Sticky Keys
```python
sticky_context = {"customer_id": "enterprise_client_1"}
```
Any custom key for your specific use case.

## 📊 Monitoring & Analytics

### Get Statistics
```python
stats = banyan.get_stats()
print(f"Logs sent: {stats['logs_sent']}")
print(f"Queue size: {stats['queue_size']}")
```

### Flush Logs
```python
# Ensure all logs are sent before shutdown
banyan.flush(timeout=30)
```

### Graceful Shutdown
```python
# Clean shutdown with log flushing
banyan.shutdown(timeout=30)
```

## 🔧 Advanced Configuration

### Custom Logger Instance
```python
from banyan import PromptStackLogger

logger = PromptStackLogger(
    api_key="your_key",
    base_url="https://app.usebanyan.com",
    project_id="your_project",
    max_retries=5,
    retry_delay=2.0,
    queue_size=2000,
    flush_interval=10.0
)

prompt_data = logger.get_prompt("my-prompt")
logger.log_prompt(input="test", output="result", prompt_data=prompt_data)
```

### Synchronous Mode
```python
banyan.configure(
    api_key="your_key",
    background_thread=False  # Disable async processing
)

# All operations will be synchronous
success = banyan.log_prompt(
    input="test",
    output="result", 
    blocking=True  # Explicit blocking
)
```

## 🚨 Error Handling

```python
try:
    prompt_data = banyan.get_prompt("non-existent-prompt")
    if not prompt_data:
        print("Prompt not found")
        return
        
    # Use prompt...
    
except Exception as e:
    print(f"Error: {e}")
    # Handle gracefully
```

## 📝 Examples

See the [`production_example.py`](production_example.py) file for comprehensive examples including:
- Configuration
- Basic Logging workflow
- Automatic experiment routing including:
- Content-hash experiments
- User-based experiments

## 🔗 Links

- [Documentation](https://docs.banyan.dev) - Full documentation
- [GitHub Repository](https://github.com/banyan-team/banyan-sdk) - Source code

## 📄 License

MIT License - see LICENSE file for details. 