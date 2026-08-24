from core.packages.schema import *


class LoginModel(BaseModel) :
    username_or_phone : str
    password : str


class SendTokenResponcee(ResponceModel) :
    message : str
    token : str

class LoginResponce(ResponceModel) :
    result : SendTokenResponcee