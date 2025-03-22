import os
import subprocess
from loguru import logger 

class Subprocessor:
    def __init__(self) -> None:
        """
        Constructor of the Processor class.

        Attributes
        ----------
        repo_url : str
            The URL of the Git repository.
            
        Returns
        -------
        None
        """

    def _run_command(self, command, cwd=None) -> str:
        """
        Execute a shell command and return the output.
        
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
            logger.info(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while executing command: {e.cmd} (return code: {e.returncode}): {e.stderr}")
            raise

    def git_authenticate(self, repository_url, local_path, github_access_token) -> None:
        """
        Clone a Git repository with authentication if it is not already done.
        
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
            self._run_command(["git", "clone", auth_repo_url, local_path])
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while cloning the repository: {e}.")
            raise

            
    def git_add_commit_push(self, local_path, commit_message) -> None:
        """
        Add, commit and push changes to the local repository.
        
        Parameters
        ----------
        local_path : str
            The local path of the repository.
        commit_message : str
            The commit message.
            
        Returns
        -------
        None
        """
        try:
            logger.info("Adding files...")
            self._run_command(["git", "add", "."], cwd=local_path)

            logger.info("Checking for changes to commit...")
            status_output = self._run_command(["git", "status", "--porcelain"], cwd=local_path)
            if not status_output.strip():
                logger.info("No changes to commit.")
                return

            logger.info(f"Creating commit with message: {commit_message}")
            self._run_command(["git", "commit", "-m", commit_message], cwd=local_path)

            logger.info("Pushing...")
            self._run_command(["git", "push"], cwd=local_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while committing or pushing: {e}")
            raise