from core.packages.schema import *


class AddPremission (BaseModel) :
    name : str 
    code : str



class EditPremission (BaseModel) :
    id : str
    name : Optional[str] = None
    code : Optional[str] = None
    status : Optional[str] = None


class CreateRoleDto (BaseModel) :
    name : str
    caption : Optional[str] = None
    premissionsid : Optional[List[str]] = None
    companyId : Optional[str] = None


class SetPremissionToRoleDto (BaseModel) :
    permissionid : str
    roleid : str


class RemovePremissionFromRole (BaseModel) :
    roleid : str 
    permissionid : str


class BanPartnerMessage (BaseModel) :
    reason : str
    extra_explain : str


class CreateCompanyDto (BaseModel) :
    name : str
    addres : str
    telphone : str

class EditRoleDto (BaseModel) :
    roleid : str 
    name : Optional[str] = None
    caption : Optional[str] = None
    premissionsid : Optional[List[str]] = None


class CreatePartnerDto (BaseModel) :
    name : str 
    username : str
    phone : str
    companyId : Optional[str] = None
    password : str = Field(..., min_length=8, max_length=64)
    role_id : Optional[str] = None



class SetRoleForPartner (BaseModel) :
    role_id : str
    partner_id : str

class EditPartner (BaseModel) :
    name : str 
    username : str
    password : str

# responces -----------------------

class AdminResponce (ResponceModel) :
    name : str
    phone : str

class PremissionsOutModel (ResponceModel , ById) :
    name: str
    status : str
    creator : Optional[AdminResponce] = None


class PremissionsResponce (ResponceModel) :
    result : List[PremissionsOutModel] = []
    total : int = 0

class PartnerPremissionsOutModel (ResponceModel , ById) :
    name: str
    status : str

class RoleOut (ResponceModel , ById) :
    name : str
    caption : Optional[str] = None
    permissions : Optional[List[PartnerPremissionsOutModel]] = None

class RolesResponce (ResponceModel) :
    result : List[RoleOut] = []
    total : int = 0


class PartnerBaseicOut (ResponceModel) :
    name : str
    username : str
    phone : str


class PartnerOutPublic (ResponceModel , ById) :
    name : str
    username : str
    phone : str
    role : Optional[RoleOut] = None
    creator : Optional[PartnerBaseicOut] = None

class PartnerOut (ResponceModel) :
    name : str
    username : str
    status : str
    phone : str
    # password : str
    role : Optional[RoleOut] = None
    creator : Optional[PartnerBaseicOut] = None


class PartnersResponce (ResponceModel) :
    result : List[PartnerOutPublic] = []
    total : int = 0


class CompanyOut(ResponceModel , ById) :
    name : str 
    addres : str
    telphone : str

    members : List[PartnerOutPublic] = []
    roles : List[RoleOut] = []



class CompanyResult (ResponceModel) :
    result : List[CompanyOut] = []
    total : int = 0