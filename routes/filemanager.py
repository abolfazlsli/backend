from core.packages.controllers import *
from services.filesmanager import *
from core.docs.files import TagsDocs

tags = TagsDocs()

file_router = APIRouter(
    prefix="/files"
)



@file_router.post("/upload" , tags=[tags.files])
async def upload_file (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Union[Admin , Partner] , Depends(get_current_admin_or_partner)] ,
    file : Annotated[UploadFile , File(...)]
) :
    # uploaded_file = file

    return await uploadFiles(db , file)





@file_router.get("/get-file/{id}" , tags=[tags.files])
async def get_file (
    db : Annotated[Session , Depends(get_db)] ,
    id : str
) :
    return await getFile(db , id)