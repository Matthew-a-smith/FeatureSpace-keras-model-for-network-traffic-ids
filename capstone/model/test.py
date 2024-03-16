import pandas as pd

# Read the CSV file
data = pd.read_csv("metaspoilt-ftp-connection.csv")

# Define columns to drop
columns_to_drop = ['tcp.dstport', 'tcp.srcport', 'date', 'time', 'ip.dst', 'ip.src', 'tcp.dstport', 'tcp.srcport',]  # Replace with the names of columns to drop

# Drop the specified columns
data.drop(columns=columns_to_drop, inplace=True)

# Save the modified data to a new CSV file
data.to_csv("modified_file.csv", index=False)

