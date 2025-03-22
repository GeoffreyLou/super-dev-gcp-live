import os
import sys
from loguru import logger
from dotenv import load_dotenv
from utils.generate_changes import GenerateChanges

if __name__ == "__main__":
    
    # Load environment variables
    load_dotenv()
    data_folder_name = os.getenv("DATA_FOLDER_NAME", 'data')
    data_file_name = os.getenv("DATA_FILE_NAME", 'changes')
    
    try:
        changes = GenerateChanges(
            data_folder_name=data_folder_name,
            data_file_name=data_file_name
        )
        changes.generate_changes()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
    