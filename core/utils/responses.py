from core.packages.controllers import *



def OkRes (context: str | dict) -> JSONResponse :
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=context
    )

def UnauthorizedRes (context: str | dict) -> JSONResponse :
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content=context
    )

def InternalServerErrorRes (context: str | dict , hiddenMaasage : str = "") -> JSONResponse :
    logger = open("./logText.txt" , "a+")
    logger.write(str(f"{context}\n{hiddenMaasage}\n"))
    logger.close()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=context
    )

def BadRequestRes (context: str | dict) -> JSONResponse :
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=context
    )

def ForbiddenRes (context: str | dict) -> JSONResponse :
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content=context
    )

def NotFoundRes (context: str | dict) -> JSONResponse :
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content=context
    )
def CreatedRes (context: str | dict) -> JSONResponse :
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=context
    )

