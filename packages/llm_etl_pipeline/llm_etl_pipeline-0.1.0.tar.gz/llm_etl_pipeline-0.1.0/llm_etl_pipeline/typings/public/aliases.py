import sys
from pathlib import Path
from typing import Annotated, Any, Literal, TypeVar, Union

import pandas as pd
from pydantic import (
    AfterValidator,
    BeforeValidator,
    Field,
    InstanceOf,
    StrictInt,
    StrictStr,
    StringConstraints,
)

# Assuming these are custom validators defined elsewhere and are correctly imported.
# If they are not used, they should be removed.
from llm_etl_pipeline.typings.internal.validators import (
    _ensure_dataframe_type,
    _validate_non_empty_dataframe,
    _validate_regex_syntax,
)

if sys.version_info >= (3, 11):
    from typing import Self
else:
    Self = TypeVar("Self")


# --- Type Definitions ---

NonZeroInt = Annotated[StrictInt, Field(ge=1)]
"""
Represents an int that must be greater or equal to 1.
"""

NonEmptyStr = Annotated[
    StrictStr, StringConstraints(strip_whitespace=True, min_length=1)
]
"""
Represents a string that must not be empty after stripping whitespace.
"""

NonEmptyListStr = Annotated[
    list[NonEmptyStr],
    Field(min_length=1, description="A list of strings that must not be empty."),
]
"""
Represents a list of strings where each string is non-empty and the list itself contains at least one item.
"""

NonEmptyDataFrame = Annotated[
    InstanceOf[pd.DataFrame],
    BeforeValidator(_ensure_dataframe_type),
    AfterValidator(_validate_non_empty_dataframe),
]
"""
Represents a pandas DataFrame that must not be None and must contain at least one row.
"""

RegexPattern = Annotated[NonEmptyStr, AfterValidator(_validate_regex_syntax)]
"""
Represents a non-empty string that must be a valid regular expression pattern.
"""

ReferenceDepth = Literal["paragraphs", "sentences"]
"""
Defines the valid literal values for specifying reference depth: 'paragraphs' or 'sentences'.
"""

ExtractionType = Literal["money", "entity"]
"""
Defines the valid literal values for specifying the extraction type: 'money' or 'tlr'.
"""


# Define standard SaT model IDs as a separate type
StandardSaTModelId = Literal[
    "sat-1l",
    "sat-1l-sm",
    "sat-3l",
    "sat-3l-sm",
    "sat-6l",
    "sat-6l-sm",
    "sat-9l",
    "sat-12l",
    "sat-12l-sm",
]
"""
Defines the literal values for standard SaT (Semantic Augmentation Tool) model identifiers.
These typically refer to pre-trained models with varying complexities (e.g., number of layers).
"""


# --- NEW VALIDATOR FOR SaTModelId ---
def _validate_sat_model_id_and_path(v: Any) -> Union[StandardSaTModelId, Path]:
    """
    Validates SaT model ID: must be a standard ID or an existing file path.
    """
    if isinstance(v, Path):
        # If it's already a Path object, ensure it exists
        if not v.exists():  # <--- NEW CHECK
            raise ValueError(f"Model path '{v}' does not exist.")
        return v

    if isinstance(v, str):
        # Check if it's a standard ID first
        if v in StandardSaTModelId.__args__:  # Access literal values from Literal type
            return v

        # If not a standard ID, treat it as a path string and check existence
        path_obj = Path(v)
        if not path_obj.exists():  # <--- NEW CHECK
            # For the test, we want "invalid-model" to fail here,
            # so it must not exist.
            raise ValueError(
                f"Model path '{v}' does not exist or is not a valid standard ID."
            )
        return path_obj

    raise TypeError(
        f"Invalid type for SaTModelId: {type(v).__name__}. Expected string or Path."
    )


# Use Annotated with the custom validator
SaTModelId = Annotated[
    Union[StandardSaTModelId, str, Path],  # Keep all original input types
    AfterValidator(_validate_sat_model_id_and_path),  # Apply the custom validator last
]
"""
Represents a SaT (Semantic Augmentation Tool) model identifier, which can be:
- A predefined standard model ID (e.g., 'sat-1l').
- A string representing a local file path to a custom model.
- A `Path` object representing a local file path to a custom model.
"""

LanguageRequirement = Literal["en"]
"""
Defines the valid literal values for language requirements, currently restricted to 'en' (English).
"""
