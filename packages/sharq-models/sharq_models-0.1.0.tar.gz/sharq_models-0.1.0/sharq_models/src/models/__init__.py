__all__ = (
    "Faculty",
    "Direction",
    "Specialization",
    "StudyForm",
    "Application",
    "User",
    "AdditionalInfo",
    "EducationInfo",
    "PassportData"
)

from .application import Application
from .faculty import Faculty
from .direction import Direction
from .specialization import Specialization
from .study_form import StudyForm

from .user import User
from  .education_info import EducationInfo
from .additional_info import AdditionalInfo
from .passport_data import PassportData
