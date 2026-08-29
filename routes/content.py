from core.packages.basic import *
from core.docs.content import Tags
from core.packages.controllers import *
from services.content import *


content_router = APIRouter(
    prefix="/content" 
)



tags = Tags()


# @content_router.post("" , tags=[tags.content])
# async def create_filds (
#     db : Annotated[Session , Depends(get_db)] ,
#     user : Annotated[Union[Admin , Partner] , Depends(require_any_permission("content.create"))]
# ) :
#     return 



@content_router.get("/filds" , tags=[tags.filds] , response_model=FildsResponce)
async def get_filds (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("filds.get"))] , 
    querySize : Annotated[GetDataQuerySize , Query()]
):
    return await getFilds(db , partner , querySize)


@content_router.get("/filds/{id}" , tags=[tags.filds])
async def get_fild_by_id (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("filds.get"))] , 
    id : str
) : 
    return await getFildById(db , partner , id)


@content_router.post("/filds" , tags=[tags.filds])
async def create_filds (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner, Depends(require_partner_permission("filds.create"))],
    data : Annotated[CreateFildDto , Body()]
):
    return await createFilds(
        db , user , data
    )

@content_router.put("/optionfild-to-fild" , tags=[tags.filds])
async def add_optionfild_to_fild (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("filds.edit"))] ,
    data : Annotated[AddFildOprionToFild , Body()]
) :
    return await addFildOptionToFild(db , partner , data)


@content_router.put("/filds" , tags=[tags.filds])
async def edit_filds (
    db : Annotated[Session , Depends(get_db)] , 
    partner : Annotated[Partner , Depends(require_partner_permission("filds.edit"))] ,
    data : Annotated[EditFildsDto , Body()]
) :
    return await editFilds(db , partner , data)

@content_router.put("/filds/unarchive/{id}" , tags=[tags.filds])
async def archive_filds (
    db : Annotated[Session , Depends(get_db)],
    partner : Annotated[Partner , Depends(require_partner_permission("filds.edit"))] ,
    id : str
) :
    return await unarchiveFilds(db , partner , id)

@content_router.delete("/filds/archive/{id}" , tags=[tags.filds])
async def archive_filds (
    db : Annotated[Session , Depends(get_db)],
    partner : Annotated[Partner , Depends(require_partner_permission("filds.edit"))] ,
    id : str
) :
    return await archiveFilds(db , partner , id)


@content_router.delete("/fildsoption" , tags=[tags.filds])
async def delete_fildoption (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("fild.edit"))] ,
    data : Annotated[RemoveOptionDto , Body()]
) :
    return await removeOptionFromFild(db , partner , data)




@content_router.post("/instance" , tags=[tags.istance])
async def create_instance (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.create"))] ,
    data : Annotated[CreateInstanceDto , Body()]
) :
    return await createInstance(db , partner , data)


@content_router.get("/instances" , tags=[tags.istance] , response_model=InstanceResponce)
async def get_instance_list (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.get"))] , 
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getInstance(db , partner , querySize)

# @content_router.get("/instance/{id}" , tags=[tags.istance])
# async def get_instance_by_id (
#     db : Annotated[Session , Depends(get_db)] ,
#     partner : Annotated[Partner , Depends(require_partner_permission("instance.get"))],
#     id : str
# ):
#     return await getInstanceById(db , partner , id)

@content_router.put("/instance" , tags=[tags.istance])
async def edit_instance(
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.edit"))] ,
    data : Annotated[EditInstanceDto , Body()]
) :
    return await editInstance(db , partner , data)



@content_router.get("/instance/filds/{instance_id}" , tags=[tags.istance] , response_model=SingleInstanceFildsOut)
async def get_instance_filds (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.get"))] ,
    instance_id : str
) :
    return await getInstanceFilds(
        db , partner , instance_id
    )


@content_router.put("/instance/unarchive/{id}" ,tags=[tags.istance])
async def unarchive_instance (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.edit"))],
    id : str
) :
    return await unarchiveInstance(db , partner , id)

@content_router.delete("/instance/archive/{id}" , tags=[tags.istance])
async def archive_instance (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.edit"))],
    id : str
) :
    return await archiveInstance(db , partner , id)

# @content_router.get("/instance/{id}" , tags=[tags.istance])
# async def get_instance_by_id (
#     db : Annotated[Session , Depends(get_db)] ,
#     partner : Annotated[Partner , Depends(require_any_permission("instance.get"))] ,
#     id : str
# ) :
#     return await getInstanceId(db , partner , id)



@content_router.post("/entry" , tags=[tags.entries])

async def create_entry (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("entry.create"))],
    data : Annotated[CreateEntryDto , Body()]
) :
    return await createEntry(db , partner , data)

@content_router.get("/entry" , tags=[tags.entries])
async def get_entrys(
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("entry.get"))] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getInstanceFilds(db , partner , querySize)


