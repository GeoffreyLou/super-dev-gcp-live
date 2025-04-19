import os
import sys
from loguru import logger
from dotenv import load_dotenv
from utils.generate_changes import GenerateChanges


if __name__ == "__main__":
        
    # Load environment variables
    load_dotenv()
    data_folder_name=os.getenv("DATA_FOLDER_NAME")
    data_file_name=os.getenv("DATA_FILE_NAME")
    repository_url=os.getenv("REPOSITORY_URL")
    user_email=os.getenv("USER_EMAIL")
    github_access_token=os.getenv("GITHUB_ACCESS_TOKEN")
    source_branch=os.getenv("SOURCE_BRANCH")
    target_branch=os.getenv("TARGET_BRANCH")
    prod_branch=os.getenv("PROD_BRANCH")
    repository_owner=os.getenv("REPOSITORY_OWNER")
    repository_name=os.getenv("REPOSITORY_NAME")
    
    try:
        # Start the workflow
        changes = GenerateChanges(
            data_folder_name=data_folder_name,
            data_file_name=data_file_name,
            repository_url=repository_url,
            user_email=user_email,
            github_access_token=github_access_token,
            repository_owner=repository_owner,
            repository_name=repository_name,
            source_branch=source_branch,
            target_branch=target_branch,
            prod_branch=prod_branch
        )
        changes.work_hard_workflow()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
    