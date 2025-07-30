import aiosqlite
import os
from typing import Optional

class SQLiteMemory:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self._db: Optional[aiosqlite.Connection] = None

    async def initialize(self):
        """Initialize the database and create tables if they don't exist."""
        self._db = await aiosqlite.connect(self.db_path)
        await self._db.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await self._db.commit()

    async def add(self, content: str):
        """Add new content to memory."""
        if not self._db:
            raise RuntimeError("Memory not initialized. Call initialize() first.")
        await self._db.execute("INSERT INTO memory (content) VALUES (?)", (content,))
        await self._db.commit()

    async def get_latest(self) -> str:
        """Get the most recent memory entry."""
        if not self._db:
            raise RuntimeError("Memory not initialized. Call initialize() first.")
        async with self._db.execute("SELECT content FROM memory ORDER BY id DESC LIMIT 1") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""

    async def get_all(self) -> list[str]:
        """Get all memory entries."""
        if not self._db:
            raise RuntimeError("Memory not initialized. Call initialize() first.")
        async with self._db.execute("SELECT content FROM memory ORDER BY id ASC") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def clear(self):
        """Clear all memory entries."""
        if not self._db:
            raise RuntimeError("Memory not initialized. Call initialize() first.")
        await self._db.execute("DELETE FROM memory")
        await self._db.commit()

    async def close(self):
        """Close the database connection."""
        if self._db:
            await self._db.close()
            self._db = None 