from pathlib import Path

import plyvel

from .log import ZephyrusLogger

logger = ZephyrusLogger(__name__)


class LevelStorage:
    def __init__(self):
        project_path = Path(__file__).absolute().parent.parent
        db_path = project_path / "storage/"
        self.db = plyvel.DB(f"{db_path}", create_if_missing=True)
