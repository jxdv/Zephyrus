from pathlib import Path

import plyvel

from .log import ZephyrusLogger

logger = ZephyrusLogger(__name__)


class LevelStorage:
    def __init__(self):
        project_path = Path(__file__).absolute().parent.parent
        db_path = project_path / "storage/"
        self.db = plyvel.DB(f"{db_path}", create_if_missing=True)

    def write_batch(self, targets):
        wb = self.db.write_batch()
        for target in targets:
            target_checksum = target.checksum()
            wb.put(str(target).encode(), target_checksum.encode())
        wb.write()
        logger.info("Baseline loaded.")

    def show_batch(self):
        for file, file_sum in self.db:
            print(file, file_sum)
