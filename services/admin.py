from core.packages.services import *
from database.admins import *
from schema.admin import *
from core.utils.dataprocess import *

async def createPremissionService (
        db : Session ,
        admin : Admin ,
        data : AddPremission 
) :
    premission = Premisions(
        name = data.name ,
        code = data.code.strip() , 
        creator_id = admin.id
    )
    db.add(premission)
    db.commit()
    return OkRes(
        {
            'result' : "premission added"
        }
    )


async def getPremisions (
        db : Session ,
        user : Union[Admin , Partner] ,
        querySize : GetDataQuerySize
) :
    premissions = (db.query(Premisions))
    return {
        "result" : premissions
        .order_by(Premisions.id.asc())
        .offset(querySize.offset)
        .limit(querySize.size).all() ,
        "total" : premissions.count()
    }


async def editPremissions (
        db : Session , 
        admin : Admin ,
        data : EditPremission
) :
    premision = db.query(Premisions).filter(Premisions.public_id == data.id).one_or_none()
    if not premision :
        return NotFoundRes(
            {
                "result" : "no premission found"
            }
        )
    update_if_not_none(premision , data , ['name' , "code" , "status"])
    db.commit()
    return OkRes(
        {
            "result" : "edit saved"
        }
    )


async def createRole (
        db : Session , 
        user : Union[Admin , Partner] ,
        data : CreateRoleDto
) :
    role = Role(
        name = data.name ,
        caption = data.caption if data.caption else ""
    )
    if data.premissionsid :
        premissions = db.query(Premisions).filter(
            Premisions.public_id.in_(data.premissionsid)
        )
        role.permissions = premissions.all()
    
    if isinstance(user , Partner) :
        role.partner_creator_id = user.id
        role.company_id = user.company_id
    elif isinstance(user , Admin) and data.companyId :
        company = db.query(Company).filter(Company.public_id == data.companyId).one_or_none()
        if company :
            role.company_id = company.id
    db.add(role)
    db.commit()
    return OkRes(
        {
            "result" : "role created"
        }
    )

async def setPremissionToRole(
        db : Session , 
        data : SetPremissionToRoleDto , 
        user : Union[Admin , Partner]
) :
    role = db.query(Role).filter(Role.public_id == data.roleid)
    premission = db.query(Premisions).filter(Premisions.public_id == data.permissionid).one_or_none()
    if isinstance(user , Partner) :
        role = role.filter(Role.company_id == user.company_id)
    if (not role.one_or_none()) or (not premission) :
        return NotFoundRes(
            {
                "result" : "data not found"
            }
        )
    premissionrole = PremisionRole(
        premision_id = premission.id ,
        role_id = role.one_or_none().id
    )
    db.add(premissionrole)
    db.commit()
    return OkRes(
        {
            "result" : 'premission opend for role'
        }
    )


async def getRoles (
        db : Session, 
        user : Admin ,
        querySize : GetDataQuerySize
) :
    roles = db.query(Role)
    if isinstance(user , Partner) :
        roles = roles.filter(or_(Role.company_id == user.company_id , Role.company_id.is_(None)) , not_(Role.id == 1))
    return {
        "result" : roles
        .order_by(Role.id.asc())
        .offset(querySize.offset)
        .limit(querySize.size)
        .all() ,
        "total" : roles.count()
    }



async def getPublicRoles(
    db: Session,
    querySize: GetDataQuerySize
):
    query = (
        db.query(Role)
        .filter(Role.company_id.is_(None) ,  not_(Role.id == 1))
    )

    total = query.count()

    result = (
        query
        .order_by(Role.id.asc())
        .offset(querySize.offset)
        .limit(querySize.size)
        .all()
    )

    return {
        "result": result,
        "total": total
    }


async def getCompanyRoles(
    db: Session,
    user: Union[Admin, Partner],
    querySize: GetDataQuerySize,
    company_id: str | None = None
):
    query = (
        db.query(Role)
        .filter(Role.company_id.isnot(None))
    )

    if isinstance(user, Partner):
        query = query.filter(
            Role.company_id == user.company_id
        )

    elif company_id is not None:
        query = query.filter(
            Role.company_id == company_id
        )

    total = query.count()

    result = (
        query
        .order_by(Role.id.asc())
        .offset(querySize.offset)
        .limit(querySize.size)
        .all()
    )

    return {
        "result": result,
        "total": total
    }


async def removePremissionFromRole (
        db : Session ,
        user : Union[Admin , Partner] ,
        data : RemovePremissionFromRole
) :
    role = db.query(Role).filter(Role.public_id == data.roleid)
    if isinstance(user , Partner) :
        role = role.filter(Role.company_id == user.company_id)
    premission = db.query(Premisions).filter(Premisions.public_id == data.permissionid).one_or_none()
    if (not role.one_or_none()) or (not premission) :
        return NotFoundRes(
            {
                "result" : "data not found"
            }
        )
    premissionrole = db.query(PremisionRole).filter(
            PremisionRole.premision_id == premission.id ,
            PremisionRole.role_id == role.one_or_none().id
        )
    if premissionrole.count() == 0 :
            return NotFoundRes(
                {
                    "result" : "cant find data"
                }
            )
    premissionrole.delete()
    db.commit()
    return OkRes(
            {
                "result" : "premission removed"
            }
        )

async def getPermissionById(
        db : Session ,
        admin : Admin ,
        id : str
) :
    premission = db.query(Premisions).filter(
        Premisions.public_id == id
    ).one_or_none()
    if not premission :
        return NotFoundRes(
            {
                "result" : 'data not found'
            }
        )
    return OkRes(
        {
            "result" : PremissionsOutModel.model_validate(premission).model_dump()
        }
    )

async def getRoleById (
        db : Session ,
        admin : Admin ,
        id : str
) :
    premission = db.query(Role).filter(
        Role.public_id == id
    ).one_or_none()
    if not premission :
        return NotFoundRes(
            {
                "result" : 'data not found'
            }
        )
    return OkRes(
        {
            "result" : RoleOut.model_validate(premission).model_dump()
        }
    )


async def editRole(
        db : Session ,
        user : Union[Admin , Partner] ,
        data : EditRoleDto
) :
    role = db.query(Role).filter(
        Role.public_id == data.roleid
    )
    if isinstance(user , Partner) :
        role = role.filter(Role.company_id == user.company_id)
    if not role.one_or_none() :
        return NotFoundRes(
            {
                "result" : "role not found"
            }
        )
    update_if_not_none(role.one_or_none() , data , ['name' , "caption"])
    if data.premissionsid :
        premissions = db.query(Premisions).filter(
            Premisions.public_id.in_(data.premissionsid)
        ).all()
        role.one_or_none().permissions = premissions
    db.commit()
    return OkRes(
        {
            "result" : {
                "message" :'role edited' ,
                "data" : RoleOut.model_validate(role.one_or_none()).model_dump()
                } 
        }
    )


async def createPartner(
        db : Session ,
        user : Union[Admin , Partner] ,
        data : CreatePartnerDto
) :
    company = None
    if isinstance(user , Partner) :
        company = db.query(Company).filter(Company.id == user.company_id).one_or_none()
    elif isinstance(user , Admin) :
        company = db.query(Company).filter(Company.public_id == data.companyId).one_or_none()
    if not company :
        return NotFoundRes(
            {
                "result" : "company not found"
            }
        )
    partner = Partner(
        name=data.name , 
        username = data.username ,
        password = data.password ,
        phone = data.phone , 
        creator_id = user.id ,
        company_id = company.id
    )
    if data.role_id :
        role = db.query(Role).filter(
            Role.public_id == data.role_id
        ).one_or_none()
        partner.role_id = role.id
    db.add(partner)
    db.commit()
    return OkRes(
        {
            "result" : "partner created"
        }
    )



async def editPartnerInfo (
        db : Session ,
        partner : Partner ,
        data : EditPartner
) :
    partner = db.query(Partner).filter(
        Partner.id == partner.id
    ).one_or_none()
    if not partner :
        return NotFoundRes(
            {
                "result" : "partner not found"
            }
        )
    update_if_not_none(partner , data , ['name' ,'username','password'])
    db.commit()
    return OkRes(
        {
            "result" : "partner edited"
        }
    )


async def banPartner(
    db: Session,
    user: Union[Partner, Admin],
    id: str,
    data: BanPartnerMessage,
):
    partner = db.query(Partner).filter(Partner.public_id == id , Partner.company_id == user.company_id).one_or_none()
    if partner is None:
        return NotFoundRes({"result": "partner not found"})

    banned_by_admin_id = None
    banned_by_partner_id = None

    if isinstance(user, Admin):
        banned_by_admin_id = user.id
    elif isinstance(user, Partner) :
        if partner.id == user.id:
            return BadRequestRes({"result": "you cannot ban yourself"})
        if not is_descendant_of(db , user.id , partner.id) :
            return ForbiddenRes(
                {
                    "result" : "you dont have acsess to this user"
                }
            )
        banned_by_partner_id = user.id
    else:
        return ForbiddenRes({"result": "access denied"})

    ban_log = PartnerBanLog(
        partner_id=partner.id,
        reason=data.reason,
        extra_explain=data.extra_explain,
        banned_by_admin_id=banned_by_admin_id,
        banned_by_partner_id=banned_by_partner_id,
    )
    db.add(ban_log)
    partner.status = "banned"
    db.commit()

    return OkRes({"result": "partner banned"})


async def setRoleForPartner (
        db : Session ,
        user : Union[Admin , Partner] ,
        data : SetRoleForPartner
) :
    if user.public_id == data.partner_id :
        return ForbiddenRes(
            {
                "result" : "you cant set role for your self"
            }
        )
    partner = None
    if isinstance(user , Admin) :
        partner = db.query(Partner).filter(
            Partner.public_id == data.partner_id , not_(Partner.company_id == 1)
        ).one_or_none()
    elif isinstance(user , Partner) :
        partnercheck = db.query(Partner).filter(
                    Partner.public_id == data.partner_id , 
                    Partner.company_id == user.company_id
            ).one_or_none()
        if partnercheck is not None and is_descendant_of(db , user.id , partnercheck.id) :
            partner = partnercheck
    else :
        return ForbiddenRes(
            {
                "result": "you have no acsess to this data"
            }
        )
    role = db.query(Role).filter(
        Role.public_id == data.role_id
    )
    if isinstance(user , Partner) :
        role = role.filter(or_(Role.company_id == user.company_id , Role.company_id == None))
    if (not partner) or (not role.one_or_none()) :
        print(partner , role.one_or_none())
        return NotFoundRes(
            {
                "result" : "cant find data"
            }
        )
    partner.role_id = role.one_or_none().id
    db.commit()
    return OkRes(
        {
            "result" : "role set for partner"
        }
    )


async def getPartners (
       db : Session ,
       user : Union[Admin , Partner] ,
       querySize : GetDataQuerySize
) :
    partners = db.query(Partner).filter(not_(Partner.company_id == 1))
    if isinstance(user , Partner) :
        partners = partners.filter(Partner.company_id == user.company_id)
    return {
        "result" : partners
        .order_by(Partner.id.asc())
        .offset(querySize.offset)
        .limit(querySize.size).all() ,
        "total" : partners.count()
    }



async def getPartnerById (
       db : Session ,
       user : Union[Admin , Partner] ,
       id : str
) :
    partners = db.query(Partner).filter(Partner.public_id == id)
    if isinstance(user , Partner) :
        partners = partners.filter(Partner.company_id == user.company_id)
    if not partners :
        return NotFoundRes(
            {
                "result" : "no data found"
            }
        )
    return {
        "result" : PartnerOutPublic.model_validate(partners.one_or_none()).model_dump()
    }


async def getProfile (
        db : Session ,
        user : Union[Admin , Partner]
) :
    
    return OkRes(
        {
            "result" : PartnerOut.model_validate(user).model_dump()
        }
    )


async def removeRole(
        db : Session ,
        user : Union[Admin , Partner],
        id : str
) :
    role = db.query(Role).filter(Role.public_id == id).first()
    partners = db.query(Partner).filter(
            Partner.role_id == role.id
        ).all()
    if isinstance(user , Admin) :
        for partner in partners:
            partner.role_id = None
        role.permissions.clear()
        db.delete(role)
        db.commit()
    elif isinstance(user , Partner) :
        if user.id == role.partner_creator_id :
            for partner in partners:
                partner.role_id = None
            role.permissions.clear()
            db.delete(role)
            db.commit()
        else :
            return ForbiddenRes(
                {
                    "result" : "you dont have acsess to this data"
                }
            )
    else :
        return ForbiddenRes(
                        {
                            "result" : "you dont have acsess to this data"
                        }
                    )
    return OkRes(
        {
            "result" : "role deleted"
        }
    )


async def createCompany(
        db : Session ,
        admin : Admin ,
        data : CreateCompanyDto
):
    company = Company(
        name = data.name ,
        addres = data.addres ,
        telphone = data.telphone ,
        creator_id = admin.id
    )
    db.add(company)
    db.commit()
    return OkRes(
        {
            "result" : "company added"
        }
    )
async def getAllCompanys (
        db : Session , 
        admin : Admin , 
        querySize : GetDataQuerySize
) :
    companys = db.query(Company)

    return {
        "result" : companys
        .offset(querySize.offset)
        .limit(querySize.size)
        .all() ,
        "total" :companys.count()
    }