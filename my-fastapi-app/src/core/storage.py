from typing import Dict, List, Optional
from src.models.schemas import (
    ProductTemplate, OptionCategory, OptionChoice, CompatibilityRule, RuleType
)

class InMemoryStorage:
    def __init__(self):
        # Storage dictionaries
        self.product_templates: Dict[str, ProductTemplate] = {}
        self.option_categories: Dict[str, Dict[str, OptionCategory]] = {}  # template_id -> {category_id -> category}
        self.option_choices: Dict[str, Dict[str, OptionChoice]] = {}  # category_id -> {choice_id -> choice}
        self.compatibility_rules: Dict[str, List[CompatibilityRule]] = {}  # template_id -> [rules]
        
        # Initialize with some sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        # Sample product template
        laptop_template = ProductTemplate(
            template_str_id="laptop_x",
            name="Laptop Model X",
            base_price=800.0
        )
        self.product_templates["laptop_x"] = laptop_template
        
        # Sample categories for laptop
        cpu_category = OptionCategory(category_str_id="cpu", name="Processor")
        ram_category = OptionCategory(category_str_id="ram", name="Memory")
        gpu_category = OptionCategory(category_str_id="gpu", name="Graphics Card")
        
        self.option_categories["laptop_x"] = {
            "cpu": cpu_category,
            "ram": ram_category,
            "gpu": gpu_category
        }
        
        # Sample CPU choices
        self.option_choices["cpu"] = {
            "intel_i7": OptionChoice(choice_str_id="intel_i7", name="Intel Core i7", price_delta=150.0),
            "intel_cpu": OptionChoice(choice_str_id="intel_cpu", name="Intel CPU", price_delta=100.0),
            "amd_cpu": OptionChoice(choice_str_id="amd_cpu", name="AMD CPU", price_delta=120.0)
        }
        
        # Sample RAM choices
        self.option_choices["ram"] = {
            "16gb_ddr4": OptionChoice(choice_str_id="16gb_ddr4", name="16GB DDR4", price_delta=200.0),
            "8gb_ddr4": OptionChoice(choice_str_id="8gb_ddr4", name="8GB DDR4", price_delta=100.0),
            "32gb_ddr4": OptionChoice(choice_str_id="32gb_ddr4", name="32GB DDR4", price_delta=400.0)
        }
        
        # Sample GPU choices
        self.option_choices["gpu"] = {
            "amd_gpu": OptionChoice(choice_str_id="amd_gpu", name="AMD GPU", price_delta=300.0),
            "intel_gpu": OptionChoice(choice_str_id="intel_gpu", name="Intel GPU", price_delta=200.0),
            "nvidia_gpu": OptionChoice(choice_str_id="nvidia_gpu", name="NVIDIA GPU", price_delta=500.0),
            "mobo_z": OptionChoice(choice_str_id="mobo_z", name="Motherboard Z", price_delta=150.0)
        }
        
        # Sample compatibility rules
        self.compatibility_rules["laptop_x"] = [
            CompatibilityRule(
                rule_type=RuleType.REQUIRES,
                primary_choice_str_id="intel_i7",
                secondary_choice_str_id="mobo_z"
            ),
            CompatibilityRule(
                rule_type=RuleType.INCOMPATIBLE_WITH,
                primary_choice_str_id="amd_gpu",
                secondary_choice_str_id="intel_cpu"
            )
        ]

# Global storage instance
storage = InMemoryStorage()
