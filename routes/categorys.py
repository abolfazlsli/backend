from core.packages.controllers import *
from schema.categorys import *
from services.category import *
from core.docs.categories import TagsDoc
category_router = APIRouter(
    prefix="/categorys"
)

tags = TagsDoc()

@category_router.post("/create" , tags=[tags.categories])
async def create_category (
    db : Annotated[Session , Depends(get_db)] ,
    admin : Annotated[Admin , Depends(get_current_admin)] , 
    data : Annotated[AddCategory , Body()]
) :
    return await createCategory(db , admin , data)


@category_router.post("/gruop/create" , tags=[tags.categories])
async def create_group_category (
    db : Annotated[Session , Depends(get_db)] ,
    admin : Annotated[Admin , Depends(get_current_admin)] ,
    data : Annotated[AddCategoryGroup , Body()]
) :
    return await createCategoryGroup(db , admin , data)




@category_router.get("/categorys" , tags=[tags.categories], response_model=GetCategoryRes)
async def get_category_list (
    db : Annotated[Session , Depends(get_db)] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getCategories(db , querySize)


@category_router.get("/group-categories" , tags=[tags.categories] , response_model=GetGroupCategoriesRes)
async def get_group_categories (
    db : Annotated[Session , Depends(get_db)] ,
    querySize : Annotated[GetDataQuerySize , Query()]
) :
    return await getGroupCategories(db , querySize)


@category_router.get("/categorys/entries" , 
                     tags=[tags.categories] ,
                       response_model=GetCategoryEntriesRes
                     )
async def get_category_entries (
    db : Annotated[Session , Depends(get_db)] ,
    filters : Annotated[GetCategorysContentBySize , Query()] ,
) :
    return await getCategorysEntries(db , filters)