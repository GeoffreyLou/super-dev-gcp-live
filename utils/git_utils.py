import os
import requests
import subprocess
from loguru import logger 

class GitUtils:
    @staticmethod
    def run_command(command, cwd: str=None) -> str:
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
    def clone_repository(repository_url: str, local_path: str, github_access_token: str) -> None:
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
            GitUtils.run_command(["git", "config", "--global", "user.email", "Super-dev@users.noreply.github.com"], cwd=local_path)
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
    def pull_branch(local_path: str, branch_name: str) -> None:
        """
        Pull the latest changes from a branch.
        
        Parameters
        ----------
        local_path : str
            The local path of the repository.
        branch_name : str
            The name of the branch to pull from.
        
        Returns
        -------
        None
        """
        try:
            logger.info(f"Pulling latest changes from branch '{branch_name}'...")
            GitUtils.run_command(["git", "pull", "origin", branch_name], cwd=local_path)
            logger.info(f"Latest changes pulled from branch '{branch_name}'.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while pulling branch: {e}")
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
        
    @staticmethod
    def create_pull_request(
            repo_owner:str, 
            repo_name:str, 
            source_branch:str, 
            target_branch:str, 
            title:str, 
            body:str, 
            github_token:str
        ) -> dict:
        """
        Create a pull request on GitHub.

        Parameters
        ----------
        repo_owner : str
            The owner of the repository (e.g., "GeoffreyLou").
        repo_name : str
            The name of the repository (e.g., "gcp-super-dev-live").
        source_branch : str
            The branch to merge from (e.g., "feat/my-feature").
        target_branch : str
            The branch to merge into (e.g., "develop").
        title : str
            The title of the pull request.
        body : str
            The body/description of the pull request.
        github_token : str
            The GitHub Personal Access Token for authentication.

        Returns
        -------
        dict
            The response from the GitHub API.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "title": title,
            "head": source_branch,
            "base": target_branch,
            "body": body
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            logger.info(f"Pull request created successfully: {response.json().get('html_url')}")
            return response.json()
        else:
            logger.error(f"Failed to create pull request: {response.status_code} - {response.text}")
            response.raise_for_status()
            
    @staticmethod
    def merge_pull_request(
            repo_owner: str, 
            repo_name: str, 
            pull_number: int, 
            github_token: str
        ) -> dict:
        """
        Merge a pull request on GitHub.

        Parameters
        ----------
        repo_owner : str
            The owner of the repository.
        repo_name : str
            The name of the repository.
        pull_number : int
            The number of the pull request to merge.
        github_token : str
            The GitHub Personal Access Token for authentication.

        Returns
        -------
        dict
            The response from the GitHub API.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/merge"
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "commit_title": f"Merge PR #{pull_number}",
            "merge_method": "merge" 
        }

        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            logger.info(f"Pull request merged successfully: {response.json()}")
            return response.json()
        else:
            logger.error(f"Failed to merge pull request: {response.status_code} - {response.text}")
            response.raise_for_status()
            
    @staticmethod
    def delete_branch(local_path: str, branch_name: str) -> None:
        """
        Delete a branch in the local repository.
        
        Parameters
        ----------
        local_path : str
            The local path of the repository.
        branch_name : str
            The name of the branch to delete.
            
        Returns
        -------
        None
        """
        try:
            logger.info(f"Deleting branch '{branch_name}'...")
            GitUtils.run_command(["git", "branch", "-D", branch_name], cwd=local_path)
            logger.info(f"Branch '{branch_name}' deleted.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while deleting branch: {e}")
            raise
        
    @staticmethod
    def delete_remote_branch(
            repo_owner: str, 
            repo_name: str, 
            branch_name: str, 
            github_token: str
        ) -> None:
        """
        Delete a remote branch from a GitHub repository.

        Parameters
        ----------
        repo_owner : str
            The owner of the repository.
        repo_name : str
            The name of the repository.
        branch_name : str
            The name of the branch to delete (e.g., "feat/my-feature").
        github_token : str
            The GitHub Personal Access Token for authentication.

        Returns
        -------
        None
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{branch_name}"
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            logger.info(f"Branch '{branch_name}' deleted successfully from remote repository.")
        elif response.status_code == 404:
            logger.error(f"Branch '{branch_name}' not found in the repository.")
        else:
            logger.error(f"Failed to delete branch '{branch_name}': {response.status_code} - {response.text}")
            response.raise_for_status()