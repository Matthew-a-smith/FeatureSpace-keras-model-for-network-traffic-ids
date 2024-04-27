import json
import pandas as pd
import tensorflow as tf
import os
import subprocess
import csv

def run_tshark_command(pcap_file):
    tshark_cmd = [
        "tshark",
        "-r", pcap_file,  # Specify the input pcap file
        "-Y", "tcp",      # Filter for TCP traffic
        "-E", "header=y",  # Add header to output
        "-T", "fields",  # Output fields
        "-E", "separator=,",  # CSV separator
        "-e", "frame.time",  # frame time
        "-e", "ip.dst",
        "-e", "ip.src",
        "-e", "tcp.dstport",
        "-e", "tcp.srcport",
        "-e", "tcp.flags",
        "-e", "tcp.window_size_value",
        "-e", "tcp.options.mss_val",
    ]
    # Capture TCP traffic using subprocess tcp.options.mss_val
    process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, universal_newlines=True)
    return process

########################
#### First Function ####
########################

def process_pcap_to_csv(pcap_file, loaded_models):
    process = run_tshark_command(pcap_file)

    csv_filename = pcap_file.split('.')[0] + ".csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = ["date", "time", "ip.dst", "ip.src", "tcp.dstport", "tcp.srcport", "tcp.flags", "tcp.window_size_value", "tcp.options.mss_val"]  # Define CSV header field names tcp.window_size_value
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        # Skip the first line containing the field names
        next(process.stdout)               
        for line in process.stdout:
            fields = line.strip().split(',')
            fields = [field if field else "0" for field in fields]
            row = {"date": fields[0],"time": fields[1], "ip.dst": fields[2], "ip.src": fields[3], "tcp.dstport": fields[4], "tcp.srcport": fields[5], "tcp.flags": fields[6], "tcp.window_size_value": fields[7], "tcp.options.mss_val": fields[8]}
            writer.writerow(row)
            csvfile.flush()  # Flush the buffer to ensure data is written to the file

    process.terminate()
    print("PCAP to CSV conversion completed.")

    # Function to make prediction on the entire dataset
    def make_predictions(data):
        input_data = {name: tf.convert_to_tensor(data[name].values.reshape(-1, 1)) for name in data.columns if name not in ['ip.src', 'ip.dst']}
        predictions = loaded_models.predict(input_data)
        return predictions.flatten()

    # Load data from CSV file
    data = pd.read_csv(csv_filename)

    # Make predictions for the entire dataset
    all_predictions = make_predictions(data)

    # Set thresholds for writing to JSON
    write_threshold = 0.95

    # Prepare output data for predictions above threshold
    output_data = []
    for index, prediction in enumerate(all_predictions):
        if prediction > write_threshold:
            output_data.append({"Index": index, "Prediction": prediction * 100, "Details": data.iloc[index].to_dict()})
        
    # Write predictions with additional information to a JSON file
    predictions_filename = pcap_file.split('.')[0] + "predictions.json"
    with open(predictions_filename, 'w') as f:
        json.dump(output_data, f, indent=4)

    print("Predictions above the threshold have been written to", predictions_filename)

    return csv_filename, predictions_filename

#########################
#### second function ####
#########################

def process_pcap_to_csv1(pcap_file, loaded_models):
    process = run_tshark_command(pcap_file)

    csv_filename = pcap_file.split('.')[0] + ".csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = ["date", "time", "ip.dst", "ip.src", "tcp.dstport", "tcp.srcport", "tcp.flags", "tcp.window_size_value", "tcp.options.mss_val"]  # Define CSV header field names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        # Skip the first line containing the field names
        next(process.stdout)
                
        for line in process.stdout:
            fields = line.strip().split(',')
            date_str = fields[0]
            time_str = fields[1]
            row = {"date": fields[0],"time": fields[1], "ip.dst": fields[2], "ip.src": fields[3], "tcp.dstport": fields[4], "tcp.srcport": fields[5], "tcp.flags": fields[6], "tcp.window_size_value": fields[7], "tcp.options.mss_val": fields[8]}
            writer.writerow(row)
            csvfile.flush()  # Flush the buffer to ensure data is written to the file

    process.terminate()

    print("PCAP to CSV conversion completed.")

    # Function to make prediction on the entire dataset
    def make_predictions(data):
        input_data = {name: tf.convert_to_tensor(data[name].values.reshape(-1, 1)) for name in data.columns if name not in ['ip.src', 'ip.dst']}
        predictions = loaded_models.predict(input_data)
        return predictions.flatten()

    # Load data from CSV file
    data = pd.read_csv(csv_filename)

    # Make predictions for the entire dataset
    all_predictions = make_predictions(data)

    # Set thresholds for printing and writing to JSON
    write_threshold = 0.95

    # Initialize a dictionary to store unique IP addresses and port counts
    unique_ips_ports = {}

    # Gather unique IP addresses and port numbers from predictions
    for index, prediction in enumerate(all_predictions):
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
    with open('capstone/app/data/csv/unique_ip_ports_count.json', 'w') as f:
        json.dump(result, f, indent=4)

    print("Unique IP addresses and number of ports scanned JSON file created successfully.")

    return csv_filename, 'capstone/app/data/csv/unique_ip_ports_count.json'
