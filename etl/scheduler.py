from apscheduler.schedulers.background import BackgroundScheduler
import time
from store_db import store_data_in_postgres
from keep_db_alive import keep_database_alive

def start_scheduler():
    """Starts the APScheduler to run tasks every 30 minutes."""
    scheduler = BackgroundScheduler()

    # Fetch AQI & store in PostgreSQL every 30 minutes
    scheduler.add_job(store_data_in_postgres, "interval", minutes=1)

    # Keep Supabase active every 30 minutes
    scheduler.add_job(keep_database_alive, "interval", minutes=1)

    scheduler.start()
    print("✅ Scheduler started! Fetching data & keeping Supabase alive every 30 minutes.")

    try:
        while True:
            time.sleep(6)  # Keep the script running
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")

# Run scheduler
if __name__ == "__main__":
    start_scheduler()
