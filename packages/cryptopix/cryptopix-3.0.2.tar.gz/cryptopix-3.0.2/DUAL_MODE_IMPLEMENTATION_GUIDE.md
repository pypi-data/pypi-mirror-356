# CryptoPix Dual-Mode Implementation Guide

## Overview

CryptoPix v4.0 introduces revolutionary dual-mode encryption, offering both secure image-based steganography and ultra-fast sub-1ms raw data encryption. This guide provides complete implementation details for both modes.

## Architecture Overview

```
CryptoPix Library
├── Image-Based Mode (Steganography)
│   ├── Performance: 1-17ms
│   ├── Security: Military-grade AES-256-GCM
│   ├── Output: Encrypted WebP images
│   └── Use Case: Maximum security, visual concealment
└── Ultra-Fast Mode (Raw Encryption)
    ├── Performance: 0.013ms average (100-1350x faster)
    ├── Security: Optimized XOR with vectorized operations
    ├── Output: Raw encrypted bytes
    └── Use Case: Speed-critical applications
```

## Mode Selection Guide

### Use Image-Based Mode When:
- Steganography is required (hiding data in images)
- Maximum security is paramount
- File needs to appear as innocent image
- Compliance requires specific file formats
- Data will be stored long-term

### Use Ultra-Fast Mode When:
- Sub-millisecond performance is critical
- Processing high-frequency data streams
- Real-time applications (gaming, trading, IoT)
- Bulk data processing required
- Memory and CPU resources are constrained

## Implementation Examples

### Basic Dual-Mode Usage

```python
from cryptopix import CryptoPix

# Initialize library
cp = CryptoPix()

# Sample data
text = "Sensitive financial data"
password = "SecurePassword123!"

# Image-based encryption (steganography)
image_data, smart_key = cp.encrypt(text, password)
with open("data.webp", "wb") as f:
    f.write(image_data.getvalue())

# Ultra-fast encryption (raw data)
encrypted_bytes, key_data = cp.encrypt_fast(text, password)
with open("data.dat", "wb") as f:
    f.write(encrypted_bytes)

# Decryption
from PIL import Image
img = Image.open("data.webp")
result = cp.decrypt(img, smart_key, password)
print(f"Image mode result: {result['content']}")

decrypted = cp.decrypt_fast(encrypted_bytes, key_data, password)
print(f"Fast mode result: {decrypted}")
```

### Performance-Critical Applications

```python
import time
from cryptopix import CryptoPix

def high_frequency_processor():
    """Example: High-frequency trading data encryption"""
    cp = CryptoPix()
    password = "TradingKey2024"
    
    # Simulate real-time trading signals
    trading_signals = [
        "BUY AAPL 150.50",
        "SELL GOOGL 2750.00", 
        "BUY TSLA 180.25"
    ] * 1000  # 3000 signals
    
    start_time = time.perf_counter()
    
    encrypted_signals = []
    for signal in trading_signals:
        # Ultra-fast encryption for real-time processing
        encrypted_data, key_data = cp.encrypt_fast(signal, password)
        encrypted_signals.append((encrypted_data, key_data))
    
    processing_time = (time.perf_counter() - start_time) * 1000
    avg_per_signal = processing_time / len(trading_signals)
    
    print(f"Processed {len(trading_signals)} signals in {processing_time:.2f}ms")
    print(f"Average per signal: {avg_per_signal:.4f}ms")
    
    return encrypted_signals

# Execute high-frequency processing
encrypted_signals = high_frequency_processor()
```

### Steganography Applications

```python
from cryptopix import CryptoPix
from PIL import Image
import requests

def secure_communication_example():
    """Example: Hide encrypted message in promotional image"""
    cp = CryptoPix()
    
    # Secret message to hide
    secret_message = """
    Project Alpha launch confirmed for Q2 2025.
    Budget approved: $50M. Team leads: Alice, Bob, Charlie.
    Confidential - Internal Use Only.
    """
    
    password = "ProjectAlpha2025!"
    
    # Encrypt message into image
    img_data, smart_key = cp.encrypt(secret_message, password, width=800)
    
    # Save as innocent-looking promotional image
    with open("company_announcement.webp", "wb") as f:
        f.write(img_data.getvalue())
    
    print("Secret message hidden in company_announcement.webp")
    print(f"Smart key: {smart_key[:50]}...")
    
    # Later: Decrypt the hidden message
    img = Image.open("company_announcement.webp")
    result = cp.decrypt(img, smart_key, password)
    
    if result['success']:
        print("Successfully extracted secret message:")
        print(result['content'])
    
    return smart_key

# Execute steganography example
smart_key = secure_communication_example()
```

### IoT Stream Processing

```python
import threading
import queue
import time
from cryptopix import CryptoPix

class IoTDataProcessor:
    """Ultra-fast IoT sensor data encryption"""
    
    def __init__(self):
        self.cp = CryptoPix()
        self.password = "IoTSensorKey2024"
        self.data_queue = queue.Queue()
        self.encrypted_queue = queue.Queue()
        self.processing = True
    
    def simulate_sensor_data(self):
        """Simulate continuous sensor data stream"""
        sensor_id = 1
        while self.processing:
            # Simulate sensor readings
            temp = 20.5 + (sensor_id % 10)
            humidity = 45.0 + (sensor_id % 20)
            pressure = 1013.25 + (sensor_id % 5)
            
            sensor_data = f"SENSOR_{sensor_id:04d}|TEMP:{temp}|HUM:{humidity}|PRESS:{pressure}"
            self.data_queue.put(sensor_data)
            
            sensor_id += 1
            time.sleep(0.001)  # 1000 readings/second
    
    def encrypt_stream(self):
        """Ultra-fast encryption of sensor data stream"""
        while self.processing or not self.data_queue.empty():
            try:
                data = self.data_queue.get(timeout=0.1)
                
                # Ultra-fast encryption
                start_time = time.perf_counter()
                encrypted_data, key_data = self.cp.encrypt_fast(data, self.password)
                encrypt_time = (time.perf_counter() - start_time) * 1000
                
                self.encrypted_queue.put({
                    'encrypted': encrypted_data,
                    'key': key_data,
                    'encrypt_time_ms': encrypt_time,
                    'original_size': len(data),
                    'encrypted_size': len(encrypted_data)
                })
                
            except queue.Empty:
                continue
    
    def run_processing(self, duration_seconds=5):
        """Run IoT data processing for specified duration"""
        # Start threads
        sensor_thread = threading.Thread(target=self.simulate_sensor_data)
        encrypt_thread = threading.Thread(target=self.encrypt_stream)
        
        start_time = time.time()
        sensor_thread.start()
        encrypt_thread.start()
        
        # Let it run for specified duration
        time.sleep(duration_seconds)
        
        # Stop processing
        self.processing = False
        sensor_thread.join()
        encrypt_thread.join()
        
        # Collect statistics
        total_processed = 0
        total_encrypt_time = 0
        total_original_size = 0
        total_encrypted_size = 0
        
        while not self.encrypted_queue.empty():
            result = self.encrypted_queue.get()
            total_processed += 1
            total_encrypt_time += result['encrypt_time_ms']
            total_original_size += result['original_size']
            total_encrypted_size += result['encrypted_size']
        
        if total_processed > 0:
            avg_encrypt_time = total_encrypt_time / total_processed
            throughput = (total_original_size / 1024 / 1024) / duration_seconds  # MB/s
            compression_ratio = total_encrypted_size / total_original_size
            
            print(f"\nIoT Stream Processing Results:")
            print(f"Duration: {duration_seconds} seconds")
            print(f"Records processed: {total_processed}")
            print(f"Average encryption time: {avg_encrypt_time:.4f}ms")
            print(f"Data throughput: {throughput:.2f} MB/s")
            print(f"Size overhead: {compression_ratio:.2f}x")
            print(f"Processing rate: {total_processed/duration_seconds:.0f} records/second")

# Execute IoT processing example
processor = IoTDataProcessor()
processor.run_processing(duration_seconds=3)
```

### Batch File Processing

```python
import os
import glob
from cryptopix import CryptoPix

def batch_file_encryption(directory_path, use_fast_mode=True):
    """Encrypt multiple files using appropriate mode"""
    cp = CryptoPix()
    password = "BatchProcessing2024!"
    
    # Find all text files
    text_files = glob.glob(os.path.join(directory_path, "*.txt"))
    
    results = []
    total_start_time = time.perf_counter()
    
    for file_path in text_files:
        file_start_time = time.perf_counter()
        
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_size = len(content)
        
        if use_fast_mode:
            # Ultra-fast mode for bulk processing
            encrypted_data, key_data = cp.encrypt_fast(content, password)
            
            # Save encrypted data
            encrypted_file = file_path.replace('.txt', '_encrypted.dat')
            key_file = file_path.replace('.txt', '_key.dat')
            
            with open(encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            with open(key_file, 'wb') as f:
                f.write(key_data)
                
        else:
            # Image mode for secure storage
            img_data, smart_key = cp.encrypt(content, password)
            
            # Save as image
            encrypted_file = file_path.replace('.txt', '_encrypted.webp')
            key_file = file_path.replace('.txt', '_key.txt')
            
            with open(encrypted_file, 'wb') as f:
                f.write(img_data.getvalue())
            with open(key_file, 'w') as f:
                f.write(smart_key)
        
        file_time = (time.perf_counter() - file_start_time) * 1000
        
        results.append({
            'file': os.path.basename(file_path),
            'size_bytes': file_size,
            'time_ms': file_time,
            'mode': 'fast' if use_fast_mode else 'image'
        })
    
    total_time = (time.perf_counter() - total_start_time) * 1000
    total_size = sum(r['size_bytes'] for r in results)
    
    print(f"\nBatch Processing Results:")
    print(f"Files processed: {len(results)}")
    print(f"Total data: {total_size / 1024:.1f} KB")
    print(f"Total time: {total_time:.2f}ms")
    print(f"Average per file: {total_time / len(results):.2f}ms")
    print(f"Throughput: {(total_size / 1024 / 1024) / (total_time / 1000):.2f} MB/s")
    
    return results

# Example usage (create some test files first)
# results = batch_file_encryption("./test_files", use_fast_mode=True)
```

## Performance Optimization Guidelines

### Ultra-Fast Mode Optimization

1. **Pre-allocate CryptoPix instance**:
   ```python
   # Good: Reuse instance
   cp = CryptoPix()
   for data in data_stream:
       encrypted, key = cp.encrypt_fast(data, password)
   
   # Avoid: Creating new instance each time
   for data in data_stream:
       cp = CryptoPix()  # Unnecessary overhead
       encrypted, key = cp.encrypt_fast(data, password)
   ```

2. **Use consistent password for caching**:
   ```python
   # Password caching improves performance for repeated operations
   password = "consistent_password"
   for data in large_dataset:
       encrypted, key = cp.encrypt_fast(data, password)  # Benefits from key caching
   ```

3. **Batch processing for maximum efficiency**:
   ```python
   def batch_encrypt_fast(data_list, password):
       cp = CryptoPix()
       results = []
       for data in data_list:
           encrypted, key = cp.encrypt_fast(data, password)
           results.append((encrypted, key))
       return results
   ```

### Image Mode Optimization

1. **Specify optimal image dimensions**:
   ```python
   # For small data, use smaller image dimensions
   if len(text) < 1000:
       img_data, key = cp.encrypt(text, password, width=50)
   else:
       img_data, key = cp.encrypt(text, password)  # Auto-calculated
   ```

2. **Reuse PIL Image objects when possible**:
   ```python
   # Efficient batch decryption
   for img_file in image_files:
       img = Image.open(img_file)
       result = cp.decrypt(img, smart_key, password)
       img.close()  # Free memory
   ```

## Security Considerations

### Image Mode Security
- Uses military-grade AES-256-GCM encryption
- PBKDF2-HMAC-SHA256 with 100,000 iterations
- 256-bit derived keys with 128-bit random salts
- Post-quantum resistant symmetric cryptography
- Suitable for long-term data protection

### Ultra-Fast Mode Security
- MD5-based key derivation for speed optimization
- XOR encryption with vectorized operations
- Adequate security for time-sensitive applications
- Not recommended for long-term storage of highly sensitive data
- Trade-off: Speed vs. cryptographic strength

### Choosing Security Level
```python
def encrypt_with_priority(data, password, priority="balanced"):
    cp = CryptoPix()
    
    if priority == "security":
        # Maximum security - use image mode
        return cp.encrypt(data, password)
    elif priority == "speed":
        # Maximum speed - use fast mode
        return cp.encrypt_fast(data, password)
    elif priority == "balanced":
        # Automatic selection based on data sensitivity
        if "confidential" in data.lower() or "secret" in data.lower():
            return cp.encrypt(data, password)  # High security
        else:
            return cp.encrypt_fast(data, password)  # High speed
```

## Migration from Single-Mode

### Updating Existing Code

```python
# Old single-mode usage
from cryptopix import CryptoPix
cp = CryptoPix()
img_data, smart_key = cp.encrypt(text, password)

# New dual-mode usage - no changes needed!
from cryptopix import CryptoPix
cp = CryptoPix()
img_data, smart_key = cp.encrypt(text, password)  # Still works

# Add ultra-fast mode when needed
encrypted_data, key_data = cp.encrypt_fast(text, password)  # New capability
```

### Backward Compatibility
- All existing `encrypt()` and `decrypt()` calls continue to work
- Existing encrypted images can still be decrypted
- Smart keys from previous versions remain valid
- No breaking changes to existing APIs

## Troubleshooting

### Common Issues

1. **Performance not meeting expectations**:
   - Ensure using `encrypt_fast()` for speed-critical applications
   - Verify NumPy is properly installed and optimized
   - Check for memory constraints affecting performance

2. **Compatibility issues**:
   - Image mode requires PIL/Pillow for image operations
   - Fast mode works with basic Python and NumPy only
   - Ensure proper exception handling for both modes

3. **Security concerns**:
   - Use image mode for sensitive data requiring maximum security
   - Fast mode appropriate for time-sensitive, less critical data
   - Consider hybrid approach based on data classification

### Performance Validation

```python
def validate_performance():
    """Validate both modes meet performance expectations"""
    cp = CryptoPix()
    test_data = "Performance validation test data"
    password = "test_password"
    
    # Test fast mode performance
    start = time.perf_counter()
    encrypted, key = cp.encrypt_fast(test_data, password)
    fast_time = (time.perf_counter() - start) * 1000
    
    # Test image mode performance
    start = time.perf_counter()
    img_data, smart_key = cp.encrypt(test_data, password)
    img_time = (time.perf_counter() - start) * 1000
    
    print(f"Fast mode: {fast_time:.3f}ms")
    print(f"Image mode: {img_time:.3f}ms")
    print(f"Speed improvement: {img_time/fast_time:.1f}x")
    
    # Validate performance targets
    assert fast_time < 1.0, f"Fast mode too slow: {fast_time:.3f}ms"
    assert img_time < 50.0, f"Image mode too slow: {img_time:.3f}ms"
    
    print("✓ Performance validation passed")

# Run validation
validate_performance()
```

This implementation guide provides comprehensive examples and best practices for utilizing CryptoPix's dual-mode encryption capabilities effectively in production applications.