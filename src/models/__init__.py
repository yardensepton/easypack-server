from typing import Optional, Annotated, List

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict, field_validator, model_validator


PyObjectId = Annotated[str, BeforeValidator(str)]
