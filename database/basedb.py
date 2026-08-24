from core.packages.database import *
class ContactInfoMixin:
    name = Column(String)
    username = Column(String, unique=True, nullable=False)
    status = Column(String , nullable=False , default="active")
    phone = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class UserInfoOrgin :
    bio = Column(String)
    email = Column(String)

    # profile_id = Column()


# class FileMixin:
#     @declared_attr
#     def file_id(cls):
#         return Column(Integer, ForeignKey("files.id"), nullable=True)

#     @declared_attr
#     def file(cls):
#         return relationship("File")