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
    repository_url = os.getenv("REPOSITORY_URL")
    github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    branch_name = os.getenv("BRANCH_NAME")
    user_email = os.getenv("USER_EMAIL")
    
    try:
        changes = GenerateChanges(
            data_folder_name=data_folder_name,
            data_file_name=data_file_name,
            repository_url=repository_url,
            github_access_token=github_access_token,
            branch_name=branch_name,
            user_email=user_email
        )
        changes.generate_changes()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
    