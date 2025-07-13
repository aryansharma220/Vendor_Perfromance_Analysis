# Vendor Performance Analysis Project

## 📊 Project Overview

This project provides a comprehensive analysis of vendor performance in the retail/wholesale industry, focusing on inventory management, sales optimization, and profitability analysis. The analysis helps identify underperforming vendors, optimize pricing strategies, and improve inventory turnover efficiency.

## 🎯 Business Problem

Effective inventory and sales management are critical for optimizing profitability in the retail and wholesale industry. Companies need to ensure that they are not incurring losses due to:
- Inefficient pricing strategies
- Poor inventory turnover
- Vendor dependency risks
- Suboptimal procurement decisions

## 🔍 Analysis Objectives

1. **Identify underperforming brands** that require promotional or pricing adjustments
2. **Determine top vendors** contributing to sales and gross profit
3. **Analyze the impact of bulk purchasing** on unit costs
4. **Assess inventory turnover** to reduce holding costs and improve efficiency
5. **Investigate profitability variance** between high-performing and low-performing vendors

## 📁 Project Structure

```
Vendor_Performance/
├── dataset/                           # Raw CSV data files
│   ├── begin_inventory.csv           # Beginning inventory data (206,529 records)
│   ├── end_inventory.csv             # Ending inventory data (224,489 records)
│   ├── purchases.csv                 # Purchase transactions (2,372,474 records)
│   ├── purchase_prices.csv           # Product pricing data (12,261 records)
│   ├── sales.csv                     # Sales transactions (12,825,363 records)
│   └── vendor_invoice.csv            # Vendor invoice data (5,543 records)
├── logs/                             # Execution logs
│   ├── ingestion_db.log              # Data ingestion process logs
│   └── get_vendor_summary.log        # Vendor summary creation logs
├── notebooks/
│   ├── Exploratory_Data_Analysis.ipynb     # Initial data exploration
│   ├── Vendor_Performance_Analysis.ipynb   # Main analysis notebook
│   └── Untitled.ipynb                      # Data ingestion notebook
├── scripts/
│   ├── ingestion_db.py               # Data ingestion script
│   └── get_vendor_summary.py         # Vendor summary creation script
├── inventory.db                      # SQLite database
├── business_problem.txt              # Business problem description
├── Data_Analytics_Workflow.png       # Project workflow diagram
└── README.md                         # This file
```

## 🗄️ Database Schema

The project uses an SQLite database with the following tables:

### Raw Data Tables
- **begin_inventory**: Starting inventory positions
- **end_inventory**: Ending inventory positions  
- **purchases**: Purchase transaction details
- **purchase_prices**: Product pricing information
- **sales**: Sales transaction records
- **vendor_invoice**: Vendor invoice summaries

### Derived Tables
- **vendor_sales_summary**: Aggregated vendor performance metrics (10,692 records)

### Key Metrics in vendor_sales_summary
- `GrossProfit`: Revenue - Cost of Goods Sold
- `ProfitMargin`: (Gross Profit / Revenue) × 100
- `StockTurnover`: Sales Quantity / Purchase Quantity
- `SalesToPurchaseRatio`: Sales Dollars / Purchase Dollars
- `UnitPurchasePrice`: Total Purchase Dollars / Purchase Quantity
- `UnsoldInventoryValue`: (Purchase Qty - Sales Qty) × Unit Price

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Required libraries: pandas, numpy, matplotlib, seaborn, sqlite3, scipy, sqlalchemy

### Installation
1. Clone the repository
2. Install required packages:
```bash
pip install pandas numpy matplotlib seaborn scipy sqlalchemy
```

### Data Ingestion
1. Run the data ingestion script:
```python
python ingestion_db.py
```
This will process all CSV files and create the SQLite database (takes ~10.8 minutes).

2. Create vendor summary table:
```python
python get_vendor_summary.py
```

### Analysis Execution
Open and run the Jupyter notebooks in the following order:
1. `Exploratory_Data_Analysis.ipynb` - Understanding the dataset
2. `Vendor_Performance_Analysis.ipynb` - Main analysis and insights

## 📈 Key Findings & Insights

### 1. Vendor Performance Distribution
- **Top 10 vendors** contribute to **XX%** of total procurement
- Significant concentration risk with key vendors
- Performance varies dramatically across vendor categories

### 2. Profit Margin Analysis
- **Low-performing vendors** maintain higher profit margins (40.48% - 42.62%)
- **High-performing vendors** have lower margins (30.74% - 31.61%)
- Statistical significance confirmed through t-test analysis

### 3. Bulk Purchase Impact
- **Large orders** achieve ~72% reduction in unit costs vs small orders
- Clear economies of scale benefit for bulk purchasing
- Optimal order sizing opportunities identified

### 4. Inventory Management
- **Stock turnover** ranges from 0 to 274.5
- Some products sell extremely fast while others remain stagnant
- Capital locked in unsold inventory: **$XXX** total

### 5. Brand Performance
- **198 brands** identified for promotional/pricing adjustments
- High-margin, low-sales brands present growth opportunities
- Clear segmentation between premium and volume brands

## 🔧 Technical Implementation

### Data Processing Pipeline
1. **Extraction**: Raw CSV files from various business systems
2. **Transformation**: Data cleaning, type conversion, null handling
3. **Loading**: SQLite database with optimized schema
4. **Aggregation**: Complex SQL queries for vendor summary creation
5. **Analysis**: Statistical analysis and visualization

### Key SQL Query (Vendor Summary Creation)
```sql
WITH FreightSummary AS (
    SELECT VendorNumber, SUM(Freight) as FreightCost 
    FROM vendor_invoice GROUP BY VendorNumber
),
PurchaseSummary AS (
    SELECT p.VendorNumber, p.VendorName, p.Brand, p.Description,
           p.PurchasePrice, pp.Volume, pp.Price as ActualPrice,
           SUM(Quantity) as TotalPurchaseQuantity,
           SUM(Dollars) as TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp ON p.brand = pp.brand
    WHERE p.purchasePrice > 0
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, 
             p.PurchasePrice, pp.Price, pp.Volume
),
SalesSummary AS (
    SELECT VendorNo, Brand,
           SUM(SalesDollars) as TotalSalesDollars,
           SUM(SalesPrice) as TotalSalesPrice,
           SUM(SalesQuantity) as TotalSalesQuantity,
           SUM(ExciseTax) as TotalExciseTax
    FROM sales GROUP BY VendorNo, Brand
)
SELECT ps.*, ss.*, fs.FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss ON ps.vendorNumber = ss.vendorNo AND ps.brand = ss.brand
LEFT JOIN FreightSummary fs ON ps.vendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC;
```

## 📊 Visualizations & Reports

The project includes comprehensive visualizations:
- Distribution plots for numerical variables
- Correlation heatmaps
- Pareto charts for vendor contribution
- Scatter plots for brand performance analysis
- Box plots for outlier detection
- Statistical confidence interval comparisons

## 🎯 Business Recommendations

### Immediate Actions
1. **Focus on high-margin, low-sales brands** for promotional campaigns
2. **Negotiate better terms** with top-contributing vendors
3. **Optimize inventory levels** for slow-moving products
4. **Implement bulk purchasing strategies** where beneficial

### Strategic Initiatives
1. **Vendor diversification** to reduce dependency risk
2. **Dynamic pricing strategies** based on margin analysis
3. **Inventory turnover optimization** programs
4. **Performance-based vendor partnerships**

## 🔄 Future Enhancements

- Real-time dashboard development
- Predictive analytics for demand forecasting
- Machine learning models for vendor performance prediction
- Integration with ERP systems for live data feeds
- Advanced statistical modeling for price optimization

## 📝 Logging & Monitoring

All processes are logged with timestamps and status updates:
- Data ingestion progress and completion times
- Error handling and recovery procedures
- Performance metrics and execution times

**Note**: This analysis was completed using Python data science stack with SQLite for data storage and Jupyter notebooks for interactive analysis. All data has been anonymized and aggregated for privacy compliance.
