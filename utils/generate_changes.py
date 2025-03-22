import random
from faker import Faker
from loguru import logger
from pathlib import Path
from .subprocessor import Subprocessor

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
            github_access_token: str
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
            
        Returns
        -------
        None
        """
        self.repository_url = repository_url
        self.github_access_token = github_access_token
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
    
    def generate_commits(self) -> None:
        """
        Generate random sentence in a file from 0 to 10 times.
        
        Returns
        -------
        None
        """
        if self._will_i_work_today():
            logger.info("I'm a super developer, I may work hard today.")
            for _ in range(self.number_of_commits):
                commit_message = Faker().sentence(nb_words=8)
                self.file_path.write_text(commit_message)
            logger.info(f'I made {self.number_of_commits} commits today, time to rest.')
        else: 
            logger.info("I'm a lazy developer, I may work tomorrow.")
            
    def generate_changes(self) -> None:
        
        sub = Subprocessor
        sub.git_authenticate(
            repository_url=self.repository_url, 
            local_path=self.data_folder, 
            github_access_token=self.github_access_token
        )