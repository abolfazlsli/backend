from core.packages.database import *
class FileManager(BasicTabales) :
    __tablename__ = "file_manager"
    file_name = Column(String , nullable=False)
    digital_name = Column(String , nullable=False)
    mimetype = Column(String , nullable=False)
    entry_data_id = Column(Integer , ForeignKey("entry_data.id") , nullable=True)

    entry_data = relationship("EntryData" , back_populates="file")