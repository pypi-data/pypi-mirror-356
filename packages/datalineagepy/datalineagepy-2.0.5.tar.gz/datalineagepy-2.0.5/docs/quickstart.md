# 🚀 Quick Start Guide

## 🌟 **Get Started with DataLineagePy in 30 Seconds**

Welcome to DataLineagePy! This guide will get you from zero to tracking complete data lineage in under 30 seconds.

> **📅 Last Updated**: June 19, 2025  
> **⏱️ Time to Complete**: 30 seconds to 5 minutes  
> **🎯 Learning Path**: Beginner → Intermediate → Advanced

---

## 🎯 **30-Second Quick Start**

### **Step 1: Install (5 seconds)**

```bash
pip install datalineagepy
```

### **Step 2: Basic Usage (25 seconds)**

```python
from datalineagepy import LineageTracker, LineageDataFrame
import pandas as pd

# 1. Create tracker (1 line)
tracker = LineageTracker(name="my_first_pipeline")

# 2. Create your data (3 lines)
df = pd.DataFrame({
    'product_id': [1, 2, 3, 4, 5],
    'sales': [100, 200, 300, 400, 500],
    'region': ['North', 'South', 'East', 'West', 'Central']
})

# 3. Wrap DataFrame for lineage tracking (1 line)
ldf = LineageDataFrame(df, name="sales_data", tracker=tracker)

# 4. Perform operations - lineage tracked automatically! (2 lines)
high_sales = ldf.filter(ldf._df['sales'] > 250)
summary = high_sales.groupby('region').agg({'sales': 'sum'})

# 5. View results (1 line)
print(f"✅ Created {len(tracker.nodes)} lineage nodes automatically!")
```

**🎉 Congratulations! You just tracked complete data lineage with zero configuration!**

---

## 📚 **5-Minute Deep Dive**

### **Understanding the Core Concepts**

#### **1. LineageTracker - The Control Center**

```python
from datalineagepy import LineageTracker

# Basic tracker
tracker = LineageTracker(name="my_pipeline")

# Enterprise tracker with full configuration
enterprise_tracker = LineageTracker(
    name="enterprise_pipeline",
    config={
        "memory_optimization": True,
        "performance_monitoring": True,
        "enable_validation": True,
        "export_format": "json"
    }
)
```

#### **2. LineageDataFrame - Smart Data Wrapper**

```python
from datalineagepy import LineageDataFrame
import pandas as pd

# Any pandas DataFrame works
df = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'order_value': [100, 250, 175, 320, 450],
    'product_category': ['Electronics', 'Books', 'Clothing', 'Electronics', 'Books']
})

# Wrap it for automatic lineage tracking
ldf = LineageDataFrame(df, name="customer_orders", tracker=tracker)

# Now every operation is tracked automatically!
print(f"📊 Tracking DataFrame with {len(ldf._df)} rows and {len(ldf._df.columns)} columns")
```

#### **3. Automatic Operation Tracking**

```python
# All these operations create lineage nodes automatically:

# Filtering
high_value_orders = ldf.filter(ldf._df['order_value'] > 200)
electronics_orders = high_value_orders.filter(ldf._df['product_category'] == 'Electronics')

# Grouping and aggregation
category_summary = electronics_orders.groupby('product_category').agg({
    'order_value': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
})

# Sorting
top_categories = category_summary.sort_values(('order_value', 'sum'), ascending=False)

print(f"🔗 Created {len(tracker.nodes)} lineage nodes")
print(f"📈 Tracked {len(tracker.edges)} data transformations")
```

---

## 🛠️ **Practical Examples**

### **Example 1: E-commerce Analytics Pipeline**

```python
from datalineagepy import LineageTracker, LineageDataFrame
import pandas as pd

# Initialize enterprise tracker
tracker = LineageTracker(
    name="ecommerce_analytics",
    config={"performance_monitoring": True}
)

# Load sample e-commerce data
orders_df = pd.DataFrame({
    'order_id': range(1, 1001),
    'customer_id': [f"CUST_{i%100:03d}" for i in range(1, 1001)],
    'product_id': [f"PROD_{i%50:03d}" for i in range(1, 1001)],
    'order_value': [round(50 + (i * 3.7) % 500, 2) for i in range(1, 1001)],
    'order_date': pd.date_range('2024-01-01', periods=1000, freq='H'),
    'region': ['North', 'South', 'East', 'West'][0:1000:250] * 250
})

# Wrap for lineage tracking
orders_ldf = LineageDataFrame(orders_df, name="raw_orders", tracker=tracker)

print(f"📊 Loaded {len(orders_ldf._df)} orders")

# Data cleaning pipeline
# Step 1: Remove invalid orders
valid_orders = orders_ldf.filter(orders_ldf._df['order_value'] > 0)
print(f"✅ Step 1: {len(valid_orders._df)} valid orders")

# Step 2: Focus on high-value orders
high_value_orders = valid_orders.filter(valid_orders._df['order_value'] > 100)
print(f"✅ Step 2: {len(high_value_orders._df)} high-value orders")

# Step 3: Add derived features
enriched_orders = high_value_orders.transform(lambda x: x.assign(
    order_month = x['order_date'].dt.strftime('%Y-%m'),
    value_category = x['order_value'].apply(
        lambda v: 'Premium' if v > 300 else 'Standard'
    )
))
print(f"✅ Step 3: Added derived features")

# Step 4: Aggregation analysis
regional_analysis = enriched_orders.groupby(['region', 'value_category']).agg({
    'order_value': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
})
print(f"✅ Step 4: Regional analysis completed")

# Final summary
monthly_trends = enriched_orders.groupby('order_month').agg({
    'order_value': 'sum',
    'order_id': 'count'
})
print(f"✅ Step 5: Monthly trends analysis")

# Show lineage summary
print(f"\n📈 Pipeline Summary:")
print(f"   🔗 Lineage nodes created: {len(tracker.nodes)}")
print(f"   📊 Data transformations: {len(tracker.edges)}")
print(f"   📋 Operations tracked: {len([n for n in tracker.nodes.values() if n.node_type == 'operation'])}")
```

### **Example 2: Data Quality Pipeline**

```python
from datalineagepy import LineageTracker, LineageDataFrame
from datalineagepy.core.validation import DataValidator
import pandas as pd
import numpy as np

# Initialize tracker with validation
tracker = LineageTracker(
    name="data_quality_pipeline",
    config={
        "enable_validation": True,
        "memory_optimization": True
    }
)

# Create sample data with quality issues
messy_data = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'email': ['user1@example.com', 'user2@example.com', None, 'invalid-email',
              'user5@example.com', '', 'user7@example.com', 'user8@example.com',
              None, 'user10@example.com'],
    'age': [25, 30, None, -5, 45, 150, 35, 28, 22, None],
    'income': [50000, 75000, 60000, None, 90000, 120000, 55000, 48000, 85000, 95000],
    'signup_date': ['2024-01-15', '2024-02-20', '2024-03-10', 'invalid-date',
                   '2024-04-05', '2024-05-12', None, '2024-06-18', '2024-07-22', '2024-08-30']
})

# Wrap for lineage tracking
raw_data = LineageDataFrame(messy_data, name="raw_user_data", tracker=tracker)
print(f"📊 Raw data: {len(raw_data._df)} rows")

# Data quality pipeline

# Step 1: Clean email addresses
clean_emails = raw_data.transform(lambda df: df.assign(
    email_clean = df['email'].fillna('').apply(
        lambda x: x if '@' in str(x) and '.' in str(x) else None
    )
))
print(f"✅ Step 1: Email cleaning completed")

# Step 2: Validate age ranges
valid_ages = clean_emails.transform(lambda df: df.assign(
    age_clean = df['age'].apply(
        lambda x: x if pd.notna(x) and 0 <= x <= 120 else None
    )
))
print(f"✅ Step 2: Age validation completed")

# Step 3: Handle missing income data
income_filled = valid_ages.transform(lambda df: df.assign(
    income_clean = df['income'].fillna(df['income'].median())
))
print(f"✅ Step 3: Income imputation completed")

# Step 4: Parse and validate dates
date_cleaned = income_filled.transform(lambda df: df.assign(
    signup_date_clean = pd.to_datetime(df['signup_date'], errors='coerce')
))
print(f"✅ Step 4: Date parsing completed")

# Step 5: Final cleanup - remove rows with critical missing data
final_clean = date_cleaned.filter(
    date_cleaned._df['email_clean'].notna() &
    date_cleaned._df['age_clean'].notna()
)
print(f"✅ Step 5: Final cleanup - {len(final_clean._df)} clean rows")

# Data validation
validator = DataValidator()
validation_rules = {
    'completeness': {'threshold': 0.8},
    'uniqueness': {'columns': ['user_id']},
    'range_check': {'column': 'age_clean', 'min': 18, 'max': 100}
}

validation_results = validator.validate_dataframe(final_clean, validation_rules)
print(f"\n📊 Data Quality Results:")
print(f"   ✅ Overall quality score: {validation_results.get('overall_score', 0):.1%}")
print(f"   📈 Data completeness: {validation_results.get('completeness_score', 0):.1%}")

# Show transformation lineage
print(f"\n🔗 Data Quality Pipeline Lineage:")
print(f"   📊 Total transformations: {len(tracker.nodes)}")
print(f"   🔄 Data flows tracked: {len(tracker.edges)}")
print(f"   📋 Quality improvements: {len(raw_data._df) - len(final_clean._df)} invalid rows removed")
```

### **Example 3: Real-time Analytics with Performance Monitoring**

```python
from datalineagepy import LineageTracker, LineageDataFrame
from datalineagepy.core.performance import PerformanceMonitor
import pandas as pd
import time

# Initialize tracker with performance monitoring
tracker = LineageTracker(
    name="realtime_analytics",
    config={
        "performance_monitoring": True,
        "memory_optimization": True
    }
)

# Enable performance monitoring
monitor = PerformanceMonitor(tracker)
monitor.start_monitoring()

# Simulate real-time data processing
print("🚀 Starting real-time analytics pipeline...")

# Generate streaming data simulation
for batch_num in range(1, 4):
    print(f"\n📊 Processing batch {batch_num}...")

    # Simulate incoming data
    batch_data = pd.DataFrame({
        'timestamp': pd.date_range(
            start=f'2025-06-19 {batch_num:02d}:00:00',
            periods=1000,
            freq='1S'
        ),
        'sensor_id': [f"SENSOR_{i%10:03d}" for i in range(1000)],
        'temperature': [20 + (i * 0.1) % 30 for i in range(1000)],
        'humidity': [30 + (i * 0.2) % 40 for i in range(1000)],
        'pressure': [1000 + (i * 0.05) % 50 for i in range(1000)]
    })

    # Track batch processing
    batch_ldf = LineageDataFrame(
        batch_data,
        name=f"sensor_batch_{batch_num}",
        tracker=tracker
    )

    # Real-time processing pipeline

    # 1. Data validation
    valid_data = batch_ldf.filter(
        (batch_ldf._df['temperature'] > 0) &
        (batch_ldf._df['humidity'] > 0) &
        (batch_ldf._df['pressure'] > 950)
    )

    # 2. Anomaly detection
    anomalies = valid_data.filter(
        (valid_data._df['temperature'] > 45) |
        (valid_data._df['humidity'] > 80)
    )

    # 3. Aggregation by sensor
    sensor_summary = valid_data.groupby('sensor_id').agg({
        'temperature': ['mean', 'min', 'max'],
        'humidity': ['mean', 'std'],
        'pressure': 'mean'
    })

    # 4. Time-based aggregation
    hourly_summary = valid_data.transform(lambda df: df.assign(
        hour = df['timestamp'].dt.floor('H')
    )).groupby('hour').agg({
        'temperature': 'mean',
        'humidity': 'mean',
        'pressure': 'mean',
        'sensor_id': 'nunique'
    })

    print(f"   ✅ Processed {len(batch_ldf._df):,} records")
    print(f"   ⚠️  Detected {len(anomalies._df)} anomalies")
    print(f"   📈 Generated summaries for {len(sensor_summary._df)} sensors")

    # Small delay to simulate real-time processing
    time.sleep(0.1)

# Get performance summary
performance_summary = monitor.get_performance_summary()

print(f"\n⚡ Performance Summary:")
print(f"   📊 Total records processed: {3000:,}")
print(f"   ⏱️  Average processing time: {performance_summary.get('average_execution_time', 0):.3f}s")
print(f"   💾 Current memory usage: {performance_summary.get('current_memory_usage', 0):.1f}MB")
print(f"   🔗 Total lineage nodes: {len(tracker.nodes)}")
print(f"   📈 Processing efficiency: Excellent")

monitor.stop_monitoring()
```

---

## 📊 **Visualization & Export**

### **Quick Visualization**

```python
# Generate lineage visualization
tracker.visualize(output_file="my_pipeline_lineage.png")
print("✅ Lineage graph saved as 'my_pipeline_lineage.png'")

# Create interactive dashboard
tracker.generate_dashboard("lineage_dashboard.html")
print("✅ Interactive dashboard saved as 'lineage_dashboard.html'")
```

### **Export Lineage Data**

```python
# Export to JSON
lineage_json = tracker.export_lineage()
print(f"📤 Exported lineage with {len(lineage_json.get('nodes', []))} nodes")

# Export to multiple formats
tracker.export_to_formats(
    base_path="lineage_exports/",
    formats=['json', 'csv', 'excel']
)
print("✅ Exported to multiple formats in 'lineage_exports/' directory")
```

---

## 🎯 **Next Steps**

### **Immediate Next Steps (5 minutes)**

1. **Try the examples above** - Copy and run them in your environment
2. **Explore your data** - Replace sample data with your own datasets
3. **Check the visualization** - Open the generated HTML dashboard

### **Short-term Learning (30 minutes)**

1. **📚 [User Guide](user-guide/)** - Comprehensive usage documentation
2. **🛠️ [API Reference](api/)** - Detailed method documentation
3. **📊 [Examples](examples/)** - More advanced examples

### **Enterprise Implementation (1-2 hours)**

1. **🏢 [Production Deployment](advanced/production.md)** - Enterprise setup
2. **📊 [Performance Optimization](benchmarks/performance.md)** - Scaling for production
3. **🔒 [Security Configuration](advanced/security.md)** - Enterprise security

---

## 🆘 **Quick Troubleshooting**

### **Common Quick Fixes**

#### **Import Error**

```python
# If you see: ImportError: No module named 'datalineagepy'
# Solution: Install the package
import subprocess
subprocess.check_call(["pip", "install", "datalineagepy"])
```

#### **Memory Issues**

```python
# If processing large datasets
tracker = LineageTracker(
    name="memory_optimized",
    config={"memory_optimization": True}
)
```

#### **Performance Issues**

```python
# Enable performance monitoring to identify bottlenecks
from datalineagepy.core.performance import PerformanceMonitor
monitor = PerformanceMonitor(tracker)
monitor.start_monitoring()
```

---

## 🎊 **You're Ready!**

**Congratulations!** You now know how to:

✅ Install and setup DataLineagePy  
✅ Create lineage trackers and wrap DataFrames  
✅ Automatically track data transformations  
✅ Generate visualizations and exports  
✅ Handle common troubleshooting scenarios

### **🚀 What's Next?**

Choose your learning path:

- **📚 [Complete User Guide](user-guide/)** - Learn all features in detail
- **🏢 [Enterprise Features](advanced/production.md)** - Production deployment
- **🧩 [Integrations](integrations/)** - Connect with other tools
- **📊 [Advanced Examples](examples/advanced/)** - Complex use cases

---

## 📞 **Need Help?**

- **💬 [GitHub Discussions](https://github.com/Arbaznazir/DataLineagePy/discussions)** - Community support
- **📚 [Documentation](index.md)** - Complete documentation
- **🐛 [Issues](https://github.com/Arbaznazir/DataLineagePy/issues)** - Bug reports
- **📧 [Enterprise Support](mailto:enterprise@datalineagepy.com)** - Priority support

---

<div align="center">

**🌟 Welcome to the DataLineagePy Community! 🌟**

_Happy lineage tracking! 🚀_

</div>

---

_Quick start guide last updated: June 19, 2025_
