"""
LemonMeringue: Enhanced Python SDK for LemonSlice API
"""

import asyncio
import time
import logging
from typing import Optional, Dict, Any, List, Callable, Union
from dataclasses import dataclass
from enum import Enum

import aiohttp
import backoff
from pydantic import BaseModel, validator


class LemonMeringueError(Exception):
    """Base exception for LemonMeringue SDK"""
    pass


class ValidationError(LemonMeringueError):
    """Raised when input validation fails"""
    pass


class APIError(LemonMeringueError):
    """Raised when API returns an error"""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class GenerationStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class RetryConfig:
    """Configuration for retry behavior"""
    max_retries: int = 3
    backoff_factor: float = 2.0
    max_backoff: float = 60.0
    retry_on_status: List[int] = None
    
    def __post_init__(self):
        if self.retry_on_status is None:
            self.retry_on_status = [500, 502, 503, 504, 429]


class GenerationRequest(BaseModel):
    """Request model for video generation"""
    img_url: str
    audio_url: Optional[str] = None
    voice_id: Optional[str] = None
    text: Optional[str] = None
    model: str = "V2.5"
    resolution: str = "512"
    crop_head: bool = False
    whole_body_mode: bool = False
    animation_style: str = "autoselect"
    expressiveness: float = 1.0
    
    @validator('expressiveness')
    def validate_expressiveness(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('expressiveness must be between 0 and 1')
        return v
    
    @validator('model')
    def validate_model(cls, v):
        if v not in ['V2', 'V2.5']:
            raise ValueError('model must be V2 or V2.5')
        return v
    
    def validate_audio_or_text(self):
        """Ensure either audio_url or both voice_id and text are provided"""
        if not self.audio_url and not (self.voice_id and self.text):
            raise ValidationError("Must provide either audio_url or both voice_id and text")


class GenerationResponse(BaseModel):
    """Response model for video generation"""
    job_id: str
    status: GenerationStatus
    video_url: Optional[str] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    created_at: Optional[str] = None


class LemonSliceClient:
    """Enhanced LemonSlice API client with retry logic and better error handling"""
    
    BASE_URL = "https://lemonslice.com/api/v2"
    
    def __init__(
        self,
        api_key: str,
        retry_config: RetryConfig = None,
        timeout: int = 30,
        enable_logging: bool = False
    ):
        self.api_key = api_key
        self.retry_config = retry_config or RetryConfig()
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        
        if enable_logging:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def __aenter__(self):
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _ensure_session(self):
        """Ensure aiohttp session is created"""
        if not self.session or self.session.closed:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=self.timeout
            )
    
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, APIError),
        max_tries=3,
        max_time=300
    )
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request with automatic retry logic"""
        await self._ensure_session()
        
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        self.logger.info(f"Making {method} request to {url}")
        
        try:
            async with self.session.request(method, url, **kwargs) as response:
                response_data = await response.json()
                
                if response.status in self.retry_config.retry_on_status:
                    raise APIError(
                        f"API returned status {response.status}",
                        status_code=response.status,
                        response=response_data
                    )
                
                if not response.ok:
                    # Provide more specific error messages based on status code
                    if response.status == 404:
                        raise APIError(
                            f"Resource not found: {endpoint}",
                            status_code=response.status,
                            response=response_data
                        )
                    elif response.status == 401:
                        raise APIError(
                            "Invalid API key or unauthorized access",
                            status_code=response.status,
                            response=response_data
                        )
                    elif response.status == 429:
                        raise APIError(
                            "Rate limit exceeded",
                            status_code=response.status,
                            response=response_data
                        )
                    else:
                        # Use error message from API if available, otherwise fallback
                        error_msg = response_data.get('error', f"API error (status {response.status})")
                        raise APIError(
                            error_msg,
                            status_code=response.status,
                            response=response_data
                        )
                
                return response_data
                
        except aiohttp.ClientError as e:
            self.logger.error(f"Request failed: {e}")
            raise APIError(f"Request failed: {e}")
    
    async def generate_video(
        self,
        request: Union[GenerationRequest, dict],
        on_progress: Optional[Callable[[GenerationResponse], None]] = None,
        poll_interval: float = 5.0
    ) -> GenerationResponse:
        """
        Generate a single video with optional progress tracking
        
        Args:
            request: Generation request parameters
            on_progress: Optional callback for progress updates
            poll_interval: How often to check for completion (seconds)
            
        Returns:
            GenerationResponse with video URL and metadata
        """
        
        if isinstance(request, dict):
            request = GenerationRequest(**request)
        
        request.validate_audio_or_text()
        
        # Submit generation job
        response_data = await self._make_request(
            'POST', 
            'generate', 
            json=request.dict(exclude_none=True)
        )
        
        job_id = response_data.get('job_id')
        if not job_id:
            raise APIError("No job_id returned from generation request")
        
        self.logger.info(f"Generation started with job_id: {job_id}")
        
        # Poll for completion
        return await self._poll_generation(job_id, on_progress, poll_interval)
    
    async def _poll_generation(
        self,
        job_id: str,
        on_progress: Optional[Callable[[GenerationResponse], None]] = None,
        poll_interval: float = 5.0
    ) -> GenerationResponse:
        """Poll generation status until completion"""
        
        start_time = time.time()
        
        while True:
            try:
                status_data = await self._make_request('GET', f'generations/{job_id}')
                
                response = GenerationResponse(**status_data)
                response.processing_time = time.time() - start_time
                
                if on_progress:
                    on_progress(response)
                
                if response.status == GenerationStatus.COMPLETED:
                    self.logger.info(f"Generation completed in {response.processing_time:.1f}s")
                    return response
                
                elif response.status == GenerationStatus.FAILED:
                    raise APIError(f"Generation failed: {response.error_message}")
                
                # Continue polling
                await asyncio.sleep(poll_interval)
                
            except APIError as e:
                if e.status_code == 404:
                    raise APIError(f"Job {job_id} not found")
                raise
    
    async def get_generation_status(self, job_id: str) -> GenerationResponse:
        """Get status of a specific generation"""
        status_data = await self._make_request('GET', f'generations/{job_id}')
        return GenerationResponse(**status_data)
    
    async def list_generations(
        self, 
        limit: int = 10, 
        offset: int = 0
    ) -> List[GenerationResponse]:
        """List recent generations"""
        params = {'limit': limit, 'offset': offset}
        response_data = await self._make_request('GET', 'generations', params=params)
        
        generations = response_data.get('generations', [])
        return [GenerationResponse(**gen) for gen in generations]
    
    async def generate_batch(
        self,
        requests: List[Union[GenerationRequest, dict]],
        on_progress: Optional[Callable[[int, int, GenerationResponse], None]] = None,
        max_concurrent: int = 3
    ) -> List[GenerationResponse]:
        """
        Generate multiple videos with concurrency control
        
        Args:
            requests: List of generation requests
            on_progress: Optional callback with (current, total, response)
            max_concurrent: Maximum concurrent generations
            
        Returns:
            List of GenerationResponse objects
        """
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def generate_one(i: int, request: Union[GenerationRequest, dict]) -> GenerationResponse:
            async with semaphore:
                def progress_callback(response):
                    if on_progress:
                        on_progress(i + 1, len(requests), response)
                
                return await self.generate_video(request, progress_callback)
        
        tasks = [generate_one(i, req) for i, req in enumerate(requests)]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def validate_inputs(self, img_url: str, audio_url: Optional[str] = None) -> Dict[str, bool]:
        """Validate image and audio URLs before generation"""
        results = {}
        
        async def check_url(url: str, url_type: str) -> bool:
            try:
                async with self.session.head(url) as response:
                    return response.ok
            except Exception as e:
                self.logger.warning(f"Failed to validate {url_type} URL {url}: {e}")
                return False
        
        await self._ensure_session()
        
        results['img_url_valid'] = await check_url(img_url, 'image')
        if audio_url:
            results['audio_url_valid'] = await check_url(audio_url, 'audio')
        
        return results

    async def quick_generate_text(
        self,
        img_url: str,
        voice_id: str,
        text: str,
        **kwargs
    ) -> GenerationResponse:
        """
        Quickly generate a video from text and voice.
        Args:
            img_url: Image URL
            voice_id: Voice ID for TTS
            text: Text to speak
            **kwargs: Additional generation parameters
        Returns:
            GenerationResponse with video URL
        """
        request = GenerationRequest(
            img_url=img_url,
            voice_id=voice_id,
            text=text,
            **kwargs
        )
        return await self.generate_video(request)

    async def quick_generate_audio(
        self,
        img_url: str,
        audio_url: str,
        **kwargs
    ) -> GenerationResponse:
        """
        Quickly generate a video from an audio file.
        Args:
            img_url: Image URL
            audio_url: Audio file URL
            **kwargs: Additional generation parameters
        Returns:
            GenerationResponse with video URL
        """
        request = GenerationRequest(
            img_url=img_url,
            audio_url=audio_url,
            **kwargs
        )
        return await self.generate_video(request)


# Available voices as constants for easy reference
class Voices:
    """Available voice IDs for text-to-speech"""
    ANDREA = "9EU0h6CVtEDS6vriwwq5"  # young woman, Spanish, Hispanic, calm, soft
    RUSSO = "DwI0NZuZgKu8SNwnpa1x"   # middle-aged man, Australian, TV, narrator
    OTANI = "3JDquces8E8bkmvbh6Bc"   # middle-aged man, Japanese
    GIOVANNI = "fzDFBB4mgvMlL36gPXcz"  # young man, Italian, deep
    MORIOKO = "8EkOjt4xTPGMclNlh1pk"   # young woman, Japanese
    ENRIQUE = "iDEmt5MnqUotdwCIVplo"   # middle-aged man, Spanish, Hispanic
    CARMELO = "bUntPeGTvR1ifSUplNsS"   # middle-aged man, Spanish, Hispanic, deep
    DANIELA = "ajOR9IDAaubDK5qtLUqQ"   # young woman, Spanish, Hispanic, upbeat
    VALLERIE = "mLJVsC2pwqCmmrBUAzg6"  # older woman, British, calm, confident
    MIA = "rCuVrCHOUMY3OwyJBJym"       # middle-aged woman, American, slow, raspy
    ALICE = "nbk2esDn4RRk4cVDdoiE"     # ASMR whispering, British woman
    RUSSELL = "NYC9WEgkq1u4jiqBseQ9"   # middle-aged man, British, dramatic
    EMMA = "AnvlJBAqSLDzEevYr9Ap"      # young woman, German
    CAMILLE = "txtf1EDouKke753vN8SL"   # young woman, French, calm
    KEVIN = "gAMZphRyrWJnLMDnom6H"     # young man, Chinese American
    AMINA = "A8rwEcJwudjohY1gjPfa"     # young woman, Nigerian
    NIA = "CBHdTdZwkV4jYoCyMV1B"       # middle-aged woman, African American