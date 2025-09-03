#!/usr/bin/env python3
"""
Enhanced Excel Analysis - Deep Dive into Calculation Patterns
"""

import pandas as pd
import numpy as np
import re
import os

def deep_analyze_calculations(file_path):
    """Deep analysis of calculation patterns in the Excel file"""
    print("🔬 Deep Analysis of Calculation Patterns...")
    print("=" * 60)
    
    excel_file = pd.ExcelFile(file_path)
    
    # Focus on the main calculation sheets
    main_sheets = ['Pavers Cal', 'Wall Cal ', 'UCara Steps', 'Stairs Olde Quarry']
    
    calculation_patterns = {}
    
    for sheet_name in main_sheets:
        print(f"\n📊 Analyzing {sheet_name}...")
        
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Look for calculation patterns
            patterns = {
                'measurements': [],
                'layers': [],
                'calculations': [],
                'materials': [],
                'dates': []
            }
            
            # Analyze column patterns
            for col in df.columns:
                col_str = str(col).lower()
                
                # Look for measurement patterns
                if any(word in col_str for word in ['feet', 'inch', 'height', 'depth', 'width', 'length']):
                    patterns['measurements'].append(col)
                
                # Look for material layers
                if any(word in col_str for word in ['paver', 'fines', 'ca11', 'base', 'layer']):
                    patterns['layers'].append(col)
                
                # Look for calculation indicators
                if any(word in col_str for word in ['calc', 'total', 'sum', 'add']):
                    patterns['calculations'].append(col)
                
                # Look for material types
                if any(word in col_str for word in ['stone', 'brick', 'concrete', 'gravel']):
                    patterns['materials'].append(col)
                
                # Look for dates
                if isinstance(col, pd.Timestamp) or 'date' in col_str:
                    patterns['dates'].append(col)
            
            # Analyze numeric patterns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Look for calculation sequences
                for i in range(len(numeric_cols) - 1):
                    col1, col2 = numeric_cols[i], numeric_cols[i + 1]
                    # Check if there's a pattern (e.g., adding heights)
                    sample_values = df[[col1, col2]].dropna().head(5)
                    if len(sample_values) > 0:
                        patterns['calculations'].append(f"{col1} -> {col2}")
            
            calculation_patterns[sheet_name] = patterns
            
            print(f"   📏 Measurements: {len(patterns['measurements'])} columns")
            print(f"   🧱 Layers: {len(patterns['layers'])} columns")
            print(f"   🧮 Calculations: {len(patterns['calculations'])} patterns")
            print(f"   📅 Dates: {len(patterns['dates'])} columns")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return calculation_patterns

def extract_business_rules(file_path):
    """Extract business rules from the Excel data"""
    print("\n📋 Extracting Business Rules...")
    print("=" * 60)
    
    rules = {
        'pavers': {
            'layers': ['Paver Height', 'Fines', 'CA11', 'Entire Depth'],
            'calculations': ['Add paver height', 'Add fines & pavers height', 'Add paver, fines, CA11 height'],
            'measurements': ['Feet', 'Inches', 'Total']
        },
        'walls': {
            'layers': ['Wall Height', 'Base', 'Foundation'],
            'calculations': ['Wall calculations', 'Base calculations'],
            'measurements': ['Height', 'Width', 'Length']
        },
        'stairs': {
            'layers': ['Step Height', 'Riser', 'Tread'],
            'calculations': ['Step calculations', 'Stair calculations'],
            'measurements': ['Rise', 'Run', 'Total Height']
        }
    }
    
    return rules

if __name__ == "__main__":
    file_path = "Elevations for Jobs Worksheet 2025.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        exit(1)
    
    # Deep analysis
    patterns = deep_analyze_calculations(file_path)
    
    # Extract business rules
    rules = extract_business_rules(file_path)
    
    print("\n✅ Analysis complete!")
    print("📊 Patterns identified for job calculator development")
