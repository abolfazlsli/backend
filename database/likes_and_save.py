from core.packages.database import *


class EntryLike(BasicTabales):
    __tablename__ = "entry_likes"

    user_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=False
    )

    entry_id = Column(
        Integer,
        ForeignKey("entries.id"),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "entry_id",
            name="uq_user_entry_like"
        ),
    )


SaveEntry = Table(
    "saves",
    Base.metadata,

    Column(
        "user_id",
        Integer,
        ForeignKey("partners.id"),
        nullable=False
    ),

    Column(
        "entry_id",
        Integer,
        ForeignKey("entries.id"),
        nullable=False
    ),

    UniqueConstraint(
        "user_id",
        "entry_id",
        name="uq_user_entry_save"
    ),
)