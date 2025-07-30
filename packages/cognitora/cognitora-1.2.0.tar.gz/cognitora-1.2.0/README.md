# Cognitora Python SDK

The official Python SDK for Cognitora - Operating System for Autonomous AI Agents.

## Features

- **Code Interpreter**: Execute Python, JavaScript, and Bash code in secure sandboxed environments
- **Compute Platform**: Run containerized workloads with flexible resource allocation
- **Session Management**: Persistent sessions with state management
- **File Operations**: Upload and manipulate files in execution environments
- **Async Support**: Full async/await support for high-performance applications
- **Type Safety**: Comprehensive type hints and data validation

## Installation

```bash
pip install cognitora
```

## Quick Start

```python
from cognitora import Cognitora

# Initialize the client
client = Cognitora(api_key="your_api_key_here")

# Execute Python code
result = client.code_interpreter.execute(
    code="print('Hello from Cognitora!')",
    language="python"
)

print(f"Status: {result.data.status}")
for output in result.data.outputs:
    print(f"{output.type}: {output.data}")
```

## Authentication

Get your API key from the [Cognitora Dashboard](https://dashboard.cognitora.com) and set it:

```python
# Method 1: Pass directly
client = Cognitora(api_key="cog_1234567890abcdef")

# Method 2: Environment variable
import os
os.environ['COGNITORA_API_KEY'] = 'cog_1234567890abcdef'
client = Cognitora()  # Will use environment variable

# Method 3: Configuration file
client = Cognitora.from_config_file("~/.cognitora/config.json")
```

## Code Interpreter

### Basic Execution

```python
# Execute Python code
result = client.code_interpreter.execute(
    code="""
import numpy as np
import matplotlib.pyplot as plt

# Create data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title('Sine Wave')
plt.show()
""",
    language="python"
)

# Check results
print(f"Execution time: {result.data.execution_time_ms}ms")
for output in result.data.outputs:
    if output.type == "display_data":
        print(f"Generated plot: {len(output.data)} bytes")
    elif output.type == "stdout":
        print(f"Output: {output.data}")
```

### Working with Sessions

```python
# Create a persistent session
session = client.code_interpreter.create_session(
    language="python",
    timeout_minutes=60,
    resources={
        "cpu_cores": 2,
        "memory_mb": 2048,
        "storage_gb": 10
    }
)

# Execute code in session (variables persist)
result1 = client.code_interpreter.execute(
    code="x = 42; y = 'Hello World'",
    session_id=session.data.session_id
)

result2 = client.code_interpreter.execute(
    code="print(f'x = {x}, y = {y}')",
    session_id=session.data.session_id
)

# Variables are maintained across executions
print(result2.data.outputs[0].data)  # Output: x = 42, y = Hello World
```

### File Operations

```python
from cognitora import FileUpload

# Prepare files
files = [
    FileUpload(
        name="data.csv",
        content="name,age,city\nJohn,30,NYC\nJane,25,LA",
        encoding="string"
    ),
    FileUpload(
        name="script.py",
        content="import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.head())",
        encoding="string"
    )
]

# Execute with files
result = client.code_interpreter.run_with_files(
    code="exec(open('script.py').read())",
    files=files,
    language="python"
)
```

### Data Science Example

```python
# Create a data science session with pre-configured environment
session = client.code_interpreter.create_session(
    language="python",
    timeout_minutes=120,
    environment={
        "PYTHONPATH": "/opt/conda/lib/python3.11/site-packages"
    },
    resources={
        "cpu_cores": 4,
        "memory_mb": 8192,
        "storage_gb": 20
    }
)

# Perform data analysis
analysis_code = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Generate sample data
np.random.seed(42)
data = {
    'feature1': np.random.normal(0, 1, 1000),
    'feature2': np.random.normal(2, 1.5, 1000),
    'target': np.random.choice([0, 1], 1000)
}
df = pd.DataFrame(data)

# Create correlation matrix
correlation_matrix = df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Matrix')
plt.show()

# Summary statistics
print("Dataset Summary:")
print(df.describe())
"""

result = client.code_interpreter.execute(
    code=analysis_code,
    session_id=session.data.session_id
)
```

## Compute Platform

### Basic Container Execution

```python
# Run a simple container
execution = client.compute.create_execution(
    image="python:3.11-slim",
    command=["python", "-c", "print('Hello from container!')"],
    cpu_cores=1.0,
    memory_mb=512,
    max_cost_credits=5
)

print(f"Execution ID: {execution.id}")
print(f"Status: {execution.status}")
```

### Machine Learning Training

```python
# Run ML training job
training_script = """
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Generate dataset
X, y = make_classification(n_samples=10000, n_features=20, n_classes=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy:.4f}')

# Save model
joblib.dump(model, '/tmp/model.pkl')
print('Model saved to /tmp/model.pkl')
"""

execution = client.compute.create_execution(
    image="python:3.11-slim",
    command=[
        "sh", "-c",
        f"pip install scikit-learn joblib && python -c \"{training_script}\""
    ],
    cpu_cores=2.0,
    memory_mb=4096,
    storage_gb=10,
    max_cost_credits=50,
    timeout_seconds=1800  # 30 minutes
)

# Wait for completion and get results
completed_execution = client.compute.wait_for_completion(execution.id)
logs = client.compute.get_execution_logs(execution.id)
print(f"Training completed with status: {completed_execution.status}")
print(f"Logs:\n{logs}")
```

### GPU Workload

```python
# Run GPU-accelerated computation
gpu_execution = client.compute.create_execution(
    image="tensorflow/tensorflow:latest-gpu",
    command=[
        "python", "-c", """
import tensorflow as tf
print('TensorFlow version:', tf.__version__)
print('GPU available:', tf.config.list_physical_devices('GPU'))

# Simple GPU computation
with tf.device('/GPU:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    c = tf.matmul(a, b)
    print('Matrix multiplication result:', c.numpy())
"""
    ],
    cpu_cores=2.0,
    memory_mb=8192,
    gpu_count=1,
    max_cost_credits=100
)
```

## Async Support

```python
import asyncio
from cognitora import CognitoraAsync

async def main():
    async with CognitoraAsync(api_key="your_api_key") as client:
        # Parallel execution
        tasks = [
            client.code_interpreter.execute(
                code=f"import time; time.sleep(1); print('Task {i} completed')",
                language="python"
            )
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks)
        
        for i, result in enumerate(results):
            print(f"Task {i}: {result.data.outputs[0].data}")

# Run async code
asyncio.run(main())
```

## Error Handling

```python
from cognitora import CognitoraError, AuthenticationError, RateLimitError

try:
    result = client.code_interpreter.execute(
        code="raise ValueError('Test error')",
        language="python"
    )
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded, please wait")
except CognitoraError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Response data: {e.response_data}")
```

## Configuration

### Environment Variables

```bash
export COGNITORA_API_KEY="your_api_key_here"
export COGNITORA_BASE_URL="https://api.cognitora.dev"  # Optional
export COGNITORA_TIMEOUT="30"  # Optional, seconds
```

### Configuration File

Create `~/.cognitora/config.json`:

```json
{
  "api_key": "your_api_key_here",
  "base_url": "https://api.cognitora.dev",
  "timeout": 30
}
```

## Best Practices

### 1. Resource Management

```python
# Always specify appropriate resources
session = client.code_interpreter.create_session(
    language="python",
    timeout_minutes=30,  # Don't set too high
    resources={
        "cpu_cores": 1.0,    # Start small
        "memory_mb": 1024,   # Adjust based on needs
        "storage_gb": 5      # Minimum required
    }
)
```

### 2. Session Lifecycle

```python
# Create session
session = client.code_interpreter.create_session()

try:
    # Use session for multiple operations
    for code_snippet in code_snippets:
        result = client.code_interpreter.execute(
            code=code_snippet,
            session_id=session.data.session_id
        )
        process_result(result)
finally:
    # Clean up
    client.code_interpreter.delete_session(session.data.session_id)
```

### 3. Error Recovery

```python
import time

def execute_with_retry(client, code, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.code_interpreter.execute(code=code)
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
        except CognitoraError as e:
            if e.status_code >= 500 and attempt < max_retries - 1:
                time.sleep(1)
                continue
            raise
```

## Advanced Examples

### Streaming Data Processing

```python
def process_large_dataset():
    session = client.code_interpreter.create_session(
        language="python",
        resources={"cpu_cores": 4, "memory_mb": 8192}
    )
    
    # Setup environment
    setup_code = """
import pandas as pd
import numpy as np
from typing import Iterator

def process_chunk(chunk_data: str) -> dict:
    # Process data chunk
    df = pd.read_csv(StringIO(chunk_data))
    return {
        'records': len(df),
        'mean': df.select_dtypes(include=[np.number]).mean().to_dict(),
        'null_counts': df.isnull().sum().to_dict()
    }
"""
    
    client.code_interpreter.execute(
        code=setup_code,
        session_id=session.data.session_id
    )
    
    # Process chunks
    results = []
    for chunk in data_chunks:
        result = client.code_interpreter.execute(
            code=f"result = process_chunk('''{chunk}''')\nprint(result)",
            session_id=session.data.session_id
        )
        results.append(result)
    
    return results
```

### Multi-Language Pipeline

```python
def ml_pipeline():
    session = client.code_interpreter.create_session(
        language="python",
        timeout_minutes=60
    )
    
    # Step 1: Data preparation (Python)
    data_prep = """
import pandas as pd
import numpy as np
import json

# Load and clean data
data = pd.read_csv('input.csv')
data_cleaned = data.dropna()
data_cleaned.to_csv('cleaned_data.csv', index=False)

# Generate metadata
metadata = {
    'original_rows': len(data),
    'cleaned_rows': len(data_cleaned),
    'columns': list(data.columns)
}

with open('metadata.json', 'w') as f:
    json.dump(metadata, f)
"""
    
    # Step 2: Feature engineering (Python)
    feature_eng = """
# Feature engineering
data = pd.read_csv('cleaned_data.csv')
# ... feature engineering code ...
data_features.to_csv('features.csv', index=False)
"""
    
    # Step 3: Visualization (Python)
    visualization = """
import matplotlib.pyplot as plt
import seaborn as sns

# Create visualizations
data = pd.read_csv('features.csv')
plt.figure(figsize=(15, 10))
# ... visualization code ...
plt.savefig('analysis.png', dpi=300, bbox_inches='tight')
"""
    
    # Execute pipeline
    steps = [data_prep, feature_eng, visualization]
    for i, step in enumerate(steps):
        result = client.code_interpreter.execute(
            code=step,
            session_id=session.data.session_id
        )
        print(f"Step {i+1} completed: {result.data.status}")
```

## API Reference

### CodeInterpreter Class

#### Methods

- `execute(code, language='python', session_id=None, files=None, timeout_seconds=60, environment=None)` - Execute code
- `create_session(language='python', timeout_minutes=60, environment=None, resources=None)` - Create session
- `list_sessions()` - List active sessions
- `get_session(session_id)` - Get session details
- `delete_session(session_id)` - Delete session
- `get_session_logs(session_id, limit=50, offset=0)` - Get session logs
- `run_python(code, session_id=None)` - Execute Python code
- `run_javascript(code, session_id=None)` - Execute JavaScript code
- `run_bash(command, session_id=None)` - Execute bash command
- `run_with_files(code, files, language='python', session_id=None)` - Execute with files

### Compute Class

#### Methods

- `create_execution(image, command, cpu_cores, memory_mb, max_cost_credits, **kwargs)` - Create execution
- `list_executions(limit=50, offset=0, status=None)` - List executions
- `get_execution(execution_id)` - Get execution details
- `cancel_execution(execution_id)` - Cancel execution
- `get_execution_logs(execution_id)` - Get execution logs
- `estimate_cost(cpu_cores, memory_mb, storage_gb=5, gpu_count=0, timeout_seconds=300)` - Estimate cost
- `wait_for_completion(execution_id, timeout_ms=300000, poll_interval_ms=5000)` - Wait for completion
- `run_and_wait(request, timeout_ms=None)` - Create and wait for execution

## Support

- **Documentation**: [docs.cognitora.com](https://docs.cognitora.com)
- **Support or get an early access**: [hello@cognitora.dev](mailto:hello@cognitora.dev)

## License

MIT License - see [LICENSE](LICENSE) file for details. 