from rest_framework import permissions

class CheckDoctorProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.role == 'doctor'

class CheckPatientProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.role == 'patient'


