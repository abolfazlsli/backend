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
    type_of : Optional[TypeOfEnum] = None
    options : Optional[List[Option]] = None


class RemoveOptionDto (BaseModel) :
    fild_id : str 
    option_id : str




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