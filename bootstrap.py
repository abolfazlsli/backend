from core.packages.database import *
from database.admins import Admin , Company , Role , Premisions
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
        if per.status_code >= 200 and per.status_code < 300 :
            print(premission , head_token , "added")
        else :
            print(per.status_code)
    return


def create_user_role():
    role = Role(
        name = "کاربر" ,
        keyName = "students" ,
        caption = "این نقش برای کاربرانی استفاده میشود که در سیستم ثبتنام میکنند " ,
        company_id = 1
    )
    db.add(role)
    db.commit()
    return "done"

def create_teachers_role() :
    role = Role(
            name = "معلم" ,
            keyName = "managers" ,
            caption = "این نقش برای کاربرانی استفاده میشود که در سیستم ثبتنام میکنند " ,
            company_id = 1
        )
    db.add(role)
    db.commit()
    return "done"


def create_userzone_admin_role() :
    role = Role(
            name = "مدیریت کاربران" ,
            keyName = "admin" ,
            caption = "این نقش برای کاربرانی استفاده میشود که در سیستم ثبتنام میکنند " ,
            company_id = 1
        )
    db.add(role)
    db.commit()
    return "done"


CONTENT_PERMISSIONS = [
    "filds.get" , "filds.create" , "filds.edit" ,
    "instance.create" , "instance.get" , "instance.edit" ,
    "entry.create" , "entry.get" , "data.create" ,
]

def assign_permissions_to_role(key_name : str , codes : list[str]) :
    role = db.query(Role).filter(Role.keyName == key_name).one_or_none()
    if not role :
        return f"role {key_name} not found"
    premissions = db.query(Premisions).filter(Premisions.code.in_(codes)).all()
    for premission in premissions :
        if premission not in role.permissions :
            role.permissions.append(premission)
    db.commit()
    return "done"


# create_admin("admin" , "admin" , "09" ,"admin")
# create_userzone_admin_role()
# assign_permissions_to_role("managers" , CONTENT_PERMISSIONS)
# assign_permissions_to_role("admin" , CONTENT_PERMISSIONS)
# insert_premissions()
# create_users_zone()
# create_user_role()
# create_teachers_role()
# create_teachers_zone()