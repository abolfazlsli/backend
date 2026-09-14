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


@content_router.put("/instance/unarchiveFilds/{instance_fildid}" , tags=[tags.istance])
async def unarchive_fild_instance (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.edit"))] ,
    instance_fildid : str
) :
    return await unarchiveInstanceFilds(db , partner , instance_fildid)


@content_router.delete("/instance/archive/{id}" , tags=[tags.istance])
async def archive_instance (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.edit"))],
    id : str
) :
    return await archiveInstance(db , partner , id)


@content_router.delete("/instance/archiveFilds/{instance_fildid}" , tags=[tags.istance])
async def archive_fild_instance (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("instance.edit"))] ,
    instance_fildid : str
) :
    return await archiveInstanceFilds(db , partner , instance_fildid)

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

@content_router.get("/entry" , tags=[tags.entries] , response_model=EntryRes)
async def get_entrys(
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("entry.get"))] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getEntrys(db , partner , querySize)



@content_router.get("/entry/filds/{entry_id}" , tags=[tags.entries] , response_model=EntryOut)
async def get_entry_filds(
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("entry.get"))] ,
    entry_id : str
) :
    return await getEntryFilds(db , partner , entry_id)


@content_router.get("/entry-placements" , tags=[tags.entries])
async def get_entry_placements (
    partner : Annotated[Partner , Depends(require_partner)]
) :
    return OkRes(
        {
            "result" : [
                {
                    "key" : "title" , 
                    "value" : "موضوع" 
                } ,
                {
                    "key" : "banner" , 
                    "value" : "بنر" 
                } ,
                {
                    "key" : "caption" , 
                    "value" : "کپشن" 
                } ,
                {
                    "key" : "badge" , 
                    "value" : "بج" 
                } ,
                {
                    "key" : "payneed" ,
                    "value" : "نیاز به پرداخت"
                }
            ]
        }
    )


@content_router.post("/senddata" , tags=[tags.entriesData])
async def create_enteryData (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("data.create"))] ,
    data : Annotated[CreateEnteryData , Body()]
) :
    return await createEntryData(db , partner , data)


@content_router.get("/entry-data" , response_model=EntryDataRes , tags=[tags.entriesData])
async def get_entry_data (
    db : Annotated[Session , Depends(get_db)] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getEntryDataList(db , querySize)