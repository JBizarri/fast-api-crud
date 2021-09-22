from ..database import engine
from . import company, user

company.models.Base.metadata.create_all(engine)
user.models.Base.metadata.create_all(engine)
