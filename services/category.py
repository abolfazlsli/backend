from core.packages.services import *
from schema.categorys import *
from database.category import *
from database.content import Entries


async def createCategory (
        db : Session ,
        admin : Admin , 
        data : AddCategory
) :
    category = Category(
            name = data.name , 
            caption = data.caption ,
        )
    db.add(category)
    db.flush()
    if data.group_id :
        gruop = db.query(GroupCategory).filter(GroupCategory.public_id == data.group_id).one_or_none()
        category.group_id = gruop.id
    db.commit()
    return OkRes(
        {
            "result" : "category added"
        }
    )



async def createCategoryGroup(
        db : Session , 
        admin : Admin ,
        data : AddCategoryGroup
) :
    gruop_category = GroupCategory(
        name = data.name , 
        caption = data.caption ,
    )
    db.add(gruop_category)
    db.flush()
    if data.categorys_id :
        categorys = db.query(Category).filter(
            Category.public_id.in_(data.categorys_id)
        ).all()
        gruop_category.categories.extend(categorys)
    if data.category :
        for i in data.category :
            category = Category(
                name = i.name ,
                caption = i.caption ,
            )
            gruop_category.categories.append(category)
    db.commit()
    return OkRes(
        {
            "result" : "gruop category added"
        }
    )


async def getCategorysEntries(
    db: Session,
    filters: GetCategorysContentBySize
):
    query = (
        db.query(Entries)
        .join(Entries.categorys)
        .filter(
            Category.public_id.in_(filters.category)
        )
        .distinct()
    )

    total = query.count()
    if total == 0 :
        return NotFoundRes(
            {
                "result" : "no data found"
            }
        )
    entries = (
        query
        .offset(filters.offset)
        .limit(filters.size)
        .all()
    )

    return {
        "result": entries,
        "total": total
    }






async def getCategories(
    db: Session,
    querySize: GetDataQuerySize
):
    query = (
        db.query(Category)
    )

    total = query.count()
    if total == 0 :
        return NotFoundRes(
            {
                "result" : "no data found"
            }
        )
    entries = (
        query
        .offset(querySize.offset)
        .limit(querySize.size)
        .all()
    )

    return {
        "result": entries,
        "total": total
    }