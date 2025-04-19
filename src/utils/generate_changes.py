import random
from faker import Faker
from pathlib import Path
from loguru import logger
from datetime import datetime
from utils.git_utils import GitUtils


class GenerateChanges: 
    """
    Generate random sentence in a file from 0 to 10 times.
    Each sentence is a commit message and will do a commit to a Github repository.
    """
    
    def __init__(
            self, 
            data_folder_name: str, 
            data_file_name: str,
            repository_url: str,
            user_email: str,
            github_access_token: str,
            repository_owner:str,
            repository_name:str,
            source_branch:str,
            target_branch:str,
            prod_branch:str
        ) -> None: 
        """
        Constructor of the GenerateChanges class.
        
        Attributes
        ----------
        data_folder_name : str
            The name of the folder where the file will be saved.
        data_file_name : str
            The name of the file where the commit messages will be saved.
            Be careful, the .txt extension will be added automatically.
        repository_url : str
            The URL of the Git repository of this project.
        user_email : str
            The email of the user who will be used to commit the changes.
        github_access_token : str
            The personal access token for authentication.
        repository_owner : str
            The owner of the repository.
        repository_name : str
            The name of the repository.
        source_branch : str
            The source branch of the repository e.g. "feature/branch_name".
        target_branch : str
            The target branch of the repository e.g. "develop".
        prod_branch : str
            The production branch of the repository e.g. "main".
        """
        project_root = Path(__file__).resolve().parent.parent
        self.data_folder = project_root / data_folder_name
        self.file_path = self.data_folder / f"{data_file_name}.txt"
        self.number_of_commits = random.randint(1, 20)
        self.repository_url = repository_url
        self.user_email = user_email
        self.github_access_token = github_access_token
        self.repository_owner=repository_owner
        self.repository_name=repository_name
        self.source_branch=source_branch
        self.target_branch=target_branch
        self.prod_branch=prod_branch
        
    def __is_new_month(self, date: datetime) -> bool:
        """
        Check if the given date is the first day of the month.
        
        Returns
        -------
        bool
            True if the date is the first day of the month, False otherwise.
        """
        return date.day == 1
    
    def __generate_sentences(self, number_of_sentences: int) -> list:
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
        faker = Faker()
        return [f":rocket: feat: {faker.sentence(nb_words=6)}" for _ in range(number_of_sentences)]
        
    def __clone_and_configure(self) -> None:
        """
        Clone the repository and configure Git.
        """
        logger.info("Cloning the repository...")
        GitUtils.clone_repository(
            repository_url=self.repository_url, 
            local_path=self.data_folder, 
            github_access_token=self.github_access_token
        )
        logger.info("Configuring Git user...")
        GitUtils.config_user(
            local_path=self.data_folder,
            user_email=self.user_email
        )

    def __setup_branches(self) -> None:
        """
        Set up the target and source branches.
        """
        logger.info(f"Checking if {self.target_branch} exists...")
        GitUtils.check_or_create_branch(
            local_path=self.data_folder, 
            branch_name=self.target_branch
        )
        logger.info(f"Pulling {self.target_branch} to have recent changes...")
        GitUtils.pull_branch(
            local_path=self.data_folder, 
            branch_name=self.target_branch
        )
        logger.info(f"Creating {self.source_branch} from {self.target_branch}...")
        GitUtils.check_or_create_branch(
            local_path=self.data_folder, 
            branch_name=self.source_branch
        )       
        
    def __generate_and_commit(self) -> None:
        """
        Generate sentences and commit them.
        """
        sentences = self.__generate_sentences(self.number_of_commits)
        for sentence in sentences:
            logger.info(f"Write and commit '{sentence}' to {self.source_branch}...")
            with self.file_path.open("a") as f:
                f.write(sentence + "\n")
                
            GitUtils.add_commit_push(
                local_path=self.data_folder, 
                commit_message=sentence, 
                branch_name=self.source_branch
        )     
      
    def __cleanup_file(self) -> None:
        """
        Clean up the file if it's the first day of the month.
        """
        if self.__is_new_month(datetime.now()):
            logger.info("It's the first day of the month, cleaning the file...")
            with self.file_path.open("w") as f:
                f.write("")
            GitUtils.add_commit_push(
                local_path=self.data_folder, 
                commit_message=":rocket: feat: cleaned the file", 
                branch_name=self.source_branch
            )     
        
    def __create_and_merge_pr(
            self, 
            source_branch: str,
            target_branch: str, 
            title: str, 
            body: str
        ) -> None:
        """
        Create and merge a pull request.
        
        Parameters
        ----------
        source_branch : str
            The source branch of the pull request e.g. "feature/branch_name".
        target_branch : str
            The target branch of the pull request e.g. "develop".
        title : str
            The title of the pull request.
        body : str
            The body of the pull request.
        """
        logger.info(f"Creating pull request from {source_branch} to {target_branch}...")
        pr = GitUtils.create_pull_request(
            repo_owner=self.repository_owner, 
            repo_name=self.repository_name, 
            source_branch=source_branch, 
            target_branch=target_branch, 
            title=title,
            body=body, 
            github_access_token=self.github_access_token
        )
        GitUtils.merge_pull_request(
            repo_owner=self.repository_owner, 
            repo_name=self.repository_name, 
            pull_number=pr["number"], 
            github_access_token=self.github_access_token
        )
        
    def __will_i_work_hard_today(self) -> bool:
        """
        Used to simulate a developer's mood.
        The developer have 80% of chance to work hard today.
        
        Returns
        -------
        bool
            True if the developer will work hard today, False otherwise.
        """
        return random.random() < 0.8
  
    def work_hard_workflow(self) -> None:
        """
        Workflow to generate changes in the repository.
        """
        if self.__will_i_work_hard_today():
            logger.info("I'm a super developer, I may work hard today...")
            try:
                self.__clone_and_configure()
                self.__setup_branches()
                self.__cleanup_file()
                self.__generate_and_commit()
                self.__create_and_merge_pr(
                    source_branch=self.source_branch, 
                    target_branch=self.target_branch,
                    title=":rocket: Super Dev is working hard today!",
                    body=f"I'm proud, I committed {self.number_of_commits} changes today."
                )
                self.__create_and_merge_pr(
                    source_branch=self.target_branch, 
                    target_branch=self.prod_branch,
                    title=":rocket: Merging changes to main!",
                    body="Incredible content in production because i'm a super developer!"
                )
                GitUtils.delete_remote_branch(
                    repo_owner=self.repository_owner, 
                    repo_name=self.repository_name, 
                    branch_name=self.source_branch, 
                    github_access_token=self.github_access_token
                )
                logger.success(f"Workflow completed successfully with {self.number_of_commits} commits.")
            except Exception as e:
                logger.error(f"An error occurred during the workflow: {e}")
                raise
        else:
            logger.info("I'm a lazy developer because I did not work on my rest day.")