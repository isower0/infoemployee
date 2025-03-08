from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    image_base64 = models.TextField(null=True, blank=True)  # เก็บ Base64 เป็นข้อความ
    def __str__(self):
        return f"{self.first_name} {self.last_name}"