from django.db import models
from django.conf import settings

class Mentor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentor_profile")
    expertise = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    bio = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Mentor: {self.user.email}"

class MentorSession(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentorship_sessions")
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session with {self.mentor.user.email} for {self.student.email}"
