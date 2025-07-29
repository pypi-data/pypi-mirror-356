from ..common.error import DatabaseError
from ..common.logger import get_logger
from ..config.config_service import ConfigService
import sqlalchemy as db

from sqlalchemy.orm import sessionmaker
from pathlib import Path
from typing import List, Optional, Any
import logging
import pandas as pd

class DBService:
    _instance = None
    logger: logging.Logger = get_logger("DBService", level="DEBUG")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        config = ConfigService()
        db_config = config.get_db_config()

        # Use SQLAlchemy to create the engine directly
        self.engine = db.create_engine(
            db_config,
            connect_args={"connect_timeout": 30},  # Increased timeout
        )

        try:
            with self.engine.connect() as connection:
                self.logger.debug("Successfully connected to the database")
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}")
            raise DatabaseError(f"Error connecting to the database: {e}")

        # Create a session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.logger.debug("DB CREATED SUCCESSFULLY")

    def get_session(self):
        return self.session
    
    def query(self, query: str) -> pd.DataFrame:
        with self.engine.connect() as connection:
            result = connection.execute(db.text(query))
            return pd.DataFrame(result.fetchall())

    def get_by_field(self, table_name: str, field_name: str, field_value: Any, schema: str = "public") -> Optional[Any]:
        """
        Get a record from a table by matching a specific field value.
        
        Parameters:
        table_name (str): The name of the table to query
        field_name (str): The name of the field to match against
        field_value (Any): The value to match
        schema (str): The schema name where the table exists (default: "public")
        
        Returns:
        Optional[Any]: The first matching record or None if no match is found
        """
        try:
            metadata = db.MetaData(schema=schema)
            table = db.Table(table_name, metadata, autoload_with=self.engine)
            
            query = db.select(table).where(table.c[field_name] == field_value)
            
            with self.engine.connect() as connection:
                result = connection.execute(query).first()
                return result[0] if result else None
                
        except Exception as e:
            self.logger.error(f"Error querying {table_name} by {field_name}: {e}")
            raise DatabaseError(f"Error querying {table_name} by {field_name}: {e}")

    def insert(self, table_name, schema_name, df):
        """
        Insert new records into the specified table.

        Parameters:
        table_name (str): The name of the table to insert records into.
        schema_name (str): The schema name where the table exists.
        df (pd.DataFrame): The DataFrame containing the records to insert.
        """
        try:
            df.to_sql(
                name=table_name,
                con=self.engine,
                schema=schema_name,
                if_exists="append",
                index=False,
            )
            self.logger.debug(f"Successfully inserted records into {table_name} table")
        except Exception as e:
            self.logger.error(f"Error in insert operation: {e}")
            raise DatabaseError(f"Error in insert operation: {e}")

    def delete_and_insert(self, table_name, schema_name, df):
        """
        Deletes all records from the specified table if it exists, then inserts new records from the DataFrame.
        If the table does not exist, it is created and records are inserted.

        Parameters:
        table_name (str): The name of the table to replace records in.
        schema_name (str): The schema name where the table exists.
        df (pd.DataFrame): The DataFrame containing the new records.
        """
        try:
            metadata = db.MetaData(schema=schema_name)
            inspector = db.inspect(self.engine)

            # Verificar si la tabla existe
            table_exists = inspector.has_table(table_name, schema=schema_name)

            with self.session as session:
                with session.begin():
                    if table_exists:
                        table = db.Table(
                            table_name, metadata, autoload_with=self.engine
                        )
                        session.execute(table.delete())
                    df.to_sql(
                        name=table_name,
                        con=self.engine,
                        schema=schema_name,
                        if_exists="append",
                        index=False,
                    )
            self.logger.debug(f"Successfully replaced records in {table_name} table")
        except Exception as e:
            self.logger.error(f"Error in delete_and_insert operation: {e}")
            raise DatabaseError(f"Error in delete_and_insert operation: {e}")

    def upsert(self):
        pass

    def get_applied_migrations(self) -> List[str]:
        """Gets already applied migrations from database"""
        with self.engine.connect() as connection:
            connection.execute(
                db.text(
                    """
                CREATE TABLE IF NOT EXISTS migration_history (
                    id SERIAL PRIMARY KEY,
                    migration_name VARCHAR(255) UNIQUE,
                    applied_at TIMESTAMP DEFAULT NOW()
                )
            """
                )
            )
            result = connection.execute(
                db.text("SELECT migration_name FROM migration_history ORDER BY id")
            )
            return [row[0] for row in result]

    def table_exists(self, table_name: str, schema: str = "public") -> bool:
        """Checks if a table exists in the database"""
        inspector = db.inspect(self.engine)
        return inspector.has_table(table_name, schema=schema)

    def run_migrations(self, migrations_path: Path, force: bool = False) -> None:
        """
        Applies pending migrations from the specified directory

        Args:
            migrations_path: Path to directory containing .sql migration files
            force: If True, forces migration application even if tables exist
        """
        self.logger.info("Initiating migration process")

        try:
            # Get applied migrations
            applied = self.get_applied_migrations()
            self.logger.info(f"Already applied migrations: {len(applied)}")

            # Get available migration files
            migrations = []
            for file in sorted(migrations_path.glob("*.sql")):
                if file.name.startswith("00") and not file.name.startswith("old/"):
                    migrations.append(file.name)

            # Filter pending migrations
            pending = [m for m in migrations if m not in applied]
            self.logger.info(f"Pending migrations: {len(pending)}")

            # Apply pending migrations
            with self.engine.begin() as connection:
                for migration in pending:
                    self.logger.info(f"Applying migration: {migration}")
                    try:
                        with open(migrations_path / migration, "r") as f:
                            sql = f.read()
                            connection.execute(db.text(sql))

                        # Register migration as applied
                        connection.execute(
                            db.text(
                                "INSERT INTO migration_history (migration_name) VALUES (:migration)"
                            ),
                            {"migration": migration},
                        )
                        self.logger.info(f"✅ Migration applied: {migration}")
                    except Exception as e:
                        self.logger.error(
                            f"Error applying migration {migration}: {str(e)}"
                        )
                        if not force:
                            raise

            if not pending:
                self.logger.info("No pending migrations")

        except Exception as e:
            self.logger.error(f"Error applying migrations: {str(e)}")
            raise

        self.logger.info("Migration process completed")

    def close_session(self):
        if self.session:
            self.session.close()

    def delete_and_insert_between_dates(
        self, table_name, schema_name, date_column, start_date, end_date, df
    ):
        """
        Delete records between two dates and insert new records atomically.

        Parameters:
        - table_name (str): The name of the table.
        - schema_name (str): The schema name where the table exists.
        - date_column (str): The name of the date column to filter the records.
        - start_date (str): The start date (inclusive) in 'YYYY-MM-DD' format.
        - end_date (str): The end date (inclusive) in 'YYYY-MM-DD' format.
        - df (pd.DataFrame): The new data to insert after deletion.
        """
        try:
            metadata = db.MetaData(schema=schema_name)
            table = db.Table(table_name, metadata, autoload_with=self.engine)
            inspector = db.inspect(self.engine)

            # Verificar si la tabla existe
            table_exists = inspector.has_table(table_name, schema=schema_name)
            delete_query = table.delete().where(
                db.and_(
                    table.c[date_column] >= start_date, table.c[date_column] <= end_date
                )
            )

            with self.session as session:
                with session.begin():
                    if table_exists:
                        session.execute(delete_query)
                    df.to_sql(
                        name=table_name,
                        con=self.engine,
                        schema=schema_name,
                        if_exists="append",
                        index=False,
                    )

            self.logger.info(
                f"Successfully replaced records in {table_name} between {start_date} and {end_date}"
            )
        except Exception as e:
            self.logger.error(
                f"Error in delete_and_insert_between_dates operation: {e}"
            )
            raise           
