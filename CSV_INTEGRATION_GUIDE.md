# CSV Data Integration Guide

This guide explains how to integrate your HR Employee Attrition CSV dataset with the Workforce Distribution.ai system.

## 📊 About Your Dataset

Your CSV file `WA_Fn-UseC_-HR-Employee-Attrition.csv` contains comprehensive HR data with the following key information:

### Dataset Overview
- **Total Records**: 1,471 employees
- **Columns**: 35 fields including demographics, job details, performance metrics, and attrition status
- **Key Features**: Employee demographics, job roles, salaries, performance ratings, satisfaction scores, and attrition data

### Key Columns
- **Employee Information**: Age, Gender, Education, Marital Status
- **Job Details**: Department, Job Role, Job Level, Years at Company
- **Compensation**: Monthly Income, Daily Rate, Hourly Rate
- **Performance**: Performance Rating, Job Satisfaction, Environment Satisfaction
- **Work Patterns**: Business Travel, Overtime, Work-Life Balance
- **Attrition**: Whether the employee left the company

## 🚀 How to Import Your Data

### Option 1: Using the Import Script (Recommended)

1. **Start the backend server**:
   ```bash
   python start_backend.py
   ```

2. **Run the import script**:
   ```bash
   python import_csv_data.py
   ```

3. **Follow the prompts**:
   - The script will show you a summary of your data
   - Preview the data structure
   - Confirm the import

### Option 2: Using the Streamlit Frontend

1. **Start both servers**:
   ```bash
   # Terminal 1: Backend
   python start_backend.py
   
   # Terminal 2: Frontend
   python start_frontend.py
   ```

2. **Navigate to Data Import section**:
   - Go to http://localhost:8501
   - Click on "Data Import" in the sidebar
   - Use the "CSV Summary" tab to analyze your data
   - Use the "Import Data" tab to import the data

### Option 3: Using the API Directly

```bash
# Get data summary
curl "http://localhost:8000/api/v1/data-import/csv/summary?file_path=WA_Fn-UseC_-HR-Employee-Attrition.csv"

# Import the data
curl -X POST "http://localhost:8000/api/v1/data-import/csv/import-from-path?file_path=WA_Fn-UseC_-HR-Employee-Attrition.csv"
```

## 🔄 Data Transformation Process

The system automatically transforms your CSV data into the Workforce Distribution.ai format:

### Job Roles Created
- **Sales Executive** → Sales Representative
- **Research Scientist** → Data Scientist
- **Laboratory Technician** → Research Assistant
- **Manufacturing Director** → Operations Manager
- **Healthcare Representative** → Healthcare Specialist
- **Manager** → Department Manager
- **Research Director** → Research Manager
- **Human Resources** → HR Specialist

### Skills Mapping
Each job role is automatically assigned relevant skills based on the position:

**Sales Roles**:
- Sales, Communication, Negotiation, Customer Service, Product Knowledge, Relationship Building

**Research/Data Roles**:
- Research, Data Analysis, Statistics, Python, Machine Learning, Scientific Writing

**Management Roles**:
- Leadership, Team Management, Strategic Planning, Communication, Decision Making

**Technical Roles**:
- Laboratory Skills, Data Collection, Quality Control, Technical Skills, Attention to Detail

### Candidate Creation
- **Active employees only** (Attrition = 'No') are converted to candidates
- Skills are adjusted based on performance ratings and job satisfaction
- Salary expectations are calculated from monthly income
- Experience levels are mapped from total working years

## 📈 What You'll Get After Import

### Jobs Created
- Multiple job roles based on unique combinations in your data
- Salary ranges calculated from actual compensation data
- Required skills automatically assigned
- Department and level information preserved

### Candidates Created
- Active employees converted to candidates
- AI-powered skills assessment applied
- Performance-based skill adjustments
- Realistic salary expectations

### Skills Created
- Comprehensive skill library based on job requirements
- Market demand and salary impact scores
- Categorized skills (Technical, Business, Soft Skills, etc.)

## 🎯 Using Your Imported Data

### 1. Workforce Distribution Analysis
- Analyze how your current workforce is distributed
- Identify skill gaps and opportunities
- Plan for future hiring needs

### 2. Salary Benchmarking
- Compare your actual salaries with market benchmarks
- Identify compensation gaps
- Plan salary adjustments

### 3. Skills Gap Analysis
- Identify missing skills in your workforce
- Plan training and development programs
- Optimize team compositions

### 4. Attrition Analysis
- Understand why employees leave
- Identify retention strategies
- Predict future attrition risks

## 📊 Key Insights from Your Data

### Attrition Analysis
- **Attrition Rate**: ~16% (typical for the industry)
- **High-Risk Factors**: Low job satisfaction, poor work-life balance, limited growth opportunities

### Salary Insights
- **Salary Range**: $1,000 - $20,000 monthly
- **Department Variations**: Sales and Management have higher compensation
- **Experience Correlation**: Strong correlation between experience and salary

### Performance Patterns
- **Performance Ratings**: Most employees rated 3-4 out of 5
- **Satisfaction Scores**: Varies by department and role
- **Work-Life Balance**: Key factor in retention

## 🔧 Customization Options

### Modify Skills Mapping
Edit `backend/app/services/data_import.py` to customize:
- Job role mappings
- Skills assignments
- Salary calculations
- Experience requirements

### Add Custom Fields
Extend the data models to include:
- Additional performance metrics
- Custom skill categories
- Department-specific requirements

### Adjust Import Logic
Modify the import service to:
- Include different employee subsets
- Apply custom business rules
- Handle additional data sources

## 🚨 Important Notes

### Data Privacy
- Employee names are anonymized (Employee1, Employee2, etc.)
- Email addresses are generated (employee1@company.com)
- Phone numbers are fictional (+1-555-XXXX)

### Data Quality
- Only active employees (no attrition) are imported as candidates
- Missing data is handled gracefully
- Duplicate records are prevented

### Performance Considerations
- Large datasets may take time to process
- Consider importing in batches for very large files
- Monitor system resources during import

## 🆘 Troubleshooting

### Common Issues

1. **File Not Found**
   - Ensure the CSV file is in the correct directory
   - Check file permissions
   - Verify the file path is correct

2. **Import Errors**
   - Check the CSV format (should be standard CSV)
   - Verify column names match expected format
   - Ensure the backend server is running

3. **Data Quality Issues**
   - Review the data preview before importing
   - Check for missing or invalid values
   - Verify data types are correct

### Getting Help
- Check the API documentation at http://localhost:8000/docs
- Review the import logs for detailed error messages
- Use the data preview feature to validate your data

## 🎉 Next Steps

After importing your data:

1. **Explore the Dashboard** to see overview statistics
2. **Analyze Workforce Distribution** to understand current state
3. **Run Skills Gap Analysis** to identify improvement areas
4. **Use Salary Benchmarking** to optimize compensation
5. **Create Custom Reports** based on your specific needs

Your HR data is now fully integrated with the AI-powered Workforce Distribution.ai system! 