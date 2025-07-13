#!/usr/bin/env python3
"""
Script to import HR Employee Attrition CSV data into Workforce Distribution.ai
"""

import requests
import json
import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

API_BASE_URL = "http://localhost:8000/api/v1"
CSV_FILE_PATH = "WA_Fn-UseC_-HR-Employee-Attrition.csv"

def test_api_connection():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is running and accessible")
            return True
        else:
            print("❌ API is not responding correctly")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend server is running on http://localhost:8000")
        return False

def get_csv_summary():
    """Get summary of the CSV data"""
    try:
        response = requests.get(f"{API_BASE_URL}/data-import/csv/summary?file_path={CSV_FILE_PATH}")
        if response.status_code == 200:
            summary = response.json()
            print("\n📊 CSV Data Summary:")
            print(f"   Total Records: {summary['total_records']}")
            print(f"   Active Employees: {summary['active_employees']}")
            print(f"   Attrition Rate: {summary['attrition_rate']:.1f}%")
            print(f"   Unique Job Roles: {summary['unique_job_roles']}")
            print(f"   Unique Departments: {summary['unique_departments']}")
            
            print(f"\n💰 Salary Statistics:")
            salary_stats = summary['salary_statistics']
            print(f"   Min: ${salary_stats['min']:,.0f}")
            print(f"   Max: ${salary_stats['max']:,.0f}")
            print(f"   Mean: ${salary_stats['mean']:,.0f}")
            print(f"   Median: ${salary_stats['median']:,.0f}")
            
            print(f"\n📈 Experience Statistics:")
            exp_stats = summary['experience_statistics']
            print(f"   Min: {exp_stats['min']:.1f} years")
            print(f"   Max: {exp_stats['max']:.1f} years")
            print(f"   Mean: {exp_stats['mean']:.1f} years")
            
            print(f"\n🏢 Job Roles Distribution:")
            for role, count in summary['job_roles'].items():
                print(f"   {role}: {count}")
            
            print(f"\n📋 Departments Distribution:")
            for dept, count in summary['departments'].items():
                print(f"   {dept}: {count}")
            
            return summary
        else:
            print(f"❌ Error getting summary: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def preview_csv_data():
    """Preview the CSV data"""
    try:
        response = requests.get(f"{API_BASE_URL}/data-import/csv/preview?file_path={CSV_FILE_PATH}&rows=5")
        if response.status_code == 200:
            preview = response.json()
            print(f"\n👀 CSV Preview (first 5 rows):")
            print(f"   Total Rows: {preview['total_rows']}")
            print(f"   Total Columns: {preview['total_columns']}")
            
            print(f"\n📋 Columns:")
            for col in preview['columns_info'][:10]:  # Show first 10 columns
                print(f"   {col['name']} ({col['type']}) - {col['unique_values']} unique values")
            
            print(f"\n📄 Sample Data:")
            for i, row in enumerate(preview['preview_data'][:3]):  # Show first 3 rows
                print(f"   Row {i+1}: {dict(list(row.items())[:5])}...")  # Show first 5 columns
            
            return preview
        else:
            print(f"❌ Error getting preview: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def import_csv_data():
    """Import the CSV data into the system"""
    try:
        print(f"\n🚀 Importing CSV data from: {CSV_FILE_PATH}")
        
        response = requests.post(f"{API_BASE_URL}/data-import/csv/import-from-path?file_path={CSV_FILE_PATH}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Data imported successfully!")
            print(f"   Jobs Created: {result['jobs_created']}")
            print(f"   Candidates Created: {result['candidates_created']}")
            print(f"   Skills Created: {result['skills_created']}")
            print(f"   Total Records Processed: {result['total_records']}")
            return result
        else:
            print(f"❌ Import failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error during import: {str(e)}")
        return None

def verify_import():
    """Verify the imported data"""
    try:
        print(f"\n🔍 Verifying imported data...")
        
        # Check jobs
        jobs_response = requests.get(f"{API_BASE_URL}/jobs/")
        if jobs_response.status_code == 200:
            jobs_data = jobs_response.json()
            print(f"   Jobs in system: {jobs_data['total']}")
        
        # Check candidates
        candidates_response = requests.get(f"{API_BASE_URL}/candidates/")
        if candidates_response.status_code == 200:
            candidates_data = candidates_response.json()
            print(f"   Candidates in system: {candidates_data['total']}")
        
        # Check dashboard stats
        stats_response = requests.get(f"{API_BASE_URL}/analysis/dashboard/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"   Total Jobs: {stats['total_jobs']}")
            print(f"   Active Jobs: {stats['active_jobs']}")
            print(f"   Total Candidates: {stats['total_candidates']}")
            print(f"   Active Candidates: {stats['active_candidates']}")
            print(f"   Average Experience: {stats['avg_experience_years']} years")
        
        return True
    except Exception as e:
        print(f"❌ Error verifying data: {str(e)}")
        return False

def main():
    """Main function"""
    print("🎯 HR Employee Attrition Data Import for Workforce Distribution.ai")
    print("=" * 60)
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE_PATH):
        print(f"❌ CSV file not found: {CSV_FILE_PATH}")
        print("Please make sure the CSV file is in the same directory as this script.")
        return
    
    # Test API connection
    if not test_api_connection():
        return
    
    # Get CSV summary
    summary = get_csv_summary()
    if not summary:
        return
    
    # Preview CSV data
    preview = preview_csv_data()
    if not preview:
        return
    
    # Ask for confirmation
    print(f"\n❓ Do you want to import this data into the system?")
    print("   This will create jobs, candidates, and skills based on the CSV data.")
    print("   Type 'yes' to continue or anything else to cancel:")
    
    user_input = input("   Your choice: ").strip().lower()
    
    if user_input != 'yes':
        print("❌ Import cancelled by user.")
        return
    
    # Import the data
    import_result = import_csv_data()
    if not import_result:
        return
    
    # Verify the import
    verify_import()
    
    print(f"\n🎉 Data import completed successfully!")
    print(f"   You can now use the Streamlit frontend to explore the imported data.")
    print(f"   Frontend URL: http://localhost:8501")
    print(f"   API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 