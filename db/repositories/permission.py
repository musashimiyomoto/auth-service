from db.models.permission import Permission
from db.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self):
        super().__init__(Permission)
