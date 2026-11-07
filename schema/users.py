from core.packages.schema import *


class RegisterStudentDto (BaseModel) :
    name : str
    username : str
    phone : str
    password : str



class LoginUserDto (BaseModel) :
    username : str
    password : str


class RoleRequestDto (BaseModel) :
    message : Optional[str] = None


class ReviewRoleRequestDto (BaseModel) :
    accept : bool


class RoleUpDto (BaseModel) :
    user_id : str
    role : Literal["students" , "managers"]


class EntryStatusDto (BaseModel) :
    status : Literal["active" , "disactive"]


class RoleRequestsFilter (GetDataQuerySize) :
    status : Optional[Literal["pendding" , "accepted" , "rejected"]] = None


class EntriesStatusFilter (GetDataQuerySize) :
    status : Optional[Literal["pendding" , "active" , "disactive"]] = "pendding"


class UsersFilter (GetDataQuerySize) :
    role : Optional[Literal["students" , "managers" , "admin"]] = None
