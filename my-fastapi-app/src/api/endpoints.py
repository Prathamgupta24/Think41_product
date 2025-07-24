from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from src.models.schemas import (
    ProductTemplateCreate, ProductTemplateResponse,
    OptionCategoryCreate, OptionCategoryResponse,
    OptionChoiceCreate, OptionChoiceResponse,
    CompatibilityRuleCreate, CompatibilityRuleResponse,
    AvailableOptionsRequest, ConfigurationValidationRequest,
    ConfigurationValidationResponse, MessageResponse
)
from src.core.service import product_service

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Welcome to the Product Configuration API!"}

# Product Template Endpoints
@router.post("/product-templates", response_model=ProductTemplateResponse)
async def create_product_template(template: ProductTemplateCreate):
    """Create a new product template"""
    try:
        created_template = product_service.create_product_template(template.dict())
        return created_template
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Option Category Endpoints
@router.post("/product-templates/{template_str_id}/option-categories", response_model=OptionCategoryResponse)
async def add_option_category(template_str_id: str, category: OptionCategoryCreate):
    """Add an option category to a template"""
    try:
        created_category = product_service.add_option_category(template_str_id, category.dict())
        return created_category
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Option Choice Endpoints
@router.post("/option-categories/{category_str_id}/choices", response_model=OptionChoiceResponse)
async def add_option_choice(category_str_id: str, choice: OptionChoiceCreate):
    """Add a specific choice to an option category"""
    try:
        created_choice = product_service.add_option_choice(category_str_id, choice.dict())
        return created_choice
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Compatibility Rule Endpoints
@router.post("/product-templates/{template_str_id}/compatibility-rules", response_model=CompatibilityRuleResponse)
async def add_compatibility_rule(template_str_id: str, rule: CompatibilityRuleCreate):
    """Store a compatibility rule between two option choices within the template"""
    try:
        created_rule = product_service.add_compatibility_rule(template_str_id, rule.dict())
        return created_rule
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Available Options Endpoint
@router.post("/product-templates/{template_str_id}/available-options/{target_category_str_id}", 
             response_model=List[OptionChoiceResponse])
async def get_available_options(template_str_id: str, target_category_str_id: str, 
                              request: AvailableOptionsRequest):
    """Based on current selections and defined compatibility rules, return a list of valid OptionChoice objects for the target_category_str_id"""
    try:
        available_options = product_service.get_available_options(
            template_str_id, 
            target_category_str_id, 
            request.current_selections
        )
        return available_options
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Configuration Validation Endpoint
@router.post("/product-templates/{template_str_id}/validate", response_model=ConfigurationValidationResponse)
async def validate_configuration(template_str_id: str, request: ConfigurationValidationRequest):
    """Validate a full configuration and get the total price"""
    try:
        # Override template_str_id from URL if different in request body
        validation_result = product_service.validate_configuration_and_get_price(
            template_str_id, 
            request.selections
        )
        return validation_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Product Configuration API is running"}