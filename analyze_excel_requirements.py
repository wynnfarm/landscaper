#!/usr/bin/env python3
"""
Excel Requirements Analyzer for Landscaper Application
Analyzes Excel files to extract business requirements and data structures
"""

import pandas as pd
import sys
import os
from pathlib import Path

def analyze_excel_file(file_path):
    """Analyze Excel file and extract requirements"""
    print("🔍 Analyzing Excel file for landscaping application requirements...")
    print("=" * 60)
    
    try:
        # Read all sheets from the Excel file
        excel_file = pd.ExcelFile(file_path)
        print(f"📊 File: {file_path}")
        print(f"📋 Sheets found: {excel_file.sheet_names}")
        print()
        
        requirements = {
            'sheets': [],
            'data_structures': [],
            'calculations': [],
            'business_logic': [],
            'user_workflows': [],
            'integration_points': []
        }
        
        # Analyze each sheet
        for sheet_name in excel_file.sheet_names:
            print(f"📄 Analyzing sheet: {sheet_name}")
            print("-" * 40)
            
            try:
                # Read the sheet
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                sheet_analysis = {
                    'name': sheet_name,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': list(df.columns),
                    'data_types': df.dtypes.to_dict(),
                    'sample_data': df.head(3).to_dict('records'),
                    'null_counts': df.isnull().sum().to_dict(),
                    'unique_values': {}
                }
                
                # Analyze unique values for categorical columns
                for col in df.columns:
                    if df[col].dtype == 'object' and len(df[col].unique()) < 20:
                        sheet_analysis['unique_values'][col] = df[col].unique().tolist()
                
                requirements['sheets'].append(sheet_analysis)
                
                # Print analysis
                print(f"   Rows: {sheet_analysis['rows']}")
                print(f"   Columns: {sheet_analysis['columns']}")
                print(f"   Column names: {sheet_analysis['column_names']}")
                print(f"   Data types: {dict(sheet_analysis['data_types'])}")
                
                # Look for potential calculations
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    print(f"   Numeric columns (potential calculations): {list(numeric_cols)}")
                
                # Look for date columns
                date_cols = []
                for col in df.columns:
                    if 'date' in col.lower() or 'time' in col.lower():
                        date_cols.append(col)
                if date_cols:
                    print(f"   Date/time columns: {date_cols}")
                
                print()
                
            except Exception as e:
                print(f"   ❌ Error analyzing sheet {sheet_name}: {e}")
                print()
        
        # Generate requirements summary
        print("📋 REQUIREMENTS ANALYSIS SUMMARY")
        print("=" * 60)
        
        # Data structures needed
        print("\n🏗️ DATA STRUCTURES NEEDED:")
        for sheet in requirements['sheets']:
            print(f"\n📊 {sheet['name']} Table:")
            for col, dtype in sheet['data_types'].items():
                print(f"   - {col}: {dtype}")
        
        # Business logic insights
        print("\n💼 BUSINESS LOGIC INSIGHTS:")
        for sheet in requirements['sheets']:
            numeric_cols = [col for col, dtype in sheet['data_types'].items() 
                           if 'int' in str(dtype) or 'float' in str(dtype)]
            if numeric_cols:
                print(f"   📈 {sheet['name']}: Potential calculations with {numeric_cols}")
        
        # User workflow suggestions
        print("\n👤 USER WORKFLOW SUGGESTIONS:")
        for sheet in requirements['sheets']:
            if 'job' in sheet['name'].lower() or 'project' in sheet['name'].lower():
                print(f"   🔄 Job/Project workflow: {sheet['name']}")
            if 'material' in sheet['name'].lower() or 'inventory' in sheet['name'].lower():
                print(f"   📦 Material management: {sheet['name']}")
            if 'customer' in sheet['name'].lower() or 'client' in sheet['name'].lower():
                print(f"   👥 Customer management: {sheet['name']}")
        
        # Integration points
        print("\n🔗 INTEGRATION POINTS:")
        print("   - Database tables for each sheet")
        print("   - API endpoints for CRUD operations")
        print("   - Form interfaces for data entry")
        print("   - Report generation capabilities")
        print("   - Data import/export functionality")
        
        # Questions for clarification
        print("\n❓ QUESTIONS FOR CLARIFICATION:")
        print("   1. What is the primary purpose of each sheet?")
        print("   2. How are calculations performed in the Excel file?")
        print("   3. What is the typical workflow for using this worksheet?")
        print("   4. Are there any formulas or macros that need to be replicated?")
        print("   5. What data validation rules exist in the Excel file?")
        print("   6. How do users currently interact with this data?")
        print("   7. What reports or outputs are generated from this data?")
        
        return requirements
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

def generate_requirements_document(requirements):
    """Generate a structured requirements document"""
    if not requirements:
        return
    
    print("\n📄 GENERATING REQUIREMENTS DOCUMENT")
    print("=" * 60)
    
    doc = f"""
# Landscaping Application Requirements Analysis
Based on Excel file: Elevations for Jobs Worksheet 2025.xlsx

## Overview
This document outlines the requirements extracted from the Excel worksheet for integration into the landscaping application.

## Data Structures

"""
    
    for sheet in requirements['sheets']:
        doc += f"""
### {sheet['name']} Table
- **Purpose**: [To be determined]
- **Rows**: {sheet['rows']}
- **Columns**: {sheet['columns']}

#### Fields:
"""
        for col, dtype in sheet['data_types'].items():
            doc += f"- {col} ({dtype})\n"
        
        if sheet['unique_values']:
            doc += "\n#### Categorical Values:\n"
            for col, values in sheet['unique_values'].items():
                doc += f"- {col}: {values}\n"
    
    doc += """
## Business Logic Requirements
[To be determined based on Excel formulas and calculations]

## User Interface Requirements
- Forms for data entry
- Tables for data display
- Search and filter capabilities
- Export functionality

## Integration Requirements
- Database schema updates
- API endpoint development
- Frontend component creation
- Data migration scripts

## Questions for Stakeholders
1. What is the primary workflow for using this worksheet?
2. Are there any complex calculations that need to be replicated?
3. What validation rules should be applied to the data?
4. How should the data be organized in the application?
5. What reporting capabilities are needed?
"""
    
    # Save requirements document
    with open('EXCEL_REQUIREMENTS_ANALYSIS.md', 'w') as f:
        f.write(doc)
    
    print("✅ Requirements document saved: EXCEL_REQUIREMENTS_ANALYSIS.md")

if __name__ == "__main__":
    # Look for the Excel file
    excel_file = "Elevations for Jobs Worksheet 2025.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        print("Please ensure the file is in the current directory.")
        sys.exit(1)
    
    # Analyze the file
    requirements = analyze_excel_file(excel_file)
    
    if requirements:
        # Generate requirements document
        generate_requirements_document(requirements)
        
        print("\n🎉 Analysis complete!")
        print("📁 Check EXCEL_REQUIREMENTS_ANALYSIS.md for detailed requirements")
    else:
        print("❌ Failed to analyze Excel file")
