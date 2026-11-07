from core.packages.services import *
from core.utils.dataprocess import validate_uploaded_file
from database.filemanager import *
import mimetypes



upload_dir = Path(settings.setting.upload_dir)
upload_dir.mkdir(exist_ok=True)

IMAGE_MIME_TYPES = {
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg+xml",
    ".bmp",
    ".tiff",
    ".x-icon",
    ".avif",
}



async def uploadFiles(
        db : Session ,
        file : UploadFile
) : 
    global upload_dir
    safefile = await validate_uploaded_file(file)
    file_path = upload_dir / safefile['safe_name']
    with open(file_path , "wb") as f:
        while cunk := await file.read(1024 * 1024) :
            f.write(cunk)
    filedb = FileManager(
        file_name = safefile['orginal_name'] ,
        digital_name = safefile['safe_name'] ,
        mimetype = safefile["memetype"]
    )
    db.add(filedb)
    db.commit()
    return {
        "id" : filedb.public_id , 
        "filename" : safefile['safe_name'] ,
        "orginal_name" : safefile['orginal_name'] ,
        "path" : str(file_path)
    }


async def getFile(
    db: Session,
    id: str
):
    file = (
        db.query(FileManager)
        .filter(FileManager.public_id == id)
        .one_or_none()
    )

    if not file:
        return NotFoundRes({
            "result": "no file found"
        })

    physical_file = Path(upload_dir) / file.digital_name

    if not physical_file.is_file():
        return NotFoundRes({
            "result": "physical file not found"
        })

    is_image = file.mimetype.lower() in IMAGE_MIME_TYPES

    media_type = mimetypes.guess_type(file.digital_name)[0] or "application/octet-stream"

    return FileResponse(
        path=physical_file,
        media_type=media_type,
        filename=None if is_image else file.file_name,
        content_disposition_type="inline" if is_image else "attachment",
    )