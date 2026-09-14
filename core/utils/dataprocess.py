from sqlalchemy import select, literal
from sqlalchemy.orm import Session
from database.admins import Partner
from fastapi import UploadFile, HTTPException
from pathlib import Path
import secrets
from enum import Enum
from typing import Any


class TypeOfEnum (str,Enum) :
    STR = "str"
    INT = "int"
    FILE = "file"
    BOOL = "bool"
    SELECT = "select"
    MULTISELECT = "multiselect"

ALLOWED_FILES = {
    # Images
    ".jpg": {
        "mime": "image/jpeg",
        "magic": [b"\xff\xd8\xff"]
    },
    ".jpeg": {
        "mime": "image/jpeg",
        "magic": [b"\xff\xd8\xff"]
    },
    ".png": {
        "mime": "image/png",
        "magic": [b"\x89PNG\r\n\x1a\n"]
    },

    # PDF
    ".pdf": {
        "mime": "application/pdf",
        "magic": [b"%PDF"]
    },

    # Word
    ".doc": {
        "mime": "application/msword",
        "magic": [b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"]
    },
    ".docx": {
        "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "magic": [b"PK\x03\x04"]
    },

    # Excel
    ".xls": {
        "mime": "application/vnd.ms-excel",
        "magic": [b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"]
    },
    ".xlsx": {
        "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "magic": [b"PK\x03\x04"]
    },

    # PowerPoint
    ".ppt": {
        "mime": "application/vnd.ms-powerpoint",
        "magic": [b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"]
    },
    ".pptx": {
        "mime": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "magic": [b"PK\x03\x04"]
    },

    # =========================
    # Video
    # =========================

    # ".mp4": {
    #     "mime": "video/mp4",
    #     "magic": [b"ftyp"]
    # },
    # ".mov": {
    #     "mime": "video/quicktime",
    #     "magic": [b"ftyp"]
    # },
    # ".webm": {
    #     "mime": "video/webm",
    #     "magic": [b"\x1a\x45\xdf\xa3"]
    # },
    # ".mkv": {
    #     "mime": "video/x-matroska",
    #     "magic": [b"\x1a\x45\xdf\xa3"]
    # },
    # ".avi": {
    #     "mime": "video/x-msvideo",
    #     "magic": [b"RIFF"]
    # },

    # =========================
    # Audio
    # =========================

    ".mp3": {
        "mime": "audio/mpeg",
        "magic": [
            b"ID3",
            b"\xff\xfb",
            b"\xff\xf3",
            b"\xff\xf2"
        ]
    },
    ".wav": {
        "mime": "audio/wav",
        "magic": [b"RIFF"]
    },
    ".ogg": {
        "mime": "audio/ogg",
        "magic": [b"OggS"]
    },
    ".oga": {
        "mime": "audio/ogg",
        "magic": [b"OggS"]
    },
    ".flac": {
        "mime": "audio/flac",
        "magic": [b"fLaC"]
    },
    ".m4a": {
        "mime": "audio/mp4",
        "magic": [b"ftyp"]
    },
}

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



MAX_FILE_SIZES = {
    "image": 10 * 1024 * 1024,       # 10 MB
    "pdf": 20 * 1024 * 1024,         # 20 MB
    "document": 20 * 1024 * 1024,    # 20 MB
    "audio": 50 * 1024 * 1024,       # 50 MB
    "video": 500 * 1024 * 1024,      # 500 MB
}


FILE_CATEGORIES = {
    # Images
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".webp": "image",
    ".gif": "image",
    ".svg": "image",
    ".bmp": "image",
    ".avif": "image",

    # PDF
    ".pdf": "pdf",

    # Documents
    ".doc": "document",
    ".docx": "document",
    ".xls": "document",
    ".xlsx": "document",
    ".ppt": "document",
    ".pptx": "document",

    # Audio
    ".mp3": "audio",
    ".wav": "audio",
    ".ogg": "audio",
    ".oga": "audio",
    ".flac": "audio",
    ".m4a": "audio",

    # Video
    # ".mp4": "video",
    # ".mov": "video",
    # ".webm": "video",
    # ".mkv": "video",
    # ".avi": "video",
}

async def validate_uploaded_file(file: UploadFile) -> str:
    """
    فایل آپلود شده را از نظر اولیه امنیتی بررسی می‌کند.
    در صورت معتبر بودن، یک filename امن برمی‌گرداند.
    """

    # -------------------------
    # 1. بررسی filename
    # -------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    original_name = Path(file.filename).name

    if original_name != file.filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )

    # -------------------------
    # 2. بررسی extension
    # -------------------------

    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_FILES:
        raise HTTPException(
            status_code=400,
            detail="File type is not allowed"
        )

    config = ALLOWED_FILES[extension]

    # -------------------------
    # 3. بررسی MIME type
    # -------------------------

    if file.content_type != config["mime"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid MIME type"
        )

    # -------------------------
    # 4. خواندن محتوا
    # -------------------------

    content = await file.read()

    # فایل را برای استفاده بعدی reset می‌کنیم
    await file.seek(0)

    # -------------------------
    # 5. بررسی حجم
    # -------------------------

    category = FILE_CATEGORIES[extension]

    max_size = MAX_FILE_SIZES[category]

    if len(content) > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. Maximum size for {category} files is {max_size // (1024 * 1024)} MB"
        )

    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty file"
        )

    # -------------------------
    # 6. بررسی Magic Bytes
    # -------------------------

    # if not any(
    #     content.startswith(signature)
    #     for signature in config["magic"]
    # ):
    #     raise HTTPException(
    #         status_code=400,
    #         detail="File content does not match its extension"
    #     )

    # -------------------------
    # 7. ساخت نام امن
    # -------------------------

    safe_filename = (
        f"{secrets.token_hex(16)}{extension}"
    )

    return {
        "safe_name" : safe_filename ,
        "orginal_name" : file.filename , 
        "file" : file ,
        "memetype" : extension
        } 







def validate_entry_value(
    type_of: TypeOfEnum,
    value: Any,
) -> tuple[bool, str | None]:

    if type_of == TypeOfEnum.STR:
        if not isinstance(value, str):
            return False, "value must be a string"

    elif type_of == TypeOfEnum.INT:
        # bool در Python زیرمجموعه int محسوب می‌شود
        if isinstance(value, bool) or not isinstance(value, int):
            return False, "value must be an integer"

    elif type_of == TypeOfEnum.BOOL:
        if not isinstance(value, bool):
            return False, "value must be a boolean"

    elif type_of == TypeOfEnum.FILE:
        if not isinstance(value, str):
            return False, "file value must be a string"

    elif type_of == TypeOfEnum.SELECT:
        if not isinstance(value, str):
            return False, "select value must be a string"

    elif type_of == TypeOfEnum.MULTISELECT:
        if not isinstance(value, list):
            return False, "multiselect value must be a list"

        if not all(isinstance(item, str) for item in value):
            return False, "multiselect values must be a list of strings"

    else:
        return False, "unsupported field type"

    return True, None