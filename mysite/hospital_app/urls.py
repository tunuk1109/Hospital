from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='user_list')


urlpatterns = [
    path('', include(router.urls)),
    path('doctors/', DoctorProfileListAPIView.as_view(), name='doctors_list'),
    path('doctor/<int:pk>/', DoctorProfileDetailAPIView.as_view(), name='doctor_detail'),
    path('doctor_create/', DoctorProfileCreateAPIView.as_view(), name='doctor_create'),

    path('departments/', DepartmentListAPIView.as_view(), name='departments_list'),
    path('specialties/', SpecialtyListAPIView.as_view(), name='specialties_list'),

    path('patients/', PatientProfileListAPIView.as_view(), name='patients_list'),
    path('patient/<int:pk>/', PatientProfileDetailAPIView.as_view(), name='patient_detail'),
    path('patient_create/', PatientProfileCreateAPIView.as_view(), name='patient_create'),

    path('appointment/', AppointmentListAPIView.as_view(), name='appointment_list'),
    path('appointment_create/', AppointmentCreateAPIView.as_view(), name='appointment_create'),

    path('medical_records/', MedicalRecordListAPIView.as_view(), name='medical_records_list'),
    path('medical_record_create/', MedicalRecordCreateAPIView.as_view(), name='medical_record_create'),
    path('medical_record/<int:pk>/', MedicalRecordRetrieveAPIView.as_view(), name='medical_record_retrieve'),

    path('feedbacks/', FeedbackListAPIView.as_view(), name='feedbacks_list'),
    path('feedback_create/', FeedbackCreateAPIView.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/', FeedbackRetrieveAPIView.as_view(), name='feedback_retrieve'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]