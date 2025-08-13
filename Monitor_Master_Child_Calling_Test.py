# main.py
import subprocess
import json

# Parameter to send
param = "Alice"

# Run child.py and capture output
result = subprocess.run(
    ["python", "Monitor_Child_Strategy_Test.py", param],
    capture_output=True,
    text=True
)

# Parse JSON output
output_dict = json.loads(result.stdout)
print(output_dict)