from core.packages.schema import *
from schema.content import EntryOutWithOutInstance , EntryDataOut





class AddCategory (BaseModel) :
    name : str
    caption : Optional[str] = None
    color : str
    icon_id : Optional[str] = None

    group_id : Optional[str] = None



GroupKind = Literal["grade" , "subject" , "type"]


GroupKind = Literal["grade" , "subject" , "type"]


class AddCategoryGroup (BaseModel) :
    name : str
    caption : Optional[str] = None
    color : str
    icon_id : Optional[str] = None
    kind : Optional[GroupKind] = None
    kind : Optional[GroupKind] = None

    categorys_id : Optional[List[str]] = None

    category : Optional[List[AddCategory]] = None


class GetGroupCategoriesQuery (GetDataQuerySize) :
    kind : Optional[GroupKind] = None


class GetCategoryCountsQuery (BaseModel) :
    rows : List[str]
    cols : Optional[List[str]] = None


class GetCategorysContentBySize (GetDataQuerySize) :
    category : Optional[List[str]] = None
    search : Optional[List[str]] = None
    entry_type : Optional[Literal["free" , "free_users" , "paid"]] = None
    sort : Optional[Literal["newest" , "best" , "most-viewed"]] = None





# --------------------------- responceses ----------------------

class GetCategoryEntriesDto (ResponceModel , ById) :
    name : str
    entries : List[EntryOutWithOutInstance]


class Icon (ResponceModel , ById) :
    file_name : str

class GetCategoryDto (ResponceModel , ById) :
    name : str
    color : str
    icon : Optional[Icon] = None


class GetCategoryRes(ResponceModel):
    result : List[GetCategoryDto]
    total : int = 0

class GetCategoryEntriesRes (ResponceModel) :
    result : List[EntryOutWithOutInstance]
    # List[GetCategoryEntriesDto]
    total : int = 0




class GetGroupCategoriesDto (ResponceModel ,ById) :
    name : str
    caption : Optional[str] = None
    color : str
    kind : Optional[str] = None
    kind : Optional[str] = None
    icon : Optional[Icon] = None
    categories : List[GetCategoryDto]

class GetGroupCategoriesRes (ResponceModel) :
    result : List[GetGroupCategoriesDto]
    total : int = 0