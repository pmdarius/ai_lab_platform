from django.db import models

class GPUMetrics(models.Model):
    gpu_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    utilization = models.FloatField()
    memory_used = models.FloatField()
    memory_total = models.FloatField()

    def __str__(self):
        return f'{self.gpu_id} @ {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
