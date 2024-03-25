import pandas as pd

# Read labeled and unlabeled data
labeled_data = pd.read_csv("ftp--metaspoilt1.csv")
unlabeled_data = pd.read_csv("test-traffic.csv")

# Assign label of 1 to the labeled data
labeled_data['label'] = 1

# Add a new column called "label" to the unlabeled data and assign zeros
unlabeled_data['label'] = 0

# Append labeled data to unlabeled data
merged_data = pd.concat([unlabeled_data, labeled_data], ignore_index=True)

# Drop specific columns from the merged data
#columns_to_drop = ['date', 'time', 'ip.dst', 'ip.src', 'tcp.dstport', 'tcp.srcport']  # Replace with the names of columns to drop
#merged_data.drop(columns=columns_to_drop, inplace=True,)

# Save the merged data
merged_data.to_csv("http-traffic.csv", index=False)
