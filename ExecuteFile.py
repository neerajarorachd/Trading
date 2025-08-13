import psutil
import subprocess
import os
from LibConstants import Const

def is_script_running(script_name):
    """Check if a script with the given name is already running."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if not proc.info['cmdline'] == None:
                if script_name in proc.info['cmdline']:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def CallMonitorScript(scriptpath):
    #Strategy_Script = "Monitor_Trades_Strategy_921.py"
    
    result = subprocess.run(
    ["python", scriptpath],
    capture_output=False,
    text=True
    )

def run_Monitor_if_not_running(script_path):
    script_name = os.path.basename(script_path)
    
    if not is_script_running(script_name):
        print(f"Starting script: {script_name}")
        subprocess.Popen(['python', script_path])
        #CallMonitorScript(script_path)
    else:
        print(f"Script already running: {script_name}")


    

# def GetFilePath(file_name):
#     from pathlib import Path

#     # Absolute path of the current script
#     file_path = Path(file_name).resolve()
#     #file_path = Path(file_name).resolve().parent #for directory path
#     #script_path = Path(__file__).resolve()
#     return file_path
