from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from rest_framework.exceptions import ValidationError


ROLE_CHOICES = (
    ('doctor', 'doctor'),
    ('patient', 'patient')
)

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(100)])
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_image', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class DoctorProfile(UserProfile):
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday')
    )
    working_days = MultiSelectField(choices=DAY_CHOICES, max_length=64, max_choices=5)
    role = models.CharField(choices=ROLE_CHOICES, max_length=16, default='doctor')
    price = models.PositiveSmallIntegerField()
    experience = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.BooleanField(default=False)
    doctor_information = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}, {self.role}'

    class Meta:
        verbose_name_plural = 'DoctorProfile'

    def get_avg_rating(self):
        rating = self.ratings.all()
        if rating.exists():
            return round(sum([i.rating for i in rating]) / rating.count(), 1)

    def get_comment_count(self):
        comment = self.ratings.all()
        if comment.exists():
            return comment.count()


class Department(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='department')
    department_name = models.CharField(max_length=64)

    def __str__(self):
        return self.department_name


class Specialty(models.Model):
    doctor = models.ManyToManyField(DoctorProfile, related_name='specialty')
    specialty_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.specialty_name


class PatientProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    emergency_contact = PhoneNumberField()
    blood_type = models.CharField(max_length=16)
    role = models.CharField(choices=ROLE_CHOICES, max_length=16, default='patient')

    def __str__(self):
        return f'{self.user}, {self.role}'


class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='doctor')
    date_time = models.DateTimeField()
    APPOINTMENT_STATUS = (
        ('planned', 'planned'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    )
    status = models.CharField(choices=APPOINTMENT_STATUS, max_length=16)

    def __str__(self):
        return f'{self.patient}, {self.doctor}'


class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescribed_medication = models.CharField(max_length=64)
    created_at = models.DateField()

    def __str__(self):
        return f'{self.patient}, {self.doctor}'


class Feedback(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.patient}, {self.doctor}'

    def clean(self):
        super().clean()
        if not self.rating and not self.comment:
            raise ValidationError('Choose minimum one of (rating, comment)!')


class Chat(models.Model):
    person = models.ManyToManyField(DoctorProfile)
    created_at = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


