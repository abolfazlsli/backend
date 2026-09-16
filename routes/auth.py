from core.packages.controllers import *
from schema.auth import LoginModel
from core.docs.auth import *
from services.auth import *
auth_router = APIRouter(
    prefix="/auth"
)

tags = TagsDocs()

@auth_router.post("/admin/login" , response_model=LoginResponce , tags=[tags.auth ])
async def admin_login (
    db : Annotated[Session , Depends(get_db)] ,
    data : Annotated[LoginModel , Body()]
):
    return await loginUser(data , db)


@auth_router.post("/partner/login" , response_model=LoginResponce , tags=[tags.auth])
async def partner_login(
    db : Annotated[Session , Depends(get_db)] ,
    data : Annotated[LoginModel , Body()]
):
    return await loginPartner(data , db)