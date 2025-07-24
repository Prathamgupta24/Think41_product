from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class RuleType(str, Enum):
    REQUIRES = "REQUIRES"
    INCOMPATIBLE_WITH = "INCOMPATIBLE_WITH"

# Product Template Models
class ProductTemplate(BaseModel):
    template_str_id: str
    name: str
    base_price: float

class ProductTemplateCreate(BaseModel):
    template_str_id: str
    name: str
    base_price: float

class ProductTemplateResponse(ProductTemplate):
    pass

# Option Category Models
class OptionCategory(BaseModel):
    category_str_id: str
    name: str

class OptionCategoryCreate(BaseModel):
    category_str_id: str
    name: str

class OptionCategoryResponse(OptionCategory):
    pass

# Option Choice Models
class OptionChoice(BaseModel):
    choice_str_id: str
    name: str
    price_delta: float

class OptionChoiceCreate(BaseModel):
    choice_str_id: str
    name: str
    price_delta: float

class OptionChoiceResponse(OptionChoice):
    pass

# Compatibility Rule Models
class CompatibilityRule(BaseModel):
    rule_type: RuleType
    primary_choice_str_id: str
    secondary_choice_str_id: str

class CompatibilityRuleCreate(BaseModel):
    rule_type: RuleType
    primary_choice_str_id: str
    secondary_choice_str_id: str

class CompatibilityRuleResponse(CompatibilityRule):
    pass

# Configuration Models
class CurrentSelections(BaseModel):
    selections: Dict[str, str]  # category_str_id -> choice_str_id

class AvailableOptionsRequest(BaseModel):
    current_selections: Dict[str, str]

class ConfigurationValidationRequest(BaseModel):
    template_str_id: str
    selections: Dict[str, str]

class ConfigurationValidationResponse(BaseModel):
    is_valid: bool
    total_price: Optional[float] = None
    errors: List[str] = []

# Response Models
class MessageResponse(BaseModel):
    message: str
    
class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None