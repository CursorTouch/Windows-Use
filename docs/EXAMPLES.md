# Windows-Use Examples

This document provides practical examples of using Windows-Use for various automation tasks.

## Basic Usage

### Simple Task Automation
```python
from windows_use import Agent

# Create an agent with default settings
agent = Agent()

# Perform a simple task
result = agent.invoke("Open Notepad and type 'Hello World'")
print(f"Task completed: {result.is_done}")
print(f"Result: {result.answer}")
```

### Using Custom Instructions
```python
from windows_use import Agent

# Create an agent with custom behavior
instructions = [
    "Always ask for confirmation before deleting files",
    "Use keyboard shortcuts when available",
    "Explain each action clearly"
]

agent = Agent(instructions=instructions)
result = agent.invoke("Clean up my desktop by organizing files into folders")
```

## Advanced Configuration

### Using Different LLM Providers
```python
from windows_use import Agent
from windows_use.llms.openai import OpenAILLM
from windows_use.llms.google import GoogleLLM

# Using OpenAI GPT-4
openai_llm = OpenAILLM(model="gpt-4", api_key="your-api-key")
agent = Agent(llm=openai_llm)

# Using Google Gemini
google_llm = GoogleLLM(model="gemini-pro", api_key="your-api-key")
agent = Agent(llm=google_llm)
```

### Performance Optimization
```python
from windows_use import Agent
from windows_use.performance import configure_logging

# Enable performance logging
logger = configure_logging(
    level="INFO",
    enable_file_logging=True,
    enable_structured_logging=True
)

# Create optimized agent
agent = Agent(
    use_vision=True,  # Better element detection
    auto_minimize=True,  # Minimize distractions
    max_steps=15  # Limit execution time
)
```

## Common Use Cases

### File Management
```python
# Organize downloads folder
result = agent.invoke("""
    Go to the Downloads folder and organize files by type:
    - Create folders for Images, Documents, Videos, and Archives
    - Move files to appropriate folders based on their extensions
    - Delete any empty folders when done
""")

# Backup important documents
result = agent.invoke("""
    Create a backup of all Word documents from the Documents folder
    to a new folder called 'Document_Backup_2024' on the Desktop
""")
```

### Application Automation
```python
# Excel automation
result = agent.invoke("""
    Open Excel and create a new spreadsheet with the following data:
    - Column A: Names (John, Jane, Bob, Alice)
    - Column B: Ages (25, 30, 35, 28)
    - Column C: Cities (New York, London, Tokyo, Paris)
    Save the file as 'employee_data.xlsx' on the Desktop
""")

# Browser automation
result = agent.invoke("""
    Open Chrome and navigate to google.com
    Search for 'Python automation tools'
    Open the first 3 results in new tabs
    Bookmark all the tabs in a folder called 'Automation Research'
""")
```

### System Administration
```python
# System cleanup
result = agent.invoke("""
    Perform system maintenance:
    1. Empty the Recycle Bin
    2. Clear browser cache and cookies
    3. Run Disk Cleanup utility
    4. Check for Windows updates
""")

# Software management
result = agent.invoke("""
    Check if Google Chrome is installed
    If not installed, download and install the latest version
    If installed, check if it needs updating
""")
```

## Error Handling

### Basic Error Handling
```python
from windows_use import Agent
from windows_use.exceptions import WindowsUseError, LLMError

agent = Agent()

try:
    result = agent.invoke("Complex automation task")
    if result.is_done:
        print(f"Success: {result.answer}")
    else:
        print(f"Failed: {result.error}")
        
except LLMError as e:
    print(f"LLM Error: {e.message}")
    print(f"Provider: {e.details.get('provider')}")
    
except WindowsUseError as e:
    print(f"Windows-Use Error: {e.message}")
    print(f"Details: {e.details}")
```

### Retry Logic
```python
from windows_use.performance import RetryManager

retry_manager = RetryManager(max_retries=3, base_delay=1.0)

def execute_task():
    return agent.invoke("Potentially flaky task")

try:
    result = retry_manager.retry(execute_task)
    print(f"Task completed after retries: {result.answer}")
except Exception as e:
    print(f"Task failed after all retries: {e}")
```

## Testing and Debugging

### Debug Mode
```python
from windows_use import Agent
from windows_use.logging import configure_logging

# Enable debug logging
logger = configure_logging(level="DEBUG")

agent = Agent()

# The agent will now log detailed information about each step
result = agent.invoke("Debug this complex task")
```

### Performance Monitoring
```python
from windows_use.performance import get_cache_stats, cleanup_caches
import time

agent = Agent()

# Monitor performance
start_time = time.time()
result = agent.invoke("Performance test task")
execution_time = time.time() - start_time

print(f"Execution time: {execution_time:.2f} seconds")
print(f"Cache stats: {get_cache_stats()}")

# Clean up caches periodically
cleanup_caches()
```

## Integration Examples

### With Scheduling
```python
import schedule
import time
from windows_use import Agent

agent = Agent()

def daily_backup():
    """Perform daily backup task."""
    result = agent.invoke("""
        Create a backup of important files:
        1. Copy Documents folder to external drive
        2. Export browser bookmarks
        3. Save email attachments from today
    """)
    print(f"Backup completed: {result.is_done}")

# Schedule daily backup at 6 PM
schedule.every().day.at("18:00").do(daily_backup)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### With Web APIs
```python
import requests
from windows_use import Agent

def process_api_data():
    """Fetch data from API and process it with Windows-Use."""
    # Fetch data from API
    response = requests.get("https://api.example.com/data")
    data = response.json()
    
    # Process data with Windows-Use
    agent = Agent()
    result = agent.invoke(f"""
        Open Excel and create a report with this data: {data}
        Format it nicely with headers and charts
        Save as 'api_report.xlsx'
    """)
    
    return result

result = process_api_data()
print(f"Report generated: {result.is_done}")
```

### With Configuration Files
```python
import json
from windows_use import Agent

# Load configuration
with open('automation_config.json', 'r') as f:
    config = json.load(f)

# Create agent with config
agent = Agent(
    instructions=config['instructions'],
    max_steps=config['max_steps'],
    use_vision=config['use_vision']
)

# Execute tasks from config
for task in config['tasks']:
    result = agent.invoke(task['description'])
    print(f"Task '{task['name']}': {result.is_done}")
```

## Best Practices

### Task Design
```python
# Good: Specific and clear instructions
result = agent.invoke("""
    Open Calculator app
    Calculate 15% tip on $45.67
    Copy the result to clipboard
""")

# Avoid: Vague or ambiguous instructions
# result = agent.invoke("Do some math stuff")
```

### Resource Management
```python
from windows_use.performance import cleanup_caches

# Clean up resources after long-running tasks
agent = Agent()

try:
    for i in range(100):
        result = agent.invoke(f"Process item {i}")
        
        # Clean up every 10 iterations
        if i % 10 == 0:
            cleanup_caches()
            
finally:
    cleanup_caches()  # Final cleanup
```

### Logging and Monitoring
```python
from windows_use.logging import get_logger

logger = get_logger("my_automation")

def automated_workflow():
    """Example of well-logged automation workflow."""
    logger.info("Starting automated workflow")
    
    try:
        agent = Agent()
        
        # Log each major step
        logger.info("Step 1: Opening application")
        result1 = agent.invoke("Open the target application")
        
        logger.info("Step 2: Processing data")
        result2 = agent.invoke("Process the data according to requirements")
        
        logger.info("Step 3: Generating report")
        result3 = agent.invoke("Generate and save the final report")
        
        logger.info("Workflow completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}", exc_info=True)
        return False

success = automated_workflow()
print(f"Workflow success: {success}")
```

## Tips and Tricks

### Handling Dynamic Content
```python
# Use conditional logic for dynamic UIs
result = agent.invoke("""
    If a popup appears asking for confirmation, click 'Yes'
    Otherwise, proceed with the main task
    Wait for the page to load completely before continuing
""")
```

### Working with Multiple Applications
```python
# Coordinate between multiple applications
result = agent.invoke("""
    1. Copy data from Excel spreadsheet in cell A1:C10
    2. Switch to Word document
    3. Paste the data as a formatted table
    4. Switch back to Excel and save the file
    5. Return to Word and save the document
""")
```

### Using Keyboard Shortcuts
```python
# Leverage keyboard shortcuts for efficiency
result = agent.invoke("""
    Use Ctrl+A to select all text
    Use Ctrl+C to copy
    Use Alt+Tab to switch to the next application
    Use Ctrl+V to paste
    Use Ctrl+S to save
""")
```

These examples should help you get started with Windows-Use and understand its capabilities. Remember to adapt the examples to your specific use cases and requirements.