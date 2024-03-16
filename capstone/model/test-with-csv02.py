import json
import pandas as pd
import tensorflow as tf

# Load the inference model
ICMP_inference_model = "Models/Inferance/meter-preter-inference_model.keras"
loaded_model = tf.keras.models.load_model(ICMP_inference_model)

# Function to make prediction on the entire dataset
def make_predictions(data):
    input_data = {name: tf.convert_to_tensor(data[name].values.reshape(-1, 1)) for name in data.columns if name not in ['ip.src', 'ip.dst', 'tcp.dstport', 'tcp.srcport', 'date', 'time', 'ip.dst', 'ip.src', 'tcp.dstport', 'tcp.srcport']}
    predictions = loaded_model.predict(input_data)
    return predictions.flatten()

# Load data from CSV file
csv_file = "data/mixed-normal-march10.csv"  # Update with CSV file path
data = pd.read_csv(csv_file)

# Make predictions for the entire dataset
all_predictions = make_predictions(data)

# Set thresholds for printing and writing to JSON
write_threshold = 0.95

# Prepare output data for predictions above threshold
output_data = []
unique_ips_ports = set()

for index, prediction in enumerate(all_predictions):
    if prediction > write_threshold:
        ip_dst = str(data.at[index, 'ip.dst'])
        ip_src = str(data.at[index, 'ip.src'])
        tcp_dstport = int(data.at[index, 'tcp.dstport'])
        tcp_srcport = int(data.at[index, 'tcp.srcport'])

        # Add the combination of IP address and port to the set
        unique_ips_ports.add((ip_dst, tcp_dstport))
        unique_ips_ports.add((ip_src, tcp_srcport))

# Convert the set of tuples to a list of dictionaries
result = [{"ip": ip, "port": port} for ip, port in unique_ips_ports]

# Sort the result by port number
result.sort(key=lambda x: x["port"])

# Write the result to a new JSON file
with open('unique_ip_ports.json', 'w') as f:
    json.dump(result, f, indent=4)

print("Unique IP addresses and port numbers JSON file created successfully.")
