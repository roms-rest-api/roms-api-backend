from api import github_instance, config, devices


class GithubSearcher:
    def __init__(self, codename: str):
        self.codename: str = codename
        self.device_obj = devices.get(self.codename)

        self.MAX_COMMITS = 16

        self.get_repo()

    def get_repo(self):
        repo_name: str = (
            f"device_{self.device_obj[0]['brand']}_{self.device_obj[0]['codename']}"
        )

        self.repo = github_instance.get_repo(
            f"{config['core']['devices_org']}/{repo_name}"
        )

    def get_changelog(self) -> str:
        if not self.device_obj[0].get("commit_hash", None):
            needed_commits: int = self.MAX_COMMITS
            commits = self.repo.get_commits()

            if commits.totalCount <= needed_commits:
                needed_commits = commits.totalCount - 1

            self.device_obj[0]["commit_hash"] = commits[needed_commits].sha

        commit_date = self.repo.get_commit(
            sha=self.device_obj[0]["commit_hash"]
        ).commit.author.date
        commits = self.repo.get_commits(since=commit_date)

        commits_txt = f"Commits since {str(commit_date)}\n"

        if commits.totalCount == 0:
            commits_txt = "No commits"
        else:
            for commit in commits:
                commits_txt += f"\n{commit.commit.message}\n======="

        # TODO: Update hash based on new build date

        return commits_txt
