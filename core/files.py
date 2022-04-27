from core.base import CrudFactory
from models.files import File

FilesCore = CrudFactory(File.__table__)
