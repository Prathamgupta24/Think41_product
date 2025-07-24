from typing import List, Dict, Optional, Tuple
from src.models.schemas import (
    ProductTemplate, OptionCategory, OptionChoice, CompatibilityRule, 
    RuleType, ConfigurationValidationResponse
)
from src.core.storage import storage

class ProductConfigurationService:
    
    def create_product_template(self, template_data: dict) -> ProductTemplate:
        """Create a new product template"""
        template = ProductTemplate(**template_data)
        storage.product_templates[template.template_str_id] = template
        
        # Initialize empty categories and rules for this template
        if template.template_str_id not in storage.option_categories:
            storage.option_categories[template.template_str_id] = {}
        if template.template_str_id not in storage.compatibility_rules:
            storage.compatibility_rules[template.template_str_id] = []
            
        return template
    
    def add_option_category(self, template_str_id: str, category_data: dict) -> OptionCategory:
        """Add an option category to a template"""
        if template_str_id not in storage.product_templates:
            raise ValueError(f"Template {template_str_id} not found")
            
        category = OptionCategory(**category_data)
        
        if template_str_id not in storage.option_categories:
            storage.option_categories[template_str_id] = {}
            
        storage.option_categories[template_str_id][category.category_str_id] = category
        
        # Initialize empty choices for this category
        if category.category_str_id not in storage.option_choices:
            storage.option_choices[category.category_str_id] = {}
            
        return category
    
    def add_option_choice(self, category_str_id: str, choice_data: dict) -> OptionChoice:
        """Add an option choice to a category"""
        choice = OptionChoice(**choice_data)
        
        if category_str_id not in storage.option_choices:
            storage.option_choices[category_str_id] = {}
            
        storage.option_choices[category_str_id][choice.choice_str_id] = choice
        return choice
    
    def add_compatibility_rule(self, template_str_id: str, rule_data: dict) -> CompatibilityRule:
        """Add a compatibility rule to a template"""
        if template_str_id not in storage.product_templates:
            raise ValueError(f"Template {template_str_id} not found")
            
        rule = CompatibilityRule(**rule_data)
        
        if template_str_id not in storage.compatibility_rules:
            storage.compatibility_rules[template_str_id] = []
            
        storage.compatibility_rules[template_str_id].append(rule)
        return rule
    
    def get_available_options(self, template_str_id: str, target_category_str_id: str, 
                            current_selections: Dict[str, str]) -> List[OptionChoice]:
        """Get available options for a category given current selections"""
        if template_str_id not in storage.product_templates:
            raise ValueError(f"Template {template_str_id} not found")
            
        if target_category_str_id not in storage.option_choices:
            return []
            
        all_choices = list(storage.option_choices[target_category_str_id].values())
        rules = storage.compatibility_rules.get(template_str_id, [])
        
        available_choices = []
        
        for choice in all_choices:
            if self._is_choice_compatible(choice.choice_str_id, current_selections, rules):
                available_choices.append(choice)
                
        return available_choices
    
    def _is_choice_compatible(self, choice_str_id: str, current_selections: Dict[str, str], 
                            rules: List[CompatibilityRule]) -> bool:
        """Check if a choice is compatible with current selections"""
        for rule in rules:
            if rule.rule_type == RuleType.INCOMPATIBLE_WITH:
                # If this choice is incompatible with any selected choice
                if rule.primary_choice_str_id == choice_str_id:
                    if rule.secondary_choice_str_id in current_selections.values():
                        return False
                # If any selected choice is incompatible with this choice
                if rule.secondary_choice_str_id == choice_str_id:
                    if rule.primary_choice_str_id in current_selections.values():
                        return False
        
        return True
    
    def validate_configuration_and_get_price(self, template_str_id: str, 
                                           selections: Dict[str, str]) -> ConfigurationValidationResponse:
        """Validate a full configuration and calculate price"""
        if template_str_id not in storage.product_templates:
            return ConfigurationValidationResponse(
                is_valid=False,
                errors=[f"Template {template_str_id} not found"]
            )
        
        template = storage.product_templates[template_str_id]
        rules = storage.compatibility_rules.get(template_str_id, [])
        errors = []
        
        # Check REQUIRES rules
        selected_choices = list(selections.values())
        for rule in rules:
            if rule.rule_type == RuleType.REQUIRES:
                if rule.primary_choice_str_id in selected_choices:
                    if rule.secondary_choice_str_id not in selected_choices:
                        errors.append(
                            f"Choice {rule.primary_choice_str_id} requires {rule.secondary_choice_str_id}"
                        )
        
        # Check INCOMPATIBLE_WITH rules
        for rule in rules:
            if rule.rule_type == RuleType.INCOMPATIBLE_WITH:
                if (rule.primary_choice_str_id in selected_choices and 
                    rule.secondary_choice_str_id in selected_choices):
                    errors.append(
                        f"Choice {rule.primary_choice_str_id} is incompatible with {rule.secondary_choice_str_id}"
                    )
        
        if errors:
            return ConfigurationValidationResponse(
                is_valid=False,
                errors=errors
            )
        
        # Calculate total price
        total_price = template.base_price
        
        for category_id, choice_id in selections.items():
            if category_id in storage.option_choices:
                if choice_id in storage.option_choices[category_id]:
                    choice = storage.option_choices[category_id][choice_id]
                    total_price += choice.price_delta
        
        return ConfigurationValidationResponse(
            is_valid=True,
            total_price=total_price,
            errors=[]
        )

# Global service instance
product_service = ProductConfigurationService()
