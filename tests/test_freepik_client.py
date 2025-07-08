"""Tests for FreepikClient"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from core.freepik_client import FreepikClient

class TestFreepikClient:
    """Test cases for FreepikClient"""
    
    @pytest.fixture
    async def client(self):
        """Create a test client"""
        async with FreepikClient() as client:
            yield client
    
    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Test client initialization"""
        client = FreepikClient()
        assert client.config is not None
        assert hasattr(client, 'session')
    
    @pytest.mark.asyncio
    async def test_webhook_url_building(self):
        """Test webhook URL building"""
        client = FreepikClient()
        url = client._build_webhook_url("mystic", "generation")
        assert "source=mystic" in url
        assert "type=generation" in url
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.request')
    async def test_generate_mystic(self, mock_request, client):
        """Test Mystic model generation"""
        # Mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"task_id": "test_task_123"}
        mock_request.return_value.__aenter__.return_value = mock_response
        
        result = await client.generate_mystic("test prompt")
        
        assert result["model"] == "mystic"
        assert "task_id" in result
        mock_request.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.request')
    async def test_generate_imagen3(self, mock_request, client):
        """Test Imagen3 model generation"""
        # Mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"task_id": "test_task_456"}
        mock_request.return_value.__aenter__.return_value = mock_response
        
        result = await client.generate_imagen3("professional headshot")
        
        assert result["model"] == "imagen3"
        assert "task_id" in result
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.request')
    async def test_upscale_image(self, mock_request, client):
        """Test image upscaling"""
        # Mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"task_id": "upscale_789"}
        mock_request.return_value.__aenter__.return_value = mock_response
        
        result = await client.upscale_image("https://example.com/image.jpg", 4)
        
        assert "task_id" in result
        mock_request.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.request')
    async def test_api_error_handling(self, mock_request, client):
        """Test API error handling"""
        # Mock error response
        mock_response = AsyncMock()
        mock_response.status = 400
        mock_response.text.return_value = "Bad Request"
        mock_request.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            await client.generate_mystic("test prompt")
        
        assert "API Error 400" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager functionality"""
        async with FreepikClient() as client:
            assert client.session is not None
        
        # Session should be closed after context
        assert client.session.closed

if __name__ == "__main__":
    pytest.main([__file__])
