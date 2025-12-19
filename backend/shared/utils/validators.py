"""
Validation utilities for FHIR and NPHIES
"""

from typing import Dict, Any, List


def validate_fhir_resource(resource: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Validate FHIR R4 resource"""
    errors = []
    
    # Basic FHIR resource validation
    if "resourceType" not in resource:
        errors.append("Missing resourceType")
    
    # Add more validation logic here
    
    return len(errors) == 0, errors


def validate_nphies_claim(claim: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Validate NPHIES claim structure"""
    errors = []
    
    # NPHIES-specific validation
    if not claim.get("patient"):
        errors.append("Missing patient reference")
    
    # Add more validation logic
    
    return len(errors) == 0, errors
