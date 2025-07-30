from enum import StrEnum
from pydantic import BaseModel, Field


class ExceptionType(StrEnum):
    UNKNOWN = "unknown"
    STATE_EXCEPTION = "state_exception"

    # Initialization errors
    EMAIL_FROM_ENV_IS_NOT_SET = "email_from_env_is_not_set"
    PASSWORD_FROM_ENV_IS_NOT_SET = "password_from_env_is_not_set"

    # Google login errors
    EMAIL_FROM_ENV_AND_FROM_MESSAGE_DOES_NOT_MATCH = (
        "email_from_env_and_from_message_does_not_match"
    )


class ErrorMessage(BaseModel):
    exception_type: ExceptionType = Field(
        ...,
        description="Type of the exception that occurred",
    )
    message: str = Field(
        ...,
        description="Detailed message describing the error",
    )
