from typing import Callable, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.security.secure import decode_access_token, security_scheme
from core.packages.database import get_db
from database.admins import Admin, Partner

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="توکن نامعتبر یا منقضی شده است",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> Partner:
    token = credentials.credentials

    payload = decode_access_token(token)
    if payload is None:
        print("payload was none")
        raise credentials_exception

    partner_id = payload.get("sub")
    if partner_id is None:
        raise credentials_exception

    user = db.query(Partner).filter(Partner.public_id == str(partner_id) , Partner.status == "active").first()
    if user is None:
        raise credentials_exception

    return user


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    token = credentials.credentials

    payload = decode_access_token(token=token)
    if payload is None:
        raise credentials_exception

    public_id = payload.get("sub")
    if public_id is None:
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.public_id == public_id , Admin.status == "active").first()
    if admin is None:
        raise credentials_exception

    return admin


def get_current_admin_or_none(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> Admin | None:
    """
    برخلاف get_current_admin، اگه ادمین نبود Exception نمیده، فقط None برمی‌گردونه.
    """
    token = credentials.credentials

    payload = decode_access_token(token=token)
    if payload is None:
        return None

    public_id = payload.get("sub")
    if public_id is None:
        return None

    return db.query(Admin).filter(Admin.public_id == public_id , Admin.status == "active").first()






def get_user_permissions(user: Partner) -> set[str]:
    if not user.role:
        return set()
    return {perm.code for perm in user.role.permissions}


def require_permission(permission_code: str) -> Callable:
    def checker(
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
        db: Session = Depends(get_db),
    ) -> Union[Admin, Partner]:
        admin = get_current_admin_or_none(credentials=credentials, db=db)
        if admin is not None:
            return admin

        user = get_current_user(credentials=credentials, db=db)
        user_permissions = get_user_permissions(user)
        if permission_code not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="برای باز شدن این روت دسترسی بالاتری لازم است",
            )
        return user

    return checker


def require_any_permission(*permission_codes: str) -> Callable:
    def checker(
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
        db: Session = Depends(get_db),
    ) -> Union[Admin, Partner]:
        admin = get_current_admin_or_none(credentials=credentials, db=db)
        if admin is not None:
            return admin

        user = get_current_user(credentials=credentials, db=db)
        user_permissions = get_user_permissions(user)
        if not any(code in user_permissions for code in permission_codes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="دسترسی کافی ندارید",
            )
        return user

    return checker




def require_partner(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> Partner:
    """
    فقط پارتنرها اجازه‌ی دسترسی دارن. ادمین‌ها به هیچ عنوان از این دیپندنسی رد نمی‌شن،
    چون فقط توی جدول Partner جستجو می‌کنیم و اصلاً چک ادمین بودن انجام نمی‌شه.
    """
    token = credentials.credentials

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    partner_id = payload.get("sub")
    if partner_id is None:
        raise credentials_exception

    partner = db.query(Partner).filter(Partner.public_id == str(partner_id) , Partner.status == "active").first()
    if partner is None:
        raise credentials_exception

    return partner


def require_partner_permission(permission_code: str) -> Callable:
    def checker(
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
        db: Session = Depends(get_db),
    ) -> Partner:
        partner = require_partner(credentials=credentials, db=db)
        partner_permissions = get_user_permissions(partner)
        if permission_code not in partner_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="برای باز شدن این روت دسترسی بالاتری لازم است",
            )
        return partner

    return checker


def get_current_admin_or_partner(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> Union[Admin, Partner]:
    """
    هم ادمین هم پارتنر می‌تونن از این دیپندنسی رد بشن، فقط احراز هویت چک می‌شه
    و هیچ چک permission ای انجام نمی‌شه.
    """
    admin = get_current_admin_or_none(credentials=credentials, db=db)
    if admin is not None:
        return admin

    user = get_current_user(credentials=credentials, db=db)
    return user