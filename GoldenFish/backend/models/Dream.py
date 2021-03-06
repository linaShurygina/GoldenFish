from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.config import Base, session


class Dream(Base):
    __tablename__ = 'dream'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_link = Column(String, nullable=True)
    store_link = Column(String, nullable=True)
    is_fulfilled = Column(Boolean)
    giver_id = Column(Integer, nullable=True)

    def __init__(self, **kwargs):
        self.owner_id = kwargs.get('owner_id')
        self.name = kwargs.get('name')
        self.is_fulfilled = False
        self.giver_id = None
        self.description = kwargs.get('description')
        self.image_link = kwargs.get('image_link')
        self.store_link = kwargs.get('store_link')

    def get_id(self) -> int:
        return self.id

    def get_owner_id(self) -> int:
        return self.owner_id

    def set_name(self, _name):
        self.name = _name

    def set_description(self, _description):
        self.description = _description

    def set_giver(self, _giver_id):
        self.giver_id = _giver_id

    def set_fulfilled(self):
        self.is_fulfilled = True
