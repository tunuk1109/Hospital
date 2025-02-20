from .models import Department, Specialty, MedicalRecord
from modeltranslation.translator import TranslationOptions, register

@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('department_name',)

@register(Specialty)
class SpecialtyTranslationOptions(TranslationOptions):
    fields = ('specialty_name',)

@register(MedicalRecord)
class MedicalRecordTranslationOptions(TranslationOptions):
    fields = ('diagnosis', 'treatment', 'prescribed_medication')