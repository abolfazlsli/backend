from core.packages.services import *
from schema.users import *

async def registerUser (
        db : Session ,
        info : RegisterStudentDto
) :
    user = Partner(
        name = info.name,
        username = info.username , 
        phone = info.phone ,
        password = info.password , 
        company_id = 1,
        role_id = 1
        
    )
    db.add(user)
    db.commit()
    token = create_access_token({"sub" : user.public_id})
    return OkRes(
        {
            "result" : {
                "message" : "user registerd" ,
                "token" : token
            }
        }
    )


async def loginUser(
        db : Session , 
        data : LoginUserDto
) :
    user = db.query(Partner).filter(
        Partner.role_id == 1 , 
        Partner.company_id == 1 ,
        or_(Partner.username == data.username , Partner.phone == data.username) ,
        Partner.password == data.password
    ).one_or_none()
    if not user : 
        return NotFoundRes(
            {
                "result" : "no user found"
            }
        )
    token = create_access_token({"sub" : user.public_id})
    return OkRes(
        {
            "result" : {
                "message" : "user logeding" ,
                "token" : token
            }
        }
    )



async def getProfile (
        db : Session , 
        user : Partner
) :
    user = db.query(Partner).filter(Partner.id == user.id).one_or_none()
    if not user : 
        return NotFoundRes(
            {
                "result" : "no user found"
            }
        )
    
    return OkRes(
        {
            "result" : {
                "name" : user.name , 
                "username" : user.username ,
                "phone" : user.phone ,
            }
        }
    )



