import subprocess
import csv
import pandas as pd
import tensorflow as tf
import json

def run_tshark_command(pcap_file):
    tshark_cmd = [
        "tshark",
        "-r", pcap_file,
        "-Y", "tcp",
        "-E", "header=y",
        "-T", "fields",
        "-E", "separator=,",
        "-e", "frame.time",
        "-e", "ip.dst",
        "-e", "ip.src",
        "-e", "tcp.dstport",
        "-e", "tcp.srcport",
        "-e", "tcp.window_size_value",
        "-e", "tcp.flags",
    ]
    process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, universal_newlines=True)
    return process

def process_pcap_to_csv(pcap_file):
    process = run_tshark_command(pcap_file)
    csv_data = []
    next(process.stdout)  # Skip the header line
    for line in process.stdout:
        fields = line.strip().split(',')
        csv_data.append({
            "date": fields[0],
            "time": fields[1],
            "ip.dst": fields[2],
            "ip.src": fields[3],
            "tcp.dstport": fields[4],
            "tcp.srcport": fields[5],
            "tcp.window_size_value": fields[6],
            "tcp.flags": fields[7]
        })
    process.terminate()
    return csv_data

def make_predictions(data, loaded_model, threshold=0.95):
    input_data = {name: tf.convert_to_tensor(data[name].values.reshape(-1, 1)) for name in data.columns if name not in ['ip.src', 'ip.dst']}
    predictions = loaded_model.predict(input_data)
    output_data = [{"Index": index, "Prediction": prediction * 100, "Details": entry}
                   for index, (prediction, entry) in enumerate(zip(predictions, data)) if prediction > threshold]
    return output_data

def get_top_predictions(predictions_data, top_n=10):
    top_predictions = predictions_data[:top_n]
    return top_predictions

# Manually provide the path to the PCAP file here
pcap_file = "/home/kali/Desktop/network-traffic/nmap-metaspoitable.pcap"

# Load your model
inference_model_path = "Models/Inferance/NMAP-inference_model.keras"
loaded_model = tf.keras.models.load_model(inference_model_path)

# Process the PCAP file and convert to CSV data
csv_data = process_pcap_to_csv(pcap_file)

# Make predictions
predictions = make_predictions(pd.DataFrame(csv_data), loaded_model)

# Write predictions to JSON file
predictions_filename = pcap_file.split('.')[0] + "_predictions.json"
with open(predictions_filename, 'w') as f:
    json.dump(predictions, f, indent=4)

print("Predictions above the threshold have been written to", predictions_filename)
