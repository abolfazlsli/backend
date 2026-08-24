from sqlalchemy import select, literal
from sqlalchemy.orm import Session
from database.admins import Partner

def update_if_not_none(target, data, fields):
    for field in fields:
        value = getattr(data, field, None)
        if value is not None:
            setattr(target, field, value)




def get_descendant_partner_ids(db: Session, root_partner_id: int) -> set[int]:
    """
    همه‌ی id های پارتنرهایی که مستقیم یا غیرمستقیم زیردست root_partner_id هستن رو برمی‌گردونه.
    یعنی کل زیردرخت، نه فقط فرزندهای بلافصل.
    """
    base = (
        select(Partner.id)
        .where(Partner.creator_id == root_partner_id)
        .cte(name="descendants", recursive=True)
    )

    partner_alias = Partner
    recursive = base.union_all(
        select(partner_alias.id).where(partner_alias.creator_id == base.c.id)
    )

    rows = db.execute(select(recursive.c.id)).all()
    return {row[0] for row in rows}


def is_descendant_of(db: Session, ancestor_id: int, target_partner_id: int) -> bool:
    """
    آیا target_partner_id در زنجیره‌ی زیردست‌های ancestor_id هست؟ (مستقیم یا غیرمستقیم)
    """
    return target_partner_id in get_descendant_partner_ids(db, ancestor_id)