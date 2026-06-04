# AI-Driven Student Performance Analytics & Early Warning System (EWS)
## Comprehensive Project Documentation

This document provides a single-point reference for the entire AI-Driven EWS project. It covers the project's goals, the Machine Learning engine, the Backend architecture, the Frontend interface, and a detailed file-by-file breakdown.

---

## 1. Project Introduction & Goals
The **Student Early Warning System (EWS)** is designed to proactively identify students at risk of academic failure or disengagement. By shifting from a reactive model (identifying failure after it happens) to a predictive model, educational institutions can intervene early—shifting the needle on student success.

### Key Objectives:
- **Predictive Risk Modeling**: Identify "At-Risk" students as early as the first few weeks of a semester.
- **Engagement Tracking**: Monitor behavioral patterns (VLE interactions) to detect subtle signs of disengagement.
- **Data-Driven Interventions**: Provide Academic Advisors with a ranked list of students needing immediate contact.

---

## 2. The Machine Learning Engine
The heart of the EWS is a predictive model trained on the Open University Learning Analytics Dataset (OULAD).

### A. Preprocessing Logic (The "Red Flag" Heuristics)
Before training, we defined three major criteria for labeling a student as **"At-Risk"**:

1.  **Performance Threshold**: 
    - **Criteria**: An average score of less than **40%** across the first two formative assessments (TMA/CMA).
    - **Logic**: Early academic struggles are strong indicators of ultimate course failure.
2.  **Engagement Threshold**:
    - **Criteria**: Total interactions (clicks) falling below **75%** of the course average.
    - **Logic**: Relative disengagement compared to peers identifies students who are not keeping up with materials.
3.  **Inactivity Threshold**:
    - **Criteria**: A continuous period of **7 days** with zero logins/activity.
    - **Logic**: A week-long gap in participation often signals a drop-out risk.

### B. Machine Learning Algorithm
- **Algorithm**: `RandomForestClassifier` (100 Estimators).
- **Why Random Forest?**: 
    - Handles mixed data types (categorical demographics + numerical behavior) perfectly.
    - Robust to outliers.
    - Provides **Feature Importance**, allowing us to explain *why* a student is at risk.
- **Target Variable**: `is_at_risk` (A binary label derived from the OR-logic of the three thresholds above).
- **Handling Imbalance**: Used `class_weight='balanced'` to ensure the model learns from both "Safe" and "At-Risk" populations.

### C. Accuracy & Metrics
- **Accuracy**: ~99.8%.
- **Context**: The model achieved near-perfect accuracy because it effectively learned the explicit heuristic logic we used for labeling. In a real-world scenario with noise, this acts as a "logic-compliance" model.

### D. Feature Importance (Top Indicators)
1.  **Inactivity Gap**: ~45% influence on prediction.
2.  **Total Clicks**: ~34% influence on prediction.
3.  **Assessment Average**: ~17% influence on prediction.

---

## 3. Backend Architecture (Django & MySQL)
The backend is built using **Django REST Framework** and serves as the data processor and prediction server.

### Technical Stack:
- **Framework**: Django 4.x
- **API**: Django REST Framework (DRF)
- **Database**: MySQL (`ews_ai_driven`)
- **ML Integration**: Joblib for loading `.pkl` models.

### Key API Endpoints:
- `/api/students/`: (GET/SEARCH) List all students and their risk probabilities.
- `/api/stats/`: (GET) Summary metrics for the dashboard header.
- `/api/course-analytics/`: (GET) Advanced analytics by region and module (includes heatmap data).
- `/api/messages/`: (GET/POST) Messaging system between advisors and students.
- `/api/interventions/`: (GET/PUT) Status tracking for at-risk interventions.

---

## 4. Frontend Architecture (React.js)
The frontend is a modern, responsive dashboard built with **Vite** and **React**.

### Design Philosophy:
- **Aesthetics**: "Premium Obsidian" theme using **Glassmorphism** (`backdrop-filter: blur(12px)`).
- **Responsive**: Mobile-first design that scales to high-resolution desktop monitors.
- **Interactive**: Real-time filtering and dynamic chart rendering.

### Visualization Stack:
- **Chart.js**: Used for the Student Risk Distribution (Doughnut) and Module Overviews.
- **D3.js-style Heatmaps**: Logical heatmaps for identifying regional/course performance clusters.
- **Lucide-React**: Premium iconography for visual indicators.

---

## 5. Detailed File Breakdown

### Root Directory
- `requirements.txt`: Python package dependencies (Django, Scikit-learn, etc.).
- `package.json`: Frontend dependencies (React, Chart.js, Vite).

### `ml/` (The AI Layer)
- `preprocessing.py`: Aggregates raw OULAD CSVs into a single `processed_data.csv` and applies labeling logic.
- `train_model.py`: Trains the Random Forest model and saves the `.pkl` artifacts.
- `student_ews_model.pkl`: The serialized AI model.
- `label_encoders.pkl`: Encoders used to convert text (e.g., 'Male') into numbers for the AI.

### `backend/analytics/` (The API Layer)
- `models.py`: Defines the `Student`, `Intervention`, and `Message` tables.
- `views.py`: Core logic for fetching aggregated statistics and student lists.
- `auth_views.py`: Dedicated views for login and registration.
- `serializers.py`: Converts database records into JSON for the frontend.
- `management/commands/import_data.py`: A powerful script that imports CSV data into MySQL and runs AI predictions simultaneously.

### `frontend/src/` (The UI Layer)
- `App.jsx`: Root component handling navigation and theme.
- `api.js`: Centralized Axios configuration for backend communication.
- `index.css`: Global design system and premium styling tokens.
- **`components/`**:
    - `Dashboard.jsx`: The main hub showing KPIs and the at-risk student list.
    - `Home.jsx`: The landing page with project features.
    - `EngagementHeatMap.jsx`: Visual cluster analysis.
    - `AdvisorOverview.jsx`: Intervention management panel.

---

## 6. Installation & Setup

### Prerequisites:
- Python 3.10+
- Node.js 18+
- MySQL Server

### Step 1: Backend Setup
1.  Navigate to `backend/`.
2.  Install requirements: `pip install -r ../requirements.txt`.
3.  Configure database in `ews_backend/settings.py`.
4.  Run migrations: `python manage.py migrate`.
5.  Import data: `python manage.py import_data`.

### Step 2: Frontend Setup
1.  Navigate to `frontend/`.
2.  Install packages: `npm install`.
3.  Run dev server: `npm run dev`.

### Step 3: Run the AI Pipeline (Optional)
If you want to retrain the model:
1.  Run `python ml/preprocessing.py`.
2.  Run `python ml/train_model.py`.

---

**End of Documentation**
