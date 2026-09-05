from core.packages.schema import *
from database.content import TypeOfEnum
from schema.admin import CompanyOut

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

    filds_id : Optional[List[str]]




class CreateEntryDto (BaseModel) :
    instance_id : str
    price : Optional[int] = 0
    entry_type : Optional[str] = "free"



# responce --------------------------


class OptionsOut (ResponceModel) :
    value : str = None
    label : str = None
    order : int = None

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


class InstanceFildsOut (ResponceModel , ById) :
    order : int
    required : bool

    fild : FildOutPublic = None

class InstanceOut (ResponceModel , ById) :
    name : str
    caption : str

    # instance_filds : Optional[List[InstanceFildsOut]] = []



class SingleInstanceOut (ResponceModel , ById) :
    name : str
    caption : str

    instance_filds : List[InstanceFildsOut] = []

class InstanceResponce (ResponceModel) :
    result : List[InstanceOut] = [] 
    total : int = 0



class SingleInstanceOutForInstanceFilds (ResponceModel) :
    id : str 
    name : str
    caption : str

class SingleInstanceFildsRes (ResponceModel) :
    instance : Optional[SingleInstanceOutForInstanceFilds] = None
    filds : List[InstanceFildsOut]

class SingleInstanceFildsOut (ResponceModel) :
    result : SingleInstanceFildsRes 


class EntryOut(ResponceModel) :
    status : str
    instance : SingleInstanceOut


class EntryRes (ResponceModel) :
    result : List[EntryOut] = []
    total : int = 0