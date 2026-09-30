from core.packages.basic import *
from core.docs.users import Tags
from core.packages.controllers import *
from schema.users import *
from services.users import *


users_router = APIRouter(
    prefix="/users"
)

@users_router.post("/register", tags=[Tags.logins])
async def register_user(
    db : Annotated[Session , Depends(get_db)], 
    info : Annotated[RegisterStudentDto , Body()]
) :
    return await registerUser(db , info)

@users_router.post("/login" , tags=[Tags.logins])
async def login_user (
    db : Annotated[Session , Depends(get_db)] ,
    data : Annotated[LoginUserDto , Body()]
) :
    return await loginUser(db , data)


@users_router.post("/role-up" , tags=[Tags.roles])
async def role_up (
    db : Annotated[Session , Depends(get_db)] ,
    usersAdmin : Annotated[Partner , Depends(require_user_by_role("admin"))]
) :
    return


@users_router.get("/profile" , tags=[Tags.logins])
async def get_user_profile (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("admin" , "managers" , "students"))]
) :
    return await getProfile(db , user)
