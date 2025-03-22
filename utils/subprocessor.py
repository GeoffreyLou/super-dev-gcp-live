import os
import subprocess
from loguru import logger 

class Subprocessor:
    def __init__(self, repo_url) -> None:
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
        self.repo_url = repo_url

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

    def git_authenticate(self, repo_url, local_path) -> None:
        """
        Clone a Git repository if it is not already done.
        
        Parameters
        ----------
        
        repo_url : str
            The URL of the Git repository.
        local_path : str
            The local path where the repository will be cloned.    
        
        Returns
        -------
        None
        """

        if os.path.exists(local_path) and os.path.isdir(local_path):
            logger.info(f"Repository already exists at {local_path}. Skipping clone.")
            return

        try:
            print(f"Clonage du dépôt {repo_url} dans {local_path}...")
            self._run_command(["git", "clone", repo_url, local_path])
        except subprocess.CalledProcessError as e:
            print(f"Error while cloning the repository: {e}.")
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