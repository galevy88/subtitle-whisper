import subprocess
import time
import os
import shutil
import glob
from cloudwatch_logger import CloudWatchLogger as logger
import logging

def run_whisper(file_name, output_directory, model_type, uid):
    logger.log(f"Model type is: {model_type}", uid=uid)
    logger.log(f"File name is: {file_name}", uid=uid)
    start_time = time.time()

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    
    command = f'whisper "{file_name}" --model {model_type}'
    logger.log(f"Start Executing command: {command}", uid=uid)

    # Get the current working directory
    cwd = os.getcwd()

    # Execute the command
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = time.time()

        # Construct the search pattern for the .srt file in the current working directory
        srt_file_pattern = os.path.join(cwd, os.path.splitext(os.path.basename(file_name))[0] + '*.srt')
        srt_file_list = glob.glob(srt_file_pattern)

        if srt_file_list:
            # Assuming the first match is the desired file
            srt_file_path = srt_file_list[0]
            # Move the SRT file to the desired output directory
            shutil.move(srt_file_path, os.path.join(output_directory, os.path.basename(srt_file_path)))
        else:
            logger.log("No SRT file found.", uid=uid)
            return 1

        # Output the result and the time taken
        logger.log(f"{result.stdout.decode()}", uid=uid)
        logger.log(f"Time Taken For Whisper: {end_time - start_time} seconds", uid=uid)

        return result.returncode
    except subprocess.CalledProcessError as e:
        # Handle the error
        end_time = time.time()
        logger.log(f"An error occurred: {e}", uid=uid)
        logger.log(f"Time Taken For Whisper: {end_time - start_time} seconds", uid=uid)
        return e.returncode
