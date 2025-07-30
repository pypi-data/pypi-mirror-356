from .registry import SchemaRegistry
from .base import BaseSchema

# Import all schema classes
from .form_1040 import Form1040
from .w2 import W2
from .w4 import W4
from .i9 import I9
from .w9 import W9
from .w8ben import W8BENSchema
from .job_application import JobApplication
from .lease_agreement import LeaseAgreement
from .hipaa_authorization import HIPAAuthorization
from .direct_deposit import DirectDeposit
from .ds11_passport import DS11Passport
from .generic import GenericSchema

# Initialize the registry when the package is imported
SchemaRegistry()

# Export public API
__all__ = [
    'BaseSchema',
    'SchemaRegistry',
    'Form1040',
    'W2',
    'W4',
    'I9',
    'W9',
    'W8BENSchema',
    'JobApplication',
    'LeaseAgreement',
    'HIPAAuthorization',
    'DirectDeposit',
    'DS11Passport',
    'GenericSchema'
]
