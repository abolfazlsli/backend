from core.packages.database import *


class GroupCategory(BasicTabales):
    __tablename__ = "group_category"

    name = Column(String, nullable=False)
    caption = Column(String, nullable=True)
    color = Column(String , nullable=False)
    icon_id = Column(Integer , ForeignKey("file_manager.id") , nullable=True)
    # نوع گروه : grade (مقطع ← پایه‌ها) , subject (گروه درسی ← درس‌ها) , type (نوع محتوا)
    kind = Column(String , nullable=True , index=True)

    icon = relationship(
        "FileManager"
    )
    categories = relationship(
        "Category",
        back_populates="group",
        order_by="Category.id"
    )


class Category(BasicTabales):
    __tablename__ = "categories"

    name = Column(String, nullable=False)
    caption = Column(String, nullable=True)
    icon_id = Column(Integer , ForeignKey("file_manager.id") , nullable=True)
    color = Column(String, nullable=False)
    group_id = Column(
        Integer,
        ForeignKey("group_category.id"),
        nullable=True
    )

    icon = relationship(
        "FileManager"
    )
    group = relationship(
        "GroupCategory",
        back_populates="categories"
    )

    entries = relationship(
        "Entries",
        secondary="entry_category" ,
         back_populates="categorys"
    )


entry_category = Table(
    "entry_category" ,
    BasicTabales.metadata,
    Column(
        "category_id" ,
        Integer , ForeignKey("categories.id") ,primary_key=True) ,
    Column(
        "entry_id" ,
        Integer , ForeignKey("entries.id") ,primary_key=True)

)

partner_category_locked = Table(
    "partner_category_lockd",
    BasicTabales.metadata,

    Column(
        "partner_id",
        Integer,
        ForeignKey("partners.id"),
        primary_key=True
    ),

    Column(
        "category_id",
        Integer,
        ForeignKey("categories.id"),
        primary_key=True
    ),
)




tags_entry = Table(
    "tags_entry" ,
    BasicTabales.metadata ,
    Column("tag_id" ,Integer , ForeignKey("tags.id") , primary_key=True),
    Column("entry_id" , Integer , ForeignKey("entries.id") , primary_key=True)
)

class Tags(BasicTabales) :
    __tablename__ = "tags"
    name = Column(String , nullable=False)

    entries = relationship(
        "Entries",
        secondary=tags_entry,
        back_populates="tags"
    )

