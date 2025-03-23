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
            branch_name: str,
            user_email: str
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
        branch_name : str
            The branch name to commit the changes.
        user_email : str
            The email of the user to commit the changes.
            
        Returns
        -------
        None
        """
        self.repository_url = repository_url
        self.github_access_token = github_access_token
        self.branch_name = branch_name
        self.user_email = user_email
        self.data_folder = Path(data_folder_name)
        self.file_path = self.data_folder / f"{data_file_name}.txt"
        self.number_of_commits = random.randint(0, 10)
        
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
                commit_message = Faker().sentence(nb_words=8)
                sentences.append(commit_message)
            return sentences
        except Exception as e:
            logger.error(f"An error occurred while generating sentences: {e}")

    def clone_repository(self) -> None:
        """
        Clone the repository if it does not exist.
        
        Returns
        -------
        None
        """
        try:
            GitUtils.git_authenticate(
                repository_url=self.repository_url, 
                local_path=self.data_folder, 
                github_access_token=self.github_access_token
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

    def change_git_branch(self) -> None:
        """
        Change the branch of the repository.
        
        Returns
        -------
        None
        """
        try:
            GitUtils.git_check_or_create_branch(
                local_path=self.data_folder, 
                branch_name=self.branch_name
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
        
    def commit_changes(self, string_list: list) -> None:
        """
        Commit the changes to the repository.
        
        Parameters
        ----------
        string_list : list
            The list of strings to commit.
        
        Returns
        -------
        None
        """
        try:
            for string in string_list:
                self.file_path.write_text(string)
                GitUtils.git_add_commit_push(
                    local_path=self.data_folder, 
                    commit_message=string,
                    branch_name=self.branch_name
                )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

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
                
                # Change the branch
                GitUtils.check_or_create_branch(
                    local_path=self.data_folder, 
                    branch_name=self.branch_name
                )

                # Generate sentences according to number of commits
                sentences = self.generate_sentences(
                    number_of_sentences=self.number_of_commits
                )
                
                # Commit each sentence written in the file
                for string in sentences:
                    self.file_path.write_text(string)
                    GitUtils.add_commit_push(
                        local_path=self.data_folder, 
                        commit_message=string,
                        branch_name=self.branch_name
                    )
                
                logger.success(f'I worked hard today with {self.number_of_commits} commits.')
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                raise
        else: 
            logger.info("I'm a lazy developer, I may work tomorrow.")