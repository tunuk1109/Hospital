from rest_framework import viewsets, generics, permissions, status, pagination
from .serializers import *
from .models import *
from .permissions import CheckDoctorProfile, CheckPatientProfile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import DoctorProfileFilter
from .paginations import DoctorProfilePagination, PatientProfilePagination, SpecialtyPagination, DepartmentPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class DoctorProfileListAPIView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DoctorProfileFilter
    search_fields = ['price', 'working_days']
    ordering_fields = ['price']
    pagination_class = DoctorProfilePagination


class DoctorProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DoctorProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = DoctorProfileDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class PatientProfileListAPIView(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PatientProfilePagination


class PatientProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckPatientProfile]



class PatientProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = PatientProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckPatientProfile]


class DepartmentListAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = DepartmentPagination
    filter_backends = [SearchFilter]
    search_fields = ['department_name']


class SpecialtyListAPIView(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtyListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = SpecialtyPagination
    filter_backends = [SearchFilter]
    search_fields = ['specialty_name']


class AppointmentListAPIView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckDoctorProfile, CheckPatientProfile]


class AppointmentCreateAPIView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckDoctorProfile]


class MedicalRecordListAPIView(generics.ListAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckDoctorProfile, CheckPatientProfile]


class MedicalRecordCreateAPIView(generics.CreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckDoctorProfile]


class MedicalRecordRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckDoctorProfile]


class FeedbackListAPIView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckPatientProfile]

    def get_queryset(self):
        return Feedback.objects.filter(patient__user=self.request.user)


class FeedbackCreateAPIView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckPatientProfile]


class FeedbackRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAdminUser]
