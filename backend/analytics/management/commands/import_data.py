import csv
import os
from django.core.management.base import BaseCommand
from analytics.models import Student
import joblib

class Command(BaseCommand):
    help = 'Imports processed student data from CSV into MySQL'

    def handle(self, *args, **options):
        import warnings
        warnings.filterwarnings("ignore")
        
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../ml/processed_data.csv'))
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../ml/student_ews_model.pkl'))
        encoder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../ml/label_encoders.pkl'))
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_path}'))
            return

        # Load model and encoders
        model = None
        encoders = None
        if os.path.exists(model_path) and os.path.exists(encoder_path):
            model = joblib.load(model_path)
            encoders = joblib.load(encoder_path)
            self.stdout.write(self.style.SUCCESS('Loaded ML model and encoders.'))

        self.stdout.write(self.style.SUCCESS(f'Reading data from {csv_path}...'))
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        
        self.stdout.write(self.style.SUCCESS(f'Preparing features for {len(rows)} students...'))
        
        cat_features = ['code_module', 'code_presentation', 'gender', 'region', 
                        'highest_education', 'imd_band', 'age_band', 'disability']
        num_features = ['num_of_prev_attempts', 'studied_credits', 
                        'avg_first_two_score', 'sum_click', 'gap']
        
        all_features = []
        for row in rows:
            feat_row = []
            for col in cat_features:
                val = str(row[col])
                try:
                    encoded_val = encoders[col].transform([val])[0]
                except:
                    encoded_val = 0 
                feat_row.append(encoded_val)
            for col in num_features:
                feat_row.append(float(row[col]))
            all_features.append(feat_row)
            
        probabilities = [0.0] * len(rows)
        if model:
            self.stdout.write(self.style.SUCCESS('Predicting risk probabilities in batch...'))
            probabilities = model.predict_proba(all_features)[:, 1]
            
        self.stdout.write(self.style.SUCCESS('Saving student records to database...'))
        students_to_create = []
        for i, row in enumerate(rows):
            student = Student(
                id_student=int(row['id_student']),
                code_module=row['code_module'],
                code_presentation=row['code_presentation'],
                gender=row['gender'],
                region=row['region'],
                highest_education=row['highest_education'],
                imd_band=row['imd_band'],
                age_band=row['age_band'],
                num_of_prev_attempts=int(row['num_of_prev_attempts']),
                studied_credits=int(row['studied_credits']),
                disability=row['disability'],
                avg_first_two_score=float(row['avg_first_two_score']),
                total_clicks=float(row['sum_click']),
                max_inactivity_gap=int(float(row['gap'])),
                perf_at_risk=True if int(float(row['perf_at_risk'])) == 1 else False,
                click_at_risk=True if int(float(row['click_at_risk'])) == 1 else False,
                inactivity_at_risk=True if int(float(row['inactivity_at_risk'])) == 1 else False,
                is_at_risk=True if int(float(row['is_at_risk'])) == 1 else False,
                risk_probability=probabilities[i]
            )
            students_to_create.append(student)
            
            if len(students_to_create) >= 1000:
                Student.objects.bulk_create(students_to_create, ignore_conflicts=True)
                students_to_create = []

        if students_to_create:
            Student.objects.bulk_create(students_to_create, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(rows)} students.'))
