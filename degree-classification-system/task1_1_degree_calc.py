import pandas as pd
import re
import os

# Debug info (optional)
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Load CSV files
modules_df = pd.read_csv("cs modules.csv")
marks_df = pd.read_csv("task1_1_marks.csv")

# Extract credits and levels from module code
modules_df.columns = ['ModuleCode', 'ModuleName']
modules_df['Credits'] = modules_df['ModuleCode'].apply(lambda x: int(re.search(r'-(\d+)-', x).group(1)))
modules_df['Level'] = modules_df['ModuleCode'].apply(lambda x: int(x[-1]))

# Transform student marks to long format
student_records = []
for _, row in marks_df.iterrows():
    student_id = row.iloc[0]
    entries = row.iloc[1:].tolist()
    for i in range(0, len(entries), 2):
        try:
            module_code = entries[i]
            mark = float(entries[i + 1])
            student_records.append({
                'StudentID': student_id,
                'ModuleCode': module_code,
                'Mark': mark
            })
        except (IndexError, ValueError):
            continue

student_df = pd.DataFrame(student_records)

# Merge with module metadata
merged_df = pd.merge(student_df, modules_df, on='ModuleCode', how='left')
merged_df = merged_df.dropna(subset=['Credits', 'Level', 'Mark'])

# Degree calculation function
def calculate_degree_with_pass_check(student_data):
    student_id = student_data['StudentID'].iloc[0]

    if (student_data['Mark'] < 40).any():
        return pd.Series({
            'StudentID': student_id,
            'Level5 Average': None,
            'Level6 Average': None,
            'Final Mark': None,
            'Classification': "Fail"
        })

    level5 = student_data[student_data['Level'] == 2]
    level6 = student_data[student_data['Level'] == 3]

    # Level 5: Best 100 credits
    level5_sorted = level5.sort_values(by='Mark', ascending=False)
    total_credits = 0
    weighted_sum = 0
    for _, row in level5_sorted.iterrows():
        if total_credits + row['Credits'] <= 100:
            total_credits += row['Credits']
            weighted_sum += row['Mark'] * row['Credits']
        elif total_credits < 100:
            partial = 100 - total_credits
            total_credits += partial
            weighted_sum += row['Mark'] * partial
            break
    avg_level5 = weighted_sum / 100 if total_credits > 0 else 0

    # Level 6: All modules
    total_credits_l6 = level6['Credits'].sum()
    weighted_sum_l6 = (level6['Mark'] * level6['Credits']).sum()
    avg_level6 = weighted_sum_l6 / total_credits_l6 if total_credits_l6 > 0 else 0

    # Final Mark
    final_mark = (avg_level6 * 3 + avg_level5) / 4

    # Classification
    if final_mark >= 70:
        classification = "First Class"
    elif final_mark >= 60:
        classification = "Second Class (Upper Division)"
    elif final_mark >= 50:
        classification = "Second Class (Lower Division)"
    elif final_mark >= 40:
        classification = "Third Class"
    else:
        classification = "Fail"

    return pd.Series({
        'StudentID': student_id,
        'Level5 Average': round(avg_level5, 2),
        'Level6 Average': round(avg_level6, 2),
        'Final Mark': round(final_mark, 2),
        'Classification': classification
    })

# Run for all students
final_results_df = merged_df.groupby('StudentID').apply(calculate_degree_with_pass_check).reset_index(drop=True)

# Save to CSV
final_results_df.to_csv("degree_results_with_pass_check.csv", index=False)
print("✅ Degree results saved to 'degree_results_with_pass_check.csv'")
