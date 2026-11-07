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
    usersAdmin : Annotated[Partner , Depends(require_user_by_role("admin"))] ,
    data : Annotated[RoleUpDto , Body()]
) :
    return await roleUp(db , usersAdmin , data)


@users_router.get("/list" , tags=[Tags.roles])
async def get_users_list (
    db : Annotated[Session , Depends(get_db)] ,
    usersAdmin : Annotated[Partner , Depends(require_user_by_role("admin"))] ,
    filters : Annotated[UsersFilter , Query()]
) :
    return await getUsers(db , filters)


@users_router.post("/role-request" , tags=[Tags.roles])
async def create_role_request (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("students"))] ,
    data : Annotated[RoleRequestDto , Body()]
) :
    return await createRoleRequest(db , user , data)


@users_router.get("/role-request" , tags=[Tags.roles])
async def get_my_role_request (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("admin" , "managers" , "students"))]
) :
    return await getMyRoleRequest(db , user)


@users_router.get("/role-requests" , tags=[Tags.roles])
async def get_role_requests (
    db : Annotated[Session , Depends(get_db)] ,
    usersAdmin : Annotated[Partner , Depends(require_user_by_role("admin"))] ,
    filters : Annotated[RoleRequestsFilter , Query()]
) :
    return await getRoleRequests(db , filters)


@users_router.put("/role-requests/{id}" , tags=[Tags.roles])
async def review_role_request (
    db : Annotated[Session , Depends(get_db)] ,
    usersAdmin : Annotated[Partner , Depends(require_user_by_role("admin"))] ,
    id : str ,
    data : Annotated[ReviewRoleRequestDto , Body()]
) :
    return await reviewRoleRequest(db , usersAdmin , id , data)


@users_router.get("/entries" , tags=[Tags.entries])
async def get_entries_by_status (
    db : Annotated[Session , Depends(get_db)] ,
    usersAdmin : Annotated[Partner , Depends(require_user_by_role("admin"))] ,
    filters : Annotated[EntriesStatusFilter , Query()]
) :
    return await getEntriesByStatus(db , filters)


@users_router.put("/entries/{id}/status" , tags=[Tags.entries])
async def set_entry_status (
    db : Annotated[Session , Depends(get_db)] ,
    usersAdmin : Annotated[Partner , Depends(require_user_by_role("admin"))] ,
    id : str ,
    data : Annotated[EntryStatusDto , Body()]
) :
    return await setEntryStatus(db , id , data)


@users_router.get("/entries/{id}/files" , tags=[Tags.entries])
async def get_entry_with_files (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("admin" , "managers" , "students"))] ,
    id : str
) :
    return await getEntryWithFiles(db , user , id)


@users_router.get("/saves" , tags=[Tags.saves])
async def get_saved_entries (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("admin" , "managers" , "students"))] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getSavedEntries(db , user , querySize)


@users_router.get("/saves/ids" , tags=[Tags.saves])
async def get_saved_entries_ids (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("admin" , "managers" , "students"))]
) :
    return await getSavedEntriesIds(db , user)


@users_router.post("/saves/{entry_id}" , tags=[Tags.saves])
async def toggle_save_entry (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("admin" , "managers" , "students"))] ,
    entry_id : str
) :
    return await toggleSaveEntry(db , user , entry_id)


@users_router.get("/purchased" , tags=[Tags.saves])
async def get_purchased_entries (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("admin" , "managers" , "students"))] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getPurchasedEntries(db , user , querySize)


@users_router.get("/profile" , tags=[Tags.logins])
async def get_user_profile (
    db : Annotated[Session , Depends(get_db)] ,
    user : Annotated[Partner , Depends(require_user_by_role("admin" , "managers" , "students"))]
) :
    return await getProfile(db , user)
