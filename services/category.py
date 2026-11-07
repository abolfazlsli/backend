from core.packages.services import *
from schema.categorys import *
from database.category import *
from database.content import Entries , EntryData , FildOptions , StatusEnum , PricingEnum , TypeOfEnum
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
        if gruop :
            category.group_id = gruop.id
        else :
            errors.append("group not found")
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
        kind = data.kind ,
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


def public_entry_dump(entry : Entries , can_see_files : bool = False) -> dict :
    """
    خروجی عمومی entry ؛ فایل‌های محتوای غیر رایگان (به جز بنر) مخفی میشن
    """
    result = EntryOutWithOutInstance.model_validate(entry).model_dump(mode="json")
    if can_see_files or entry.entry_type == PricingEnum.FREE :
        return result
    for item in result["data"] :
        if item["fild"]["type_of"] == TypeOfEnum.FILE.value and item["placement"] != "banner" :
            item["value"] = None
    return result


def apply_entries_filters(query , filters : GetCategorysContentBySize) :
    # هر شناسه یک شرط جدا (AND) ؛ شناسه می‌تونه دسته‌بندی یا گروه باشه
    for category_id in filters.category or [] :
        query = query.filter(
            Entries.categorys.any(
                or_(
                    Category.public_id == category_id ,
                    Category.group.has(GroupCategory.public_id == category_id)
                )
            )
        )
    for term in filters.search or [] :
        term = term.strip()
        if not term :
            continue
        like = f"%{term}%"
        query = query.filter(
            or_(
                Entries.data.any(
                    or_(
                        EntryData.value_str.ilike(like) ,
                        EntryData.selected_options.any(FildOptions.label.ilike(like))
                    )
                ) ,
                Entries.categorys.any(
                    or_(
                        Category.name.ilike(like) ,
                        Category.group.has(GroupCategory.name.ilike(like))
                    )
                )
            )
        )
    if filters.entry_type :
        query = query.filter(Entries.entry_type == filters.entry_type)
    return query


async def getCategorysEntries(
    db: Session,
    filters: GetCategorysContentBySize
):
    query = db.query(Entries).filter(Entries.status == StatusEnum.ACTIVE)
    query = apply_entries_filters(query , filters)

    total = query.count()

    if filters.sort in ("best" , "most-viewed") :
        query = query.order_by(Entries.like_count.desc().nullslast() , Entries.id.desc())
    else :
        query = query.order_by(Entries.id.desc())

    entries = (
        query
        .offset(filters.offset)
        .limit(filters.size)
        .all()
    )

    return OkRes({
        "result": [public_entry_dump(entry) for entry in entries],
        "total": total
    })


async def getPublicEntryById(
    db : Session ,
    id : str
) :
    entry = db.query(Entries).filter(
        Entries.public_id == id ,
        Entries.status == StatusEnum.ACTIVE
    ).one_or_none()
    if not entry :
        return NotFoundRes(
            {
                "result" : "no data found"
            }
        )
    return OkRes(
        {
            "result" : public_entry_dump(entry)
        }
    )




async def getCategories(
    db: Session,
    querySize: GetDataQuerySize
):
    query = (
        db.query(Category)
    )

    total = query.count()
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
        querySize : GetGroupCategoriesQuery
) :
    group_categories = db.query(GroupCategory)
    if querySize.kind :
        group_categories = group_categories.filter(GroupCategory.kind == querySize.kind)
    total = group_categories.count()
    result = (group_categories
    .order_by(GroupCategory.id.asc())
    .offset(querySize.offset)
    .limit(querySize.size)
    .all())
    return {
        "result" : result , 
        "total" : total
    }


async def getCategoryCounts (
        db : Session ,
        filters : GetCategoryCountsQuery
) :
    """
    تعداد محتوای فعال هر دسته‌بندی (rows) و در صورت ارسال cols تعداد مشترک هر row با هر col
    خروجی : { row_id : { "total" : n , col_id : n } }
    """
    from sqlalchemy.orm import aliased

    row_cat = aliased(Category)
    row_link = aliased(entry_category)

    base = (
        db.query(row_cat.public_id , func.count(func.distinct(Entries.id)))
        .join(row_link , row_link.c.category_id == row_cat.id)
        .join(Entries , Entries.id == row_link.c.entry_id)
        .filter(row_cat.public_id.in_(filters.rows) , Entries.status == StatusEnum.ACTIVE)
        .group_by(row_cat.public_id)
    )
    result = {row : {"total" : 0} for row in filters.rows}
    for row_id , count in base.all() :
        result[row_id]["total"] = count

    if filters.cols :
        col_cat = aliased(Category)
        col_link = aliased(entry_category)
        pairs = (
            db.query(row_cat.public_id , col_cat.public_id , func.count(func.distinct(Entries.id)))
            .join(row_link , row_link.c.category_id == row_cat.id)
            .join(Entries , Entries.id == row_link.c.entry_id)
            .join(col_link , col_link.c.entry_id == Entries.id)
            .join(col_cat , col_cat.id == col_link.c.category_id)
            .filter(
                row_cat.public_id.in_(filters.rows) ,
                col_cat.public_id.in_(filters.cols) ,
                Entries.status == StatusEnum.ACTIVE
            )
            .group_by(row_cat.public_id , col_cat.public_id)
        )
        for row_id in result :
            for col_id in filters.cols :
                result[row_id][col_id] = 0
        for row_id , col_id , count in pairs.all() :
            result[row_id][col_id] = count

    return OkRes({"result" : result})


async def getStats (
        db : Session
) :
    from database.admins import Partner , Role , Company
    company = db.query(Company).filter(Company.name == "users_zone").one_or_none()

    def count_role(key : str) :
        if not company :
            return 0
        return db.query(Partner).filter(
            Partner.company_id == company.id ,
            Partner.status == "active" ,
            Partner.role.has(Role.keyName == key)
        ).count()

    return OkRes(
        {
            "result" : {
                "contents" : db.query(Entries).filter(Entries.status == StatusEnum.ACTIVE).count() ,
                "teachers" : count_role("managers") ,
                "students" : count_role("students") ,
                "categories" : db.query(Category).count()
            }
        }
    )
