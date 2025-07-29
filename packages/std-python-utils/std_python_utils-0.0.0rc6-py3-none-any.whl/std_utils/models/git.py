from pydantic import BaseModel


class GithubRepository(BaseModel):
    owner: str
    name: str


class GithubRepositoryBranch(BaseModel):
    repo_branch: str
    repo: GithubRepository
