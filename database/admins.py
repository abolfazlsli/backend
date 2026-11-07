from core.packages.database import *
from .basedb import *
from database.likes_and_save import SaveEntry
from database.category import partner_category_locked



class Admin(BasicTabales , ContactInfoMixin) :
    __tablename__ = "admins"
    created_permissions = relationship("Premisions", back_populates="creator")
    created_companys = relationship("Company" , back_populates="creator")


class Premisions (BasicTabales) :
    __tablename__ = "premisions"
    name = Column(String , nullable=False)
    code = Column(String , nullable=False , index=True) # resource.action
    status = Column(String , nullable=False , default="active")
    creator_id = Column(Integer , ForeignKey("admins.id") , nullable=False)
    creator = relationship("Admin" , back_populates="created_permissions")
    roles = relationship("Role", secondary="promision_roles", back_populates="permissions")


class PremisionRole (BasicTabales) :
    __tablename__ = "promision_roles" 
    premision_id = Column(Integer , ForeignKey("premisions.id") , nullable=False) 
    role_id = Column(Integer , ForeignKey("roles.id") , nullable=False)

class Role (BasicTabales) :
    __tablename__ = "roles"
    name = Column(String , nullable=False)
    keyName = Column(String)
    caption = Column(String)
    partner_creator_id = Column(Integer, nullable=True)
    company_id = Column(Integer, ForeignKey("companys.id") , nullable=True)
    permissions = relationship("Premisions", secondary="promision_roles", back_populates="roles")
    comany = relationship("Company" , back_populates="roles")

class Partner (BasicTabales , ContactInfoMixin) :
    __tablename__ = "partners"
    creator_id = Column(Integer, ForeignKey("partners.id"), nullable=True)
    role_id = Column(Integer , ForeignKey("roles.id"))
    company_id = Column(Integer , ForeignKey("companys.id") , nullable=False)
    
    comany = relationship("Company" , back_populates="members")
    creator = relationship(
        "Partner",
        remote_side="Partner.id",
        back_populates="created_partners",
    )
    created_partners = relationship(
        "Partner",
        back_populates="creator",
    )
    role = relationship("Role")
    ban_logs = relationship(
        "PartnerBanLog",
        foreign_keys="PartnerBanLog.partner_id",
        back_populates="partner",
        order_by="PartnerBanLog.id.desc()",
    )

    saved_entries = relationship(
        "Entries",
        secondary=SaveEntry,
        back_populates="saved_by"
    )
    acsess_keys = relationship("PartnerAcsessKeys" , back_populates="partner")
    categorys = relationship("Category" , secondary=partner_category_locked)


class PartnerBanLog(BasicTabales):
    __tablename__ = "partner_ban_logs"

    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    reason = Column(String, nullable=False)
    extra_explain = Column(String , nullable=False)
    banned_by_admin_id = Column(Integer, ForeignKey("admins.id"), nullable=True)
    banned_by_partner_id = Column(Integer, ForeignKey("partners.id"), nullable=True)    
    partner = relationship(
        "Partner",
        foreign_keys=[partner_id],
        back_populates="ban_logs",
    )    
    banned_by_admin = relationship("Admin", foreign_keys=[banned_by_admin_id])
    banned_by_partner = relationship("Partner", foreign_keys=[banned_by_partner_id])




class Company(BasicTabales) :
    __tablename__ = "companys"
    name = Column(String , nullable=False)
    addres = Column(String , nullable=False)
    telphone = Column(String , nullable=False)
    creator_id = Column(Integer , ForeignKey("admins.id") , nullable=False)
    status = Column(String , nullable=False , default="active")

    members = relationship("Partner" , back_populates="comany")
    roles = relationship("Role" , back_populates="comany")
    creator = relationship("Admin" , back_populates="created_companys") 
    filds = relationship("Filds" , back_populates="company")
    instances = relationship("Instances" , back_populates="company")
    entries = relationship("Entries", back_populates="company") 


class RoleRequest(BasicTabales):
    __tablename__ = "role_requests"

    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    status = Column(String, nullable=False, default="pendding")
    message = Column(String, nullable=True)
    reviewed_by_id = Column(Integer, ForeignKey("partners.id"), nullable=True)

    partner = relationship("Partner", foreign_keys=[partner_id])
    role = relationship("Role")
    reviewed_by = relationship("Partner", foreign_keys=[reviewed_by_id])
