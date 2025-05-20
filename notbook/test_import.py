import sys
import os

project_root = r'C:\Users\tsion\OneDrive\Desktop\solar-challenge-week1'
os.chdir(project_root)
sys.path.append(project_root)

# Try importing the analysis package
try:
    import analysis
    print("Imported 'analysis' package successfully!")
except Exception as e:
    print("Error importing 'analysis':", e)

# Try importing perform_eda directly
try:
    from analysis import perform_eda
    print("Imported 'perform_eda' successfully!")
except Exception as e:
    print("Error importing 'perform_eda':", e)