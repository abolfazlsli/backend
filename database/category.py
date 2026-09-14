from core.packages.database import *



class Category (BasicTabales) :
    __tablename__ = "categorys"
    name = Column(String , nullable=False)
    caption = Column(String)

    entries = relationship("Entries" , secondary="entry_category")

class EntryCategory (BasicTabales) :
    __tablename__ = "entry_category"
    category_id = Column(Integer , ForeignKey("categorys.id") , nullable=False)
    entry_id = Column(Integer , ForeignKey("entries.id") , nullable=False)


class PartnerCategoryLocked(BasicTabales) :
    __tablename__ = "partner_category_lockd"

    partner_id = Column(Integer , ForeignKey("partners.id") , nullable=False)
    category_id = Column(Integer , ForeignKey("categorys.id") , nullable=False)

    __table_args__ = UniqueConstraint(
        "partner_id" ,
        "category_id" ,
        name="unique_parner_locked"
    )

