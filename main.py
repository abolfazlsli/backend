from core.packages.basic import *
from services.mainservice import *
from core.settings import settings
from routes.admin import admin_router
from routes.auth import auth_router
from routes.content import content_router
from routes.users import users_router
from routes.filemanager import file_router

app = FastAPI(
    docs_url=settings.setting.docs_url ,
    redoc_url=settings.setting.redocx_url ,
    title=settings.setting.title ,
    description=settings.setting.version,
    version=settings.setting.version ,
    # open
)


# allow_origins = {
#     "production": [
#         "*" ,
#         "https://ojagh.org",
#     ],
#     "stage": [
#         "*" ,
#         "https://web-stage.ojagh.org",
#         "https://api-stage.ojagh.org",
#         "https://media-stage.ojagh.org",
#     ],
#     "develop": [
#         "*" ,
#         "https://web-develop.ojagh.org",
#         "https://api-develop.ojagh.org",
#         "https://media-develop.ojagh.org",
#     ],
# }.get(settings.status, [])

# Middleware Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'] ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health-check" , tags=['health'])
async def healthCheck () :
    return await healthCheckService()




app.include_router(router=admin_router)
app.include_router(router=content_router)
app.include_router(router=users_router)

app.include_router(router=file_router)
app.include_router(router=auth_router)
