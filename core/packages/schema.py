from pydantic import *
from typing import *


class GetDataQuerySize (BaseModel) :
    offset : int = Field(default=0 , ge=0)
    size : int = Field(default=30 , ge=1 , le=30)



class ResponceModel (BaseModel) :
    model_config = ConfigDict(
        from_attributes=True,   
        populate_by_name=True,  
    )


class ById (BaseModel) :
    id : str = Field(validation_alias="public_id")