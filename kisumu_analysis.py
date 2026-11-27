import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# STEP 1: Create two messy sample DataFrames
# --------------------------------------------------

# File 1: Attendance records
attendance = pd.DataFrame({
    "school name": [  # Note: lowercase + space, different from file 2
        "Kisumu Primary",
        "Maseno High School",
        "KISUMU PRIMARY ",  # Naming inconsistency 1: case + extra space
        "Nyakach Girls",
        "Muhoroni Primary School", # Naming inconsistency 2: extra word "School"
        "Kisumu Primary", # Duplicate row
        "Ahero Primary",
        "Kajulu High",
        "Kombewa Primary",
        "Seme Secondary"
    ],
    "average_attendance_pct": [88, 92, 88, 75, 81, 88, 68, 95, 78, np.nan], # Missing value
    "county": ["Kisumu"] * 10
})

# File 2: Infrastructure data
infrastructure = pd.DataFrame({
    "school_name": [ # Note: underscore, different from file 1
        "Kisumu Primary School",
        "Maseno High",
        "Nyakach Girls School",
        "Muhoroni Primary",
        "Ahero Primary School",
        "Kajulu High School",
        "Kombewa Primary School",
        "Seme Secondary School",
        "Pap Onditi Primary",
        "Kisumu Primary School" # Duplicate row
    ],
    "num_classrooms": [12, 18, 8, 10, 6, 20, 9, 14, 7, 12],
    "water_access": ["Yes", "Yes", "No", "Yes", "No", "Yes", "Yes", "Yes", "No", "Yes"]
})

print("BEFORE CLEANING")
print(f"Attendance: {len(attendance)} rows")
print(f"Infrastructure: {len(infrastructure)} rows")
print(attendance.head())
print(infrastructure.head())

# --------------------------------------------------
# STEP 2: Clean
# --------------------------------------------------

def clean_name(name):
    """Standardize school names so they can merge"""
    name = str(name).lower().strip()  # lower + remove extra spaces
    name = name.replace(" school", "").replace(" primary", "").replace(" secondary", "").replace(" high", "")
    name = name.replace("  ", " ") # remove double spaces
    return name.strip()

# Apply to both
attendance["school_clean"] = attendance["school name"].apply(clean_name)
infrastructure["school_clean"] = infrastructure["school_name"].apply(clean_name)

# Remove duplicates - keep first occurrence
attendance = attendance.drop_duplicates(subset=["school_clean"], keep="first")
infrastructure = infrastructure.drop_duplicates(subset=["school_clean"], keep="first")

# Handle missing values - drop schools with no attendance (can't analyze them)
attendance = attendance.dropna(subset=["average_attendance_pct"])

print("\nAFTER CLEANING")
print(f"Attendance: {len(attendance)} rows")
print(f"Infrastructure: {len(infrastructure)} rows")

# --------------------------------------------------
# STEP 3: Merge on common key (school_clean)
# --------------------------------------------------
merged = pd.merge(attendance, infrastructure, on="school_clean", how="inner")

print(f"\nMerged: {len(merged)} rows")
print(merged[["school_clean", "average_attendance_pct", "num_classrooms", "water_access"]])

# --------------------------------------------------
# STEP 4: Answer the question - correlation + scatter
# --------------------------------------------------
correlation = merged["num_classrooms"].corr(merged["average_attendance_pct"])
print(f"\nCorrelation between classrooms and attendance: {correlation:.2f}")

# Scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(merged["num_classrooms"], merged["average_attendance_pct"], s=100, color="#1f77b4")

# Add trend line
z = np.polyfit(merged["num_classrooms"], merged["average_attendance_pct"], 1)
p = np.poly1d(z)
plt.plot(merged["num_classrooms"], p(merged["num_classrooms"]), color="red", linestyle="--")

plt.title("Kisumu: Do More Classrooms Mean Better Attendance?")
plt.xlabel("Number of Classrooms")
plt.ylabel("Average Attendance (%)")
plt.grid(True, alpha=0.3)

# Label each point
for i, row in merged.iterrows():
    plt.annotate(row["school_clean"], (row["num_classrooms"], row["average_attendance_pct"]), fontsize=8, xytext=(5, 5), textcoords="offset points")

plt.tight_layout()
plt.savefig("kisumu_attendance_vs_classrooms.png")
plt.show()

print("\nPlot saved as kisumu_attendance_vs_classrooms.png")