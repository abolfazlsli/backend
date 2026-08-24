from core.packages.services import *
from schema.content import *
from database.content import *
from core.utils.dataprocess import update_if_not_none


async def createFilds (
        db : Session ,
        user : Partner ,
        data : CreateFildDto
) :
    if isinstance(user , Admin) :
        return ForbiddenRes(
            {
                "result" : "sorry admin have no acsess here"
            }
        )
    if data.type_of in (TypeOfEnum.SELECT , TypeOfEnum.MULTISELECT) :
        if not data.options or len(data.options) == 0:
            return BadRequestRes(
            {
                "result" : "we need options of select"
            }
        )
    fild = Filds(
        name=data.name ,
        type_of=data.type_of ,
        company_id = user.company_id ,
        creator_id = user.id
    )
    db.add(fild)
    db.flush()
    if (data.options) and (data.type_of in (TypeOfEnum.SELECT , TypeOfEnum.MULTISELECT)):
        for i in data.options :
            db.add(
                FildOptions(fild_id = fild.id , value = i.value , label = i.label , order = i.order , company_id = user.company_id , creator_id = user.id)
            )
    db.commit()
    return OkRes(
        {
            "result" : "fild created"
        }
    )


async def editFilds (
        db : Session ,
        partner : Partner ,
        data : EditFildsDto
) :
    if data.type_of in (TypeOfEnum.SELECT , TypeOfEnum.MULTISELECT) :
            if not data.options or len(data.options) :
                return BadRequestRes(
                    {
                        "result" : "we need options while data type is select or multiselect"
                    }
                )
    fild = db.query(Filds).filter(Filds.public_id == data.fild_id , Filds.company_id == partner.company_id).one_or_none()
    if not fild :
        return NotFoundRes(
            {
                "result" : "no fild found"
            }
        )
    update_if_not_none(fild , data , ['name' , 'type_of'])
    if data.options :
        fild.options = []
        for i in data.options :
            db.add(
                FildOptions(fild_id = fild.id , value = i.value , label = i.label , order = i.order)
            )
    db.commit()

    return OkRes(
        {
            "result" : "fild edited"
        }
    )



async def removeOptionFromFild (
        db : Session , 
        partner : Partner ,
        data : RemoveOptionDto
) :
    fild = db.query(Filds).filter(
        Filds.company_id == partner.company_id ,
        Filds.public_id == data.fild_id
    ).one_or_none()
    if not fild :
        return NotFoundRes(
            {
                "result" : "no fild found"
            }
        )
    fildOption = db.query(FildOptions).filter(
        FildOptions.fild_id == fild.id ,
        FildOptions.public_id == data.option_id
    ).one_or_none()

    if not fildOption :
        return NotFoundRes(
            {
                "result" : "no fild option found"
            }
        )
    fildOption.is_active = False
    db.commit()
    return OkRes(
        {
            "result" : "fild option removed"
        }
    )



async def getFilds (
        db : Session ,
        partner : Partner ,
        querySize : GetDataQuerySize
) :
    filds = db.query(Filds)
    total = filds.count()
    
    return {
        "result" : filds
        .offset(querySize.offset)
        .limit(querySize.size)
        .all() ,
        "total" : total
    }