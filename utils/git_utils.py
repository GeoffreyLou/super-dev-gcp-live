import os
import subprocess
from loguru import logger 

class GitUtils:
    
    @staticmethod
    def run_command(command, cwd: str) -> str:
        """
        Execute a shell command and return the output if required.
        
        Parameters
        ----------
        command : list
            The command to execute.
        cwd : str
            The current working directory.
            
        Returns
        -------
        str
            The output of the command.  
        """
        try:
            result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while executing command: {e.cmd} (return code: {e.returncode}): {e.stderr}")
            raise

    @staticmethod
    def clone_repository(repository_url: str, local_path: str,github_access_token: str) -> None:
        """
        Clone a Git repository with authentication.
        
        Parameters
        ----------
        repository_url : str
            The URL of the Git repository.
        local_path : str
            The local path where the repository will be cloned.
        github_access_token : str
            The personal access token for authentication.
        
        Returns
        -------
        None
        """
        if os.path.exists(local_path) and os.path.isdir(local_path):
            logger.info(f"Repository already exists at {local_path}. Skipping clone.")
            return

        # Inject the token into the repository URL
        if repository_url.startswith("https://"):
            auth_repo_url = repository_url.replace("https://", f"https://{github_access_token}@")
        else:
            raise ValueError("Unsupported repository URL format. Only HTTPS is supported.")

        try:
            logger.info(f"Cloning repository {repository_url} into {local_path}...")
            GitUtils.run_command(["git", "clone", auth_repo_url, local_path])
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while cloning the repository: {e}.")
            raise
        
    @staticmethod
    def config_user(local_path: str, user_email: str) -> None:
        """
        Configure the Git user name and email.
        
        Parameters
        ----------
        local_path : str
            The local path of the repository.
        user_email : str
            The email of the user.
        
        Returns
        -------
        None
        """
        try:
            logger.info("Configuring Git user...")
            GitUtils.run_command(["git", "config", "--global", "user.name", "Super-dev"], cwd=local_path)
            GitUtils.run_command(["git", "config", "--global", "user.email", user_email], cwd=local_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while configuring Git user: {e}.")
            raise

    @staticmethod
    def check_or_create_branch(local_path: str, branch_name: str) -> None:
        """
        Check if a branch exists in the local repository, and create it if it doesn't exist.
        
        Parameters
        ----------
        local_path : str
            The local path of the repository.
        branch_name : str
            The name of the branch to check or create.
        
        Returns
        -------
        None
        """
        try:
            logger.info(f"Checking if branch '{branch_name}' exists...")
            # Check if the branch exists
            branches = GitUtils.run_command(["git", "branch", "--list", branch_name], cwd=local_path)
            if branch_name in branches:
                logger.info(f"Branch '{branch_name}' already exists.")
                GitUtils.run_command(["git", "checkout", branch_name], cwd=local_path)
                logger.info(f"Working in branch '{branch_name}'.")
            else:
                logger.info(f"Branch '{branch_name}' does not exist. Creating it...")
                GitUtils.run_command(["git", "checkout", "-b", branch_name], cwd=local_path)
                logger.info(f"Branch '{branch_name}' created and checked out.")
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while checking or creating branch: {e}")
            raise     
        
    @staticmethod
    def add_commit_push(local_path: str, commit_message: str, branch_name: str) -> None:
        """
        Add, commit and push changes to the local repository.
        
        Parameters
        ----------
        local_path : str
            The local path of the repository.
        commit_message : str
            The commit message.
        branch_name : str
            The name of the branch to push to.
            
        Returns
        -------
        None
        """
        try:
            logger.info("Adding files...")
            GitUtils.run_command(["git", "add", "."], cwd=local_path)

            logger.info("Checking for changes to commit...")
            status_output = GitUtils.run_command(["git", "status", "--porcelain"], cwd=local_path)
            if not status_output.strip():
                logger.info("No changes to commit.")
                return

            logger.info(f"Creating commit with message: {commit_message}")
            GitUtils.run_command(["git", "commit", "-m", commit_message], cwd=local_path)

            logger.info("Pushing...")
            GitUtils.run_command(["git", "push", "--set-upstream", "origin", branch_name], cwd=local_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while committing or pushing: {e}")
            raise