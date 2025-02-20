from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class UserProfilePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'age', 'phone_number', 'profile_picture']


class UserProfileAppointmentPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class SpecialtyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'specialty_name']


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['specialty_name']


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']


class PatientProfileListSerializer(serializers.ModelSerializer):
    user = UserProfilePatientSerializer()

    class Meta:
        model = PatientProfile
        fields = ['id', 'user', 'emergency_contact', 'blood_type']


class PatientProfileDetailSerializer(serializers.ModelSerializer):
    user = UserProfilePatientSerializer()

    class Meta:
        model = PatientProfile
        fields = ['user','emergency_contact', 'blood_type', 'role']


class PatientProfileAppointmentSerializer(serializers.ModelSerializer):
    user = UserProfileAppointmentPatientSerializer()

    class Meta:
        model = PatientProfile
        fields = ['user']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientProfileAppointmentSerializer()
    doctor = UserProfileAppointmentSerializer()
    date_time = serializers.DateTimeField(format('%d-%B-%Y %H:%M'))

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date_time', 'status']


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientProfileAppointmentSerializer()
    doctor = UserProfileAppointmentSerializer()

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'treatment',
                  'prescribed_medication', 'created_at']


class FeedbackSerializer(serializers.ModelSerializer):
    patient = PatientProfileAppointmentSerializer()
    doctor = UserProfileAppointmentSerializer()
    created_at = serializers.DateTimeField(format('%d-%b-%Y %H:%M'))


    class Meta:
        model = Feedback
        fields = ['id', 'patient', 'doctor', 'rating', 'comment', 'created_at']



class DoctorProfileListSerializer(serializers.ModelSerializer):
    specialty = SpecialtySerializer(many=True, read_only=True)
    department = DepartmentSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = ['id', 'first_name', 'last_name', 'specialty', 'department',
                  'price', 'working_days', 'avg_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()


class DoctorProfileDetailSerializer(serializers.ModelSerializer):
    specialty = SpecialtySerializer(many=True, read_only=True)
    department = DepartmentSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = ['first_name', 'last_name', 'age', 'phone_number', 'profile_picture', 'specialty', 'department',
                  'shift_start', 'shift_end', 'working_days', 'role', 'doctor_information', 'experience', 'gender', 'price', 'avg_rating', 'comment_count']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_comment_count(self, obj):
        return obj.get_comment_count()

