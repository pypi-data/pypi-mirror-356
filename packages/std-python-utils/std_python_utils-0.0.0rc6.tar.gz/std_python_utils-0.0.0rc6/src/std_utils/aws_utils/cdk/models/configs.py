from abc import abstractmethod
from typing import Type

from aws_cdk import App, Stage
from pydantic import BaseModel, ConfigDict, Field

from std_utils.models.git import GithubRepositoryBranch


class PipelineStage(Stage):

    @property
    @abstractmethod
    def kwargs(self) -> dict:
        raise NotImplementedError()


class PipelineConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    parent: App
    connection_arn: str
    repository_branch: GithubRepositoryBranch
    trigger_on_push: bool = True
    self_mutation: bool = True
    docker_enabled: bool = True
    stage_types: list[Type[PipelineStage]] = Field(min_length=1)

    @property
    def docker_enabled_for_self_mutation(self) -> bool:
        return self.self_mutation and self.docker_enabled
