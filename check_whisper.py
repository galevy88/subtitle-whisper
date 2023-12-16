import subprocess
import time

def run_whisper(file_name):
    start_time = time.time()
    
    # Construct the command to execute
    command = f'whisper "{file_name}" --model tiny'
    
    # Execute the command
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = time.time()
        
        # Output the result and the time taken
        print("Output:\n", result.stdout.decode())
        print("Errors:\n", result.stderr.decode())
        print(f"Time taken: {end_time - start_time} seconds")
        
        return result.returncode  # Returns 0 if command was successful
    except subprocess.CalledProcessError as e:
        # Handle the error
        end_time = time.time()
        print(f"An error occurred: {e}")
        print(f"Time taken: {end_time - start_time} seconds")
        return e.returncode

# Usage
run_whisper("palse.mp3")
