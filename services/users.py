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


from database.admins import RoleRequest
from database.content import Entries , PartnerAcsessKeys , StatusEnum , PricingEnum
from services.category import public_entry_dump


def get_users_zone(db : Session) :
    return db.query(Company).filter(
        Company.name == "users_zone"
    ).one_or_none()


def user_out(user : Partner) -> dict :
    return {
        "id" : user.public_id ,
        "name" : user.name ,
        "username" : user.username ,
        "phone" : user.phone ,
        "status" : user.status ,
        "role" : user.role.keyName if user.role else None
    }


def role_request_out(item : RoleRequest) -> dict :
    return {
        "id" : item.public_id ,
        "status" : item.status ,
        "message" : item.message ,
        "role" : item.role.keyName if item.role else None ,
        "create_at" : item.create_at.isoformat() if item.create_at else None ,
        "user" : user_out(item.partner)
    }


# ---------------- saves ----------------

async def toggleSaveEntry (
        db : Session ,
        user : Partner ,
        entry_id : str
) :
    entry = db.query(Entries).filter(
        Entries.public_id == entry_id ,
        Entries.status == StatusEnum.ACTIVE
    ).one_or_none()
    if not entry :
        return NotFoundRes(
            {
                "result" : "no entry found"
            }
        )
    user = db.query(Partner).filter(Partner.id == user.id).one()
    if entry in user.saved_entries :
        user.saved_entries.remove(entry)
        saved = False
    else :
        user.saved_entries.append(entry)
        saved = True
    db.commit()
    return OkRes(
        {
            "result" : {
                "saved" : saved
            }
        }
    )


async def getSavedEntries (
        db : Session ,
        user : Partner ,
        querySize : GetDataQuerySize
) :
    query = db.query(Entries).filter(
        Entries.saved_by.any(Partner.id == user.id) ,
        Entries.status == StatusEnum.ACTIVE
    )
    total = query.count()
    entries = (
        query
        .order_by(Entries.id.desc())
        .offset(querySize.offset)
        .limit(querySize.size)
        .all()
    )
    return OkRes(
        {
            "result" : [public_entry_dump(entry) for entry in entries] ,
            "total" : total
        }
    )


async def getSavedEntriesIds (
        db : Session ,
        user : Partner
) :
    user = db.query(Partner).filter(Partner.id == user.id).one()
    return OkRes(
        {
            "result" : [entry.public_id for entry in user.saved_entries]
        }
    )


async def getEntryWithFiles (
        db : Session ,
        user : Partner ,
        entry_id : str
) :
    entry = db.query(Entries).filter(
        Entries.public_id == entry_id ,
        Entries.status == StatusEnum.ACTIVE
    ).one_or_none()
    if not entry :
        return NotFoundRes(
            {
                "result" : "no entry found"
            }
        )
    if entry.entry_type == PricingEnum.PRICING and entry.creator_id != user.id :
        has_key = db.query(PartnerAcsessKeys).filter(
            PartnerAcsessKeys.entry_id == entry.id ,
            PartnerAcsessKeys.creator_id == user.id
        ).count() > 0
        if not has_key :
            return ForbiddenRes(
                {
                    "result" : "you need to buy this entry"
                }
            )
    return OkRes(
        {
            "result" : public_entry_dump(entry , can_see_files=True)
        }
    )


# ---------------- role requests ----------------

async def createRoleRequest (
        db : Session ,
        user : Partner ,
        data : RoleRequestDto
) :
    role = db.query(Role).filter(Role.keyName == "managers").one_or_none()
    if not role :
        return InternalServerErrorRes(
            {
                "result" : "cant find role"
            }
        )
    pending = db.query(RoleRequest).filter(
        RoleRequest.partner_id == user.id ,
        RoleRequest.status == "pendding"
    ).count()
    if pending :
        return BadRequestRes(
            {
                "result" : "you already have a pending request"
            }
        )
    db.add(
        RoleRequest(
            partner_id = user.id ,
            role_id = role.id ,
            message = data.message
        )
    )
    db.commit()
    return OkRes(
        {
            "result" : "request sent"
        }
    )


async def getMyRoleRequest (
        db : Session ,
        user : Partner
) :
    item = db.query(RoleRequest).filter(
        RoleRequest.partner_id == user.id
    ).order_by(RoleRequest.id.desc()).first()
    return OkRes(
        {
            "result" : role_request_out(item) if item else None
        }
    )


async def getRoleRequests (
        db : Session ,
        filters : RoleRequestsFilter
) :
    query = db.query(RoleRequest)
    if filters.status :
        query = query.filter(RoleRequest.status == filters.status)
    total = query.count()
    items = (
        query
        .order_by(RoleRequest.id.desc())
        .offset(filters.offset)
        .limit(filters.size)
        .all()
    )
    return OkRes(
        {
            "result" : [role_request_out(item) for item in items] ,
            "total" : total
        }
    )


async def reviewRoleRequest (
        db : Session ,
        admin : Partner ,
        id : str ,
        data : ReviewRoleRequestDto
) :
    item = db.query(RoleRequest).filter(
        RoleRequest.public_id == id ,
        RoleRequest.status == "pendding"
    ).one_or_none()
    if not item :
        return NotFoundRes(
            {
                "result" : "no request found"
            }
        )
    item.status = "accepted" if data.accept else "rejected"
    item.reviewed_by_id = admin.id
    if data.accept :
        item.partner.role_id = item.role_id
    db.commit()
    return OkRes(
        {
            "result" : f"request {item.status}"
        }
    )


async def roleUp (
        db : Session ,
        admin : Partner ,
        data : RoleUpDto
) :
    if admin.public_id == data.user_id :
        return ForbiddenRes(
            {
                "result" : "you cant set role for your self"
            }
        )
    company = get_users_zone(db)
    user = db.query(Partner).filter(
        Partner.public_id == data.user_id ,
        Partner.company_id == company.id ,
        Partner.role.has(Role.keyName.in_(["students" , "managers"]))
    ).one_or_none()
    role = db.query(Role).filter(Role.keyName == data.role).one_or_none()
    if not user or not role :
        return NotFoundRes(
            {
                "result" : "cant find data"
            }
        )
    user.role_id = role.id
    db.commit()
    return OkRes(
        {
            "result" : "role changed"
        }
    )


async def getUsers (
        db : Session ,
        filters : UsersFilter
) :
    company = get_users_zone(db)
    query = db.query(Partner).filter(Partner.company_id == company.id)
    if filters.role :
        query = query.filter(Partner.role.has(Role.keyName == filters.role))
    total = query.count()
    items = (
        query
        .order_by(Partner.id.desc())
        .offset(filters.offset)
        .limit(filters.size)
        .all()
    )
    return OkRes(
        {
            "result" : [user_out(item) for item in items] ,
            "total" : total
        }
    )


# ---------------- entries moderation ----------------

async def getEntriesByStatus (
        db : Session ,
        filters : EntriesStatusFilter
) :
    company = get_users_zone(db)
    query = db.query(Entries).filter(Entries.company_id == company.id)
    if filters.status :
        query = query.filter(Entries.status == filters.status)
    total = query.count()
    items = (
        query
        .order_by(Entries.id.desc())
        .offset(filters.offset)
        .limit(filters.size)
        .all()
    )
    return OkRes(
        {
            "result" : [public_entry_dump(item , can_see_files=True) for item in items] ,
            "total" : total
        }
    )


async def setEntryStatus (
        db : Session ,
        id : str ,
        data : EntryStatusDto
) :
    company = get_users_zone(db)
    entry = db.query(Entries).filter(
        Entries.public_id == id ,
        Entries.company_id == company.id
    ).one_or_none()
    if not entry :
        return NotFoundRes(
            {
                "result" : "no entry found"
            }
        )
    entry.status = data.status
    db.commit()
    return OkRes(
        {
            "result" : "entry status changed"
        }
    )


async def getPurchasedEntries (
        db : Session ,
        user : Partner ,
        querySize : GetDataQuerySize
) :
    # محتواهایی که کاربر کلید دسترسی‌شون رو داره (خریداری شده)
    query = db.query(Entries).filter(
        Entries.id.in_(
            db.query(PartnerAcsessKeys.entry_id).filter(PartnerAcsessKeys.creator_id == user.id)
        ) ,
        Entries.status == StatusEnum.ACTIVE
    )
    total = query.count()
    entries = (
        query
        .order_by(Entries.id.desc())
        .offset(querySize.offset)
        .limit(querySize.size)
        .all()
    )
    return OkRes(
        {
            "result" : [public_entry_dump(entry , can_see_files=True) for entry in entries] ,
            "total" : total
        }
    )
