import json
import pandas as pd
import tensorflow as tf

# Load the inference model
inference_model_path = "live-model/Models/Inferance/meter-preter-movement-inference_model.keras"
loaded_model = tf.keras.models.load_model(inference_model_path)

# Function to make prediction on the entire dataset
def make_predictions(data):
    input_data = {name: tf.convert_to_tensor(data[name].values.reshape(-1, 1)) for name in data.columns if name not in ['ip.src', 'ip.dst']}
    predictions = loaded_model.predict(input_data)
    return predictions.flatten()

# Load data from CSV file
csv_file = "movement.csv"
data = pd.read_csv(csv_file)

# Make predictions
predictions = make_predictions(data)

# Set thresholds for printing and writing to JSON
write_threshold = 0.95

# Initialize a dictionary to store unique IP addresses and port counts
unique_ips_ports = {}

# Gather unique IP addresses and port numbers from predictions
for index, prediction in enumerate(predictions):
    if prediction > write_threshold:
        ip_dst = str(data.at[index, 'ip.dst'])
        tcp_dstport = int(data.at[index, 'tcp.dstport'])
        
        # Add IP address if not present, otherwise increment port count
        if ip_dst not in unique_ips_ports:
            unique_ips_ports[ip_dst] = set()
        unique_ips_ports[ip_dst].add(tcp_dstport)

# Convert dictionary to list of dictionaries
result = [{"ip": ip, "ports_scanned": len(ports)} for ip, ports in unique_ips_ports.items()]

# Write the result to a new JSON file
with open('unique_ip_ports_count.json', 'w') as f:
    json.dump(result, f, indent=4)

print("Unique IP addresses and number of ports scanned JSON file created successfully.")

# Prepare output data for predictions above threshold
output_data = []
for index, prediction in enumerate(predictions):
    if prediction > write_threshold:
        output_data.append({"Index": index, "Prediction": prediction * 100, "Details": data.iloc[index].to_dict()})
        
# Write predictions with additional information to a JSON file
output_file = "predictions.json"
with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=4)

print("Predictions above the threshold have been written to", output_file)
