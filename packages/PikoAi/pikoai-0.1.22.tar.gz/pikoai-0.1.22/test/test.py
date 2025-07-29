import sys
import os

# Add the Src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Src')))

from Env.python_executor import PythonExecutor

def read_test_script(filename):
    """Read the content of a test script file"""
    with open(filename, 'r') as file:
        return file.read()

def main():
    # Initialize the Python executor
    executor = PythonExecutor()
    
    # Get the full path to testscript1.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_script_path = os.path.join(script_dir, 'testscript2.txt')
    
    # Read the test script
    code = read_test_script(test_script_path)
    
    # Execute the code
    result = executor.execute(code)
    print(result)

if __name__ == "__main__":
    main()
