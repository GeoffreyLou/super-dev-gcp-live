import os
import sys
from loguru import logger
from dotenv import load_dotenv
from utils.generate_changes import GenerateChanges

if __name__ == "__main__":
    
    # Load environment variables
    load_dotenv()
    data_folder_name=os.getenv("DATA_FOLDER_NAME", 'data')
    data_file_name=os.getenv("DATA_FILE_NAME", 'changes')
    repository_url=os.getenv("REPOSITORY_URL")
    github_access_token=os.getenv("GITHUB_ACCESS_TOKEN")
    source_branch=os.getenv("SOURCE_BRANCH")
    user_email=os.getenv("USER_EMAIL")
    repository_owner=os.getenv("REPOSITORY_OWNER")
    repository_name=os.getenv("REPOSITORY_NAME")
    target_branch=os.getenv("TARGET_BRANCH")
    
    try:
        changes = GenerateChanges(
            data_folder_name=data_folder_name,
            data_file_name=data_file_name,
            repository_url=repository_url,
            github_access_token=github_access_token,
            user_email=user_email,
            repository_owner=repository_owner,
            repository_name=repository_name,
            source_branch=source_branch,
            target_branch=target_branch
        )
        changes.generate_changes()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
    