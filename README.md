# EduSense — AI-Powered Student Early Warning System

An intelligent platform that uses machine learning to identify at-risk students early and enable proactive interventions by academic advisors.

## 🎯 Features

- **ML-Powered Risk Detection**: Random Forest model analyzes student engagement, performance, and behavioral patterns
- **Real-Time Dashboard**: Advisors see comprehensive analytics across all students and courses
- **Student Profiles**: Detailed risk indicators (performance, engagement, inactivity)
- **Intervention Tracking**: Monitor and manage support actions for at-risk students
- **Communication Hub**: Built-in messaging between advisors and students
- **Course Analytics**: Regional and module-based performance heatmaps
- **PDF Reports**: Generate downloadable reports for institutional use
- **Role-Based Access**: Separate views for advisors (full access) and students (personal data only)

## 🛠️ Tech Stack

**Backend:**
- Django 5.2.11 + Django REST Framework
- SQLite (default) / MySQL (optional)
- scikit-learn 1.8.0 (Random Forest)
- pandas, numpy, joblib

**Frontend:**
- React 19 + Vite
- Chart.js + D3.js for visualizations
- Axios for API communication
- React Router for navigation

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.9+** (Python 3.12 recommended)
- **Node.js 18+** and npm
- **pip** (Python package manager)

Optional:
- **MySQL** (if you prefer MySQL over SQLite)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd EARLY_warning_SYS
```

### Step 2: Set Up Python Virtual Environment

Open a terminal in the project root:

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If you encounter issues with `mysqlclient` installation on Windows, you can skip it (the project uses SQLite by default):
> ```bash
> pip install Django==5.2.11 djangorestframework==3.16.1 django-cors-headers==4.9.0 pandas==2.2.3 numpy==1.26.4 scikit-learn==1.8.0 joblib==1.4.2 requests==2.31.0
> ```

### Step 4: Run ML Data Preprocessing & Model Training

These scripts process the raw OULAD dataset and train the risk prediction model:

```bash
python ml\preprocessing.py
python ml\train_model.py
```

**Expected output:**
- `ml/processed_data.csv` — cleaned and feature-engineered dataset
- `ml/student_ews_model.pkl` — trained Random Forest model
- `ml/label_encoders.pkl` — categorical feature encoders

### Step 5: Set Up Django Backend

Navigate to the backend folder and run migrations:

```bash
cd backend
python manage.py migrate
```

Import student data into the database:

```bash
python manage.py import_data
```

**Expected output:** `Successfully imported XXXX students.`

Create an advisor account (superuser):

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- **Username** (e.g., `advisor`)
- **Email** (optional)
- **Password** (will be hidden as you type)

### Step 6: Start the Django Development Server

```bash
python manage.py runserver
```

✅ **Backend running at:** [http://localhost:8000](http://localhost:8000)

**Keep this terminal open.**

### Step 7: Set Up React Frontend

Open a **second terminal** and navigate to the frontend folder:

```bash
cd frontend
npm install
```

Start the Vite development server:

```bash
npm run dev
```

✅ **Frontend running at:** [http://localhost:5173](http://localhost:5173)

---

## 🎓 Using the Application

### Login as Advisor

1. Open [http://localhost:5173](http://localhost:5173) in your browser
2. Click **Sign In**
3. Use the superuser credentials you created
4. You'll see the full advisor dashboard with:
   - Overview: Risk distribution, stats, top at-risk students
   - Students: Searchable list of all students
   - Communications: Messaging hub
   - Course Analytics: Regional/module performance heatmaps
   - Intervention Tracker: Manage support actions
   - Reports: Generate PDF reports

### Login as Student

Students must first **register** using their student ID as the username:

1. Go to [http://localhost:5173/register](http://localhost:5173/register)
2. **Username:** Use a student ID from the database (e.g., `6516`, `8462`, `11391`)
3. **Password:** Any password (e.g., `student123`)
4. **Email:** Optional
5. Click **Create Account**
6. Log in with those credentials

Students see:
- Personal performance metrics
- Risk indicators (if at-risk)
- Messages from advisors
- Course engagement data

### Sample Student IDs

| Student ID | Module | Risk Status |
|------------|--------|-------------|
| `6516` | AAA | At Risk |
| `8462` | DDD | At Risk |
| `11391` | AAA | At Risk |
| `23629` | BBB | At Risk |
| `3733` | DDD | Safe |
| `23632` | BBB | Safe |

---

## 📁 Project Structure

```
EARLY_warning_SYS/
├── backend/                # Django REST API
│   ├── analytics/          # Main app (models, views, serializers)
│   ├── ews_backend/        # Project settings
│   ├── db.sqlite3          # SQLite database
│   └── manage.py
├── frontend/               # React + Vite app
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── api.js          # Axios API client
│   │   ├── App.jsx         # Main app + routing
│   │   └── main.jsx        # Entry point
│   ├── package.json
│   └── vite.config.js
├── ml/                     # Machine learning pipeline
│   ├── preprocessing.py    # Data cleaning & feature engineering
│   ├── train_model.py      # Model training script
│   ├── processed_data.csv  # Processed dataset (generated)
│   ├── student_ews_model.pkl  # Trained model (generated)
│   └── label_encoders.pkl  # Encoders (generated)
├── dataset/                # Raw OULAD dataset
│   ├── studentInfo.csv
│   ├── studentAssessment.csv
│   ├── studentVle.csv
│   └── ...
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🔧 Configuration

### Database Options

**SQLite (Default):**
- No additional setup required
- Database file: `backend/db.sqlite3`

**MySQL (Optional):**
1. Install MySQL and create a database:
   ```sql
   CREATE DATABASE ews_ai_driven;
   ```
2. Edit `backend/ews_backend/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'ews_ai_driven',
           'USER': 'root',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
3. Re-run migrations:
   ```bash
   python manage.py migrate
   python manage.py import_data
   ```

### Frontend API URL

If deploying or changing backend port, update the API base URL in `frontend/src/api.js`:

```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000/api',  // Change this URL
  headers: {
    'Content-Type': 'application/json',
  },
});
```

---

## 🐛 Troubleshooting

### Issue: `numpy import error` when running ML scripts

**Solution:**
```bash
# From project root (not ml folder)
pip uninstall numpy -y
pip install --force-reinstall --no-cache-dir numpy==1.26.4
python ml\preprocessing.py
```

### Issue: `pandas._libs.pandas_parser` ModuleNotFoundError

**Solution:**
```bash
pip install --force-reinstall --no-cache-dir pandas==2.2.3
```

### Issue: `sklearn.__check_build` error when importing data

**Solution:** The model was trained with a different Python/sklearn version. Retrain:
```bash
pip install --force-reinstall --no-cache-dir scikit-learn==1.8.0
python ml\train_model.py
python manage.py import_data
```

### Issue: Student login shows "No performance data found"

**Cause:** Student hasn't registered yet, or username doesn't match a student ID in the database.

**Solution:**
1. Register at `/register` with username = student ID (e.g., `6516`)
2. Then log in with those credentials

### Issue: Advisor sees "No performance data found"

**Cause:** Browser localStorage has stale `role: student` cached.

**Solution:**
1. Open DevTools (F12) → Application → Local Storage
2. Clear all storage for `http://localhost:5173`
3. Log in again

---

## 📊 Dataset Information

This project uses the **Open University Learning Analytics Dataset (OULAD)**:
- 32,593 students across 7 modules
- Engagement data (VLE clicks, assessment scores)
- Demographics (region, education level, disability status)

**Features used in ML model:**
- Performance: Average scores on first two assessments
- Engagement: Total VLE clicks
- Behavioral: Maximum inactivity gap (days)
- Demographics: Age, region, prior attempts, disability

---

## 📦 Deployment Notes

### Backend (Django)

1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Use a production WSGI server (e.g., Gunicorn, uWSGI)
4. Set up a reverse proxy (Nginx, Apache)
5. Use PostgreSQL or MySQL for production database

### Frontend (React)

1. Build production assets:
   ```bash
   npm run build
   ```
2. Serve the `dist/` folder with a static file server or CDN
3. Update API base URL to production backend

---

## 📝 License

[Add your license here]

---

## 🤝 Support

For issues or questions:
- Check the Troubleshooting section above
- Review Django/React logs in the terminal
- Verify all dependencies are installed correctly

---

**Built with ❤️ for educational institutions to support student success.**
"# Early-Warning-System" 
