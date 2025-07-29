import pytest
import aiohttp
from unittest.mock import AsyncMock, MagicMock, patch
import json

from agentic_profile_auth.web_did_resolver import (
    WebDidResolver,
    get_web_resolver,
    web_did_to_url,
    select_protocol
)
from agentic_profile_auth.did_core_types import parse_did

class TestWebDidToUrl:
    """Test the web_did_to_url function"""
    
    def test_basic_web_did(self):
        """Test basic web DID conversion"""
        did = "did:web:example.com"
        parsed = parse_did(did)
        url = web_did_to_url(did, parsed)
        assert url == "https://example.com/.well-known/did.json"
    
    def test_web_did_with_subdomain(self):
        """Test web DID with subdomain"""
        did = "did:web:example.com:user"
        parsed = parse_did(did)
        url = web_did_to_url(did, parsed)
        assert url == "https://example.com/user/did.json"
    
    def test_web_did_with_multiple_subdomains(self):
        """Test web DID with multiple subdomains"""
        did = "did:web:example.com:user:profile"
        parsed = parse_did(did)
        url = web_did_to_url(did, parsed)
        assert url == "https://example.com/user/profile/did.json"
    
    def test_localhost_web_did(self):
        """Test localhost web DID (should use HTTP)"""
        did = "did:web:localhost:8080"
        parsed = parse_did(did)
        url = web_did_to_url(did, parsed)
        assert url == "http://localhost:8080/.well-known/did.json"
    
    def test_web_did_with_query(self):
        """Test web DID with query parameters"""
        did = "did:web:example.com?version=1"
        parsed = parse_did(did)
        url = web_did_to_url(did, parsed)
        assert url == "https://example.com/.well-known/did.json?version=1"
    
    def test_web_did_with_path_raises_error(self):
        """Test that web DIDs with paths raise an error"""
        did = "did:web:example.com/path"
        parsed = parse_did(did)
        with pytest.raises(ValueError, match="Web DIDs do not support paths"):
            web_did_to_url(did, parsed)
    
    def test_non_web_did_raises_error(self):
        """Test that non-web DIDs raise an error"""
        did = "did:example:123"
        parsed = parse_did(did)
        with pytest.raises(ValueError, match="Only did:web is supported"):
            web_did_to_url(did, parsed)
    
    def test_invalid_did_raises_error(self):
        """Test that invalid DIDs raise an error"""
        with pytest.raises(ValueError, match="Failed to parse DID"):
            web_did_to_url("invalid")

class TestSelectProtocol:
    """Test the select_protocol function"""
    
    def test_localhost_uses_http(self):
        """Test that localhost uses HTTP"""
        assert select_protocol("localhost") == "http"
        assert select_protocol("localhost:8080") == "http"
    
    def test_other_domains_use_https(self):
        """Test that other domains use HTTPS"""
        assert select_protocol("example.com") == "https"
        assert select_protocol("api.example.com") == "https"
        assert select_protocol("127.0.0.1") == "https"

class TestWebDidResolver:
    """Test the WebDidResolver class"""
    
    @pytest.fixture
    def mock_session(self):
        """Create a mock aiohttp session"""
        session = AsyncMock(spec=aiohttp.ClientSession)
        return session
    
    @pytest.fixture
    def sample_did_document(self):
        """Sample DID document for testing"""
        return {
            "id": "did:web:example.com",
            "@context": ["https://www.w3.org/ns/did/v1"],
            "verificationMethod": [
                {
                    "id": "did:web:example.com#key-1",
                    "type": "JsonWebKey2020",
                    "controller": "did:web:example.com",
                    "publicKeyJwk": {
                        "kty": "OKP",
                        "crv": "Ed25519",
                        "x": "test-key"
                    }
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_successful_resolution(self, mock_session, sample_did_document):
        """Test successful DID resolution"""
        # Mock the HTTP response
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value=sample_did_document)
        mock_session.get = AsyncMock(return_value=mock_response)
        
        resolver = WebDidResolver(mock_session)
        parsed = parse_did("did:web:example.com")
        
        result = await resolver.resolve("did:web:example.com", parsed, {})
        
        assert result["didDocument"] == sample_did_document
        assert result["didDocumentMetadata"] == {}
        assert result["didResolutionMetadata"]["contentType"] == "application/did+ld+json"
        
        # Verify the correct URL was called
        mock_session.get.assert_called_once_with("https://example.com/.well-known/did.json")
    
    @pytest.mark.asyncio
    async def test_resolution_without_context(self, mock_session):
        """Test resolution of DID document without @context"""
        did_document = {
            "id": "did:web:example.com",
            "verificationMethod": []
        }
        
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value=did_document)
        mock_session.get = AsyncMock(return_value=mock_response)
        
        resolver = WebDidResolver(mock_session)
        parsed = parse_did("did:web:example.com")
        
        result = await resolver.resolve("did:web:example.com", parsed, {})
        
        assert result["didResolutionMetadata"]["contentType"] == "application/did+json"
    
    @pytest.mark.asyncio
    async def test_http_error(self, mock_session):
        """Test handling of HTTP errors"""
        mock_response = AsyncMock()
        mock_response.ok = False
        mock_response.status = 404
        mock_session.get = AsyncMock(return_value=mock_response)
        
        resolver = WebDidResolver(mock_session)
        parsed = parse_did("did:web:example.com")
        
        result = await resolver.resolve("did:web:example.com", parsed, {})
        
        assert result["didDocument"] is None
        assert "error" in result["didResolutionMetadata"]
        assert "HTTP error 404" in result["didResolutionMetadata"]["message"]
    
    @pytest.mark.asyncio
    async def test_invalid_json_response(self, mock_session):
        """Test handling of invalid JSON responses"""
        mock_response = AsyncMock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value="invalid json")
        mock_session.get = AsyncMock(return_value=mock_response)
        
        resolver = WebDidResolver(mock_session)
        parsed = parse_did("did:web:example.com")
        
        result = await resolver.resolve("did:web:example.com", parsed, {})
        
        assert result["didDocument"] is None
        assert "error" in result["didResolutionMetadata"]
        assert "Invalid DID Document format" in result["didResolutionMetadata"]["message"]
    
    @pytest.mark.asyncio
    async def test_network_exception(self, mock_session):
        """Test handling of network exceptions"""
        mock_session.get.side_effect = Exception("Network error")
        
        resolver = WebDidResolver(mock_session)
        parsed = parse_did("did:web:example.com")
        
        result = await resolver.resolve("did:web:example.com", parsed, {})
        
        assert result["didDocument"] is None
        assert "error" in result["didResolutionMetadata"]
        assert "Network error" in result["didResolutionMetadata"]["message"]
    
    @pytest.mark.asyncio
    async def test_resolver_without_session(self, sample_did_document):
        """Test resolver creates its own session when none provided"""
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = AsyncMock()
            mock_session_class.return_value.__aenter__.return_value = mock_session
            
            mock_response = AsyncMock()
            mock_response.ok = True
            mock_response.json.return_value = sample_did_document
            mock_session.get.return_value = mock_response
            
            resolver = WebDidResolver()
            parsed = parse_did("did:web:example.com")
            
            result = await resolver.resolve("did:web:example.com", parsed, {})
            
            assert result["didDocument"] == sample_did_document
            mock_session_class.assert_called_once()

class TestGetWebResolver:
    """Test the get_web_resolver function"""
    
    def test_get_web_resolver(self):
        """Test that get_web_resolver returns the correct structure"""
        session = AsyncMock()
        resolver_dict = get_web_resolver(session)
        
        assert "web" in resolver_dict
        assert isinstance(resolver_dict["web"], WebDidResolver)
        assert resolver_dict["web"]._session == session
    
    def test_get_web_resolver_without_session(self):
        """Test that get_web_resolver works without a session"""
        resolver_dict = get_web_resolver()
        
        assert "web" in resolver_dict
        assert isinstance(resolver_dict["web"], WebDidResolver)
        assert resolver_dict["web"]._session is None 