"""Data models for the Freepik AI Orchestrator"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ModelType(Enum):
    """Available AI models"""
    MYSTIC = "mystic"
    IMAGEN3 = "imagen3"
    FLUX_DEV = "flux-dev"
    CLASSIC_FAST = "classic-fast"
    AUTO = "auto"

class WorkflowAction(Enum):
    """Available workflow actions"""
    GENERATE = "generate"
    UPSCALE = "upscale"
    RELIGHT = "relight"
    REMOVE_BACKGROUND = "remove_background"
    STYLE_TRANSFER = "style_transfer"
    VARIANTS = "variants"

@dataclass
class GenerationRequest:
    """Image generation request model"""
    prompt: str
    model: ModelType = ModelType.AUTO
    style: Optional[str] = None
    aspect_ratio: Optional[str] = None
    quality_level: int = 8
    creativity_level: int = 5
    webhook_url: Optional[str] = None
    user_id: Optional[str] = None

@dataclass
class OptimizationResult:
    """LLM optimization result model"""
    model: str
    enhanced_prompt: str
    style: str
    aspect_ratio: str
    reasoning: str
    post_processing: List[str]
    alternative_model: str
    confidence: float

@dataclass
class GenerationResult:
    """Image generation result model"""
    task_id: str
    model_used: str
    status: TaskStatus
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    error_message: Optional[str] = None
    optimization: Optional[OptimizationResult] = None
    processing_time: Optional[int] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass
class WorkflowStep:
    """Individual workflow step model"""
    action: WorkflowAction
    params: Dict[str, Any]
    model: Optional[str] = None

@dataclass
class WorkflowTemplate:
    """Workflow template model"""
    id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    estimated_time: str
    estimated_cost: str
    is_custom: bool = False

@dataclass
class UserAnalytics:
    """User analytics model"""
    user_id: str
    period_days: int
    total_generations: int
    successful_generations: int
    failed_generations: int
    success_rate: float
    total_cost_cents: int
    average_processing_time: float
    models_used: Dict[str, int]
    daily_stats: List[Dict[str, Any]]

@dataclass
class APIError:
    """API error model"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

@dataclass
class WebhookPayload:
    """Webhook payload model"""
    event: str
    task_id: str
    timestamp: datetime
    data: Dict[str, Any]

@dataclass
class UserPreferences:
    """User preferences model"""
    preferred_model: ModelType = ModelType.AUTO
    default_style: Optional[str] = None
    default_aspect_ratio: str = "16:9"
    quality_level: int = 8
    creativity_level: int = 5
    enable_post_processing: bool = True
    auto_upscale: bool = False
    enable_variations: bool = False

@dataclass
class PostProcessingRequest:
    """Post-processing request model"""
    image_url: str
    action: WorkflowAction
    params: Dict[str, Any]
    webhook_url: Optional[str] = None

# Model mapping for API responses
MODEL_MAPPING = {
    "mystic": ModelType.MYSTIC,
    "imagen3": ModelType.IMAGEN3,
    "flux-dev": ModelType.FLUX_DEV,
    "classic-fast": ModelType.CLASSIC_FAST,
    "auto": ModelType.AUTO
}

# Style options
STYLE_OPTIONS = [
    "photorealistic",
    "artistic",
    "cinematic",
    "technical",
    "abstract",
    "professional_photography",
    "product_photography",
    "marketing",
    "concept_art",
    "digital_art",
    "illustration"
]

# Aspect ratio options
ASPECT_RATIO_OPTIONS = [
    "auto",
    "16:9",
    "1:1", 
    "9:16",
    "4:3",
    "3:2",
    "21:9"
]

# Validation functions
def validate_generation_request(request: GenerationRequest) -> List[str]:
    """Validate generation request and return list of errors"""
    errors = []
    
    if not request.prompt or len(request.prompt.strip()) == 0:
        errors.append("Prompt is required")
    
    if len(request.prompt) > 2000:
        errors.append("Prompt too long (max 2000 characters)")
    
    if request.quality_level < 1 or request.quality_level > 10:
        errors.append("Quality level must be between 1 and 10")
    
    if request.creativity_level < 1 or request.creativity_level > 10:
        errors.append("Creativity level must be between 1 and 10")
    
    if request.style and request.style not in STYLE_OPTIONS:
        errors.append(f"Invalid style. Must be one of: {', '.join(STYLE_OPTIONS)}")
    
    if request.aspect_ratio and request.aspect_ratio not in ASPECT_RATIO_OPTIONS:
        errors.append(f"Invalid aspect ratio. Must be one of: {', '.join(ASPECT_RATIO_OPTIONS)}")
    
    return errors

def validate_workflow_step(step: WorkflowStep) -> List[str]:
    """Validate workflow step and return list of errors"""
    errors = []
    
    if not isinstance(step.action, WorkflowAction):
        errors.append("Invalid workflow action")
    
    if not isinstance(step.params, dict):
        errors.append("Step params must be a dictionary")
    
    # Validate specific action requirements
    if step.action == WorkflowAction.UPSCALE:
        if "factor" not in step.params:
            errors.append("Upscale action requires 'factor' parameter")
        elif not isinstance(step.params["factor"], int) or step.params["factor"] not in [2, 4, 8]:
            errors.append("Upscale factor must be 2, 4, or 8")
    
    return errors

# Helper functions
def model_to_string(model: ModelType) -> str:
    """Convert ModelType enum to string"""
    return model.value

def string_to_model(model_str: str) -> ModelType:
    """Convert string to ModelType enum"""
    return MODEL_MAPPING.get(model_str, ModelType.AUTO)

def calculate_success_rate(successful: int, total: int) -> float:
    """Calculate success rate percentage"""
    if total == 0:
        return 0.0
    return round((successful / total) * 100, 2)

def estimate_cost(model: ModelType, post_processing: List[str] = None) -> float:
    """Estimate cost for generation and post-processing"""
    base_costs = {
        ModelType.MYSTIC: 0.30,
        ModelType.IMAGEN3: 0.45,
        ModelType.FLUX_DEV: 0.60,
        ModelType.CLASSIC_FAST: 0.15,
        ModelType.AUTO: 0.35  # Average cost
    }
    
    processing_costs = {
        "upscale": 0.20,
        "relight": 0.15,
        "remove_background": 0.10,
        "style_transfer": 0.25,
        "variants": 0.20
    }
    
    total_cost = base_costs.get(model, 0.35)
    
    if post_processing:
        for process in post_processing:
            total_cost += processing_costs.get(process, 0.10)
    
    return round(total_cost, 2)
