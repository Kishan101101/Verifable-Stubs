"""
OpenAPI schema generator with Pydantic model support.
This maps routes to their request/response Pydantic schemas for Swagger UI documentation.
"""
from typing import Type, Dict, Any
from pydantic import BaseModel


def pydantic_to_openapi_schema(model: Type[BaseModel]) -> Dict[str, Any]:
    """Convert Pydantic model to OpenAPI 3.0 schema."""
    if not hasattr(model, 'model_fields'):
        return {'type': 'object'}
    
    properties = {}
    required = []
    
    for field_name, field_info in model.model_fields.items():
        field_type = field_info.annotation
        field_schema = {'description': field_info.description or ''}
        
        # Handle basic types
        origin = getattr(field_type, '__origin__', None)
        
        if field_type == str or field_type == type(str):
            field_schema['type'] = 'string'
        elif field_type == int or field_type == type(int):
            field_schema['type'] = 'integer'
        elif field_type == float or field_type == type(float):
            field_schema['type'] = 'number'
        elif field_type == bool or field_type == type(bool):
            field_schema['type'] = 'boolean'
        elif origin is list:
            field_schema['type'] = 'array'
            field_schema['items'] = {'type': 'object'}
        elif hasattr(field_type, 'model_fields'):  # Nested Pydantic model
            field_schema = pydantic_to_openapi_schema(field_type)
        else:
            field_schema['type'] = 'object'
        
        properties[field_name] = field_schema
        
        # Check if field is required (has no default)
        if field_info.is_required():
            required.append(field_name)
    
    schema = {
        'type': 'object',
        'properties': properties,
    }
    
    if required:
        schema['required'] = required
    
    return schema


# Route-to-schema mappings
ROUTE_SCHEMAS = {
    # Doctor routes
    '/api/v1/doctors/admin/add': {
        'request': 'DoctorSeedSchema',
        'response': 'DoctorResponseSchema',
    },
    '/api/v1/doctors/psv/verify': {
        'request': 'GenericVerifySchema',
        'response': 'GenericVerifySchema',
    },
    '/api/v1/doctors/psv/license/status': {
        'response': 'LicenseStatusSchema',
    },
    '/api/v1/doctors/psv/degree/info': {
        'response': 'DegreeInfoSchema',
    },
    '/api/v1/doctors/psv/board-cert/info': {
        'response': 'BoardCertInfoSchema',
    },
    '/api/v1/doctors/psv/training/info': {
        'response': 'TrainingInfoSchema',
    },
    '/api/v1/doctors/psv/employment/info': {
        'response': 'EmploymentInfoSchema',
    },
    '/api/v1/doctors/psv/disciplines/check': {
        'response': 'DisciplinaryCheckSchema',
    },
    '/api/v1/doctors/psv/malpractice/history': {
        'response': 'MalpracticeHistorySchema',
    },
    # Academic routes
    '/api/v1/academic/admin/students': {
        'request': 'StudentSeedSchema',
        'response': 'StudentResponseSchema',
    },
    '/api/v1/academic/admin/eligibility-rules': {
        'request': 'EligibilityRuleSchema',
        'response': 'EligibilityRuleSchema',
    },
    '/api/v1/academic/admin/merit-rules': {
        'request': 'MeritRuleSchema',
        'response': 'MeritRuleSchema',
    },
    '/api/v1/academic/check-eligibility': {
        'response': 'EligibilityCheckSchema',
    },
    '/api/v1/academic/calculate-merit': {
        'response': 'MeritCalculationSchema',
    },
    '/api/v1/academic/verify/roll-number': {
        'response': 'RollNumberLookupSchema',
    },
    '/api/v1/academic/verify/certificate': {
        'response': 'RollNumberLookupSchema',
    },
    # Insurance routes
    '/api/v1/insurance/admin/medical-enrichment': {
        'request': 'MedicalEnrichmentRequestSchema',
        'response': 'MedicalEnrichmentResponseSchema',
    },
    '/api/v1/insurance/admin/reviewer-request': {
        'request': 'ReviewerRequestSchema',
        'response': 'ReviewerRequestResponseSchema',
    },
    '/api/v1/insurance/admin/payout-request': {
        'request': 'PayoutRequestSchema',
        'response': 'PayoutRequestResponseSchema',
    },
    '/api/v1/insurance/admin/notification': {
        'request': 'NotificationRequestSchema',
        'response': 'NotificationResponseSchema',
    },
    '/api/v1/insurance/medical/enrich': {
        'request': 'MedicalEnrichmentRequestSchema',
        'response': 'MedicalDataEnrichmentSchema',
    },
    '/api/v1/insurance/notification/send': {
        'request': 'NotificationRequestSchema',
        'response': 'NotificationResponseSchema',
    },
    '/api/v1/insurance/payout/process': {
        'request': 'PayoutRequestSchema',
        'response': 'PayoutRequestResponseSchema',
    },
    '/api/v1/insurance/claims/review': {
        'request': 'ClaimReviewSchema',
        'response': 'ClaimReviewSchema',
    },
}


def get_schema_class(schema_name: str):
    """Dynamically import and return Pydantic schema class by name."""
    try:
        from app.schemas.doctor_schema import (
            DoctorSeedSchema, DoctorResponseSchema, LicenseStatusSchema,
            DegreeInfoSchema, BoardCertInfoSchema, TrainingInfoSchema,
            EmploymentInfoSchema, DisciplinaryCheckSchema, MalpracticeHistorySchema,
            GenericVerifySchema
        )
        from app.schemas.academic_schema import (
            StudentSeedSchema, StudentResponseSchema, MeritRuleSchema, EligibilityRuleSchema,
            RollNumberLookupSchema, EligibilityCheckSchema, MeritCalculationSchema
        )
        from app.schemas.insurance_schema import (
            MedicalEnrichmentRequestSchema, MedicalEnrichmentResponseSchema,
            NotificationRequestSchema, NotificationResponseSchema,
            PayoutRequestSchema, PayoutRequestResponseSchema, ReviewerRequestSchema,
            ReviewerRequestResponseSchema, MedicalDataEnrichmentSchema
        )
        
        schemas = {
            # Doctor schemas
            'DoctorSeedSchema': DoctorSeedSchema,
            'DoctorResponseSchema': DoctorResponseSchema,
            'LicenseStatusSchema': LicenseStatusSchema,
            'DegreeInfoSchema': DegreeInfoSchema,
            'BoardCertInfoSchema': BoardCertInfoSchema,
            'TrainingInfoSchema': TrainingInfoSchema,
            'EmploymentInfoSchema': EmploymentInfoSchema,
            'DisciplinaryCheckSchema': DisciplinaryCheckSchema,
            'MalpracticeHistorySchema': MalpracticeHistorySchema,
            'GenericVerifySchema': GenericVerifySchema,
            # Academic schemas
            'StudentSeedSchema': StudentSeedSchema,
            'StudentResponseSchema': StudentResponseSchema,
            'MeritRuleSchema': MeritRuleSchema,
            'EligibilityRuleSchema': EligibilityRuleSchema,
            'RollNumberLookupSchema': RollNumberLookupSchema,
            'EligibilityCheckSchema': EligibilityCheckSchema,
            'MeritCalculationSchema': MeritCalculationSchema,
            # Insurance schemas
            'MedicalEnrichmentRequestSchema': MedicalEnrichmentRequestSchema,
            'MedicalEnrichmentResponseSchema': MedicalEnrichmentResponseSchema,
            'NotificationRequestSchema': NotificationRequestSchema,
            'NotificationResponseSchema': NotificationResponseSchema,
            'PayoutRequestSchema': PayoutRequestSchema,
            'PayoutRequestResponseSchema': PayoutRequestResponseSchema,
            'ReviewerRequestSchema': ReviewerRequestSchema,
            'ReviewerRequestResponseSchema': ReviewerRequestResponseSchema,
            'MedicalDataEnrichmentSchema': MedicalDataEnrichmentSchema,
            'ClaimReviewSchema': MedicalDataEnrichmentSchema,  # Fallback
        }
        
        return schemas.get(schema_name)
    except ImportError as e:
        print(f"Import error in get_schema_class: {e}")
        return None
