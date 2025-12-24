"""
MySQL Database Setup Script

Creates the database and verifies connection before running init_db.py
"""

import pymysql
import sys

# MySQL connection settings
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root1"
DATABASE_NAME = "lung_cancer_db"

def create_database():
    """Create database if it doesn't exist"""
    try:
        # Connect to MySQL server (without database)
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create database with UTF8 charset
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Database '{DATABASE_NAME}' created/verified successfully")
        
        # Show all databases
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print(f"\n📊 Available databases:")
        for db in databases:
            marker = "👉" if db[0] == DATABASE_NAME else "  "
            print(f"{marker} {db[0]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Verify credentials (root/root1)")
        print("3. Check if MySQL is accessible on localhost")
        return False

def verify_connection():
    """Verify we can connect to the database"""
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DATABASE_NAME
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"\n✅ Connected to MySQL {version[0]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MySQL Database Setup for Lung Cancer Detection System\n")
    
    # Step 1: Create database
    if not create_database():
        print("\n❌ Failed to create database. Exiting.")
        sys.exit(1)
    
    # Step 2: Verify connection
    if not verify_connection():
        print("\n❌ Failed to verify connection. Exiting.")
        sys.exit(1)
    
    print("\n✅ Database setup complete!")
    print("\n📝 Next steps:")
    print("   1. Install PyMySQL: pip install pymysql")
    print("   2. Run: python -m app.db.init_db")
