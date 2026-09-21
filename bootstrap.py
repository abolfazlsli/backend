from core.packages.database import *
from database.admins import Admin , Company , Role
from database.content import Entries
import json , requests

db = SeeseionLocal()

def create_admin (
        name : str ,
        username : str ,
        phone : str ,
        password : str
) :
    admin = Admin(
        name = name ,
        username = username ,
        phone = phone ,
        password = password
    )
        
    db.add(admin)
    db.commit()
    return "done"

def create_users_zone () :
    user_zone = Company(
        name = "users_zone" ,
        addres = "یه جای خوب",
        telphone = "051",
        creator_id =1
    )
    db.add(user_zone)
    db.commit()
    return "done"

def create_teachers_zone () :
    user_zone = Company(
            name = "teachers_zone" ,
            addres = "یه جای خوب",
            telphone = "052",
            creator_id =1
        )
    db.add(user_zone)
    db.commit()
    return "done"


def insert_premissions () :
    premissions_file = open("./seeds/premissions.json" , "rb")
    premissions = json.loads(premissions_file.read())
    admin = db.query(Admin).filter(
        Admin.id == 1
    ).one_or_none()
    if not admin :
        return "error user not found"
    token = requests.post(
        "http://127.0.0.1:8000/auth/admin/login" , json={
        "username_or_phone": admin.phone,
        "password": admin.password
        })
    if token.status_code == 200 :
        head_token = json.loads(token.content)['result']['token']
    for premission in premissions :
        per = requests.post(
            "http://127.0.0.1:8000/admin/permissions" , json=premission , headers={
                "authorizations" : head_token
            }
        )
        if per.status_code :
            print(premission , head_token , "added")
    return


def create_user_role():
    role = Role(
        name = "کاربر" ,
        caption = "این نقش برای کاربرانی استفاده میشود که در سیستم ثبتنام میکنند " ,
        company_id = 1
    )
    db.add(role)
    db.commit()
    return "done"


create_admin("admin" , "admin" , "09" ,"admin")
create_users_zone()
create_user_role()
create_teachers_zone()
insert_premissions()