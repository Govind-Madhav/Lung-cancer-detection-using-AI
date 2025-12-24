"""Quick MySQL verification using Python"""
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root1",
    database="lung_cancer_db"
)

cursor = connection.cursor()

print("=" * 60)
print("MySQL VERIFICATION - lung_cancer_db")
print("=" * 60)

# Show tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print(f"\n✅ Tables ({len(tables)} total):")
for table in tables:
    print(f"   • {table[0]}")

# Count models
cursor.execute("SELECT COUNT(*) FROM models")
model_count = cursor.fetchone()[0]
print(f"\n✅ Models seeded: {model_count}")

# Show models
cursor.execute("SELECT model_name, model_version, model_type FROM models")
models = cursor.fetchall()
for model in models:
    print(f"   • {model[0]} {model[1]} ({model[2]})")

# Count audit logs
cursor.execute("SELECT COUNT(*) FROM audit_logs")
audit_count = cursor.fetchone()[0]
print(f"\n✅ Audit logs: {audit_count}")

# Show recent audit logs
cursor.execute("SELECT event_type, message FROM audit_logs ORDER BY created_at DESC LIMIT 5")
logs = cursor.fetchall()
for log in logs:
    print(f"   • {log[0]}: {log[1]}")

# Check indexes
print(f"\n✅ Indexes created:")
cursor.execute("SHOW INDEX FROM predictions")
indexes = cursor.fetchall()
for idx in indexes:
    if idx[2] not in ['PRIMARY']:  # Skip primary key
        print(f"   • {idx[2]} on {idx[4]}")

cursor.close()
connection.close()

print("\n" + "=" * 60)
print("✅ Database verification complete!")
print("=" * 60)
