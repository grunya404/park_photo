### For a new basic set of CRUD operations you could just do

~~~python
from .base import CRUDBase
from app import models, schemas

item = CRUDBase[models.Item, schemas.Item, schemas.ItemCreate, schemas.ItemUpdate](models.Item)
~~~