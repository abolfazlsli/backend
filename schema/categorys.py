from core.packages.schema import *
from schema.content import EntryOutWithOutInstance , EntryDataOut





class AddCategory (BaseModel) :
    name : str
    caption : Optional[str] = None

    group_id : Optional[str] = None



class AddCategoryGroup (BaseModel) :
    name : str 
    caption : Optional[str] = None

    categorys_id : Optional[List[str]] = None

    category : Optional[List[AddCategory]] = None


class GetCategorysContentBySize (GetDataQuerySize) :
    category : Optional[List[str]] = None





# --------------------------- responceses ----------------------

class GetCategoryEntriesDto (ResponceModel , ById) :
    name : str
    entries : List[EntryOutWithOutInstance]


class GetCategoryDto (ResponceModel , ById) :
    name : str


class GetCategoryRes(ResponceModel):
    result : List[GetCategoryDto]
    total : int = 0

class GetCategoryEntriesRes (ResponceModel) :
    result : List[EntryOutWithOutInstance]
    # List[GetCategoryEntriesDto]
    total : int = 0