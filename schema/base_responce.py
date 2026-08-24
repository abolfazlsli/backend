from core.packages.schema import *
class GetDataQuerySize (BaseModel) :
    offset : int = Field(default=0 , ge=0)
    size : int = Field(default=30 , ge=1 , le=30)
