"""
MySQL Database Verification Script

Verifies all tables were created correctly and shows sample data
"""

import pymysql
from tabulate import tabulate

# MySQL connection settings
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root1"
DATABASE_NAME = "lung_cancer_db"

def verify_tables():
    """Verify all tables exist"""
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DATABASE_NAME
    )
    
    cursor = connection.cursor()
    
    print("📋 Checking tables...\n")
    
    # Get all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    expected_tables = ['patients', 'models', 'predictions', 'explainability_artifacts', 'audit_logs']
    actual_tables = [table[0] for table in tables]
    
    for table in expected_tables:
        status = "✅" if table in actual_tables else "❌"
        print(f"{status} {table}")
    
    print(f"\n📊 Total tables: {len(actual_tables)}")
    
    # Check models table
    print("\n" +  "="*60)
    print("🤖 MODELS TABLE")
    print("="*60)
    cursor.execute("SELECT * FROM models")
    models = cursor.fetchall()
    
    if models:
        cursor.execute("DESCRIBE models")
        columns = [col[0] for col in cursor.fetchall()]
        print(tabulate(models, headers=columns, tablefmt="grid"))
    else:
        print("⚠️  No models found")
    
    # Check audit logs
    print("\n" + "="*60)
    print("📝 AUDIT LOGS TABLE")
    print("="*60)
    cursor.execute("SELECT * FROM audit_logs")
    logs = cursor.fetchall()
    
    if logs:
        cursor.execute("DESCRIBE audit_logs")
        columns = [col[0] for col in cursor.fetchall()]
        print(tabulate(logs, headers=columns, tablefmt="grid"))
    else:
        print("⚠️  No audit logs found")
    
    # Show table structures
    print("\n" + "="*60)
    print("🏗️  TABLE STRUCTURES")
    print("="*60)
    
    for table in expected_tables:
        if table in actual_tables:
            print(f"\n📌 {table.upper()}")
            cursor.execute(f"DESCRIBE {table}")
            structure = cursor.fetchall()
            print(tabulate(structure, headers=['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'], tablefmt="simple"))
    
    cursor.close()
    connection.close()

if __name__ == "__main__":
    try:
        verify_tables()
        print("\n" + "="*60)
        print("✅ Verification complete!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
