from core.packages.services import *
from schema.categorys import *
from database.category import *
from database.content import Entries
from database.filemanager import FileManager

async def createCategory (
        db : Session ,
        admin : Admin , 
        data : AddCategory
) :
    errors = []
    category = Category(
            name = data.name , 
            caption = data.caption ,
            color = data.color
        )
    if data.icon_id :
        icon_file = db.query(FileManager).filter(
            FileManager.public_id == data.icon_id
        ).one_or_none()
        if not icon_file :
            errors.append("file not found")
        else :
            category.icon_id = icon_file.id
    db.add(category)
    db.flush()
    if data.group_id :
        gruop = db.query(GroupCategory).filter(GroupCategory.public_id == data.group_id).one_or_none()
        category.group_id = gruop.id
    db.commit()
    return OkRes(
        {
            "result" : "category added" , 
            "warrnings" : errors
        }
    )



async def createCategoryGroup(
        db : Session , 
        admin : Admin ,
        data : AddCategoryGroup
) :
    errors = []
    gruop_category = GroupCategory(
        name = data.name , 
        caption = data.caption ,
        color = data.color ,
    )
    db.add(gruop_category)
    db.flush()
    if data.icon_id :
        icon_file = db.query(FileManager).filter(
                    FileManager.public_id == data.icon_id
                ).one_or_none()
        if not icon_file :
            errors.append("file not found")
        else :
            gruop_category.icon_id = icon_file.id
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
                color = i.color
            )
            if i.icon_id :
                icon_file_c = db.query(FileManager).filter(
                        FileManager.public_id == i.icon_id
                    ).one_or_none()
                if not icon_file_c :
                    errors.append(f"file not found, File id : {i.icon_id}")
                else :
                    category.icon_id = icon_file_c.id
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
        .distinct()
    )

    total = query.count()
    if total == 0 :
        return NotFoundRes(
            {
                "result" : "no data found"
            }
        )
    if filters.category :
        query.filter(
            Category.public_id.in_(filters.category)
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


async def getGroupCategories (
        db : Session , 
        querySize : GetDataQuerySize
) :
    group_categories = db.query(GroupCategory)
    total = group_categories.count()
    result = (group_categories
    .offset(querySize.offset)
    .limit(querySize.size)
    .all())
    return {
        "result" : result , 
        "total" : total
    }