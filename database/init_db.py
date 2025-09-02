#!/usr/bin/env python3
"""
Database initialization script for Landscaper Staff Application
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import get_database_url, DATABASE_CONFIG

def init_database():
    """Initialize the database with schema and seed data"""
    
    # Get database URL
    database_url = get_database_url()
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        print(f"Connecting to database: {DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"Connected to PostgreSQL: {version}")
        
        # Read and execute schema
        schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_file):
            print("Executing database schema...")
            with open(schema_file, 'r') as f:
                schema_sql = f.read()
            
            with engine.connect() as conn:
                # Split by semicolon and execute each statement
                statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
                for statement in statements:
                    if statement:
                        try:
                            conn.execute(text(statement))
                        except SQLAlchemyError as e:
                            # Skip errors for existing objects
                            if 'already exists' not in str(e).lower():
                                print(f"Warning: {e}")
                conn.commit()
            print("Schema executed successfully")
        else:
            print(f"Schema file not found: {schema_file}")
        
        # Read and execute seed data
        seed_file = os.path.join(os.path.dirname(__file__), 'seed_data.sql')
        if os.path.exists(seed_file):
            print("Loading seed data...")
            with open(seed_file, 'r') as f:
                seed_sql = f.read()
            
            with engine.connect() as conn:
                # Split by semicolon and execute each statement
                statements = [stmt.strip() for stmt in seed_sql.split(';') if stmt.strip()]
                for statement in statements:
                    if statement:
                        try:
                            conn.execute(text(statement))
                        except SQLAlchemyError as e:
                            # Skip errors for existing data
                            if 'duplicate key' not in str(e).lower() and 'already exists' not in str(e).lower():
                                print(f"Warning: {e}")
                conn.commit()
            print("Seed data loaded successfully")
        else:
            print(f"Seed file not found: {seed_file}")
        
        print("Database initialization completed successfully!")
        
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    init_database()
