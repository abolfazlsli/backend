from core.packages.schema import *


class RegisterStudentDto (BaseModel) :
    name : str
    username : str
    phone : str
    password : str



class LoginUserDto (BaseModel) :
    username : str
    password : str