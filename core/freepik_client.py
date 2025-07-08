import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional
from config.settings import CONFIG

class FreepikClient:
    """Async client for Freepik API with comprehensive model support"""
    
    def __init__(self):
        self.config = CONFIG["freepik"]
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "FreepikOrchestrator/1.0"
            },
            timeout=aiohttp.ClientTimeout(total=60)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _build_webhook_url(self, source: str, task_type: str = "generation") -> str:
        """Build webhook URL with tracking parameters"""
        return f"{self.config.webhook_url}?source={source}&type={task_type}&env={self.config.environment}"
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        url = f"{self.config.base_url}{endpoint}"
        
        try:
            async with self.session.request(method, url, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API Error {response.status}: {error_text}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    # Core Generation Methods
    async def generate_mystic(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate with Freepik's Mystic model"""
        payload = {
            "prompt": prompt,
            "webhook_url": self._build_webhook_url("mystic"),
            **kwargs
        }
        
        result = await self._make_request("POST", "/v1/ai/text-to-image/mystic", json=payload)
        return {"model": "mystic", **result}
    
    async def generate_imagen3(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate with Google's Imagen3"""
        payload = {
            "prompt": prompt,
            "webhook_url": self._build_webhook_url("imagen3"),
            **kwargs
        }
        
        result = await self._make_request("POST", "/v1/ai/text-to-image/imagen3", json=payload)
        return {"model": "imagen3", **result}
    
    async def generate_flux_dev(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate with Flux Dev"""
        payload = {
            "prompt": prompt,
            "webhook_url": self._build_webhook_url("flux-dev"),
            **kwargs
        }
        
        result = await self._make_request("POST", "/v1/ai/text-to-image/flux-dev", json=payload)
        return {"model": "flux-dev", **result}
    
    async def generate_classic_fast(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate with Classic Fast (synchronous)"""
        payload = {
            "prompt": prompt,
            **kwargs
        }
        
        result = await self._make_request("POST", "/v1/ai/text-to-image", json=payload)
        return {"model": "classic-fast", "synchronous": True, **result}
    
    # Post-Processing Methods
    async def upscale_image(self, image_url: str, scale_factor: int = 4) -> Dict[str, Any]:
        """Upscale image using Magnific"""
        payload = {
            "image_url": image_url,
            "scale_factor": scale_factor,
            "webhook_url": self._build_webhook_url("upscale", "post-processing")
        }
        
        return await self._make_request("POST", "/v1/ai/image-upscaler", json=payload)
    
    async def relight_image(self, image_url: str, lighting_style: str = "professional") -> Dict[str, Any]:
        """Relight image"""
        payload = {
            "image_url": image_url,
            "lighting_style": lighting_style,
            "webhook_url": self._build_webhook_url("relight", "post-processing")
        }
        
        return await self._make_request("POST", "/v1/ai/image-relight", json=payload)
    
    async def style_transfer(self, source_url: str, style_url: str) -> Dict[str, Any]:
        """Apply style transfer"""
        payload = {
            "source_image_url": source_url,
            "style_image_url": style_url,
            "webhook_url": self._build_webhook_url("style-transfer", "post-processing")
        }
        
        return await self._make_request("POST", "/v1/ai/image-style-transfer", json=payload)
    
    async def remove_background(self, image_url: str) -> Dict[str, Any]:
        """Remove background (synchronous)"""
        payload = {"image_url": image_url}
        return await self._make_request("POST", "/v1/ai/remove-background/beta", json=payload)
    
    # Status Methods
    async def get_task_status(self, task_id: str, model: str) -> Dict[str, Any]:
        """Get status of async task"""
        endpoints = {
            "mystic": "/v1/ai/text-to-image/mystic",
            "imagen3": "/v1/ai/text-to-image/imagen3",
            "flux-dev": "/v1/ai/text-to-image/flux-dev",
            "upscale": "/v1/ai/image-upscaler",
            "relight": "/v1/ai/image-relight",
            "style-transfer": "/v1/ai/image-style-transfer"
        }
        
        endpoint = endpoints.get(model, "/v1/ai/text-to-image/mystic")
        return await self._make_request("GET", f"{endpoint}/{task_id}")
