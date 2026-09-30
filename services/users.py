from core.packages.services import *
from schema.users import *
from database.admins import Role ,Company

async def registerUser (
        db : Session ,
        info : RegisterStudentDto
) :
    role = db.query(Role).filter(
        Role.keyName == "students"
    ).one_or_none()
    company = db.query(Company).filter(
        Company.name == "users_zone"
    ).one_or_none()
    if not company :
        return InternalServerErrorRes(
                    {
                        "result" : "cant find scope"
                    }
                )
    if not role : 
        return InternalServerErrorRes(
            {
                "result" : "cant find role"
            }
        )
    user = Partner(
        name = info.name,
        username = info.username , 
        phone = info.phone ,
        password = info.password , 
        company_id = company.id,
        role_id = role.id
        
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
    company = db.query(Company).filter(
        Company.name == "users_zone"
    ).one_or_none()
    user = db.query(Partner).filter(
        Partner.role.has(
            or_(
                Role.keyName == "students",
                Role.keyName == "managers" , 
                Role.keyName == "admin"
            )
        ),
        Partner.company_id == company.id ,
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
                "role" : user.role.keyName
            }
        }
    )



