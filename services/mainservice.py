from core.packages.basic import *
async def healthCheckService () :
    return OkRes({
        "result" : {
            "message" : "server is running" , 
            "version" : "1.0.0"
        }
    })