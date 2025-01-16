# **Shorten URL Service**

## **Overview**
Shorten URL is a FastAPI-based application for creating, managing, and monitoring shortened URLs. It includes functionalities such as tracking accesses, automated cleanup of inactive URLs, and generating charts for data visualization.

## **Features**
- **Shorten URLs**: Create short, user-friendly URLs for long links.
- **Redirect**: Automatically redirect users from short URLs to the original ones.
- **Access Tracking**: Log every access for each shortened URL.
- **Dashboard APIs**:
  - Top 3 most accessed URLs.
  - Time since the last access for each URL.
  - Daily registration and access statistics.
- **Automated Cleanup**: Remove URLs that haven’t been accessed in the last 7 days (runs every 1 minute).
- **Chart Generation**:
  - Daily registrations.
  - Total daily accesses.
  - Per-link daily accesses.
- **PostgreSQL Integration**: Efficient database design with views, stored procedures, and triggers.

## **Technologies Used**
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Task Scheduler**: [APScheduler](https://apscheduler.readthedocs.io/)
- **Visualization**: [Matplotlib](https://matplotlib.org/)
- **Deployment**: Docker (Not yet!)

---

## **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/SobhanMoghimi/shorten-url.git
cd shorten-url
```
### **2. Install Dependencies**
It’s recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Setup the Database**
- Create a PostgreSQL database named `url_shortener`:
```sql
CREATE DATABASE url_shortener;
```
- Run the SQL scripts to create tables, views, and stored procedures:
  - db-changes/01-Initial-db.sql

---

## **Running the Application**

### **2. Access API Documentation**
- Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the Swagger UI.

---

## **Project Structure**
```plaintext
shorten-url/
├── app/
│   ├── dal/                # Data Access Layer
│   ├── controller/         # API Routes
│   ├── models/             # Pydantic Models
│   ├── scheduler.py        # Background Jobs with APScheduler
│   ├── utils/              # Utility Functions
│   ├── main.py             # FastAPI Application Entry Point
├── charts/                 # Generated Charts
├── db-changes/             # SQL Scripts for Database Initialization
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```
---

## **APIs**

### **URL Operations**
| Method | Endpoint              | Description                         |
|--------|-----------------------|-------------------------------------|
| POST   | `/shorten`            | Create a short URL                 |
| GET    | `/{short_url}`        | Redirect to the original URL       |

### **Dashboard**
| Method | Endpoint                             | Description                                     |
|--------|-------------------------------------|------------------------------------------------|
| GET    | `/dashboard/top_3_accessed_urls`    | Retrieve the top 3 most accessed URLs          |
| GET    | `/dashboard/urls_time_since_last_access` | Get time since the last access for each URL   |
| GET    | `/dashboard/registered_urls_each_day` | Get daily registration statistics             |
| GET    | `/dashboard/accesses_per_day_per_url` | Get daily access statistics per URL           |
| POST   | `/dashboard/generate_charts`        | Generate and save charts for analytics         |
| GET    | `/dashboard/charts/{chart_name}`    | Retrieve a specific chart                      |

---

## **Automated Cleanup**
The application includes a scheduled job that:
- Runs every 1 minutes.
- Deletes URLs that haven’t been accessed for the last 7 days.
- Implemented using APScheduler and PostgreSQL stored procedures.

---

## **Visualization**
Generated charts are stored in the `charts` folder:
- **`daily_registrations.jpeg`**: Daily registrations.
- **`total_daily_accesses.jpeg`**: Total accesses across all URLs.
- **`access_per_day_{shortened_url}.jpeg`**: Daily accesses for each URL.

---

## **Development and Contribution**
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request for review.

---
