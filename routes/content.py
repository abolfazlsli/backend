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

@content_router.post("/filds" , tags=[tags.filds])
async def create_filds (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner, Depends(require_partner_permission("filds.create"))],
    data : Annotated[CreateFildDto , Body()]
):
    return await createFilds(
        db , user , data
    )

@content_router.put("/filds" , tags=[tags.filds])
async def edit_filds (
    db : Annotated[Session , Depends(get_db)] , 
    partner : Annotated[Partner , Depends(require_partner_permission("filds.edit"))] ,
    data : Annotated[EditFildsDto , Body()]
) :
    return await editFilds(db , partner , data)

@content_router.delete("/fildsoption" , tags=[tags.filds])
async def delete_fildoption (
    db : Annotated[Session , Depends(get_db)] ,
    partner : Annotated[Partner , Depends(require_partner_permission("fild.edit"))] ,
    data : Annotated[RemoveOptionDto , Body()]
) :
    return await removeOptionFromFild(db , partner , data)