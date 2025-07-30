# 🍋 LemonMeringue

> **v0.1.2** — **Upcoming in a future LemonMeringue release:** Support for Instagram!

A fluffy layer of reliability and ease-of-use on top of the LemonSlice API

Enhanced Python SDK for the [LemonSlice API](https://lemonslice.com) with automatic retry logic, progress tracking, better error handling, and batch processing.

[![PyPI version](https://badge.fury.io/py/lemonmeringue.svg)](https://badge.fury.io/py/lemonmeringue)
[![Python Support](https://img.shields.io/pypi/pyversions/lemonmeringue.svg)](https://pypi.org/project/lemonmeringue/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📚 Table of Contents

- [Why LemonMeringue?](#-why-lemonmeringue)
- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Quick Generate](#quick-generate-one-liner)
- [Testing Guide](#-testing-guide)
- [Advanced Usage](#-advanced-usage)
  - [Batch Processing](#batch-processing)
  - [Custom Retry Configuration](#custom-retry-configuration)
  - [Input Validation](#input-validation)
- [Available Voices](#-available-voices)
- [Configuration Options](#️-configuration-options)
  - [Generation Parameters](#generation-parameters)
  - [Client Configuration](#client-configuration)
- [Error Handling](#-error-handling)

## 🎯 Why LemonMeringue?

**Before (Raw LemonSlice API):**

```python
# 20+ lines of boilerplate code
import requests
import time

response = requests.post("https://lemonslice.com/api/v2/generate",
    headers={"Authorization": "Bearer your_key"},
    json={"img_url": "...", "voice_id": "...", "text": "..."}
)

job_id = response.json()["job_id"]

# Manual polling loop
while True:
    status = requests.get(f"https://lemonslice.com/api/v2/generations/{job_id}")
    if status.json()["status"] == "completed":
        break
    time.sleep(5)  # Hope nothing goes wrong!

# Manual error handling, no retries, no progress tracking...
```

**After (LemonMeringue):**

````python
# 3 lines of code - everything handled automatically
from lemonmeringue import LemonSliceClient, Voices

async def main():
    async with LemonSliceClient(api_key) as client:
        result = await client.quick_generate_text(
            img_url=img_url,
            voice_id=Voices.ANDREA,
            text="Hello world!"
        )
        print(f"✅ Video ready: {result.video_url}")

# ... existing code ...
### 🚀 **Convenience Functions**

- **Problem**: Setting up clients and making requests is verbose
- **Solution**: `client.quick_generate_text()` and `client.quick_generate_audio()` for simple use cases, context managers for complex ones

## ✨ Key Features

### 🔄 **Automatic Retry Logic**

- **Problem**: LemonSlice API sometimes has temporary issues (500 errors, rate limits)
- **Solution**: Exponential backoff retries with configurable settings

### 📊 **Progress Tracking**

- **Problem**: Users don't know how long generation takes or current status
- **Solution**: Real-time progress callbacks with status updates

### ✅ **Input Validation**

- **Problem**: Invalid parameters cause confusing API errors
- **Solution**: Pre-validation with clear error messages before API calls

### 📦 **Batch Processing**

- **Problem**: Generating 10 videos = 10 separate API calls + manual management
- **Solution**: Concurrent batch processing with automatic queue management

### 🚀 **Convenience Functions**

- **Problem**: Setting up clients and making requests is verbose
- **Solution**: `client.quick_generate_text()` and `client.quick_generate_audio()` for simple use cases, context managers for complex ones

### 🎯 **Type Hints & IDE Support**

- **Problem**: Users don't know what parameters are available
- **Solution**: Full type hints for auto-completion and error detection

## 🚀 Quick Start

### Installation

```bash
pip install lemonmeringue
````

### Basic Usage

```python
import asyncio
from lemonmeringue import LemonSliceClient, GenerationRequest, Voices

async def main():
    async with LemonSliceClient("your_api_key") as client:
        # Generate a video with progress tracking
        response = await client.generate_video(
            GenerationRequest(
                img_url="https://example.com/image.jpg",
                voice_id=Voices.ANDREA,
                text="Hello, this is a test!",
                expressiveness=0.8
            ),
            on_progress=lambda r: print(f"Status: {r.status.value}")
        )

        print(f"✅ Video generated: {response.video_url}")
        print(f"⏱️  Processing time: {response.processing_time:.1f}s")

asyncio.run(main())
```

### Quick Generate (One-liner)

```python
import asyncio
from lemonmeringue import LemonSliceClient, Voices

async def main():
    async with LemonSliceClient("your_api_key") as client:
        # Quick generate from text and voice
        result = await client.quick_generate_text(
            img_url="https://example.com/image.jpg",
            voice_id=Voices.ANDREA,
            text="Hello world!"
        )
        print(f"Video (text+voice): {result.video_url}")

        # Quick generate from audio file
        result2 = await client.quick_generate_audio(
            img_url="https://example.com/image.jpg",
            audio_url="https://example.com/audio.mp3"
        )
        print(f"Video (audio): {result2.video_url}")

asyncio.run(main())
```

## 🧪 Testing Guide

> **Note**: As of June 19, 2025, running the complete test suite costs approximately $0.60 in LemonSlice API credits.

### 1. Set Up Your Environment

```bash
# In your lemonmeringue repo directory
export LEMONSLICE_API_KEY="your_actual_api_key_here"
```

### 2. Run All Tests

```bash
python setup_and_test.py
```

### 3. Run Comprehensive Feature Tests

```bash
python test_all_features.py
```

### 4. Quick Test Only

```bash
python setup_and_test.py test-only
```

---

### What Gets Tested

- ✅ Basic Functionality (video generation)
- ✅ Progress Tracking (real-time status)
- ✅ Input Validation (invalid parameters)
- ✅ Quick Generate (convenience function)
- ✅ Batch Processing (multiple videos)
- ✅ Retry Logic (error handling)
- ✅ Different Voices (voice options)
- ✅ Error Handling (exceptions)
- ✅ URL Validation (input checking)
- ✅ Parameter Testing (models/resolutions)

---

### Example Output

```bash
🧪 Starting LemonMeringue comprehensive test suite...
🔑 Using API key: sk_1234...
🖼️  Test image: https://6ammc3n5zzf5ljnz...

🧪 Test 1/10: Basic Functionality
✅ Basic Functionality: Generated in 45.2s

🧪 Test 2/10: Progress Tracking
   📊 Progress update: processing
   📊 Progress update: completed
✅ Progress Tracking: 2 status updates received

...

📊 Test Summary: 10/10 passed
🎉 All tests passed! LemonMeringue is working perfectly!
```

---

**Ready to Test?**  
Just set your API key and run `python setup_and_test.py` to verify all features with the real LemonSlice API. No file uploads needed—public image URLs are used.

## 🔧 Advanced Usage

### Batch Processing

Generate multiple videos concurrently:

```python
requests = [
    {"img_url": "img1.jpg", "voice_id": Voices.ANDREA, "text": "First video"},
    {"img_url": "img2.jpg", "voice_id": Voices.RUSSO, "text": "Second video"},
    {"img_url": "img3.jpg", "voice_id": Voices.EMMA, "text": "Third video"},
]

responses = await client.generate_batch(
    requests,
    on_progress=lambda i, total, response: print(f"Video {i}/{total}: {response.status.value}"),
    max_concurrent=3
)

for i, response in enumerate(responses):
    if isinstance(response, Exception):
        print(f"❌ Video {i+1} failed: {response}")
    else:
        print(f"✅ Video {i+1}: {response.video_url}")
```

### Custom Retry Configuration

```python
from lemonmeringue import RetryConfig

retry_config = RetryConfig(
    max_retries=5,
    backoff_factor=1.5,
    max_backoff=120.0
)

client = LemonSliceClient(
    api_key="your_api_key",
    retry_config=retry_config,
    enable_logging=True
)
```

### Input Validation

```python
# Validate URLs before generation
validation = await client.validate_inputs(
    img_url="https://example.com/image.jpg",
    audio_url="https://example.com/audio.mp3"
)

if validation['img_url_valid'] and validation.get('audio_url_valid', True):
    # Proceed with generation
    pass
else:
    print("❌ Invalid input URLs")
```

## 🎭 Available Voices

```python
from lemonmeringue import Voices

# Popular voices
Voices.ANDREA    # Young woman, Spanish, calm, soft
Voices.RUSSO     # Middle-aged man, Australian, narrator
Voices.EMMA      # Young woman, German
Voices.GIOVANNI  # Young man, Italian, deep
Voices.RUSSELL   # Middle-aged man, British, dramatic

# Use in requests
request = GenerationRequest(
    img_url="image.jpg",
    voice_id=Voices.ANDREA,
    text="Your text here"
)
```

## 🛠️ Configuration Options

### Generation Parameters

```python
request = GenerationRequest(
    img_url="https://example.com/image.jpg",
    audio_url="https://example.com/audio.mp3",  # Optional
    voice_id=Voices.ANDREA,                     # For TTS
    text="Text to speak",                       # For TTS
    model="V2.5",                              # V2 or V2.5
    resolution="512",                          # 320, 512, or 640
    crop_head=False,                           # Focus on head region
    animation_style="autoselect",              # autoselect, face_only, entire_image
    expressiveness=1.0,                        # 0.0 to 1.0
)
```

### Client Configuration

```python
client = LemonSliceClient(
    api_key="your_api_key",
    timeout=60,                    # Request timeout in seconds
    enable_logging=True,           # Enable debug logging
    retry_config=RetryConfig(...)  # Custom retry behavior
)
```

## 🔍 Error Handling

```python
from lemonmeringue import APIError, ValidationError

try:
    response = await client.generate_video(request)
except ValidationError as e:
    print(f"❌ Invalid input: {e}")
except APIError as e:
    print(f"❌ API error ({e.status_code}): {e}")
    if e.response:
        print(f"Response details: {e.response}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

## 📊 Response Information

```python
response = await client.generate_video(request)

print(f"Job ID: {response.job_id}")
print(f"Status: {response.status.value}")
print(f"Video URL: {response.video_url}")
print(f"Processing time: {response.processing_time:.1f}s")
print(f"Created at: {response.created_at}")
```

## 🔗 API Compatibility

This SDK wraps the [LemonSlice API v2](https://lemonslice.com/developer). You'll need a LemonSlice API key to use this package.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Links

- **PyPI**: https://pypi.org/project/lemonmeringue/
- **GitHub**: https://github.com/neeldatta/lemonmeringue
- **LemonSlice API**: https://lemonslice.com/developer

---

Made with 🍋 by Neel Datta
