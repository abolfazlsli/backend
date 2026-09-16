from core.packages.controllers import *
from core.packages.database import *
from core.docs import admins
from database.admins import *
from services.admin import *
from schema.admin import *

admin_router = APIRouter(
    prefix="/admin" ,
)

tags = admins.TagsDocs()

@admin_router.post("/permissions" , tags=[tags.premisions])
async def create_premision (
    db : Annotated[Session , Depends(get_db)] ,
    admin : Annotated[Admin , Depends(get_current_admin)] ,
    data : Annotated[AddPremission , Body()]
    ) :
    return await createPremissionService(db , admin , data)

@admin_router.get("/permissions" , tags=[tags.premisions] , response_model=PremissionsResponce)
async def get_premisions (
    db : Annotated[Session , Depends(get_db)] , 
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("premissions.read"))] ,
    filters : Annotated[GetDataQuerySize , Query()]
) :
    return await getPremisions(db , user , filters)

@admin_router.get("/permissions/{id}" , tags=[tags.premisions])
async def get_permissions_by_id (
    db : Annotated[Session , Depends(get_db)], 
    admin : Annotated[Admin , Depends(get_current_admin)] ,
    id : str
) :
    return await getPermissionById(db , admin , id)

@admin_router.put("/premissions" , tags=[tags.premisions])
async def edit_premission (
    db : Annotated[Session , Depends(get_db)] ,
    admin : Annotated[Admin , Depends(get_current_admin)] ,
    data : Annotated[EditPremission , Body()]
) :
    return await editPremissions(db , admin , data)



@admin_router.post("/roles" , tags=[tags.roles])
async def create_role (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Pattern] , Depends(require_any_permission("role.create"))],
    data : Annotated[CreateRoleDto , Body()]
) :
    return await createRole(db , user , data)

@admin_router.get("/roles" , tags=[tags.roles] , response_model=RolesResponce)
async def get_roles (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("role.get"))] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getRoles(db , user , querySize)

@admin_router.get("/roles/public" , tags=[tags.roles] , response_model=RolesResponce)
async def get_public_roles (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_permission("role.get"))] , 
    querySize : Annotated[GetDataQuerySize , Query()]
):
    return await getPublicRoles(db , querySize)



@admin_router.get("/roles/company" , tags=[tags.roles] , response_model=RolesResponce)
@admin_router.get("/roles/company/{id}" , tags=[tags.roles] , response_model=RolesResponce)
async def get_company_roles (
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[Admin | Partner, Depends(require_permission("role.get"))],
    querySize: Annotated[GetDataQuerySize, Depends()],
    id: str | None = None,
) :
    return await getCompanyRoles(db , user , querySize , id)


@admin_router.get("/roles/{id}" , tags=[tags.roles])
async def get_role_by_id (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("role.get"))] ,
    id : str
) :
    return await getRoleById(db , user , id)

@admin_router.put("/roles" ,tags=[tags.roles])
async def edit_role(
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("role.edit"))],
    data : Annotated[EditRoleDto , Body()]
) :
    return await editRole(db , user , data)

@admin_router.put("/asying-premission-to-role" , tags=[tags.roles])
async def set_premission_for_role (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("role.edit"))] ,
    data : Annotated[SetPremissionToRoleDto , Body()]
):
    return await setPremissionToRole(db , data , user)


@admin_router.delete("/remove-premission" ,  tags=[tags.roles])
async def delete_premission_from_partner(
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("role.remove.premission"))] ,
    data : Annotated[RemovePremissionFromRole , Body()]
) :
    
    return await removePremissionFromRole(db , user , data)


@admin_router.delete("/role/{id}" , tags=[tags.roles])
async def remove_role (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Partner , Admin] , Depends(require_any_permission('role.remove'))] ,
    id : str
) :
    return await removeRole(db , user , id)

@admin_router.post("/partner" , tags=[tags.partners])
async def create_partner (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("partners.create"))] ,
    data : Annotated[CreatePartnerDto , Body()]
) :
    return await createPartner(db , user , data)

@admin_router.put("/partner" , tags=[tags.partners])
async def edit_partner (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner)] ,
    data : Annotated[EditPartner , Body()]
) :
    return await editPartnerInfo(db , partner , data)


@admin_router.put("/set-role" , tags=[tags.partners])
async def set_role_for_partner(
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("partners.role.set"))] ,
    data : Annotated[SetRoleForPartner , Body()]

) :
    return await setRoleForPartner(db , user , data)


@admin_router.get("/partners" , response_model=PartnersResponce , tags=[tags.partners])
async def get_all_partners (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("partners.get"))] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getPartners(db , user , querySize)



@admin_router.get("/partners/{id}" , tags=[tags.partners])
async def get_partners_by_id (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("partners.get"))] ,
    id : str
) :
    return await getPartnerById(db , user , id)

@admin_router.get("/me" , tags=[tags.partners])
async def get_partner_profile(
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin ,Partner] , Depends(get_current_admin_or_partner)]
) :
    return await getProfile(db , user)


@admin_router.delete("/partner/{id}" , tags=[tags.partners])
async def ban_partner (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(get_current_admin_or_partner)] ,
    id : str ,
    data : Annotated[BanPartnerMessage , Body()]
) :
    return await banPartner(db , user , id , data)



@admin_router.post("/company" , tags=[tags.companys])
async def create_company (
    db : Annotated[Session , Depends(get_db)] ,
    admin : Annotated[Admin , Depends(get_current_admin)],
    data : Annotated[CreateCompanyDto , Body()]
) :
    return await createCompany(db , admin , data)


@admin_router.get("/companys" , tags=[tags.companys] , response_model=CompanyResult)
async def get_all_companys (
    db : Annotated[Session , Depends(get_db)] ,
    admin : Annotated[Admin , Depends(get_current_admin)] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getAllCompanys(db , admin , querySize)