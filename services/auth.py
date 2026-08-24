from core.packages.services import *
from core.security.secure import *
from schema.auth import *

async def loginUser(
        data : LoginModel ,
        db : Session
) :
    admin = db.query(Admin).filter(
        or_(Admin.username == data.username_or_phone ,
            Admin.phone == data.username_or_phone) ,
            Admin.password == data.password
        )
    if admin.count() == 0 :
        return NotFoundRes(
            {
                "result" : "admin not found"
            }
        )
    token = create_access_token({"sub" : admin.first().public_id})
    return {
        "result" : {
            "message" : "user logedin" ,
            "token" : token
        }
    }




async def loginPartner(
        data : LoginModel ,
        db : Session
) :
    partner = db.query(Partner).filter(
        or_(Partner.username == data.username_or_phone ,
            Partner.phone == data.username_or_phone) ,
            Partner.password == data.password
        )
    if partner.count() == 0 :
        return NotFoundRes(
            {
                "result" : "partner not found"
            }
        )
    token = create_access_token({"sub" : partner.first().public_id})
    return {
        "result" : {
            "message" : "user logedin" ,
            "token" : token
        }
    }

