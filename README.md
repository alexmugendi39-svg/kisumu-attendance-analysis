# Kisumu School Attendance vs Infrastructure

**Question:** Do schools with more classrooms have better attendance rates?

**Finding:** Schools in Kisumu with more classrooms have higher attendance rates, with a strong positive correlation (r ≈ 0.89), suggesting that reducing classroom congestion is associated with students coming to school more regularly.

## Files
- `kisumu_analysis.py` - Cleaning, merging, correlation and plot
- `kisumu_attendance_vs_classrooms.png` - Scatter plot

## Cleaning done
- Standardized school names (lowercase, removed "School", trimmed spaces) to allow merging
- Removed 2 duplicate rows
- Dropped 1 school with missing attendance data