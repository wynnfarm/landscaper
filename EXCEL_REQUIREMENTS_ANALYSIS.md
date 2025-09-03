
# Landscaping Application Requirements Analysis
Based on Excel file: Elevations for Jobs Worksheet 2025.xlsx

## Overview
This document outlines the requirements extracted from the Excel worksheet for integration into the landscaping application.

## Data Structures


### Pavers Cal Table
- **Purpose**: [To be determined]
- **Rows**: 49
- **Columns**: 45

#### Fields:
- Name (object)
- Unnamed: 1 (object)
- Unnamed: 2 (object)
- Unnamed: 3 (object)
- Unnamed: 4 (object)
- Unnamed: 5 (object)
- Unnamed: 6 (float64)
- Unnamed: 7 (object)
- Unnamed: 8 (object)
- Unnamed: 9 (object)
- Unnamed: 10 (float64)
- Unnamed: 11 (object)
- Unnamed: 12 (object)
- Unnamed: 13 (object)
- Unnamed: 14 (float64)
- Unnamed: 15 (object)
- Unnamed: 16 (object)
- Unnamed: 17 (object)
- Unnamed: 18 (float64)
- Unnamed: 19 (object)
- Unnamed: 20 (object)
- Unnamed: 21 (object)
- Unnamed: 22 (float64)
- Unnamed: 23 (float64)
- Unnamed: 24 (float64)
- Unnamed: 25 (float64)
- Unnamed: 26 (float64)
- Unnamed: 27 (float64)
- Unnamed: 28 (object)
- Unnamed: 29 (object)
- Unnamed: 30 (object)
- Unnamed: 31 (float64)
- Unnamed: 32 (object)
- Unnamed: 33 (object)
- Unnamed: 34 (object)
- Unnamed: 35 (object)
- Unnamed: 36 (float64)
- Unnamed: 37 (object)
- Unnamed: 38 (object)
- Unnamed: 39 (object)
- Unnamed: 40 (float64)
- Unnamed: 41 (object)
- Unnamed: 42 (object)
- Unnamed: 43 (object)
- Unnamed: 44 (object)

#### Categorical Values:
- Unnamed: 2: [nan, 'Originals', 'Feet']
- Unnamed: 3: [nan, 'In', 0]
- Unnamed: 4: [nan, 'Inches']
- Unnamed: 5: [nan, 'Total', 0]
- Unnamed: 7: [nan, 'Paver Height - top of', '1/8 Over', 0.125]
- Unnamed: 8: [nan, '(Hand Calc)', 'Ft', 3, 1]
- Unnamed: 9: [nan, 'Inches', -35.875, -11.875]
- Unnamed: 11: [nan, 'Fines -  top of', 'Add paver height', 2.375, 2.5]
- Unnamed: 12: [nan, '(Hand Calc)', 'Ft', 4, 3, 2]
- Unnamed: 13: [nan, 'Inches', -45.5, -33.5, -21.5]
- Unnamed: 15: [nan, 'CA11 - top of', 'Add fines & pavers height', 3.625, 3.75]
- Unnamed: 16: [nan, '(Hand Calc)', 'Ft', 4, 3, 2]
- Unnamed: 17: [nan, 'Inches', -44.25, -32.25, -20.25]
- Unnamed: 19: [nan, 'Entire Depth - Under', 'Add paver, fines, CA11 height', 9.625, 9.75]
- Unnamed: 20: [nan, '(Hand Calc)', 'Ft', 4, 2]
- Unnamed: 21: [nan, 'Inches', -38.25, -14.25]
- Unnamed: 28: [nan, datetime.datetime(2023, 7, 18, 0, 0), 'Laser A', 4, 48, 3.25, 51.25, 'Difference + Original Numbers', 51.375]
- Unnamed: 29: [nan, 'Feet', 'Feet in Inches', 'Inches', 'Total', 'Difference', '(Hand Calc)', 'Ft', 4, 3, 2]
- Unnamed: 30: [nan, 'Inches', 3.375, 15.375, 27.375]
- Unnamed: 32: [nan, 'Fines -  top of', 'Add paver height', 2.375, 53.75]
- Unnamed: 33: [nan, '(Hand Calc)', 'Ft', 4, 3, 2]
- Unnamed: 34: [nan, 'Inches', 5.75, 17.75, 29.75]
- Unnamed: 37: [nan, 'CA11 - top of', 'Add fines & pavers height', 3.625, 55]
- Unnamed: 38: [nan, '(Hand Calc)', 'Ft', 4, 3, 2]
- Unnamed: 39: [nan, 'Inches', 7, 19, 31]
- Unnamed: 41: [nan, 'Entire Depth - Under', 'Add paver, fines, CA11 height', 9.625, 61]
- Unnamed: 42: [nan, '(Hand Calc)', 'Ft', 5, 4, 3]
- Unnamed: 43: [nan, 'Inches', 1, 13, 25]

### Wall Cal  Table
- **Purpose**: [To be determined]
- **Rows**: 62
- **Columns**: 49

#### Fields:
- Name (object)
- Unnamed: 1 (object)
- Unnamed: 2 (object)
- Unnamed: 3 (object)
- Unnamed: 4 (object)
- Unnamed: 5 (object)
- Unnamed: 6 (float64)
- Unnamed: 7 (object)
- Unnamed: 8 (object)
- Unnamed: 9 (object)
- Unnamed: 10 (float64)
- Unnamed: 11 (object)
- Unnamed: 12 (object)
- Unnamed: 13 (object)
- Unnamed: 14 (float64)
- Unnamed: 15 (object)
- Unnamed: 16 (object)
- Unnamed: 17 (object)
- Unnamed: 18 (float64)
- Unnamed: 19 (object)
- Unnamed: 20 (object)
- Unnamed: 21 (object)
- Unnamed: 22 (float64)
- Unnamed: 23 (object)
- Unnamed: 24 (object)
- Unnamed: 25 (object)
- Unnamed: 26 (float64)
- Unnamed: 27 (float64)
- Unnamed: 28 (float64)
- Unnamed: 29 (object)
- Unnamed: 30 (object)
- Unnamed: 31 (object)
- Unnamed: 32 (float64)
- Unnamed: 33 (object)
- Unnamed: 34 (object)
- Unnamed: 35 (object)
- Unnamed: 36 (object)
- Unnamed: 37 (object)
- Unnamed: 38 (object)
- Unnamed: 39 (object)
- Unnamed: 40 (float64)
- Unnamed: 41 (object)
- Unnamed: 42 (object)
- Unnamed: 43 (object)
- Unnamed: 44 (float64)
- Unnamed: 45 (object)
- Unnamed: 46 (object)
- Unnamed: 47 (object)
- Unnamed: 48 (object)

#### Categorical Values:
- Unnamed: 1: [nan, 'Description', 'Benchmark', 'Wall Numbers', 15, 16, 17, 18, 19, 20]
- Unnamed: 2: [nan, 'Feet', 'Base Paver Olde Quarry - Double number if buring 2', 'Universal base Units', 'Fines', 'CA11', 0]
- Unnamed: 3: [nan, 'In', 0]
- Unnamed: 4: [nan, 'Inches', 0]
- Unnamed: 5: [nan, 'Total', 0]
- Unnamed: 7: [nan, 'Paver Height - top of', 0]
- Unnamed: 8: [nan, '(Hand Calc)', 'Ft', 3]
- Unnamed: 9: [nan, 'Inches', -36]
- Unnamed: 11: [nan, 'UBU -  top of', '1 Block', 4.5, '2 Blocks', 9, 13.5]
- Unnamed: 12: [nan, '(Hand Calc)', 'Ft', 3]
- Unnamed: 13: [nan, 'Inches', -31.5, -27, -22.5]
- Unnamed: 15: [nan, 'Fines - top of', 'Add pvr & UBU height', 6.75, 11.25, 15.75]
- Unnamed: 16: [nan, '(Hand Calc)', 'Ft', 3, 4]
- Unnamed: 17: [nan, 'Inches', -29.25, -41.25, -24.75, -36.75, -20.25, -32.25]
- Unnamed: 19: [nan, 'CA11 - top of', 'Add pvr, UBU, & fines height', 8, 12.5, 17]
- Unnamed: 20: [nan, '(Hand Calc)', 'Ft', 3, 4]
- Unnamed: 21: [nan, 'Inches', -28, -40, -23.5, -35.5, -19, -31]
- Unnamed: 23: [nan, 'Entire Depth - Under', 'Add pvr, UBU, fines, & CA11 height', 14, 18.5, 23]
- Unnamed: 24: [nan, '(Hand Calc)', 'Ft', 4]
- Unnamed: 25: [nan, 'Inches', -34, -29.5, -25]
- Unnamed: 29: [nan, 'Laser A', 0, 'Paver Height - top of', datetime.time(0, 0)]
- Unnamed: 30: [nan, '(Hand Calc)', 'Ft', 3]
- Unnamed: 31: [nan, 'Inches', -36]
- Unnamed: 33: [nan, 'One Block', 'UBU -  top of', 'Add pvr', 4.5, '2 Blocks', 9, '3 Blocks', 13.5]
- Unnamed: 34: [nan, '(Hand Calc)', 'Ft', 3, 4]
- Unnamed: 35: [nan, 'Inches', -31.5, -43.5, -27, -39, -22.5, -34.5]
- Unnamed: 36: [nan, 'Wall Numbers', 15, 16, 17, 18, 19, 20]
- Unnamed: 37: [nan, 'Fines - top of', 'Add pvr & UBU height', 6.75, 11.25, 15.75]
- Unnamed: 38: [nan, '(Hand Calc)', 'Ft', 4, 3]
- Unnamed: 39: [nan, 'Inches', -41.25, -29.25, -36.75, -32.25]
- Unnamed: 41: [nan, 'One Block', 'CA11 - top of', 'Add pvr, UBU, & fines height', 8, '2 Blocks', 12.5, '3 Blocks', 17]
- Unnamed: 42: [nan, '(Hand Calc)', 'Ft', 4, 3]
- Unnamed: 43: [nan, 'Inches', -40, -28, -35.5, -31]
- Unnamed: 45: [nan, 'Entire Depth - Under', 'Add pvr, UBU, fines, & CA11 height', 14, 18.5, 23]
- Unnamed: 46: [nan, '(Hand Calc)', 'Ft', 4]
- Unnamed: 47: [nan, 'Inches', -34, -29.5, -25]
- Unnamed: 48: [nan, 'Wall Numbers', 15, 16, 17, 18, 19, 20]

### UCara Steps Table
- **Purpose**: [To be determined]
- **Rows**: 39
- **Columns**: 25

#### Fields:
- Unnamed: 0 (object)
- Unnamed: 1 (object)
- Unnamed: 2 (object)
- Unnamed: 3 (float64)
- Unnamed: 4 (float64)
- Unnamed: 5 (object)
- Unnamed: 6 (object)
- Unnamed: 7 (object)
- Unnamed: 8 (object)
- Unnamed: 9 (float64)
- Unnamed: 10 (object)
- Unnamed: 11 (object)
- Unnamed: 12 (object)
- Unnamed: 13 (object)
- Unnamed: 14 (float64)
- Unnamed: 15 (float64)
- Unnamed: 16 (float64)
- Unnamed: 17 (float64)
- 2023-07-14 00:00:00 (object)
- Unnamed: 19 (object)
- Unnamed: 20 (object)
- Unnamed: 21 (object)
- Unnamed: 22 (object)
- Unnamed: 23 (object)
- Unnamed: 24 (object)

#### Categorical Values:
- Unnamed: 5: [nan, 'Feet', 1]
- Unnamed: 6: [nan, 'Standard Steps', 2.75, 5.875, 2.25, 1.25, 6, 18.125, 'In', 12, 0]
- Unnamed: 7: [nan, 'Ledgestone', 'Height of Backers', 'Universal Base Units', 'Fines', 'CA11 - 12" Under Stairs, Can Change', 'Total', 'Inches', 11.375]
- Unnamed: 11: [nan, '(Hand Calc)', 'Ft', 3, 4, 6, 7, 5]
- Unnamed: 13: [nan, 'Ledgestone', 'Height of Backers', 'Universal Base Units', 'Fines', 'CA11 - 12" Under Stairs, Can Change', 'Total']
- Unnamed: 19: ['***The Difference from previous Day', nan, 'Feet', 'Feet in Inches', 'Inches', 'Total', 'Difference', '(Hand Calc)', 'Ft', 2, 4, 5, 6, 3]
- Unnamed: 20: [nan, 'Inches', 3.375, 6.125, 11.5, 1.75, 3, 0, 2.25, 3.5, 9.5, 0.25, 8.375, 9.625, 3.625, 6.375, 9.75]
- Unnamed: 22: [nan, 'Day 1 ', 4, 48, 3.25, 51.25, 0]
- Unnamed: 23: [nan, 4, '(Hand Calc)', 'Ft']
- Unnamed: 24: [nan, 'Inches', 0]

### Stairs Olde Quarry Table
- **Purpose**: [To be determined]
- **Rows**: 38
- **Columns**: 55

#### Fields:
- Unnamed: 0 (object)
- Unnamed: 1 (object)
- Unnamed: 2 (object)
- Unnamed: 3 (object)
- Unnamed: 4 (object)
- Unnamed: 5 (object)
- Unnamed: 6 (float64)
- BACK WALL (object)
- Unnamed: 8 (object)
- Unnamed: 9 (object)
- Unnamed: 10 (float64)
- Unnamed: 11 (object)
- Unnamed: 12 (object)
- Unnamed: 13 (object)
- Unnamed: 14 (float64)
- Unnamed: 15 (object)
- Unnamed: 16 (object)
- Unnamed: 17 (object)
- Unnamed: 18 (float64)
- Unnamed: 19 (object)
- Unnamed: 20 (object)
- Unnamed: 21 (object)
- Unnamed: 22 (float64)
- Unnamed: 23 (object)
- Unnamed: 24 (object)
- Unnamed: 25 (object)
- Unnamed: 26 (float64)
- Unnamed: 27 (object)
- Unnamed: 28 (object)
- Unnamed: 29 (object)
- Unnamed: 30 (float64)
- Unnamed: 31 (float64)
- 2022-10-05 00:00:00 (object)
- Unnamed: 33 (object)
- Unnamed: 34 (object)
- Unnamed: 35 (float64)
- Unnamed: 36 (object)
- Unnamed: 37 (object)
- Unnamed: 38 (object)
- Unnamed: 39 (float64)
- Unnamed: 40 (object)
- Unnamed: 41 (object)
- Unnamed: 42 (object)
- Unnamed: 43 (float64)
- Unnamed: 44 (object)
- Unnamed: 45 (object)
- Unnamed: 46 (object)
- Unnamed: 47 (float64)
- Unnamed: 48 (object)
- Unnamed: 49 (object)
- Unnamed: 50 (object)
- Unnamed: 51 (float64)
- Unnamed: 52 (object)
- Unnamed: 53 (object)
- Unnamed: 54 (object)

#### Categorical Values:
- Unnamed: 2: [nan, 'Feet', 1]
- Unnamed: 3: [nan, 'In', 0, 12]
- Unnamed: 4: [nan, 'Inches', 0]
- Unnamed: 5: [nan, 'Total', 0, 12]
- BACK WALL: [2.75, 31.5, 2.25, 36.5, nan, 'Step Height - Height of Stairs', 0, 12]
- Unnamed: 8: ['Ledgestone', 'OQ (4.5*7Rows, Front is 6 Rows)', 'UBU', nan, '(Hand Calc)', 'Ft', 4, 1]
- Unnamed: 9: [nan, 'Inches', -48, -12, 0]
- Unnamed: 11: [nan, 'OQ - Top of', 'Add Height of Ledgestone', 2.75, 14.75]
- Unnamed: 12: [nan, '(Hand Calc)', 'Ft', 4, 1]
- Unnamed: 13: [nan, 'Inches', -45.25, -9.25, 2.75]
- Unnamed: 15: [nan, 'UBU - Top of ', 'Add Ledgestone & OQ', 11.75, 34.25, 23.75]
- Unnamed: 16: [nan, '(Hand Calc)', 'Ft', 7, 5, 1]
- Unnamed: 17: [nan, 'Inches', -49.75, -48.25, -0.25, 11.75]
- Unnamed: 19: [nan, 'Fines - Top of ', 'Add Ledge, OQ, & UBU height', 14, 36.5, 26]
- Unnamed: 20: [nan, '(Hand Calc)', 'Ft', 7, 5, 2]
- Unnamed: 21: [nan, 'Inches', -47.5, -46, -10, 2]
- Unnamed: 23: [nan, 'CA11 - Top of', 'Add Ledge, OQ, UBU, & Fines height', 15.25, 37.75, 27.25]
- Unnamed: 24: [nan, '(Hand Calc)', 'Ft', 7, 5, 2]
- Unnamed: 25: [nan, 'Inches', -46.25, -44.75, -8.75, 3.25]
- Unnamed: 27: [nan, 'Entire Depth - Under', 'Add pvr, UBU, fines, & CA11 height', 27.25, 49.75, 39.25]
- Unnamed: 28: [nan, '(Hand Calc)', 'Ft', 8, 6, 3]
- Unnamed: 29: [nan, 'Inches', -46.25, -44.75, -8.75, 3.25]
- 2022-10-05 00:00:00: ['Laser A', nan, 0, 6, 18, 'Step Height - Height of Landing', 30]
- Unnamed: 33: [nan, 'Feet', 'Feet in Inches', 'Inches', 'Total', 'Difference', '(Hand Calc)', 'Ft', 1]
- Unnamed: 34: [nan, 'Inches', 6, 18]
- Unnamed: 36: [nan, 'OQ - Top of', 'Add Height of Ledgestone', 2.75, 20.75, 32.75]
- Unnamed: 37: [nan, '(Hand Calc)', 'Ft', 1]
- Unnamed: 38: [nan, 'Inches', 8.75, 20.75]
- Unnamed: 40: [nan, 'UBU - Top of ', 'Add Ledgestone & OQ', 11.75, 29.75, 41.75]
- Unnamed: 41: [nan, '(Hand Calc)', 'Ft', 2]
- Unnamed: 42: [nan, 'Inches', 5.75, 17.75]
- Unnamed: 44: [nan, 'Fines - Top of ', 'Add Ledge, OQ, & UBU height', 14, 32, 44]
- Unnamed: 45: [nan, '(Hand Calc)', 'Ft', 2]
- Unnamed: 46: [nan, 'Inches', 8, 20]
- Unnamed: 48: [nan, 'CA11 - Top of', 'Add Ledge, OQ, UBU, & Fines height', 15.25, 33.25, 45.25]
- Unnamed: 49: [nan, '(Hand Calc)', 'Ft', 2]
- Unnamed: 50: [nan, 'Inches', 9.25, 21.25]
- Unnamed: 52: [nan, 'Entire Depth - Under', 'Add pvr, UBU, fines, & CA11 height', 27.25, 45.25, 57.25]
- Unnamed: 53: [nan, '(Hand Calc)', 'Ft', 4]
- Unnamed: 54: [nan, 'Inches', -2.75, 9.25]

### Pisa XL Stepped Stairs (Marik) Table
- **Purpose**: [To be determined]
- **Rows**: 43
- **Columns**: 55

#### Fields:
- Unnamed: 0 (object)
- Side 1 (object)
- Unnamed: 2 (object)
- Unnamed: 3 (object)
- Unnamed: 4 (object)
- Unnamed: 5 (object)
- Unnamed: 6 (float64)
- Unnamed: 7 (object)
- Unnamed: 8 (object)
- Unnamed: 9 (object)
- Unnamed: 10 (float64)
- Unnamed: 11 (object)
- Unnamed: 12 (object)
- Unnamed: 13 (object)
- Unnamed: 14 (float64)
- Unnamed: 15 (object)
- Unnamed: 16 (object)
- Unnamed: 17 (object)
- Unnamed: 18 (float64)
- Unnamed: 19 (object)
- Unnamed: 20 (object)
- Unnamed: 21 (object)
- Unnamed: 22 (float64)
- Unnamed: 23 (object)
- Unnamed: 24 (object)
- Unnamed: 25 (object)
- Unnamed: 26 (float64)
- Unnamed: 27 (object)
- Unnamed: 28 (object)
- Unnamed: 29 (object)
- Unnamed: 30 (object)
- Unnamed: 31 (float64)
- 2024-08-27 00:00:00 (object)
- Unnamed: 33 (object)
- Unnamed: 34 (object)
- Unnamed: 35 (float64)
- Unnamed: 36 (object)
- Unnamed: 37 (object)
- Unnamed: 38 (object)
- Unnamed: 39 (float64)
- Unnamed: 40 (object)
- Unnamed: 41 (object)
- Unnamed: 42 (object)
- Unnamed: 43 (float64)
- Unnamed: 44 (object)
- Unnamed: 45 (object)
- Unnamed: 46 (object)
- Unnamed: 47 (float64)
- Unnamed: 48 (object)
- Unnamed: 49 (object)
- Unnamed: 50 (object)
- Unnamed: 51 (float64)
- Unnamed: 52 (object)
- Unnamed: 53 (object)
- Unnamed: 54 (object)

#### Categorical Values:
- Unnamed: 2: [nan, 'Feet', 2]
- Unnamed: 3: [nan, 'In', 24, 0]
- Unnamed: 4: [nan, 'Inches', 9.5]
- Unnamed: 5: [nan, 'Total', 33.5, 0]
- Unnamed: 7: [nan, 'Step Height - Height of Stairs', 0, 33.5]
- Unnamed: 8: [nan, '(Hand Calc)', 'Ft', 2, 4, 1, 0, 3, 5]
- Unnamed: 9: [nan, 'Inches', 9.5, -48, -12, 0, -36, -60]
- Unnamed: 11: [nan, 'OQ - Top of', 'Add Height of Pisa Coping', 3, 36.5, 0]
- Unnamed: 12: [nan, '(Hand Calc)', 'Ft', 3, 4, 1, 0, 5]
- Unnamed: 13: [nan, 'Inches', 0.5, -45, -9, 0, -36, -48, -60]
- Unnamed: 15: [nan, 'UBU - Top of ', 'Add Pisa & Pisa XL', 38.25, 71.75, 5.875]
- Unnamed: 16: [nan, '(Hand Calc)', 'Ft', 5, 1, 0, 3, 4]
- Unnamed: 17: [nan, 'Inches', 11.75, -21.75, 26.25, 0, -30.125, -42.125, -54.125]
- Unnamed: 19: [nan, 'Total Heights', 'Fines - Top of ', 'Add Ledge, OQ, & UBU height', 40.5, 74, 8.125]
- Unnamed: 20: [nan, '(Hand Calc)', 'Ft', 6, 5, 2, 0, 3, 4]
- Unnamed: 21: [nan, 'Inches', 2, -19.5, 16.5, 0, -27.875, -39.875, -51.875, -63.875]
- Unnamed: 23: [nan, 'CA11 - Top of', 'Add Ledge, OQ, UBU, & Fines height', 41.75, 75.25, 9.375]
- Unnamed: 24: [nan, '(Hand Calc)', 'Ft', 6, 5, 2, 3, 4]
- Unnamed: 25: [nan, 'Inches', 3.25, -18.25, 17.75, 0, -26.625, -38.625, -50.625, -62.625]
- Unnamed: 27: [nan, 'Entire Depth - Under', 'Add pvr, UBU, fines, & CA11 height', 47.75, 81.25, 15.375]
- Unnamed: 28: [nan, '(Hand Calc)', 'Ft', 7, 6, 3, 0, 4, 5]
- Unnamed: 29: [nan, 'Inches', -2.75, -24.25, 11.75, 0, -32.625, -44.625, -56.625, -68.625]
- Unnamed: 30: [nan, 'Block 1', 'Block 2', 'Block 3', 'Block 4', 'Block 5 ( 1/2 Buried)', 'Block 6 (fully Buried)']
- 2024-08-27 00:00:00: ['Laser A', 2, 24, 9.625, 33.625, 0.125, nan, 'Step Height - Height of Landing', 0, datetime.datetime(2024, 8, 27, 0, 0)]
- Unnamed: 33: [nan, 'Feet', 'Feet in Inches', 'Inches', 'Total', 'Difference', '(Hand Calc)', 'Ft', 2, 1, 3, 4, 5]
- Unnamed: 34: [nan, 'Inches', 9.625, -11.875, -2.375, -14.375, -26.375]
- Unnamed: 36: [nan, 'OQ - Top of', 'Add Height of Ledgestone', 3, 36.625, 3.125, 0, 33.625]
- Unnamed: 37: [nan, '(Hand Calc)', 'Ft', 3, 1, 2, 4, 5]
- Unnamed: 38: [nan, 'Inches', 0.625, -8.875, 9.625, -2.375, -14.375, -26.375]
- Unnamed: 40: [nan, 'UBU - Top of ', 'Add Ledgestone & OQ', 38.25, 71.875, 38.375, 5.875, 39.5]
- Unnamed: 41: [nan, '(Hand Calc)', 'Ft', 5, 2, 3, 4]
- Unnamed: 42: [nan, 'Inches', 11.875, 14.375, 3.5, -8.5, -20.5]
- Unnamed: 44: [nan, 'Fines - Top of ', 'Add Ledge, OQ, & UBU height', 40.5, 74.125, 40.625, 8.125, 41.75]
- Unnamed: 45: [nan, '(Hand Calc)', 'Ft', 6, 2, 3, 4, 5]
- Unnamed: 46: [nan, 'Inches', 2.125, 16.625, 5.75, -6.25, -18.25, -30.25]
- Unnamed: 48: [nan, 'CA11 - Top of', 'Add Ledge, OQ, UBU, & Fines height', 41.75, 75.375, 41.875, 9.375, 43]
- Unnamed: 49: [nan, '(Hand Calc)', 'Ft', 6, 2, 3, 4, 5]
- Unnamed: 50: [nan, 'Inches', 3.375, 17.875, 7, -5, -17, -29]
- Unnamed: 52: [nan, 'Entire Depth - Under', 'Add pvr, UBU, fines, & CA11 height', 47.75, 81.375, 50.875, 15.375, 49]
- Unnamed: 53: [nan, '(Hand Calc)', 'Ft', 7, 4, 5, 6]
- Unnamed: 54: [nan, 'Inches', -2.625, 2.875, 1, -11, -23, -35]

### Sheet3 Table
- **Purpose**: [To be determined]
- **Rows**: 25
- **Columns**: 2

#### Fields:
- Unnamed: 0 (object)
- Unnamed: 1 (object)

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
