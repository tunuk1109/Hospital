from django_filters import FilterSet
from .models import DoctorProfile

class DoctorProfileFilter(FilterSet):
    class Meta:
        model = DoctorProfile
        fields = {

            'price': ['gt', 'lt']
        }