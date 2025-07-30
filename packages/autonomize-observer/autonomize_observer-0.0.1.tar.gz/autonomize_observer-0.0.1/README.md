# Autonomize Observer

A comprehensive SDK for monitoring, tracing, and tracking costs for LLM applications with deep MLflow integration.

## Features

- **Automated LLM Monitoring**: Automatically monitor API calls for clients like OpenAI and Anthropic.
- **End-to-End Agent Tracing**: Trace complex, multi-step agent or flow executions, capturing performance, costs, and data at each step.
- **Centralized Cost Tracking**: Consolidate token usage and costs from multiple LLM calls within a single agent run.
- **Rich MLflow Integration**: Log traces, metrics, parameters, and artifacts to MLflow for powerful experiment tracking and visualization.
- **Async First**: Designed for modern, asynchronous applications.

## Installation

Install the package using pip:

```bash
pip install autonomize-observer
```

### With Provider-Specific Dependencies

```bash
# For OpenAI support
pip install "autonomize-observer[openai]"

# For Anthropic support
pip install "autonomize-observer[anthropic]"

# For both OpenAI and Anthropic
pip install "autonomize-observer[openai,anthropic]"
```

## Core Features

### 1. Automated LLM Monitoring

Wrap your LLM client with `monitor` to automatically track every API call, including performance, token usage, and costs. This is ideal for scenarios where you want detailed logs for each individual LLM interaction.

```python
import os
from openai import OpenAI
from autonomize_observer import monitor

# Set your MLflow tracking URI if not using a local server
# os.environ["MLFLOW_TRACKING_URI"] = "https://your-mlflow-server.com"

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Enable monitoring
# The first argument is the client, and the experiment_name is for MLflow.
monitor(client, experiment_name="Monitored LLM Calls")

# Use the client as normal - every call is now tracked in MLflow
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the capital of France?"}]
)
print(response.choices[0].message.content)
```

### 2. End-to-End Agent and Flow Tracing

For complex, multi-step processes like LangChain agents, the `MLflowLangflowTracer` provides a powerful way to capture the entire execution in a single, coherent trace. It automatically consolidates metrics from all LLM calls made during the run.

See the full examples in the `examples/notebooks/` directory.

```python
import os
import uuid
import time
from openai import OpenAI
from autonomize_observer.tracing import MLflowLangflowTracer
from autonomize_observer import monitor

# Initialize tracer
tracer = MLflowLangflowTracer(
    trace_name='Multi-Step AI Workflow',
    trace_type='flow',
    project_name='autonomize-observer-demo',
    trace_id=uuid.uuid4()
)

# Wait for tracer to be ready
while not tracer.ready:
    time.sleep(0.1)

# Initialize OpenAI client with monitoring
client = OpenAI()
monitor(client, use_async=False)  # Use sync monitoring to respect tracer's run

try:
    # Step 1: Research Phase
    tracer.add_trace(
        trace_id="research_step",
        trace_name="Research Phase",
        trace_type="llm",
        inputs={"query": "machine learning applications"},
        metadata={"step": 1}
    )
    
    research_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a research assistant."},
            {"role": "user", "content": "Research machine learning applications in healthcare"}
        ],
        max_tokens=200
    )
    
    research_result = research_response.choices[0].message.content
    tracer.end_trace(trace_id="research_step", outputs={"result": research_result})
    
    # Step 2: Analysis Phase
    tracer.add_trace(
        trace_id="analysis_step", 
        trace_name="Analysis Phase",
        trace_type="llm",
        inputs={"research_data": research_result},
        metadata={"step": 2}
    )
    
    analysis_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a data analyst."},
            {"role": "user", "content": f"Analyze this research: {research_result}"}
        ],
        max_tokens=200
    )
    
    analysis_result = analysis_response.choices[0].message.content
    tracer.end_trace(trace_id="analysis_step", outputs={"result": analysis_result})
    
    # End the overall trace
    workflow_inputs = {"workflow_type": "multi_step_ai", "steps": 2}
    workflow_outputs = {
        "research": research_result,
        "analysis": analysis_result
    }
    
    tracer.end(
        inputs=workflow_inputs,
        outputs=workflow_outputs
    )
    
    print("✅ Workflow completed successfully!")
    print("🔗 Check your MLflow UI for comprehensive trace data")

except Exception as e:
    print(f"❌ Error in workflow: {e}")
    tracer.end(
        inputs=workflow_inputs,
        outputs={},
        error=e
    )
```

This will produce a single run in MLflow under your experiment, containing:
- A full, visual trace of the workflow's execution path.
- Consolidated metrics like `total_cost`, `total_tokens`, and `duration_seconds`.
- Detailed cost breakdowns and I/O artifacts.

## Quick Start

### Basic Usage with OpenAI

```python
import os
from openai import OpenAI
from autonomize_observer import monitor

# Set environment variables for authentication
os.environ["MLFLOW_TRACKING_URI"] = "https://your-mlflow-server.com"
# OR use Modelhub credentials:
# os.environ["MODELHUB_URI"] = "https://your-modelhub-url.com"
# os.environ["MODELHUB_AUTH_CLIENT_ID"] = "your-client-id"
# os.environ["MODELHUB_AUTH_CLIENT_SECRET"] = "your-client-secret"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Create OpenAI client
client = OpenAI()

# Enable monitoring (provider is auto-detected)
monitor(client)

# Use the client as normal - monitoring happens automatically
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}
    ]
)

print(response.choices[0].message.content)
```

### Using with Anthropic

```python
import os
import anthropic
from autonomize_observer import monitor

# Set environment variables
os.environ["MLFLOW_TRACKING_URI"] = "https://your-mlflow-server.com"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key"

# Create Anthropic client
client = anthropic.Anthropic()

# Enable monitoring with explicit provider specification
monitor(client, provider="anthropic")

# Use the client normally
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "What is machine learning?"}
    ]
)

print(response.content[0].text)
```

## Package Structure

The package is organized into the following modules:

- **`autonomize_observer.tracing`**: MLflow tracing and span management
- **`autonomize_observer.monitoring`**: Async monitoring, cost tracking, and client monitoring
- **`autonomize_observer.core`**: MLflow client management and core exceptions
- **`autonomize_observer.visualization`**: Cost visualization and dashboards
- **`autonomize_observer.utils`**: Logging utilities

## Examples

Comprehensive examples are available in the `examples/notebooks/` directory:

- **`01_basic_monitoring.ipynb`**: Basic client monitoring setup with OpenAI
- **`02_advanced_tracing.ipynb`**: MLflow Langflow Tracer usage with multi-step workflows
- **`03_cost_tracking.ipynb`**: Custom cost rate configuration and cost analysis

## Configuration

### Setting Up Credentials

The SDK supports different authentication methods:

#### Option 1: Direct MLflow Server
```python
import os
os.environ["MLFLOW_TRACKING_URI"] = "https://your-mlflow-server.com"
```

#### Option 2: Modelhub Integration
```python
import os
os.environ["MODELHUB_URI"] = "https://your-modelhub-url.com"
os.environ["MODELHUB_AUTH_CLIENT_ID"] = "your-client-id"
os.environ["MODELHUB_AUTH_CLIENT_SECRET"] = "your-client-secret"
```

### Custom Cost Rates

Configure custom cost rates for different models:

```python
from autonomize_observer.monitoring import CostTracker

# Define custom cost rates ($ per 1K tokens)
custom_rates = {
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    "claude-3-opus": {"input": 15.0, "output": 75.0},
    "my-custom-model": {"input": 0.25, "output": 0.75}
}

# Initialize cost tracker with custom rates
cost_tracker = CostTracker(cost_rates=custom_rates)
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MLFLOW_TRACKING_URI` | MLflow server URL | Yes (if not using Modelhub) |
| `MODELHUB_URI` | Modelhub server URL | Yes (if not using direct MLflow) |
| `MODELHUB_AUTH_CLIENT_ID` | Modelhub client ID | Yes (if using Modelhub) |
| `MODELHUB_AUTH_CLIENT_SECRET` | Modelhub client secret | Yes (if using Modelhub) |
| `AUTONOMIZE_EXPERIMENT_NAME` | Default experiment name | No |
| `OPENAI_API_KEY` | OpenAI API key | Yes (for OpenAI) |
| `ANTHROPIC_API_KEY` | Anthropic API key | Yes (for Anthropic) |

## License

Proprietary © Autonomize.ai