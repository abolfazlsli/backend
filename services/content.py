from core.packages.services import *
from schema.content import *
from database.content import *
from core.utils.dataprocess import update_if_not_none ,validate_entry_value
from core.packages.database import generate_public_id
from database.category import *


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
    # if data.type_of in (TypeOfEnum.SELECT , TypeOfEnum.MULTISELECT) :
    #         if not data.options or len(data.options) :
    #             return BadRequestRes(
    #                 {
    #                     "result" : "we need options while data type is select or multiselect"
    #                 }
    #             )
    fild = db.query(Filds).filter(Filds.public_id == data.fild_id , Filds.company_id == partner.company_id , Filds.status == StatusEnum.ACTIVE).one_or_none()
    if not fild :
        return NotFoundRes(
            {
                "result" : "no fild found"
            }
        )
    update_if_not_none(fild , data , ['name'])
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



async def createInstance (
        db : Session ,
        partner : Partner ,
        data : CreateInstanceDto
) :
    instance = Instances(
        name = data.name,
        caption = data.caption ,
        company_id = partner.company_id ,
        creator_id = partner.id
    )
    db.add(instance)
    db.flush()
    if data.filds :
        filds = db.query(Filds).filter(Filds.public_id.in_(data.filds) , Filds.status == StatusEnum.ACTIVE , Filds.company_id == partner.company_id).all()
        for fild in filds:
            db.add(
                InstanceFilds(
                    fild_id = fild.id , instance_id = instance.id, company_id = partner.company_id , creator_id = partner.id
                )
            )
    db.commit()
    return OkRes(
        {
            "result" : "instance generated"
        }
    )


async def getInstance(
        db : Session , 
        partner : Partner , 
        querySize : GetDataQuerySize
) :
    instances = db.query(Instances).filter(Instances.company_id == partner.company_id , Instances.status == StatusEnum.ACTIVE)
    total = instances.count()

    return {
        "result" : instances
        .offset(querySize.offset)
        .limit(querySize.size)
        .all() ,
        "total" : total
    }


async def addFildOptionToFild (
        db : Session ,
        partner : Partner ,
        data : AddFildOprionToFild
) :
    fild = db.query(Filds).filter(
        Filds.public_id == data.fild_id ,
        Filds.company_id == partner.company_id
    ).one_or_none()
    if not fild :
        return NotFoundRes(
            {
                "result" : "no fild found"
            }
        )
    if fild.type_of not in (TypeOfEnum.SELECT , TypeOfEnum.MULTISELECT) :
        return BadRequestRes(
            {
                "result" : "this fild is not select or multiselect"
            }
        )
    for fildoption in data.options :
        db.add(
            FildOptions(
                fild_id = fild.id ,
                value = fildoption.value ,
                label = fildoption.label ,
                order = fildoption.order
            )
        )
    db.commit()
    return OkRes(
        {
            "result" : "filds added"
        }
    )


async def editInstance(
        db : Session ,
        partner : Partner ,
        data : EditInstanceDto
) :
    instance = db.query(Instances).filter(
        Instances.public_id == data.instance_id , Instances.company_id == partner.company_id 
    ).one_or_none()
    if not instance :
        return NotFoundRes(
            {
                "result" : "no insance find"
            }
        )
    update_if_not_none(instance , data , ['name' , "caption"])
    if data.filds_id :
        filds = db.query(Filds).filter(Instances.public_id.in_(data.filds_id))
        for i in filds.all():
            db.add(
                InstanceFilds(
                    instance_id = instance.id ,
                    fild_id = i.id
                    )
            )
    db.commit()
    return OkRes(
        {
            "result" : "instance edited"
        }
    )


# async def getInstanceById (
#         db : Session ,
#         partner : Partner ,
#         id : str
# ):
#     instance = db.query(Instances).filter(Instances.public_id == id , Instances.company_id == partner.company_id , Instances.status == StatusEnum.ACTIVE).one_or_none()
#     if not instance :
#         return NotFoundRes(
#             {
#                 "result" : "no data found"
#             }
#         )
#     return OkRes(
#         {
#             "result" : InstanceOut.model_validate(instance).model_dump()
#         }
#     )



async def archiveInstance (
        db : Session ,
        partner : Partner ,
        id : str
) :
    instance = db.query(Instances).filter(
        Instances.company_id == partner.company_id ,
        Instances.public_id == id ,
        Instances.status == StatusEnum.ACTIVE
    ).one_or_none()
    if not instance :
        return NotFoundRes(
            {
                "result" : "no data founc"
            }
        )
    instance.status = StatusEnum.DISACTIVE
    db.commit()
    return OkRes(
        {
            "result" : "instance archived"
        }
    )



async def unarchiveInstance (
        db : Session ,
        partner : Partner ,
        id : str
) :
    instance = db.query(Instances).filter(
        Instances.company_id == partner.company_id ,
        Instances.public_id == id ,
        Instances.status == StatusEnum.DISACTIVE
    ).one_or_none()
    if not instance :
        return NotFoundRes(
            {
                "result" : "no data founc"
            }
        )
    instance.status = StatusEnum.ACTIVE
    db.commit()
    return OkRes(
        {
            "result" : "instance unarchived"
        }
    )


async def archiveFilds (
        db : Session , 
        partner : Partner , 
        id : str
) :
    fild = db.query(Filds).filter(
        Filds.public_id == id ,
        Filds.company_id == partner.company_id ,
        Filds.status == StatusEnum.ACTIVE
    ).one_or_none()
    if not fild :
        return NotFoundRes(
            {
                "result" : "no data found"
            }
        )
    fild.status == StatusEnum.DISACTIVE
    db.commit()

    return OkRes(
        {
            "result" : "fild archived"
        }
    )

async def unarchiveFilds (
        db : Session , 
        partner : Partner , 
        id : str
) :
    fild = db.query(Filds).filter(
        Filds.public_id == id ,
        Filds.company_id == partner.company_id ,
        Filds.status == StatusEnum.DISACTIVE
    ).one_or_none()
    if not fild :
        return NotFoundRes(
            {
                "result" : "no data found"
            }
        )
    fild.status == StatusEnum.ACTIVE
    db.commit()

    return OkRes(
        {
            "result" : "fild archived"
        }
    )



async def archiveInstanceFilds (
        db : Session ,
        partner : Partner ,
        id : str
) :
    instance_fild = db.query(InstanceFilds).filter(
        InstanceFilds.id == id ,
        InstanceFilds.status == StatusEnum.ACTIVE , 
        InstanceFilds.company_id == partner.company_id ,
    ).one_or_none()
    if not instance_fild : 
        return NotFoundRes(
            {
                "result" : "instance fild not found"
            }
        )
    instance_fild.status = StatusEnum.DISACTIVE
    db.commit()
    return OkRes(
        {
            "result" : "Instance Fild archived"
        }
    )


async def unarchiveInstanceFilds (
        db : Session ,
        partner : Partner ,
        id : str
) :
    instance_fild = db.query(InstanceFilds).filter(
        InstanceFilds.id == id ,
        InstanceFilds.status == StatusEnum.DISACTIVE , 
        InstanceFilds.company_id == partner.company_id ,
    ).one_or_none()
    if not instance_fild : 
        return NotFoundRes(
            {
                "result" : "instance fild not found"
            }
        )
    instance_fild.status = StatusEnum.ACTIVE
    db.commit()
    return OkRes(
        {
            "result" : "Instance Fild unarchiver"
        }
    )

async def getFildById (
        db : Session , 
        partner : Partner , 
        id : str
) :
    fild = db.query(Filds).filter(
        Filds.company_id == partner.company_id , 
        Filds.status == StatusEnum.ACTIVE ,
        Filds.public_id == id
    ).one_or_none()
    if not fild : 
        return NotFoundRes(
            {
                "result" : "no data found"
            }
        )
    return OkRes(
        {
            "result" : FildOutPublic.model_validate(fild).model_dump()
        }
    )


async def createEntry(
        db : Session , 
        partner : Partner , 
        data : CreateEntryDto
) : 
    instance = db.query(Instances).filter(
        Instances.public_id == data.instance_id ,
        Instances.company_id == partner.company_id ,
        Instances.status == StatusEnum.ACTIVE
    ).one_or_none()
    entry = Entries(
        instance_id = instance.id ,
        company_id = partner.company_id ,
        creator_id = partner.id
    )
    if data.categorys :
        categorys = db.query(Category).filter(
            Category.public_id.in_(data.categorys)
        ).all()
        entry.categorys.extend(categorys)
    db.add(entry)
    if data.entry_type :
        entry.entry_type = data.entry_type
    if data.price and data.entry_type == "paid" :
        entry.price = data.price
        entry.acsess_id = generate_public_id()
    db.commit()
    return OkRes(
        {
            "result" : {
                "message" : "entry added" ,
                "entry_id" : entry.public_id
            }
        }
    )


async def getInstanceFilds (
        db : Session ,
        partner : Partner ,
        id : str
) :
    instance = db.query(Instances).filter(
        Instances.public_id == id ,
        Instances.company_id == partner.company_id , 
        Instances.status == StatusEnum.ACTIVE
    ).one_or_none()
    if not instance :
        return NotFoundRes(
            {
                "result" : "no finds found"
            }
        )
    instance_filds = db.query(InstanceFilds).filter(
        InstanceFilds.company_id == partner.company_id ,
        InstanceFilds.instance_id == instance.id , 
        InstanceFilds.status == StatusEnum.ACTIVE
    ).all()
    return {
        "result" : {
            "instance" : {
                "id" : id ,
                "name" : instance.name ,
                "caption" : instance.caption
                } ,
            "filds" : instance_filds
        }
    }




async def getEntrys (
        db : Session ,
        partner : Partner ,
        querySize : GetDataQuerySize
) :
    entrys = db.query(Entries).filter(
        Entries.company_id == partner.company_id ,
        Entries.creator_id == partner.id ,
        or_(Entries.status == StatusEnum.PENDDING , Entries.status == StatusEnum.ACTIVE)
    )
    return {
        "result" : entrys
        .offset(querySize.offset)
        .limit(querySize.size)
        .all() ,
        "total" : entrys.count()
    }

async def getEntryFilds (
        db : Session , 
        partner : Partner ,
        entry_id : str
) :
    entry = db.query(Entries).filter(
        Entries.company_id == partner.company_id ,
        Entries.creator_id == partner.id ,
        not_(Entries.status == StatusEnum.DISACTIVE) ,
        Entries.public_id == entry_id
    ).one_or_none()
    if not entry :
        return NotFoundRes(
            {
                "result" : "cant find data"
            }
        )
    
    return entry



# async def getInstanceId (
#         db : Session ,
#         partner : Partner ,
#         id : str
# ) :
#     instance = db.query(Instances).filter(
#         Instances.company_id == partner.company_id ,
#         Instances.status == StatusEnum.ACTIVE ,
#         Instances.public_id == id
#     ).one_or_none()
#     if not instance :
#         return NotFoundRes(
#             {
#                 "result" : "no instance found"
#             }
#         )
#     return OkRes(
#         {
#             "result" : SingleInstanceOut.model_validate(instance).model_dump()
#         }
#     )



async def createEntryData(
    db: Session,
    partner: Partner,
    data: CreateEnteryData
):
    # ---------------------------------
    # Get Entry
    # ---------------------------------

    entry = (
        db.query(Entries)
        .filter(
            Entries.public_id == data.entry_id,
            Entries.company_id == partner.company_id,
        )
        .one_or_none()
    )

    if not entry:
        return NotFoundRes({
            "result": "no entry found"
        })

    errors = []

    # ---------------------------------
    # Get all fields in one query
    # ---------------------------------

    field_ids = [item.fild_id for item in data.filds]

    fields = (
        db.query(Filds)
        .filter(
            Filds.public_id.in_(field_ids),
            Filds.company_id == partner.company_id,
        )
        .all()
    )

    fields_map = {
        field.public_id: field
        for field in fields
    }

    # ---------------------------------
    # Validate fields
    # ---------------------------------

    for item in data.filds:

        field = fields_map.get(item.fild_id)

        if not field:
            errors.append({
                "fild_id": item.fild_id,
                "result": "field invalid, not found"
            })
            continue

        value = item.data.value

        # -----------------------------
        # Validate value
        # -----------------------------

        is_valid, error = validate_entry_value(
            field.type_of,
            value
        )

        if not is_valid:
            errors.append({
                "fild_id": item.fild_id,
                "result": error
            })
            continue

        # -----------------------------
        # Create EntryData
        # -----------------------------

        entrydata = EntryData(
            company_id=partner.company_id,
            creator_id=partner.id,
            fild_id=field.id,
            entry_id=entry.id,
            placement=item.data.placement,
        )

        # -----------------------------
        # Set primitive values
        # -----------------------------

        if field.type_of == TypeOfEnum.STR:

            entrydata.value_str = value

        elif field.type_of == TypeOfEnum.INT:

            entrydata.value_int = value

        elif field.type_of == TypeOfEnum.BOOL:

            entrydata.value_bool = value

        # -----------------------------
        # FILE
        # -----------------------------

        elif field.type_of == TypeOfEnum.FILE:

            file = (
                db.query(FileManager)
                .filter(
                    FileManager.public_id == value,
                )
                .one_or_none()
            )

            if not file:
                errors.append({
                    "fild_id": item.fild_id,
                    "result": "file not found"
                })
                continue

            entrydata.file = file

        # -----------------------------
        # SELECT
        # -----------------------------

        elif field.type_of == TypeOfEnum.SELECT:

            option = (
                db.query(FildOptions)
                .filter(
                    FildOptions.public_id == value,
                    FildOptions.fild_id == field.id,
                    FildOptions.company_id == partner.company_id,
                    FildOptions.is_active.is_(True),
                )
                .one_or_none()
            )

            if not option:
                errors.append({
                    "fild_id": item.fild_id,
                    "result": "invalid option"
                })
                continue

            entrydata.selected_options.append(option)

        # -----------------------------
        # MULTISELECT
        # -----------------------------

        elif field.type_of == TypeOfEnum.MULTISELECT:

            options = (
                db.query(FildOptions)
                .filter(
                    FildOptions.public_id.in_(value),
                    FildOptions.fild_id == field.id,
                    FildOptions.company_id == partner.company_id,
                    FildOptions.is_active.is_(True),
                )
                .all()
            )

            if len(options) != len(set(value)):
                errors.append({
                    "fild_id": item.fild_id,
                    "result": "one or more options are invalid"
                })
                continue

            entrydata.selected_options.extend(options)

        else:

            errors.append({
                "fild_id": item.fild_id,
                "result": "type is not valid"
            })
            continue

        db.add(entrydata)

    # ---------------------------------
    # Rollback if validation failed
    # ---------------------------------

    if errors:
        db.rollback()

        return {
            "result": "validation error",
            "errors": errors
        }

    # ---------------------------------
    # Commit
    # ---------------------------------

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "result": "success"
    }

async def getEntryDataList(
    db: Session,
    querySize: GetDataQuerySize
):
    query = db.query(EntryData)

    total = query.with_entities(
        func.count(EntryData.id)
    ).scalar()

    items = (
        query
        .limit(querySize.size)
        .offset(querySize.offset)
        .all()
    )

    return {
        "result": items,
        "total": total,
    }