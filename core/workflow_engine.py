import asyncio
from typing import Dict, Any, List
from core.freepik_client import FreepikClient
from core.llm_orchestrator import LLMOrchestrator

class WorkflowEngine:
    """Orchestrates multi-step AI workflows"""
    
    def __init__(self):
        self.llm = LLMOrchestrator()
        self.workflows = self._load_workflow_templates()
    
    def _load_workflow_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined workflow templates"""
        return {
            "professional_headshot": {
                "name": "Professional Headshot",
                "description": "High-quality professional headshots with optimal lighting",
                "steps": [
                    {"action": "generate", "model": "imagen3", "params": {"style": "professional_photography"}},
                    {"action": "relight", "params": {"lighting": "professional_portrait"}},
                    {"action": "upscale", "params": {"factor": 4}},
                    {"action": "variants", "params": {"count": 3, "variation_type": "lighting"}}
                ],
                "estimated_time": "3-4 minutes",
                "estimated_cost": "$1.20"
            },
            
            "product_photography": {
                "name": "Product Photography",
                "description": "E-commerce ready product images with multiple angles",
                "steps": [
                    {"action": "generate", "model": "imagen3", "params": {"style": "product_photography"}},
                    {"action": "remove_background"},
                    {"action": "relight", "params": {"lighting": "studio"}},
                    {"action": "variants", "params": {"count": 4, "variation_type": "angle"}},
                    {"action": "upscale", "params": {"factor": 4}}
                ],
                "estimated_time": "4-5 minutes",
                "estimated_cost": "$2.50"
            },
            
            "marketing_materials": {
                "name": "Marketing Materials",
                "description": "Social media and marketing content with brand consistency",
                "steps": [
                    {"action": "generate", "model": "mystic", "params": {"style": "marketing"}},
                    {"action": "style_variants", "params": {"styles": ["modern", "classic", "bold"]}},
                    {"action": "aspect_ratio_variants", "params": {"ratios": ["16:9", "1:1", "9:16"]}},
                    {"action": "brand_overlay", "params": {"overlay_type": "logo"}}
                ],
                "estimated_time": "3-4 minutes",
                "estimated_cost": "$1.80"
            }
        }
    
    async def execute_workflow(self, workflow_name: str, prompt: str, custom_params: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Execute a predefined workflow"""
        
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        workflow = self.workflows[workflow_name]
        
        # For demo purposes, return mock execution result
        return {
            "workflow_name": workflow_name,
            "status": "completed",
            "results": [{"action": step["action"], "status": "completed"} for step in workflow["steps"]],
            "final_image_url": "https://example.com/result.jpg",
            "execution_log": {
                "workflow_name": workflow_name,
                "prompt": prompt,
                "steps_completed": workflow["steps"],
                "status": "completed",
                "total_time": 120
            }
        }
    
    def get_available_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available workflows"""
        return {k: {
            "name": v["name"],
            "description": v["description"],
            "estimated_time": v["estimated_time"],
            "estimated_cost": v["estimated_cost"],
            "steps_count": len(v["steps"])
        } for k, v in self.workflows.items()}
    
    async def estimate_workflow_cost(self, workflow_name: str) -> Dict[str, Any]:
        """Estimate cost and time for a workflow"""
        
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        workflow = self.workflows[workflow_name]
        
        # Cost estimation logic
        cost_map = {
            "generate": 0.30,
            "upscale": 0.20,
            "relight": 0.15,
            "remove_background": 0.10,
            "style_transfer": 0.25,
            "variants": 0.20
        }
        
        total_cost = 0
        time_estimate = 0
        
        for step in workflow["steps"]:
            action = step["action"]
            step_cost = cost_map.get(action, 0.10)
            total_cost += step_cost
            time_estimate += 30  # 30 seconds per step average
        
        return {
            "estimated_cost": f"${total_cost:.2f}",
            "estimated_time_seconds": time_estimate,
            "estimated_time_formatted": f"{time_estimate // 60}:{time_estimate % 60:02d}",
            "steps_count": len(workflow["steps"]),
            "complexity": "high" if len(workflow["steps"]) > 4 else "medium" if len(workflow["steps"]) > 2 else "low"
        }
