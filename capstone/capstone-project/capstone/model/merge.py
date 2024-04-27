import pandas as pd
import yaml

# Read the specific destination address from config.yaml
with open('capstone/model/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
specific_dst = config['Network_address']

# Read the first CSV file (network traffic data)
network_traffic = pd.read_csv("normal_traffic.csv", usecols=['ip.dst', 'ip.src'])

# Read the second CSV file (pulses from alien vault)
alien_pulses = pd.read_csv("output_indicators.csv", header=None, names=['ip'])

# Create a DataFrame for the alien vault data with 'src' and 'dst' columns
alien_vault_data = pd.DataFrame({'ip.src': alien_pulses['ip'], 'ip.dst': specific_dst, 'label': 1})

# Create empty DataFrames for network traffic data
network_traffic['label'] = 0
network_traffic = network_traffic.rename(columns={'ip.src': 'ip.src', 'ip.dst': 'ip.dst'})

# Concatenate the network traffic data with the alien vault data
combined = pd.concat([network_traffic, alien_vault_data], ignore_index=True)
# Shuffle the combined DataFrame
combined = combined.sample(frac=1).reset_index(drop=True)
# Save the combined data to a new CSV file
combined.to_csv("combined_data.csv", index=False)
