from pydantic import BaseModel, ConfigDict


class FrozenStdBaseModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        validate_by_alias=True,
        validate_return=True,
        validate_by_name=True,
        extra='forbid',
        revalidate_instances='always',
        validate_default=True,
        validate_assignment=True,
        regex_engine='python-re',
        validation_error_cause=True
    )


class StdBaseModel(FrozenStdBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
