import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def keep_database_alive():
    """Prevents Supabase PostgreSQL from going idle by running a small query."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")  # Keep DB active
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Supabase kept alive successfully.")
    except Exception as e:
        print(f"❌ Failed to keep DB alive: {e}")

# Run the function
if __name__ == "__main__":
    keep_database_alive()
