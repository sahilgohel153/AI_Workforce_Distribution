from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict
import os
import tempfile
from ...core.database import get_db
from ...services.data_import import DataImportService

router = APIRouter()
data_import_service = DataImportService()

@router.post("/csv/upload")
async def upload_csv_data(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and import CSV data into the system
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Import data
        result = data_import_service.import_csv_data(temp_file_path, db)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if result["success"]:
            return {
                "message": "Data imported successfully",
                "jobs_created": result["jobs_created"],
                "candidates_created": result["candidates_created"],
                "skills_created": result["skills_created"],
                "total_records": result["total_records"]
            }
        else:
            raise HTTPException(status_code=500, detail=f"Import failed: {result['error']}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/csv/import-from-path")
async def import_csv_from_path(
    file_path: str,
    db: Session = Depends(get_db)
):
    """
    Import CSV data from a specific file path
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_path.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        result = data_import_service.import_csv_data(file_path, db)
        
        if result["success"]:
            return {
                "message": "Data imported successfully",
                "jobs_created": result["jobs_created"],
                "candidates_created": result["candidates_created"],
                "skills_created": result["skills_created"],
                "total_records": result["total_records"]
            }
        else:
            raise HTTPException(status_code=500, detail=f"Import failed: {result['error']}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/csv/summary")
async def get_csv_summary(file_path: str):
    """
    Get summary of CSV data without importing
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_path.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        summary = data_import_service.get_import_summary(file_path)
        
        if "error" in summary:
            raise HTTPException(status_code=500, detail=f"Error analyzing file: {summary['error']}")
        
        return summary
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing file: {str(e)}")

@router.get("/csv/preview")
async def preview_csv_data(file_path: str, rows: int = 10):
    """
    Preview CSV data (first N rows)
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_path.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        
        # Get column information
        columns_info = []
        for col in df.columns:
            columns_info.append({
                "name": col,
                "type": str(df[col].dtype),
                "unique_values": df[col].nunique(),
                "null_count": df[col].isnull().sum()
            })
        
        # Get preview data
        preview_data = df.head(rows).to_dict('records')
        
        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns_info": columns_info,
            "preview_data": preview_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}") 