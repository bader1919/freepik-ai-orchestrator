"""Tests for LLMOrchestrator"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from core.llm_orchestrator import LLMOrchestrator

class TestLLMOrchestrator:
    """Test cases for LLMOrchestrator"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create a test orchestrator"""
        return LLMOrchestrator()
    
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initialization"""
        assert orchestrator.config is not None
        assert hasattr(orchestrator, 'llm_provider')
    
    @pytest.mark.asyncio
    async def test_optimize_for_freepik_basic(self, orchestrator):
        """Test basic prompt optimization"""
        result = await orchestrator.optimize_for_freepik("professional headshot")
        
        assert "model" in result
        assert "enhanced_prompt" in result
        assert "style" in result
        assert "reasoning" in result
        assert result["confidence"] > 0
    
    @pytest.mark.asyncio
    async def test_optimize_professional_prompt(self, orchestrator):
        """Test optimization for professional prompts"""
        result = await orchestrator.optimize_for_freepik("professional headshot of businessman")
        
        # Should select imagen3 for professional photography
        assert result["model"] in ["imagen3", "mystic"]
        assert "professional" in result["enhanced_prompt"]
    
    @pytest.mark.asyncio
    async def test_optimize_artistic_prompt(self, orchestrator):
        """Test optimization for artistic prompts"""
        result = await orchestrator.optimize_for_freepik("creative abstract digital art")
        
        # Should select flux-dev or mystic for artistic content
        assert result["model"] in ["flux-dev", "mystic"]
        assert result["style"] in ["artistic", "balanced"]
    
    @pytest.mark.asyncio
    async def test_optimize_simple_prompt(self, orchestrator):
        """Test optimization for simple prompts"""
        result = await orchestrator.optimize_for_freepik("quick simple sketch")
        
        # Should select classic-fast for simple requests
        assert result["model"] in ["classic-fast", "mystic"]
    
    @pytest.mark.asyncio
    async def test_process_user_request(self, orchestrator):
        """Test complete user request processing"""
        result = await orchestrator.process_user_request(
            "professional headshot",
            {"quality_level": 8}
        )
        
        assert "task_id" in result
        assert "model_used" in result
        assert "optimization" in result
        assert "estimated_completion" in result
    
    @pytest.mark.asyncio
    async def test_analyze_image_requirements(self, orchestrator):
        """Test image requirements analysis"""
        result = await orchestrator.analyze_image_requirements(
            "professional corporate headshot for LinkedIn profile"
        )
        
        assert "use_case" in result
        assert "complexity" in result
        assert "realism_level" in result
        assert "recommended_workflow" in result
        assert "estimated_cost" in result
    
    def test_mock_optimization_keywords(self, orchestrator):
        """Test keyword-based model selection"""
        # Test imagen3 keywords
        result = orchestrator._create_mock_optimization("professional portrait photography")
        assert result["model"] == "imagen3"
        
        # Test flux-dev keywords
        result = orchestrator._create_mock_optimization("artistic creative illustration")
        assert result["model"] == "flux-dev"
        
        # Test classic-fast keywords
        result = orchestrator._create_mock_optimization("simple quick draft")
        assert result["model"] == "classic-fast"
        
        # Test default (mystic)
        result = orchestrator._create_mock_optimization("general image request")
        assert result["model"] == "mystic"
    
    def test_prompt_enhancement(self, orchestrator):
        """Test prompt enhancement logic"""
        # Short prompt should be enhanced
        short_result = orchestrator._create_mock_optimization("cat")
        assert len(short_result["enhanced_prompt"]) > len("cat")
        
        # Long prompt should remain mostly unchanged
        long_prompt = "A detailed professional headshot of a confident businesswoman in a modern office setting"
        long_result = orchestrator._create_mock_optimization(long_prompt)
        assert long_prompt in long_result["enhanced_prompt"]
    
    @pytest.mark.asyncio
    async def test_preferences_handling(self, orchestrator):
        """Test handling of user preferences"""
        preferences = {
            "quality_level": 9,
            "creativity_level": 7,
            "style": "cinematic"
        }
        
        result = await orchestrator.process_user_request(
            "portrait photo",
            preferences
        )
        
        assert result["optimization"]["confidence"] > 0
        assert "task_id" in result

if __name__ == "__main__":
    pytest.main([__file__])
