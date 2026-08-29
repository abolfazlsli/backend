from core.packages.database import *
from database.filemanager import FileManager

class TypeOfEnum (str,Enum) :
    STR = "str"
    INT = "int"
    FILE = "file"
    BOOL = "bool"
    SELECT = "select"
    MULTISELECT = "multiselect"


class StatusEnum (str , Enum) :
    ACTIVE = "active"
    DISACTIVE = "disactive"

class Filds (ByCompanyAndCreator) :
    __tablename__ = "filds"

    name = Column(String , nullable=False)
    type_of = Column(
                ENUM(
                    TypeOfEnum,
                    name="type_of_enum",
                    values_callable=lambda enum: [e.value for e in enum],
                ),
                nullable=False,
            )
    
    status = Column(ENUM(StatusEnum) , default=StatusEnum.ACTIVE , nullable=False)
    company = relationship("Company" , back_populates="filds")
    partner = relationship("Partner")
    instances = relationship("Instances", secondary="instancefilds", back_populates="filds")
    options = relationship("FildOptions", back_populates="fild", order_by="FildOptions.order", cascade="all, delete-orphan")


class FildOptions(ByCompanyAndCreator):
    __tablename__ = "fild_options"

    fild_id = Column(Integer, ForeignKey("filds.id"), nullable=False)
    value = Column(String, nullable=False)
    label = Column(String, nullable=False)     
    order = Column(Integer, default=0)

    is_active = Column(Boolean , nullable=False , default=True)

    fild = relationship("Filds", back_populates="options")

    __table_args__ = (UniqueConstraint("fild_id", "value", name="uq_fild_option_value"),)


class InstanceFilds (ByCompanyAndCreator) :
    __tablename__ = "instancefilds"

    instance_id = Column(Integer , ForeignKey('instances.id') , nullable=False)
    fild_id = Column(Integer , ForeignKey('filds.id') , nullable=False)
    order = Column(Integer, default=0)
    required = Column(Boolean, default=False) 

    instance = relationship("Instances", back_populates="instance_filds")
    fild = relationship("Filds")

    __table_args__ = (UniqueConstraint("instance_id", "fild_id", name="uq_instance_fild"),)



class Instances (ByCompanyAndCreator) :
    __tablename__ = "instances"

    name = Column(String , nullable=False)
    caption = Column(String)
    # order = Column(Integer, default=0)
    # required = Column(Boolean, default=False)
    status = Column(ENUM(StatusEnum) , default=StatusEnum.ACTIVE , nullable=False)

    company = relationship("Company" , back_populates="instances")
    partner = relationship("Partner")
    filds = relationship("Filds", secondary="instancefilds", viewonly=True)
    instance_filds = relationship(
        "InstanceFilds",
        back_populates="instance",
        order_by="InstanceFilds.order",
        cascade="all, delete-orphan",
    )

class EntryDataOptions(ByCompanyAndCreator):
    __tablename__ = "entry_data_options"

    entry_data_id = Column(Integer, ForeignKey("entry_data.id"), nullable=False)
    fild_option_id = Column(Integer, ForeignKey("fild_options.id"), nullable=False)

    __table_args__ = (UniqueConstraint("entry_data_id", "fild_option_id", name="uq_entry_data_option"),)

class Entries(ByCompanyAndCreator):
    __tablename__ = "entries"
    instance_id = Column(Integer, ForeignKey("instances.id"), nullable=False) 

    instance = relationship("Instances")
    company = relationship("Company", back_populates="entries")
    creator = relationship("Partner")
    data = relationship("EntryData", back_populates="entry")


class EntryData(ByCompanyAndCreator):
    __tablename__ = "entry_data"
    entry_id = Column(Integer, ForeignKey("entries.id"), nullable=False)
    fild_id = Column(Integer, ForeignKey("filds.id"), nullable=False)

    value_str = Column(String, nullable=True)
    value_int = Column(Integer, nullable=True)
    value_bool = Column(Boolean, nullable=True)
    value_file_id = Column(Integer, ForeignKey("file_manager.id"), nullable=True)

    entry = relationship("Entries", back_populates="data")
    fild = relationship("Filds")
    file = relationship("FileManager")
    selected_options = relationship("FildOptions", secondary="entry_data_options")
    __table_args__ = (UniqueConstraint("entry_id", "fild_id", name="uq_entry_fild"),)

    @property
    def value(self):
        if self.fild.type_of == TypeOfEnum.FILE:
            return self.file.public_id if self.file else None
        if self.fild.type_of == TypeOfEnum.SELECT:
            opt = self.selected_options[0] if self.selected_options else None
            return opt.public_id if opt else None
        if self.fild.type_of == TypeOfEnum.MULTISELECT:
            return [o.public_id for o in self.selected_options]
        mapping = {
            TypeOfEnum.STR: self.value_str,
            TypeOfEnum.INT: self.value_int,
            TypeOfEnum.BOOL: self.value_bool,
        }
        return mapping.get(self.fild.type_of)