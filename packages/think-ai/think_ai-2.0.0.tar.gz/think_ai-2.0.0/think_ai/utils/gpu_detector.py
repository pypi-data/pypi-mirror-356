#!/usr/bin/env python3
"""GPU detection and automatic configuration for Think AI."""

import torch
import platform
from typing import Dict, Any
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


def detect_best_device() -> Dict[str, Any]:
    """Detect the best available device for running models."""
    device_info = {
        "device": "cpu",
        "device_name": "CPU",
        "memory": None,
        "capability": None,
        "recommendations": []
    }
    
    # Check for CUDA (NVIDIA GPU)
    if torch.cuda.is_available():
        device_info["device"] = "cuda"
        device_info["device_name"] = torch.cuda.get_device_name(0)
        device_info["memory"] = f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB"
        device_info["capability"] = f"{torch.cuda.get_device_capability(0)[0]}.{torch.cuda.get_device_capability(0)[1]}"
        
        # Check if it's a good GPU
        memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
        if memory_gb >= 8:
            device_info["recommendations"].append("Excellent GPU! Can run large models fast.")
        elif memory_gb >= 4:
            device_info["recommendations"].append("Good GPU! Suitable for most models.")
        else:
            device_info["recommendations"].append("Limited GPU memory. Consider smaller models.")
            
        logger.info(f"🎮 NVIDIA GPU detected: {device_info['device_name']} ({device_info['memory']})")
        
    # Check for MPS (Apple Silicon)
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        device_info["device"] = "mps"
        device_info["device_name"] = "Apple Silicon GPU"
        
        # Get Mac info
        if platform.system() == "Darwin":
            import subprocess
            try:
                chip_info = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).decode().strip()
                device_info["device_name"] = chip_info
            except:
                pass
                
        device_info["recommendations"].append("Apple Silicon detected. Good for medium-sized models.")
        logger.info(f"🍎 Apple Silicon GPU detected: {device_info['device_name']}")
        
    # Check for ROCm (AMD GPU)
    elif hasattr(torch, 'hip') and torch.hip.is_available():
        device_info["device"] = "cuda"  # ROCm uses CUDA interface
        device_info["device_name"] = "AMD GPU (ROCm)"
        device_info["recommendations"].append("AMD GPU detected. Performance may vary.")
        logger.info("🔴 AMD GPU detected (ROCm)")
        
    else:
        # CPU only
        import psutil
        cpu_count = psutil.cpu_count(logical=True)
        try:
            cpu_freq = psutil.cpu_freq().max / 1000  # GHz
            device_info["device_name"] = f"CPU ({cpu_count} cores @ {cpu_freq:.1f}GHz)"
        except:
            device_info["device_name"] = f"CPU ({cpu_count} cores)"
            
        device_info["recommendations"].append("No GPU detected. Consider using smaller models or cloud GPU.")
        logger.warning("⚠️ No GPU detected - using CPU (will be slow)")
    
    return device_info


def get_optimal_model_config(device_info: Dict[str, Any]) -> Dict[str, Any]:
    """Get optimal model configuration based on device."""
    config = {
        "device": device_info["device"],
        "dtype": "float32",  # Default
        "model_name": "Qwen/Qwen2.5-Coder-1.5B-Instruct",  # Default
        "max_tokens": 5000,  # High token limit for GPUs
        "batch_size": 1,
        "use_flash_attention": False,
        "load_in_8bit": False,
        "load_in_4bit": False
    }
    
    if device_info["device"] == "cuda":
        # NVIDIA GPU optimizations
        memory_gb = float(device_info["memory"].replace(" GB", "")) if device_info["memory"] else 4
        
        if memory_gb >= 16:
            # High-end GPU (RTX 3090, 4090, A100, etc.)
            config["dtype"] = "float16"
            config["batch_size"] = 4
            config["use_flash_attention"] = True
            logger.info("🚀 High-end GPU detected - using optimal settings")
            
        elif memory_gb >= 8:
            # Mid-range GPU (RTX 3070, 3080, etc.)
            config["dtype"] = "float16"
            config["batch_size"] = 2
            config["use_flash_attention"] = True
            logger.info("✅ Good GPU detected - using balanced settings")
            
        elif memory_gb >= 6:
            # Entry-level GPU (RTX 3060, etc.)
            config["dtype"] = "float16"
            config["batch_size"] = 1
            config["load_in_8bit"] = True
            logger.info("💡 Entry GPU detected - using memory-efficient settings")
            
        else:
            # Low memory GPU
            config["dtype"] = "float16"
            config["load_in_4bit"] = True
            config["model_name"] = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Smaller model
            logger.warning("⚠️ Low GPU memory - using smaller model")
            
    elif device_info["device"] == "mps":
        # Apple Silicon optimizations
        config["dtype"] = "float16"
        config["batch_size"] = 1
        # MPS doesn't support all operations, be conservative
        logger.info("🍎 Apple Silicon - using MPS-compatible settings")
        
    else:
        # CPU optimizations
        config["dtype"] = "float32"  # More stable on CPU
        config["batch_size"] = 1
        config["model_name"] = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Smaller for CPU
        logger.info("💻 CPU mode - using smaller model for better performance")
    
    return config


def auto_configure_for_device() -> Dict[str, Any]:
    """Automatically configure Think AI for the best available device."""
    print("\n🔍 Auto-detecting best compute device...")
    
    # Detect device
    device_info = detect_best_device()
    
    # Get optimal config
    config = get_optimal_model_config(device_info)
    
    # Print summary
    print(f"\n✅ Detected: {device_info['device_name']}")
    if device_info['memory']:
        print(f"   Memory: {device_info['memory']}")
    
    print(f"\n🎯 Optimal Configuration:")
    print(f"   Device: {config['device']}")
    print(f"   Model: {config['model_name']}")
    print(f"   Precision: {config['dtype']}")
    print(f"   Batch Size: {config['batch_size']}")
    
    if device_info['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in device_info['recommendations']:
            print(f"   - {rec}")
    
    return config


# Auto-detect on import
if __name__ == "__main__":
    config = auto_configure_for_device()
    print(f"\n📝 Configuration ready!")
    print(json.dumps(config, indent=2))