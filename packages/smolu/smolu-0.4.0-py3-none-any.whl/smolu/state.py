from sqlite3 import connect
import os
from .config import Config


class State:
    def __init__(self, config: Config):
        self.config = config

    def __enter__(self) -> "State":
        need_init = not os.path.exists(self.config.state_db)
        self.co = connect(self.config.state_db)

        if need_init:
            self.co.execute(
                "CREATE TABLE state (id TEXT PRIMARY KEY, target TEXT)"
            )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.co.commit()
        self.co.close()

    def record(self, id: str, target: str):
        if not self.co:
            raise RuntimeError("State not initialized")
        self.co.execute(
            "INSERT INTO state VALUES (?, ?)",
            (id, target),
        )

    def list(self) -> list[tuple[str, str]]:
        return list(self.co.execute("SELECT * FROM state").fetchall())

    def find(self, search: str) -> str | None:
        (id,) = self.co.execute("SELECT id FROM state WHERE id = ?", (search,)).fetchone()
        if not id:
            (id,) = self.co.execute(
                "SELECT id FROM state WHERE target = ?", (search,)
            ).fetchone()

        return id

    def remove(self, id: str):
        self.co.execute("DELETE FROM state WHERE id = ?", (id,))
