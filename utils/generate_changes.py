import random
from faker import Faker
from loguru import logger
from pathlib import Path
from .git_utils import GitUtils

class GenerateChanges: 
    """
    Generate random sentence in a file from 0 to 10 times.
    The sentence will allways overwrite the previous one.
    Each sentence is a commit message and will do a commit to a Github repository.
    """
    
    def __init__(
            self, 
            data_folder_name: str, 
            data_file_name: str,
            repository_url: str,
            github_access_token: str,
            user_email: str,
            repository_owner:str,
            repository_name:str,
            source_branch:str,
            target_branch:str
        ) -> None: 
        """
        Constructor of the GenerateChanges class.
        
        Attributes
        ----------
        data_folder_name : str
            The name of the folder where the file will be saved.
        data_file_name : str
            The name of the file where the commit messages will be saved.
            Be careuful, the .txt extension will be added automatically.
        repository_url : str
            The URL of the Git repository of this project.
        github_access_token : str
            The personal access token for authentication.
        user_email : str
            The email of the user to commit the changes.
        repository_owner : str
            The owner of the repository.
        repository_name : str
            The name of the repository.
        source_branch : str
            The source branch of the repository.
        target_branch : str
            The target branch of the repository.
            
        Returns
        -------
        None
        """
        self.repository_url = repository_url
        self.github_access_token = github_access_token
        self.user_email = user_email
        self.repository_owner=repository_owner
        self.repository_name=repository_name
        self.source_branch=source_branch
        self.target_branch=target_branch
        self.data_folder = Path(data_folder_name)
        self.file_path = self.data_folder / f"{data_file_name}.txt"
        self.number_of_commits = random.randint(1, 2)
        
    def _will_i_work_today(self) -> bool:
        """
        Check if the developer will work today.
        The number of commits must be greater than 0.
        
        Returns
        -------
        bool
            True if the developer will work today, False otherwise.
        """
        return True if self.number_of_commits > 0 else False 
    
    def generate_sentences(self, number_of_sentences: int) -> list:
        """
        Generate random sentence in a list according to number passed as parameter.
        
        Parameters
        ----------
        number_of_sentences : int
            The number of sentences to generate.
        
        Returns
        -------
        list
            The list of sentences.
        """

        try:
            sentences = []
            for _ in range(number_of_sentences):
                commit_message = f":rocket: feat: {Faker().sentence(nb_words=6)}"
                sentences.append(commit_message)
            return sentences
        except Exception as e:
            logger.error(f"An error occurred while generating sentences: {e}")


    def generate_changes(self) -> None:
        """
        Workflow to generate the changes in the repository.
        If the developer will work today, the repository will be cloned.
        The branch will be changed and the sentences will be generated and committed.
        Each commit will be pushed. 
        """
      
        if self._will_i_work_today():
            logger.info("I'm a super developer, I may work hard today.")   
        
            try:
                # Clone the repository and config
                GitUtils.clone_repository(
                    repository_url=self.repository_url, 
                    local_path=self.data_folder, 
                    github_access_token=self.github_access_token
                )
                
                GitUtils.config_user(
                    local_path=self.data_folder,
                    user_email=self.user_email
                )
                
                # Change the branch to develop (target branch)
                GitUtils.check_or_create_branch(
                    local_path=self.data_folder, 
                    branch_name=self.target_branch
                )
                
                # Pull
                GitUtils.pull_branch(
                    local_path=self.data_folder, 
                    branch_name=self.target_branch
                )
                
                # Create source branch
                GitUtils.check_or_create_branch(
                    local_path=self.data_folder, 
                    branch_name=self.source_branch
                )

                # Generate sentences according to number of commits
                sentences = self.generate_sentences(
                    number_of_sentences=self.number_of_commits
                )
                
                # Commit each sentence written in the file
                for string in sentences:
                    with self.file_path.open("a") as f:
                        f.write(string)
                    GitUtils.add_commit_push(
                        local_path=self.data_folder, 
                        commit_message=string,
                        branch_name=self.source_branch
                    )
                    
                # clear the file to avoir conflicts
                with self.file_path.open("w") as f:
                    f.write("")
                GitUtils.add_commit_push(
                    local_path=self.data_folder, 
                    commit_message=":rocket: feat: clear file",
                    branch_name=self.source_branch
                )
                
                # Create a pull request
                pr = GitUtils.create_pull_request(
                    repo_owner=self.repository_owner,
                    repo_name=self.repository_name,
                    source_branch=self.source_branch,
                    target_branch=self.target_branch,
                    title=":rocket: Super Dev is working hard today!",
                    body=f"I'm proud, I commited {self.number_of_commits} changes today.",
                    github_token=self.github_access_token
                )
                
                # Merge the pull request
                GitUtils.merge_pull_request(
                    repo_owner=self.repository_owner,
                    repo_name=self.repository_name,
                    pull_number=pr["number"],
                    github_token=self.github_access_token
                )
                
                # Change the branch to develop (target branch)
                GitUtils.check_or_create_branch(
                    local_path=self.data_folder, 
                    branch_name=self.target_branch
                )              
                
                # Delete branch
                GitUtils.delete_branch(
                    local_path=self.data_folder, 
                    branch_name=self.source_branch
                )
                
                # Create a pull request to merge develop into main
                final_pr = GitUtils.create_pull_request(
                    repo_owner=self.repository_owner,
                    repo_name=self.repository_name,
                    source_branch=self.target_branch,
                    target_branch="main",
                    title=":rocket: Super Dev is working hard today!",
                    body=f"I'm proud, I commited {self.number_of_commits} changes today.",
                    github_token=self.github_access_token
                )
                
                # Merge the pull request
                GitUtils.merge_pull_request(
                    repo_owner=self.repository_owner,
                    repo_name=self.repository_name,
                    pull_number=final_pr["number"],
                    github_token=self.github_access_token
                )
                
                # Delete remote branch
                GitUtils.delete_remote_branch(
                    repo_owner=self.repository_owner,
                    repo_name=self.repository_name,
                    branch_name=self.source_branch,
                    github_token=self.github_access_token
                )
                
                logger.success(f'I worked hard today with {self.number_of_commits} commits.')
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                raise
        else: 
            logger.info("I'm a lazy developer, I may work tomorrow.")