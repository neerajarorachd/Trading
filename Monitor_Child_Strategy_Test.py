# child.py
import sys
import json

def main():
    # Read argument
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    
    # Create a dictionary to return
    result = {
        "greeting": f"Hello, {name}!",
        "length": len(name)
    }
    
    # Print the dictionary as JSON
    print(json.dumps(result))

if __name__ == "__main__":
    main()