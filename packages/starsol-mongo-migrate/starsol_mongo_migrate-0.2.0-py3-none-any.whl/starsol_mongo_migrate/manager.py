import os
from pathlib import Path
from typing import TYPE_CHECKING

from .db import get_client, get_db_version, set_db_version
from .migration_path import (
    EmptyMigrationPathError,
    LoadMigrationError,
    MigrationPath,
    RevisionNotFoundError,
    RevisionOrderError,
)
from .template import generate_migration_template

if TYPE_CHECKING:
    from pymongo import MongoClient

__all__ = ('MigrationManager',)


class MigrationManager:
    """
    A Python interface for managing MongoDB migrations.

    This class provides programmatic access to all migration operations
    that are available through the CLI interface.
    """

    def __init__(self, mongo_uri: str, migrations_dir: str | Path = 'versions'):
        """
        Initialize the migration manager.

        Args:
            mongo_uri: MongoDB connection URI
            migrations_dir: Directory containing migration files (default: 'versions')
        """
        self.mongo_uri = mongo_uri
        self.migrations_dir = Path(migrations_dir)
        self._client: 'MongoClient | None' = None

    @property
    def client(self) -> 'MongoClient':
        """Get or create MongoDB client."""
        if self._client is None:
            self._client = get_client(self.mongo_uri)
        return self._client

    def close(self) -> None:
        """Close the MongoDB client connection."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> 'MigrationManager':
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        self.close()

    def init(self) -> None:
        """
        Initialize migration directory and database version collection.

        Creates the migrations directory if it doesn't exist and sets up
        the database version tracking collection.
        """
        set_db_version(self.client, None)
        os.makedirs(self.migrations_dir, exist_ok=True)

    def generate(self, name: str) -> str:
        """
        Generate a new migration file.

        Args:
            name: Name of the migration

        Returns:
            The revision ID of the generated migration

        Raises:
            LoadMigrationError: If existing migrations cannot be loaded
        """
        try:
            migrations = MigrationPath.load_from_dir(self.migrations_dir)
            down_revision = migrations.head.revision
        except EmptyMigrationPathError:
            down_revision = None
        except LoadMigrationError as e:
            raise LoadMigrationError(f'Error loading migrations: {e}') from e

        revision, migration_code = generate_migration_template(
            name, down_revision=down_revision
        )

        migration_file = self.migrations_dir / f'{revision}_{name}.py'
        with open(migration_file, 'w', encoding='utf-8') as f:
            f.write(migration_code)

        return revision  # type: ignore[no-any-return]

    def list_migrations(self) -> list[tuple[str, str]]:
        """
        List all migrations in reverse order (newest first).

        Returns:
            List of tuples containing (revision, name) for each migration

        Raises:
            EmptyMigrationPathError: If no migrations are found
            LoadMigrationError: If migrations cannot be loaded
        """
        migrations = MigrationPath.load_from_dir(self.migrations_dir)
        return [(mig.revision, mig.name) for mig in reversed(migrations)]

    def current_revision(self) -> str | None:
        """
        Get the current database revision.

        Returns:
            Current revision ID, or None if no migrations have been applied
        """
        return get_db_version(self.client)  # type: ignore[no-any-return]

    def upgrade(
        self, target_revision: str | None = None, use_transactions: bool = True
    ) -> None:
        """
        Upgrade database to the specified revision.

        Args:
            target_revision: Target revision to upgrade to. If None, upgrades to head.
            use_transactions: Whether to use transactions (requires replica set)

        Raises:
            EmptyMigrationPathError: If no migrations are found
            LoadMigrationError: If migrations cannot be loaded
            RevisionNotFoundError: If target revision doesn't exist
            RevisionOrderError: If target revision is not a valid upgrade target
        """
        try:
            migrations = MigrationPath.load_from_dir(self.migrations_dir)
        except EmptyMigrationPathError as e:
            raise EmptyMigrationPathError('No migrations found') from e
        except LoadMigrationError as e:
            raise LoadMigrationError(f'Error loading migrations: {e}') from e

        try:
            migrations.upgrade(
                self.client,
                target_revision or migrations.head.revision,
                use_session=use_transactions,
            )
        except (RevisionNotFoundError, RevisionOrderError) as e:
            raise e

    def downgrade(
        self, target_revision: str | None = None, use_transactions: bool = True
    ) -> None:
        """
        Downgrade database to the specified revision.

        Args:
            target_revision: Target revision to downgrade to. If None, downgrades to root.
            use_transactions: Whether to use transactions (requires replica set)

        Raises:
            EmptyMigrationPathError: If no migrations are found
            LoadMigrationError: If migrations cannot be loaded
            RevisionNotFoundError: If target revision doesn't exist
            RevisionOrderError: If target revision is not a valid downgrade target
        """
        try:
            migrations = MigrationPath.load_from_dir(self.migrations_dir)
        except EmptyMigrationPathError as e:
            raise EmptyMigrationPathError('No migrations found') from e
        except LoadMigrationError as e:
            raise LoadMigrationError(f'Error loading migrations: {e}') from e

        try:
            migrations.downgrade(
                self.client, target_revision, use_session=use_transactions
            )
        except (RevisionNotFoundError, RevisionOrderError) as e:
            raise e

    def get_migration_path(self) -> MigrationPath:
        """
        Get the loaded migration path object.

        Returns:
            MigrationPath instance with all loaded migrations

        Raises:
            EmptyMigrationPathError: If no migrations are found
            LoadMigrationError: If migrations cannot be loaded
        """
        return MigrationPath.load_from_dir(self.migrations_dir)
