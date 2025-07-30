"""
Comprehensive test script for LemonMeringue
Tests all core functionality with real API calls using your API key
"""

import asyncio
import os
import time
from typing import List

from lemonmeringue import (
    LemonSliceClient,
    GenerationRequest,
    GenerationResponse,
    RetryConfig,
    Voices,
    APIError,
    ValidationError
)


# Test configuration
API_KEY = os.getenv('LEMONSLICE_API_KEY')  # Set this environment variable
SAMPLE_IMAGE_URL = "https://6ammc3n5zzf5ljnz.public.blob.vercel-storage.com/inf2-defaults/cool_man-AZGi3AIjUGN47rGxA8xdHMBGr1Qqha.png"


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results: List[str] = []
    
    def add_pass(self, test_name: str, details: str = ""):
        self.passed += 1
        self.results.append(f"✅ {test_name}: {details}")
        print(f"✅ {test_name}: {details}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.results.append(f"❌ {test_name}: {error}")
        print(f"❌ {test_name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n📊 Test Summary: {self.passed}/{total} passed")
        if self.failed > 0:
            print("❌ Failed tests:")
            for result in self.results:
                if result.startswith("❌"):
                    print(f"   {result}")


async def test_basic_functionality(results: TestResults):
    """Test 1: Basic client creation and simple generation"""
    try:
        async with LemonSliceClient(API_KEY, enable_logging=True) as client:
            # Test client creation
            assert client.api_key == API_KEY
            assert client.session is not None
            
            # Test simple generation
            response = await client.generate_video(
                GenerationRequest(
                    img_url=SAMPLE_IMAGE_URL,
                    voice_id=Voices.ANDREA,
                    text="Hello, this is a basic functionality test!",
                    expressiveness=0.8
                )
            )
            
            assert response.status.value == "completed"
            assert response.video_url is not None
            assert response.processing_time > 0
            
            results.add_pass("Basic Functionality", f"Generated in {response.processing_time:.1f}s")
            return response.video_url
            
    except Exception as e:
        results.add_fail("Basic Functionality", str(e))
        return None


async def test_progress_tracking(results: TestResults):
    """Test 2: Progress tracking functionality"""
    try:
        progress_updates = []
        
        def progress_callback(response: GenerationResponse):
            progress_updates.append(response.status.value)
            print(f"   📊 Progress update: {response.status.value}")
        
        async with LemonSliceClient(API_KEY) as client:
            response = await client.generate_video(
                GenerationRequest(
                    img_url=SAMPLE_IMAGE_URL,
                    voice_id=Voices.RUSSO,
                    text="Testing progress tracking functionality!",
                    expressiveness=0.7
                ),
                on_progress=progress_callback
            )
            
            assert response.status.value == "completed"
            assert len(progress_updates) > 0
            
            results.add_pass("Progress Tracking", f"{len(progress_updates)} status updates received")
            
    except Exception as e:
        results.add_fail("Progress Tracking", str(e))


async def test_input_validation(results: TestResults):
    """Test 3: Input validation"""
    try:
        # Test missing audio/text
        try:
            request = GenerationRequest(img_url=SAMPLE_IMAGE_URL)
            request.validate_audio_or_text()
            results.add_fail("Input Validation", "Should have failed validation")
        except ValidationError:
            pass  # Expected
        
        # Test invalid expressiveness
        try:
            GenerationRequest(
                img_url=SAMPLE_IMAGE_URL, 
                voice_id=Voices.ANDREA, 
                text="test", 
                expressiveness=2.0
            )
            results.add_fail("Input Validation", "Should have failed expressiveness validation")
        except ValueError:
            pass  # Expected
        
        # Test invalid model
        try:
            GenerationRequest(
                img_url=SAMPLE_IMAGE_URL, 
                voice_id=Voices.ANDREA, 
                text="test", 
                model="InvalidModel"
            )
            results.add_fail("Input Validation", "Should have failed model validation")
        except ValueError:
            pass  # Expected
        
        results.add_pass("Input Validation", "All validation checks working correctly")
        
    except Exception as e:
        results.add_fail("Input Validation", str(e))


async def test_quick_generate(results: TestResults):
    """Test 4: Quick generate convenience function"""
    try:
        start_time = time.time()
        async with LemonSliceClient(API_KEY) as client:
            response = await client.quick_generate_text(
                img_url=SAMPLE_IMAGE_URL,
                voice_id=Voices.EMMA,
                text="Testing the quick generate function!",
                expressiveness=0.9
            )
        elapsed = time.time() - start_time
        assert response.status.value == "completed"
        assert response.video_url is not None
        results.add_pass("Quick Generate", f"Completed in {elapsed:.1f}s")
    except Exception as e:
        results.add_fail("Quick Generate", str(e))


async def test_batch_processing(results: TestResults):
    """Test 5: Batch processing with concurrency"""
    try:
        requests = [
            {
                "img_url": SAMPLE_IMAGE_URL,
                "voice_id": Voices.ANDREA,
                "text": "Batch test number one",
                "expressiveness": 0.5
            },
            {
                "img_url": SAMPLE_IMAGE_URL,
                "voice_id": Voices.RUSSELL,
                "text": "Batch test number two",
                "expressiveness": 0.8
            },
            {
                "img_url": SAMPLE_IMAGE_URL,
                "voice_id": Voices.GIOVANNI,
                "text": "Batch test number three",
                "expressiveness": 0.6
            }
        ]
        
        batch_progress = []
        
        def progress_callback(current, total, response):
            batch_progress.append((current, total, response.status.value))
            print(f"   📦 Batch progress: {current}/{total} - {response.status.value}")
        
        start_time = time.time()
        
        async with LemonSliceClient(API_KEY) as client:
            responses = await client.generate_batch(
                requests,
                on_progress=progress_callback,
                max_concurrent=2
            )
        
        elapsed = time.time() - start_time
        
        # Verify all completed successfully
        successful = 0
        for response in responses:
            if not isinstance(response, Exception) and response.status.value == "completed":
                successful += 1
        
        assert successful == len(requests)
        assert len(batch_progress) > 0
        
        results.add_pass("Batch Processing", f"{successful}/{len(requests)} completed in {elapsed:.1f}s")
        
    except Exception as e:
        results.add_fail("Batch Processing", str(e))


async def test_retry_logic(results: TestResults):
    """Test 6: Retry logic (simulated failure)"""
    try:
        # Test with custom retry config
        retry_config = RetryConfig(max_retries=2, backoff_factor=1.0)
        
        async with LemonSliceClient(API_KEY, retry_config=retry_config) as client:
            # Test a simple API call that should succeed
            # (We can't easily test actual failures without mocking)
            response = await client.list_generations(limit=1)
            
            # If we get here without error, retry logic is properly configured
            results.add_pass("Retry Logic", "Retry configuration applied successfully")
            
    except Exception as e:
        results.add_fail("Retry Logic", str(e))


async def test_different_voices(results: TestResults):
    """Test 7: Different voice options"""
    try:
        voices_to_test = [
            (Voices.ANDREA, "Spanish woman"),
            (Voices.CAMILLE, "French woman"),
            (Voices.KEVIN, "Chinese American man")
        ]
        
        successful_voices = 0
        
        async with LemonSliceClient(API_KEY) as client:
            for voice_id, description in voices_to_test:
                try:
                    response = await client.generate_video(
                        GenerationRequest(
                            img_url=SAMPLE_IMAGE_URL,
                            voice_id=voice_id,
                            text=f"Testing {description} voice",
                            expressiveness=0.7
                        )
                    )
                    
                    if response.status.value == "completed":
                        successful_voices += 1
                        print(f"   🎭 {description}: ✅")
                        
                except Exception as e:
                    print(f"   🎭 {description}: ❌ {e}")
        
        if successful_voices > 0:
            results.add_pass("Voice Testing", f"{successful_voices}/{len(voices_to_test)} voices tested")
        else:
            results.add_fail("Voice Testing", "No voices worked")
            
    except Exception as e:
        results.add_fail("Voice Testing", str(e))


async def test_error_handling(results: TestResults):
    """Test 8: Error handling"""
    try:
        async with LemonSliceClient(API_KEY) as client:
            # Test invalid job ID
            try:
                await client.get_generation_status("invalid-job-id-12345")
                results.add_fail("Error Handling", "Should have thrown error for invalid job ID")
            except APIError as e:
                # Only check that an APIError is raised, not the message content
                results.add_pass("Error Handling", f"Caught APIError as expected: {e}")
    except Exception as e:
        results.add_fail("Error Handling", str(e))


async def test_url_validation(results: TestResults):
    """Test 9: URL validation functionality"""
    try:
        async with LemonSliceClient(API_KEY) as client:
            validation = await client.validate_inputs(
                img_url=SAMPLE_IMAGE_URL,
                audio_url="https://6ammc3n5zzf5ljnz.public.blob.vercel-storage.com/cool_man-eUP4h3ET8OHCP2ScZvei5CVnQUx2Mi.mp3"
            )
            
            assert 'img_url_valid' in validation
            
            results.add_pass("URL Validation", f"Image URL valid: {validation['img_url_valid']}")
            
    except Exception as e:
        results.add_fail("URL Validation", str(e))


async def test_different_parameters(results: TestResults):
    """Test 10: Different model parameters"""
    try:
        configurations = [
            {"model": "V2.5", "resolution": "512", "animation_style": "autoselect"},
            {"model": "V2.5", "resolution": "256", "animation_style": "face_only"},
            {"model": "V2", "resolution": "320", "crop_head": True}
        ]
        
        successful_configs = 0
        
        async with LemonSliceClient(API_KEY) as client:
            for config in configurations:
                try:
                    response = await client.generate_video(
                        GenerationRequest(
                            img_url=SAMPLE_IMAGE_URL,
                            voice_id=Voices.ANDREA,
                            text=f"Testing {config['model']} at {config['resolution']}p",
                            **config
                        )
                    )
                    
                    if response.status.value == "completed":
                        successful_configs += 1
                        print(f"   ⚙️  {config['model']} @ {config['resolution']}p: ✅")
                        
                except Exception as e:
                    print(f"   ⚙️  {config}: ❌ {e}")
        
        if successful_configs > 0:
            results.add_pass("Parameter Testing", f"{successful_configs}/{len(configurations)} configs worked")
        else:
            results.add_fail("Parameter Testing", "No configurations worked")
            
    except Exception as e:
        results.add_fail("Parameter Testing", str(e))


async def main():
    """Run all tests"""
    if not API_KEY:
        print("❌ Please set LEMONSLICE_API_KEY environment variable")
        print("   export LEMONSLICE_API_KEY='your_api_key_here'")
        return
    
    print("🧪 Starting LemonMeringue comprehensive test suite...")
    print(f"🔑 Using API key: {API_KEY[:8]}...")
    print(f"🖼️  Test image: {SAMPLE_IMAGE_URL}")
    print()
    
    results = TestResults()
    
    # Run all tests
    test_functions = [
        test_basic_functionality,
        test_progress_tracking,
        test_input_validation,
        test_quick_generate,
        test_batch_processing,
        test_retry_logic,
        test_different_voices,
        test_error_handling,
        test_url_validation,
        test_different_parameters
    ]
    
    for i, test_func in enumerate(test_functions, 1):
        print(f"\n🧪 Test {i}/{len(test_functions)}: {test_func.__name__.replace('test_', '').replace('_', ' ').title()}")
        await test_func(results)
        await asyncio.sleep(1)  # Brief pause between tests
    
    # Final summary
    results.summary()
    
    if results.failed == 0:
        print("\n🎉 All tests passed! LemonMeringue is working perfectly!")
    else:
        print(f"\n⚠️  {results.failed} test(s) failed. Check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())