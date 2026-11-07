from core.packages.schema import *
from datetime import datetime
from database.content import TypeOfEnum
from schema.admin import CompanyOut
from schema.admin import PartnerOutPublicWithNoCreator
class Option (BaseModel) :
    label : str
    value : str 
    order : int

class CreateFildDto (BaseModel) :
    name : str
    type_of : TypeOfEnum
    options : Optional[List[Option]] = None

class EditFildsDto (BaseModel) :
    fild_id : str
    name : Optional[str] = None
    options : Optional[List[Option]] = None


class RemoveOptionDto (BaseModel) :
    fild_id : str 
    option_id : str



class CreateInstanceDto (BaseModel) :
    name : str
    caption : Optional[str] = None

    filds : Optional[List[str]] = None

class AddFildOprionToFild (BaseModel) :
    fild_id : str
    options : List[Option]




class EditInstanceDto (BaseModel) :
    instance_id : str
    name : Optional[str] = None
    caption : Optional[str] = None

    filds_id : Optional[List[str]] = None




class MyEntriesFilter (GetDataQuerySize) :
    status : Optional[Literal["pendding" , "active" , "disactive"]] = None


class CreateEntryDto (BaseModel) :
    instance_id : str
    price : Optional[int] = Field(default=0 , ge=0)
    entry_type : Optional[Literal["free" , "free_users" , "paid"]] = "free"
    categorys : Optional[List[str]] = None



class EntryDataHolderDto (BaseModel) :
    value : str | int | bool | list[str]
    placement : str


class EntryDataDto (BaseModel) :
    fild_id : str
    data : EntryDataHolderDto


class CreateEnteryData (BaseModel) :
    entry_id : str
    filds : List[EntryDataDto]

# responce --------------------------





class OptionsOut (ResponceModel , ById) :
    value : str = None
    label : str = None
    order : int = None
    is_active : Optional[bool] = True

class FildsOut(ResponceModel , ById) :
    name : str
    type_of : TypeOfEnum

    company : CompanyOut

    options : Optional[OptionsOut] = []


class FildOutPublic (ResponceModel , ById) :
    name : str
    type_of : TypeOfEnum

    options : Optional[List[OptionsOut]] = []

class FildsResponce(ResponceModel) :
    result : List[FildOutPublic] = [] 
    total : int = 0


class InstanceFildsOut (ResponceModel) :
    order : Optional[int] = 0
    required : Optional[bool] = False

    fild : FildOutPublic = None

class InstanceOut (ResponceModel , ById) :
    name : str
    caption : Optional[str] = None

    # instance_filds : Optional[List[InstanceFildsOut]] = []



class SingleInstanceOut (ResponceModel , ById) :
    name : str
    caption : Optional[str] = None

    instance_filds : List[InstanceFildsOut] = []


class InstanceResponce (ResponceModel) :
    result : List[InstanceOut]
    total : int = 0



class SingleInstanceOutForInstanceFilds (ResponceModel) :
    id : str 
    name : str
    caption : Optional[str] = None

class SingleInstanceFildsRes (ResponceModel) :
    instance : Optional[SingleInstanceOutForInstanceFilds] = None
    filds : List[InstanceFildsOut]

class SingleInstanceFildsOut (ResponceModel) :
    result : SingleInstanceFildsRes 


class CategoryGroupMiniDto (ResponceModel , ById) :
    name : str
    kind : Optional[str] = None


class CategoryDto (ResponceModel , ById) :
    name : str
    group : Optional[CategoryGroupMiniDto] = None


class EntryDataPublicOut (ResponceModel) :
    placement : str
    value : Any = None
    label : Any = None
    fild : FildOutPublic


class CreatorPublicOut (ResponceModel) :
    name : Optional[str] = None


class EntryOut(ResponceModel , ById) :
    status : str
    entry_type : str
    price : Optional[int] = None
    like_count : Optional[int] = 0
    create_at : Optional[datetime] = None
    instance : SingleInstanceOut
    categorys : List[CategoryDto]
    data : List[EntryDataPublicOut]
    creator : PartnerOutPublicWithNoCreator


class EntryOutWithOutInstance(ResponceModel , ById) :
    status : str
    entry_type : str
    price : Optional[int] = None
    like_count : Optional[int] = 0
    create_at : Optional[datetime] = None
    categorys : List[CategoryDto]
    data : List[EntryDataPublicOut]
    creator : Optional[CreatorPublicOut] = None


class EntryRes (ResponceModel) :
    result : List[EntryOut] = []
    total : int = 0


class EntryDataOut (ResponceModel) :
    placement : str
    value : Any
    fild : FildOutPublic
    entry : EntryOut



class EntryDataRes (ResponceModel) :
    result : List[EntryDataOut] = [] 
    total : int