import subprocess
import sys
import os

def main():
    base_path = os.path.dirname(__file__)
    exe_path = os.path.join(base_path, 'scylla_pd.exe')

    args = sys.argv[1:]
    
    result = subprocess.run([exe_path] + args)
    
    sys.exit(result.returncode)