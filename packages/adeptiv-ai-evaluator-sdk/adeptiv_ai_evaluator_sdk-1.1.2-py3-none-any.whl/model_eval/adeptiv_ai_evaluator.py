import os
import time
import uuid
from typing import Dict, Optional, Any, List
import aiohttp
import logging
from dataclasses import dataclass, asdict
import random
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LLMResponseTestCase:
    """Test case for LLM evaluation - supports single or multiple exchanges"""
    query: str
    llm_response: str
    llm_expected_response: Optional[str] = ""
    retrieved_chunks: Optional[List[str]] = None
    system_context: Optional[List[str]] = None
    
    def validate(self):
        """Check if test case is valid"""
        if not self.query:
            raise ValueError("query is required")
        if not self.llm_response:
            raise ValueError("llm_response is required")

@dataclass
class LLMSequentialestCase:
    """Test case for multi-step conversations"""
    test_cases: List[LLMResponseTestCase]
    app_role: str
    role_description:str
    prompt_guidelines:Optional[str] = ""
    model_name: str = "gpt-4"
    
    def validate(self):
        """Check if conversational test case is valid"""
        if not self.test_cases:
            raise ValueError("test_cases cannot be empty")
        if len(self.test_cases) < 1:
            raise ValueError("need at least 1 test case")
        
        for i, test_case in enumerate(self.test_cases):
            try:
                test_case.validate()
            except ValueError as e:
                raise ValueError(f"test case {i}: {e}")
        
        if not self.app_role:
            raise ValueError("app_role is required")
        if not self.role_description:
            raise ValueError("role_description is required")

class AsyncEvaluatorClient:
    """Client for testing LLM outputs with anonymous session support and sampling"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        client_secret: Optional[str] = None,
        source: Optional[str] = None,
        session_alias: Optional[str] = None,  # NEW
        custom_headers: Optional[Dict[str, str]] = None,
        sample_ratio: float = 1.0,
    ):
        self.api_key = api_key 
        self.client_secret = client_secret 
        self.source = source
        self.base_url = "https://api-dev.adeptiv.ai"

        if not self.api_key or not self.client_secret:
            raise ValueError("API key and client secret are required.")

        if not self.base_url.startswith("https://"):
            raise ValueError("Only HTTPS base URLs are allowed.")

        self.api_endpoint = f"{self.base_url}/api/llm/process/output/"
        self.verify_url = f"{self.base_url}/api/project/verify-keys/"
        self.sample_ratio = sample_ratio
        self.session_alias = session_alias 

        self.session_id: Optional[str] = None
        self.project_id: Optional[str] = None
        self.is_connected = False
        self.custom_headers = custom_headers or {}

    async def connect(self) -> Dict:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "X-SECRET-Key": self.client_secret,
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.verify_url, headers=headers) as response:
                    if response.status == 200:
                        self.is_connected = True
                        data = await response.json()
                        self.project_id = data.get('data').get("project_id")
                        self.session_id = self._auto_create_session()
                        logger.info(f"Connected. Session: {self.session_id}")
                        
                        return {"is_connected": True, "project_id": self.project_id}
                    else:
                        return {"is_connected": False, "status": response.status}
            except Exception as e:
                logger.error(f"Connection error: {e}")
                return {"is_connected": False, "error": str(e)}

    def _auto_create_session(self) -> str:
        """Create session ID: either passed in by user or randomly generated"""
        if self.session_alias:
            session_id = f"alias_{self.session_alias}{self.project_id}_{uuid.uuid4().hex[:6]}"
        else:
            session_id = f"anon_{self.project_id}{uuid.uuid4().hex[:8]}"
            
        logger.info(f"Generated session ID: {session_id}")
        
        return session_id

    def _should_sample(self) -> bool:
        return random.random() < self.sample_ratio

    async def send_output(self, test_case: LLMResponseTestCase) -> Dict[str, Any]:
        if not self.is_connected or not self.session_id:
            raise RuntimeError("Not connected. Call connect() first.")

        if not self._should_sample():
            logger.info("Skipping test case due to sampling settings.")
            pass

        test_case.validate()
        payload = {
            "project_id": self.project_id,
            "client_session_id": self.session_id,
            "timestamp": time.time(),
            "data": asdict(test_case),
            "api_key":self.api_key,
            "client_secret": self.client_secret,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self.api_endpoint,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        return {"status": "success", "api_response": await response.json()}
                    else:
                        return {"status": "error", "details": await response.text()}
        except Exception as e:
            logger.error(f"Send failed: {e}")
            return {"status": "error", "details": str(e)}

    async def close(self):
        self.is_connected = False
        self.session_id = None
        logger.info("Client disconnected.")
