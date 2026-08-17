import sqlite3
from contextlib import contextmanager
from typing import Any


class StateManagementDatabase:

    def __init__(
        self,
        database_path: str = "cloud_state.db",
    ):

        self.database_path = database_path

        self._initialize()

    @contextmanager
    def connection(self):

        connection = sqlite3.connect(
            self.database_path
        )

        try:
            yield connection
            connection.commit()

        finally:
            connection.close()

    def _initialize(self):

        with self.connection() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS
                resource_state (
                    resource_id TEXT PRIMARY KEY,
                    resource_type TEXT NOT NULL,
                    tenant_id TEXT,
                    state TEXT NOT NULL,
                    metadata TEXT
                )
                """
            )

    def save_resource(
        self,
        resource_id: str,
        resource_type: str,
        tenant_id: str | None,
        state: str,
        metadata: str = "{}",
    ) -> None:

        with self.connection() as connection:

            connection.execute(
                """
                INSERT INTO resource_state (
                    resource_id,
                    resource_type,
                    tenant_id,
                    state,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?)

                ON CONFLICT(resource_id)
                DO UPDATE SET
                    resource_type =
                        excluded.resource_type,
                    tenant_id =
                        excluded.tenant_id,
                    state =
                        excluded.state,
                    metadata =
                        excluded.metadata
                """,
                (
                    resource_id,
                    resource_type,
                    tenant_id,
                    state,
                    metadata,
                ),
            )

    def get_resource(
        self,
        resource_id: str,
    ) -> dict[str, Any] | None:

        with self.connection() as connection:

            row = connection.execute(
                """
                SELECT
                    resource_id,
                    resource_type,
                    tenant_id,
                    state,
                    metadata
                FROM resource_state
                WHERE resource_id = ?
                """,
                (resource_id,),
            ).fetchone()

        if row is None:
            return None

        return {
            "resource_id": row[0],
            "resource_type": row[1],
            "tenant_id": row[2],
            "state": row[3],
            "metadata": row[4],
        }

    def list_tenant_resources(
        self,
        tenant_id: str,
    ) -> list[dict[str, Any]]:

        with self.connection() as connection:

            rows = connection.execute(
                """
                SELECT
                    resource_id,
                    resource_type,
                    tenant_id,
                    state,
                    metadata
                FROM resource_state
                WHERE tenant_id = ?
                """,
                (tenant_id,),
            ).fetchall()

        return [
            {
                "resource_id": row[0],
                "resource_type": row[1],
                "tenant_id": row[2],
                "state": row[3],
                "metadata": row[4],
            }
            for row in rows
        ]