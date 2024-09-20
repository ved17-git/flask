import pandas as pd

# Load the provided CSV file
file_path = 'C:\Users\manoj\Desktop\Mini_Project\project.csv'
movies_df = pd.read_csv(file_path)

# Display the first few rows to understand its structure
movies_df.head()
