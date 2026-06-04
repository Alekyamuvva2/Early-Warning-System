from django.db import models

class Student(models.Model):
    id_student = models.IntegerField(unique=True, primary_key=True)
    code_module = models.CharField(max_length=10, db_index=True)

    code_presentation = models.CharField(max_length=10)
    gender = models.CharField(max_length=2)
    region = models.CharField(max_length=100, db_index=True)

    highest_education = models.CharField(max_length=100)
    imd_band = models.CharField(max_length=10, null=True, blank=True)
    age_band = models.CharField(max_length=10)
    num_of_prev_attempts = models.IntegerField(default=0)
    studied_credits = models.IntegerField(default=0)
    disability = models.CharField(max_length=2)
    
    # Precomputed analytics
    avg_first_two_score = models.FloatField(default=0.0)
    total_clicks = models.FloatField(default=0.0)
    max_inactivity_gap = models.IntegerField(default=0)
    
    # Model Flags
    perf_at_risk = models.BooleanField(default=False)
    click_at_risk = models.BooleanField(default=False)
    inactivity_at_risk = models.BooleanField(default=False)
    
    # Final ML Prediction Label
    is_at_risk = models.BooleanField(default=False, db_index=True)

    risk_probability = models.FloatField(default=0.0)

    def __str__(self):
        return f"Student {self.id_student} ({self.code_module})"

class DashboardMetric(models.Model):
    """To store global stats for the dashboard"""
    total_students = models.IntegerField()
    total_at_risk = models.IntegerField()
    avg_engagement = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

class Message(models.Model):
    SENDER_CHOICES = (
        ('advisor', 'Academic Advisor'),
        ('student', 'Student'),
        ('system', 'System'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=15, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

class Intervention(models.Model):
    STATUS_CHOICES = (
        ('needs_action', 'Needs Action'),
        ('contacted', 'Contacted'),
        ('resolved', 'Resolved'),
    )
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='intervention')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='needs_action')
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Intervention for {self.student.id_student} - {self.status}"
