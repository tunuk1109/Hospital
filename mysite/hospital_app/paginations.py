from rest_framework.pagination import PageNumberPagination

class DoctorProfilePagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5

class PatientProfilePagination(PageNumberPagination):
    page_size = 2


class SpecialtyPagination(PageNumberPagination):
    page_size = 5


class DepartmentPagination(PageNumberPagination):
    page_size = 5
