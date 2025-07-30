# 💾 Installation Guide

## 🌟 **Enterprise Installation for DataLineagePy**

This comprehensive guide covers all installation methods for DataLineagePy, from quick development setup to enterprise production deployments.

> **📅 Last Updated**: June 19, 2025  
> **🔧 Supported Platforms**: Windows, macOS, Linux  
> **🐍 Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12

---

## 📋 **System Requirements**

### **Minimum Requirements**

- **Python**: 3.8+ (3.9+ recommended)
- **Memory**: 512MB RAM
- **Storage**: 100MB free space
- **Operating System**: Windows 10+, macOS 10.14+, Linux (any modern distribution)

### **Recommended for Production**

- **Python**: 3.11+ (optimal performance)
- **Memory**: 2GB+ RAM
- **Storage**: 1GB+ free space
- **CPU**: 2+ cores
- **Network**: Stable internet connection for package downloads

### **Enterprise Production Requirements**

- **Python**: 3.11+
- **Memory**: 4GB+ RAM
- **Storage**: 5GB+ free space
- **CPU**: 4+ cores
- **Network**: High-speed connection
- **Security**: Python virtual environment isolation

---

## 🚀 **Quick Installation (Recommended)**

### **Option 1: PyPI Installation**

```bash
# Basic installation
pip install datalineagepy

# Verify installation
python -c "import datalineagepy; print(f'DataLineagePy v{datalineagepy.__version__} installed successfully!')"
```

### **Option 2: With Optional Dependencies**

```bash
# Installation with visualization support
pip install datalineagepy[viz]

# Installation with all optional features
pip install datalineagepy[all]

# Installation with development tools
pip install datalineagepy[dev]
```

### **Option 3: Latest Development Version**

```bash
# Install latest development version
pip install git+https://github.com/Arbaznazir/DataLineagePy.git

# Or specific branch
pip install git+https://github.com/Arbaznazir/DataLineagePy.git@development
```

---

## 🛠️ **Detailed Installation Methods**

### **Method 1: Virtual Environment Setup (Recommended)**

#### **For Windows:**

```powershell
# Create project directory
mkdir my_datalineage_project
cd my_datalineage_project

# Create virtual environment
python -m venv datalineage_env

# Activate virtual environment
datalineage_env\Scripts\activate

# Install DataLineagePy
pip install datalineagepy

# Verify installation
python -c "import datalineagepy; print('Installation successful!')"
```

#### **For macOS/Linux:**

```bash
# Create project directory
mkdir my_datalineage_project
cd my_datalineage_project

# Create virtual environment
python3 -m venv datalineage_env

# Activate virtual environment
source datalineage_env/bin/activate

# Install DataLineagePy
pip install datalineagepy

# Verify installation
python -c "import datalineagepy; print('Installation successful!')"
```

### **Method 2: Conda Installation**

```bash
# Create conda environment
conda create -n datalineage python=3.11
conda activate datalineage

# Install DataLineagePy via pip (recommended)
pip install datalineagepy

# Or install from conda-forge (coming soon)
# conda install -c conda-forge datalineagepy
```

### **Method 3: Docker Installation**

#### **Quick Docker Run:**

```bash
# Pull official image
docker pull datalineagepy/datalineagepy:latest

# Run interactive session
docker run -it datalineagepy/datalineagepy:latest python

# Run with volume mount for persistence
docker run -it -v $(pwd):/workspace datalineagepy/datalineagepy:latest
```

#### **Custom Dockerfile:**

```dockerfile
# Dockerfile for your project
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install DataLineagePy
RUN pip install datalineagepy

# Copy your application
COPY . .

# Run your application
CMD ["python", "your_lineage_script.py"]
```

### **Method 4: Development Installation**

```bash
# Clone repository
git clone https://github.com/Arbaznazir/DataLineagePy.git
cd DataLineagePy

# Create development environment
python -m venv dev_env
source dev_env/bin/activate  # Windows: dev_env\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[dev]

# Run tests to verify
pytest tests/
```

---

## 🔧 **Configuration & Setup**

### **Basic Configuration**

Create a configuration file `datalineage_config.py`:

```python
# datalineage_config.py
DATALINEAGE_CONFIG = {
    "default_tracker_name": "my_pipeline",
    "enable_performance_monitoring": True,
    "enable_memory_optimization": True,
    "export_format": "json",
    "visualization_backend": "matplotlib",
    "log_level": "INFO"
}
```

### **Environment Variables**

```bash
# Optional environment variables
export DATALINEAGE_DEFAULT_TRACKER="production_pipeline"
export DATALINEAGE_ENABLE_MONITORING="true"
export DATALINEAGE_LOG_LEVEL="INFO"
export DATALINEAGE_EXPORT_PATH="/data/lineage"
```

### **Advanced Configuration**

```python
# advanced_config.py
from datalineagepy import LineageTracker

# Enterprise configuration
tracker = LineageTracker(
    name="enterprise_pipeline",
    config={
        "memory_optimization": True,
        "performance_monitoring": True,
        "enable_validation": True,
        "enable_security": True,
        "audit_trail": True,
        "export_formats": ["json", "csv", "excel"],
        "visualization": {
            "backend": "plotly",
            "interactive": True,
            "theme": "enterprise"
        },
        "monitoring": {
            "enable_alerts": True,
            "memory_threshold_mb": 1000,
            "performance_threshold_ms": 500
        }
    }
)
```

---

## ✅ **Installation Verification**

### **Basic Verification**

```python
# verify_installation.py
import datalineagepy
import pandas as pd

print(f"✅ DataLineagePy Version: {datalineagepy.__version__}")
print("✅ Core imports successful")

# Test basic functionality
from datalineagepy import LineageTracker, LineageDataFrame

# Create test tracker
tracker = LineageTracker(name="test_tracker")
print("✅ LineageTracker created successfully")

# Create test DataFrame
df = pd.DataFrame({'test': [1, 2, 3]})
ldf = LineageDataFrame(df, name="test_data", tracker=tracker)
print("✅ LineageDataFrame created successfully")

# Test basic operation
result = ldf.filter(ldf._df['test'] > 1)
print("✅ Basic operations working")

print("\n🎉 DataLineagePy installation verified successfully!")
```

### **Advanced Verification**

```python
# advanced_verification.py
import datalineagepy
from datalineagepy import LineageTracker, LineageDataFrame
from datalineagepy.core.analytics import DataProfiler
from datalineagepy.core.validation import DataValidator
from datalineagepy.visualization import GraphVisualizer
import pandas as pd

print("🔍 Running comprehensive verification...")

# Test core functionality
tracker = LineageTracker(name="verification_test")
df = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'value': [10, 20, 30, 40, 50],
    'category': ['A', 'B', 'A', 'B', 'A']
})
ldf = LineageDataFrame(df, name="test_data", tracker=tracker)

# Test operations
filtered = ldf.filter(ldf._df['value'] > 25)
grouped = filtered.groupby('category').agg({'value': 'sum'})
print("✅ Data operations working")

# Test analytics
profiler = DataProfiler()
profile = profiler.profile_dataset(ldf)
print(f"✅ Data profiling working - Quality score: {profile.get('quality_score', 'N/A')}")

# Test validation
validator = DataValidator()
rules = {'completeness': {'threshold': 0.8}}
validation_result = validator.validate_dataframe(ldf, rules)
print("✅ Data validation working")

# Test visualization
try:
    visualizer = GraphVisualizer(tracker)
    print("✅ Visualization module loaded")
except ImportError as e:
    print(f"⚠️  Visualization dependencies missing: {e}")
    print("   Install with: pip install datalineagepy[viz]")

# Test export
lineage_data = tracker.export_lineage()
print("✅ Lineage export working")

print("\n🎉 All advanced features verified successfully!")
```

### **Performance Verification**

```python
# performance_verification.py
import time
import psutil
import pandas as pd
from datalineagepy import LineageTracker, LineageDataFrame

print("⚡ Running performance verification...")

# Create large test dataset
size = 10000
df = pd.DataFrame({
    'id': range(size),
    'value': range(size),
    'category': ['A', 'B', 'C'] * (size // 3 + 1)
})

# Measure performance
start_time = time.time()
start_memory = psutil.Process().memory_info().rss / 1024 / 1024

tracker = LineageTracker(name="performance_test")
ldf = LineageDataFrame(df, name="large_data", tracker=tracker)

# Perform operations
filtered = ldf.filter(ldf._df['value'] > size//2)
grouped = filtered.groupby('category').agg({'value': ['sum', 'mean', 'count']})

end_time = time.time()
end_memory = psutil.Process().memory_info().rss / 1024 / 1024

execution_time = end_time - start_time
memory_used = end_memory - start_memory

print(f"✅ Performance test completed:")
print(f"   📊 Dataset size: {size:,} rows")
print(f"   ⏱️  Execution time: {execution_time:.3f} seconds")
print(f"   💾 Memory used: {memory_used:.1f} MB")
print(f"   📈 Lineage nodes created: {len(tracker.nodes)}")

# Performance thresholds
if execution_time < 1.0:
    print("✅ Performance: Excellent")
elif execution_time < 5.0:
    print("✅ Performance: Good")
else:
    print("⚠️  Performance: Consider optimization")

print("\n🎉 Performance verification completed!")
```

---

## 🐳 **Container Deployment**

### **Docker Compose Setup**

```yaml
# docker-compose.yml
version: "3.8"

services:
  datalineage:
    image: datalineagepy/datalineagepy:latest
    container_name: datalineage_app
    volumes:
      - ./data:/app/data
      - ./output:/app/output
    environment:
      - DATALINEAGE_DEFAULT_TRACKER=production_pipeline
      - DATALINEAGE_ENABLE_MONITORING=true
    command: python your_pipeline.py

  jupyter:
    image: jupyter/datascience-notebook
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
    environment:
      - JUPYTER_TOKEN=your_token_here
    command: start-notebook.sh --NotebookApp.token='your_token_here'
```

### **Kubernetes Deployment**

```yaml
# kubernetes-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: datalineage-deployment
  labels:
    app: datalineage
spec:
  replicas: 3
  selector:
    matchLabels:
      app: datalineage
  template:
    metadata:
      labels:
        app: datalineage
    spec:
      containers:
        - name: datalineage
          image: datalineagepy/datalineagepy:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATALINEAGE_ENV
              value: "production"
            - name: DATALINEAGE_ENABLE_MONITORING
              value: "true"
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
          volumeMounts:
            - name: data-volume
              mountPath: /app/data
      volumes:
        - name: data-volume
          persistentVolumeClaim:
            claimName: datalineage-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: datalineage-service
spec:
  selector:
    app: datalineage
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

---

## 🔧 **Troubleshooting Installation Issues**

### **Common Issues & Solutions**

#### **Issue 1: Python Version Compatibility**

```bash
# Error: "DataLineagePy requires Python 3.8+"
# Solution: Check Python version
python --version

# If Python 3.8+ not available, install it:
# Windows: Download from python.org
# macOS: brew install python@3.11
# Ubuntu: apt-get install python3.11
```

#### **Issue 2: Permission Errors**

```bash
# Error: "Permission denied" during pip install
# Solution: Use user installation
pip install --user datalineagepy

# Or use virtual environment (recommended)
python -m venv env && source env/bin/activate
```

#### **Issue 3: Missing Dependencies**

```bash
# Error: "No module named 'pandas'"
# Solution: Install dependencies explicitly
pip install pandas numpy matplotlib
pip install datalineagepy
```

#### **Issue 4: Import Errors**

```python
# Error: "ImportError: cannot import name 'LineageTracker'"
# Solution: Check installation
import sys
print(sys.path)

# Reinstall if necessary
pip uninstall datalineagepy -y
pip install datalineagepy
```

#### **Issue 5: Memory Issues**

```python
# Error: "MemoryError" with large datasets
# Solution: Enable memory optimization
from datalineagepy import LineageTracker

tracker = LineageTracker(
    name="memory_optimized",
    config={"memory_optimization": True}
)
```

### **Advanced Troubleshooting**

#### **Debug Installation**

```bash
# Create debug environment
python -m venv debug_env
source debug_env/bin/activate  # Windows: debug_env\Scripts\activate

# Install with verbose output
pip install -v datalineagepy

# Check package info
pip show datalineagepy
pip list | grep datalineage
```

#### **System Information Collection**

```python
# system_info.py
import sys
import platform
import pandas as pd
import numpy as np

print("🔍 System Information:")
print(f"Python Version: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Architecture: {platform.architecture()}")
print(f"Pandas Version: {pd.__version__}")
print(f"NumPy Version: {np.__version__}")

try:
    import datalineagepy
    print(f"DataLineagePy Version: {datalineagepy.__version__}")
    print("✅ DataLineagePy imported successfully")
except ImportError as e:
    print(f"❌ DataLineagePy import failed: {e}")
```

---

## 📚 **Next Steps**

After successful installation:

1. **📖 [Quick Start Guide](quickstart.md)** - Get started in 30 seconds
2. **🛠️ [API Reference](api/)** - Explore all available methods
3. **📊 [Examples](examples/)** - See practical usage examples
4. **🏢 [Production Deployment](advanced/production.md)** - Enterprise setup

---

## 🆘 **Getting Help**

If you encounter issues:

- **📚 [FAQ](faq.md)** - Check frequently asked questions
- **🐛 [GitHub Issues](https://github.com/Arbaznazir/DataLineagePy/issues)** - Report bugs
- **💬 [Discussions](https://github.com/Arbaznazir/DataLineagePy/discussions)** - Community support
- **📧 [Enterprise Support](mailto:enterprise@datalineagepy.com)** - Priority support

---

_Installation guide last updated: June 19, 2025_
