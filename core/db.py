import os
import shutil
from pathlib import Path

import plyvel

from .log import ZephyrusLogger

logger = ZephyrusLogger(__name__)


class LevelStorage:
    def __init__(self):
        project_path = Path(__file__).absolute().parent.parent
        db_path = project_path / "storage"

        if os.path.exists(db_path):
            shutil.rmtree(db_path)

        self.db = plyvel.DB(f"{db_path}", create_if_missing=True)

    def write_batch(self, targets):
        wb = self.db.write_batch()
        for target in targets:
            target_checksum = target.checksum()
            wb.put(str(target).encode(), target_checksum.encode())
        wb.write()
        logger.info("Baseline loaded.")

    def verify_integrity(self, target_path, target_checksum):
        sn = self.db.snapshot()
        stored_checksum = sn.get(target_path.encode())

        return stored_checksum.decode() == target_checksum

    def close_db(self):
        if not self.db.closed:
            self.db.close()
            del self.db
