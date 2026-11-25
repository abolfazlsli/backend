
import json
import requests

from core.packages.database import *
from database.admins import *
from database.filemanager import *
from database.content import *


# ---------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------

db = SeeseionLocal()

API_BASE_URL = "http://127.0.0.1:8000"


def commit():
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise


# ---------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------

def create_admin(
    name: str,
    username: str,
    phone: str,
    password: str,
):
    admin = db.query(Admin).filter(
        (Admin.username == username) |
        (Admin.phone == phone)
    ).first()

    if admin:
        return "admin already exists"

    admin = Admin(
        name=name,
        username=username,
        phone=phone,
        password=password,
    )

    db.add(admin)
    commit()

    return "done"


# ---------------------------------------------------------------------
# Companies / Zones
# ---------------------------------------------------------------------

ZONES = [
    {
        "name": "users_zone",
        "address": "یه جای خوب",
        "telephone": "051",
        "creator_id": 1,
    },
    {
        "name": "teachers_zone",
        "address": "یه جای خوب",
        "telephone": "052",
        "creator_id": 1,
    },
]


def create_zone(
    name: str,
    address: str,
    telephone: str,
    creator_id: int,
):
    zone = db.query(Company).filter(
        Company.name == name
    ).first()

    if zone:
        return f"{name} already exists"

    zone = Company(
        name=name,
        addres=address,
        telphone=telephone,
        creator_id=creator_id,
    )

    db.add(zone)
    commit()

    return "done"


def create_zones():
    for zone in ZONES:
        print(create_zone(**zone))


# ---------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------

ROLES = [
    {
        "name": "کاربر",
        "keyName": "students",
        "caption": "این نقش برای کاربرانی استفاده میشود که در سیستم ثبتنام میکنند",
        "company_id": 1,
    },
    {
        "name": "معلم",
        "keyName": "managers",
        "caption": "این نقش برای کاربران معلم استفاده میشود",
        "company_id": 1,
    },
    {
        "name": "مدیریت کاربران",
        "keyName": "admin",
        "caption": "این نقش برای مدیریت کاربران استفاده میشود",
        "company_id": 1,
    },
]


def create_role(
    name: str,
    keyName: str,
    caption: str,
    company_id: int,
):
    role = db.query(Role).filter(
        Role.keyName == keyName
    ).first()

    if role:
        return f"{keyName} already exists"

    role = Role(
        name=name,
        keyName=keyName,
        caption=caption,
        company_id=company_id,
    )

    db.add(role)
    commit()

    return "done"


def create_roles():
    for role in ROLES:
        print(create_role(**role))


# ---------------------------------------------------------------------
# Permissions
# ---------------------------------------------------------------------

CONTENT_PERMISSIONS = [
    "filds.get",
    "filds.create",
    "filds.edit",
    "instance.create",
    "instance.get",
    "instance.edit",
    "entry.create",
    "entry.get",
    "data.create",
]


def assign_permissions_to_role(
    key_name: str,
    codes: list[str],
):
    role = db.query(Role).filter(
        Role.keyName == key_name
    ).one_or_none()

    if not role:
        return f"role {key_name} not found"

    permissions = db.query(Premisions).filter(
        Premisions.code.in_(codes)
    ).all()

    existing_codes = {
        permission.code
        for permission in role.permissions
    }

    for permission in permissions:
        if permission.code not in existing_codes:
            role.permissions.append(permission)

    commit()

    return "done"


# ---------------------------------------------------------------------
# Permission API Seeder
# ---------------------------------------------------------------------

def insert_permissions(
    file_path: str = "./seeds/premissions.json",
):
    admin = db.query(Admin).filter(
        Admin.id == 1
    ).one_or_none()

    if not admin:
        return "error: admin not found"

    login_response = requests.post(
        f"{API_BASE_URL}/auth/admin/login",
        json={
            "username_or_phone": admin.phone,
            "password": admin.password,
        },
        timeout=15,
    )

    login_response.raise_for_status()

    token = login_response.json()["result"]["token"]

    with open(file_path, "r", encoding="utf-8") as file:
        permissions = json.load(file)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    for permission in permissions:
        try:
            response = requests.post(
                f"{API_BASE_URL}/admin/permissions",
                json=permission,
                headers=headers,
                timeout=15,
            )

            response.raise_for_status()

            print(permission, "added")

        except requests.RequestException as error:
            print(permission, "failed:", error)



def create_paratner () :
    # create manager 
    manager_role = db.query(Role).filter(
        Role.keyName == "admin"
    ).one_or_none()
    manager = Partner(
        name="مدیر کاربران" , 
        username = "users_manager" , 
        status = "active" ,
        phone = "admin",
        password = "admin" ,
        role_id = manager_role.id
    )
    db.add(manager)
    db.commit()


# ---------------------------------------------------------------------
# Seeder Runner
# ---------------------------------------------------------------------

def run_seeds():
    try:
        create_admin(
            name="admin",
            username="admin",
            phone="09",
            password="admin",
        )

        insert_permissions()
        create_zones()
        create_roles()

        assign_permissions_to_role(
            "managers",
            CONTENT_PERMISSIONS,
        )

        assign_permissions_to_role(
            "admin",
            CONTENT_PERMISSIONS,
        )
        create_paratner()


    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
