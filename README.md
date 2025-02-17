# **Vietnam Air Quality Data Pipeline**

## **Overview**

This project implements an **automated ETL pipeline** to **collect, process, and store real-time air quality data** for **Hanoi, Da Nang, and Ho Chi Minh City**. The data is retrieved from the **World Air Quality Index API**, processed, and stored in a **cloud-hosted PostgreSQL database (Supabase)**. Additionally, a **local data lake** stores raw JSON responses for backup and future processing.

A **Power BI dashboard** visualizes air pollution trends and key metrics, enabling data-driven insights.

---

## **Features**

✅ **Automated ETL Pipeline:** Batches and processes air quality data every **30 minutes**  
✅ **Multi-City Coverage:** Fetches air quality data for **Hanoi, Da Nang, Ho Chi Minh City**  
✅ **Local Data Lake:** Stores raw JSON responses for backup and reprocessing  
✅ **Cloud PostgreSQL Database:** Structured data storage using **Supabase**  
✅ **Data Cleaning & Processing:** Handles missing values and ensures valid numerical data  
✅ **Interactive Dashboard:** **Power BI** visualization of trends and pollutant levels (PM2.5, PM10, CO, NO₂, O₃, SO₂)  
✅ **Scalable & Modular Codebase:** Built with **Python, APScheduler, PostgreSQL, Power BI**  

---

## **Tech Stack**

- **Python** (ETL Processing)
- **APScheduler** (Automated Task Scheduling)
- **PostgreSQL (Supabase)** (Cloud-hosted Data Warehouse)
- **Power BI** (Data Visualization)
- **JSON & Pandas** (Data Handling)
- **Requests** (API Calls)

---

## **Installation & Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-repo/vietnam-air-quality.git
cd vietnam-air-quality
```

### **2. Create a Virtual Environment & Install Dependencies**

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### **3. Configure Environment Variables**

Create a `.env` file in the root directory and add the following environment variables:

```bash
API_TOKEN=your_api_key_here
DB_HOST=your_supabase_host
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=5432
```

### **4. Run the ETL Pipeline**

```bash
python etl/scheduler.py
```

## **Project Structure**

```bash
📂 vietnam-air-quality
├── 📁 data_lake           # Local storage for raw API responses
│   ├── raw_data/          # JSON files from API
├── 📁 etl                 # ETL processing scripts
│   ├── fetch_aqi.py       # Fetches AQI data from the API
│   ├── store_db.py        # Processes & stores data in PostgreSQL
│   ├── scheduler.py       # Runs ETL tasks on a schedule
│   ├── keep_db_alive.py   # Keeps Supabase database active
├── .env                   # Environment variables (DO NOT SHARE)
├── requirements.txt       # Dependencies
├── README.md              # Documentation
```

## **Power BI Dashboard**

After connecting Power BI to the Supabase PostgreSQL database, you can create an interactive dashboard to visualize:

Real-time AQI values across different cities
Trends over time (e.g., daily PM2.5 levels)
Comparisons of pollutants (CO, NO₂, O₃, SO₂, etc.)
Geospatial visualizations using latitude/longitude data

## **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## **Contributors**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
🚀 Happy coding!
