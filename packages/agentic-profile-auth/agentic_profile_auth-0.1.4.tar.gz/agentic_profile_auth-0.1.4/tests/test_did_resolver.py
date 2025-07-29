import logging
logging.basicConfig(level=logging.DEBUG)

import pytest
import aiohttp
import json
from unittest.mock import AsyncMock, MagicMock
from typing import Dict, Any, Optional
from pydantic import BaseModel

from agentic_profile_auth.did_resolver import (
    HttpDidResolver,
    ParsedDID,
    parse_did,
    ResolverRegistry
)
from agentic_profile_auth.models import AgenticProfile, DID, VerificationMethod, Service, AgentService
from agentic_profile_auth import InMemoryAgenticProfileStore

# Test data
TEST_DID = "did:example:123"
TEST_DID_WITH_FRAGMENT = "did:example:123#key-1"
TEST_DID_WITH_PARAMS = "did:example:123;version=1"
TEST_DID_WITH_PATH = "did:example:123/path"
TEST_DID_WITH_QUERY = "did:example:123?query=value"
TEST_DID_WITH_ALL = "did:example:123;version=1/path?query=value#key-1"

TEST_PROFILE = AgenticProfile(
    id=TEST_DID,
    name="Test Agent",
    verification_method=[
        VerificationMethod(
            id=f"{TEST_DID}#key-1",
            type="Ed25519VerificationKey2018",
            controller=TEST_DID,
            public_key_multibase="z6Mkf5rGMoatrSj1f4CyvuHBeXJELe9RPdzo2PKGNCKVtZxP"
        )
    ],
    service=[
        AgentService(
            id=f"{TEST_DID}#service-1",
            type="AgenticProfileService",
            service_endpoint="https://example.com/profile",
            name="Test Service",
            capability_invocation=[f"{TEST_DID}#key-1"]
        )
    ]
)

def to_dict(obj):
    if isinstance(obj, BaseModel):
        return {k: to_dict(v) for k, v in obj.dict().items()}
    elif isinstance(obj, list):
        return [to_dict(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    else:
        return obj

@pytest.fixture
def mock_session():
    """Create a mock aiohttp session"""
    session = AsyncMock(spec=aiohttp.ClientSession)
    return session

@pytest.fixture
def real_store():
    """Create a real in-memory agentic profile store for caching tests"""
    return InMemoryAgenticProfileStore()

@pytest.fixture
def mock_resolver():
    """Create a mock resolver"""
    resolver = AsyncMock(spec=ResolverRegistry)
    resolver.resolve.return_value = {
        "didDocument": to_dict(TEST_PROFILE),
        "didDocumentMetadata": {},
        "didResolutionMetadata": {"contentType": "application/json"}
    }
    return resolver

@pytest.mark.asyncio
async def test_parse_did():
    """Test DID parsing"""
    # Test basic DID
    parsed = parse_did(TEST_DID)
    assert parsed is not None
    assert parsed.did == TEST_DID
    assert parsed.method == "example"
    assert parsed.id == "123"
    
    # Test DID with fragment
    parsed = parse_did(TEST_DID_WITH_FRAGMENT)
    assert parsed is not None
    assert parsed.fragment == "key-1"
    
    # Test DID with params
    parsed = parse_did(TEST_DID_WITH_PARAMS)
    assert parsed is not None
    assert parsed.params == {"version": "1"}
    
    # Test DID with path
    parsed = parse_did(TEST_DID_WITH_PATH)
    assert parsed is not None
    assert parsed.path == "/path"
    
    # Test DID with query
    parsed = parse_did(TEST_DID_WITH_QUERY)
    assert parsed is not None
    assert parsed.query == "query=value"
    
    # Test DID with all components
    parsed = parse_did(TEST_DID_WITH_ALL)
    assert parsed is not None
    assert parsed.params == {"version": "1"}
    assert parsed.path == "/path"
    assert parsed.query == "query=value"
    assert parsed.fragment == "key-1"
    
    # Test invalid DID
    assert parse_did("invalid") is None

@pytest.mark.asyncio
async def test_create_resolver_with_session(mock_session, real_store, mock_resolver):
    """Test creating a resolver with a session"""
    resolver = HttpDidResolver(
        session=mock_session,
        store=real_store,
        registry={"example": mock_resolver}
    )
    assert resolver._session == mock_session
    assert resolver._own_session is False
    assert resolver._store == real_store
    assert resolver._registry == {"example": mock_resolver}

@pytest.mark.asyncio
async def test_create_resolver_without_session(real_store, mock_resolver):
    """Test creating a resolver without a session"""
    resolver = HttpDidResolver(
        store=real_store,
        registry={"example": mock_resolver}
    )
    assert resolver._session is None
    assert resolver._own_session is True
    assert resolver._store == real_store
    assert resolver._registry == {"example": mock_resolver}

@pytest.mark.asyncio
async def test_resolve_cached_profile(mock_session, real_store, mock_resolver):
    """Test resolving a cached profile"""
    # Save profile to store
    await real_store.save_agentic_profile(TEST_PROFILE)
    
    resolver = HttpDidResolver(
        session=mock_session,
        store=real_store,
        registry={"example": mock_resolver}
    )
    
    profile, metadata = await resolver.resolve(TEST_DID)
    assert profile == TEST_PROFILE
    assert metadata == {}
    
    # Verify resolver wasn't called
    mock_resolver.resolve.assert_not_called()

@pytest.mark.asyncio
async def test_resolve_non_existent_did(mock_session, real_store, mock_resolver):
    """Test resolving a non-existent DID"""
    mock_resolver.resolve.return_value = {
        "didResolutionMetadata": {
            "error": "notFound",
            "message": "DID not found"
        }
    }
    
    resolver = HttpDidResolver(
        session=mock_session,
        store=real_store,
        registry={"example": mock_resolver}
    )
    
    profile, metadata = await resolver.resolve(TEST_DID)
    assert profile is None
    assert metadata == {
        "error": "notFound",
        "message": "DID not found"
    }

@pytest.mark.asyncio
async def test_resolve_network_error(mock_session, real_store, mock_resolver):
    """Test handling network errors"""
    mock_resolver.resolve.side_effect = Exception("Network error")
    
    resolver = HttpDidResolver(
        session=mock_session,
        store=real_store,
        registry={"example": mock_resolver}
    )
    
    profile, metadata = await resolver.resolve(TEST_DID)
    assert profile is None
    assert metadata == {
        "error": "resolutionFailed",
        "message": "Network error"
    }

@pytest.mark.asyncio
async def test_resolve_invalid_did(mock_session, real_store, mock_resolver):
    """Test resolving an invalid DID"""
    resolver = HttpDidResolver(
        session=mock_session,
        store=real_store,
        registry={"example": mock_resolver}
    )
    
    profile, metadata = await resolver.resolve("invalid")
    assert profile is None
    assert metadata == {
        "error": "invalidDid",
        "message": "Invalid DID format: invalid"
    }

@pytest.mark.asyncio
async def test_resolve_unsupported_method(mock_session, real_store):
    """Test resolving a DID with an unsupported method"""
    resolver = HttpDidResolver(
        session=mock_session,
        store=real_store,
        registry={}
    )
    
    profile, metadata = await resolver.resolve(TEST_DID)
    assert profile is None
    assert metadata == {
        "error": "unsupportedDidMethod",
        "message": "Unsupported DID method: example"
    }

@pytest.mark.asyncio
async def test_resolver_cache_middleware(mock_session, real_store, mock_resolver):
    """Test the resolver cache middleware"""
    resolver = HttpDidResolver(
        session=mock_session,
        store=real_store,
        registry={"example": mock_resolver}
    )
    
    # First resolve - should use resolver
    profile, metadata = await resolver.resolve(TEST_DID)
    assert profile == TEST_PROFILE
    assert metadata == {}
    mock_resolver.resolve.assert_called_once()
    
    # Test no-cache parameter - should bypass cache
    mock_resolver.reset_mock()
    profile, metadata = await resolver.resolve(f"{TEST_DID};no-cache=true")
    assert profile == TEST_PROFILE
    assert metadata == {}
    mock_resolver.resolve.assert_called_once()
    
    # Test that cache is working by checking store has the profile
    cached_profile = await real_store.load_agentic_profile(TEST_DID)
    assert cached_profile is not None
    assert cached_profile.id == TEST_PROFILE.id

@pytest.mark.asyncio
async def test_session_management():
    """Test session management"""
    async with HttpDidResolver() as resolver:
        assert resolver._session is not None
        assert resolver._own_session is True
    
    assert resolver._session is None 