import enum
from datetime import datetime

from pydantic import BaseModel, Field


# Classic datatypes
class Integer(BaseModel):
    """Integer to represent the result of a computation."""

    value: int = Field(
        ...,
        description="The integer result of the computation.",
        examples=[0],
    )


class Datetime(BaseModel):
    """Datetime to represent the result of a computation."""

    value: datetime = Field(
        ...,
        description="The datetime result of the computation.",
        examples=[datetime(2023, 10, 1, 12, 0, 0)],
    )


class String(BaseModel):
    """String result of the computation."""

    result: str = Field(
        ...,
        description="The result the computation represented as a string.",
        examples=["42"],
    )


# Neural-result datatypes
class SentimentLabel(enum.Enum):
    """SentimentLabelLabel to represent the result of a computation."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Sentiment(BaseModel):
    """Sentiment to used to classify a data value."""

    label: SentimentLabel = Field(
        ...,
        description="The Sentiment label of the data.",
        examples=[SentimentLabel.POSITIVE],
    )
