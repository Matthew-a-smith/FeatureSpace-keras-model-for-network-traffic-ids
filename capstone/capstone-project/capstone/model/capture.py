import csv
import subprocess
import time
import yaml

def capture_http_traffic():
    # Read the specific destination address from config.yaml
    with open('capstone/model/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    specific_dst = config['Network_address']

    # Define the tshark command to capture HTTP traffic and output as CSV
    tshark_cmd = [
        "tshark",
        "-i", "wlan0",  # Specify the interface you want to capture traffic on
        "-Y", f"ip.addr == {specific_dst}",  # Filter for traffic with the specific destination address
        "-E", "header=y",  # Add header to output
        "-T", "fields",  # Output fields
        "-E", "separator=,",  # CSV separator
        "-e", "frame.time",  # Add frame time
        "-e", "ip.dst",
        "-e", "ip.src",
        "-e", "tcp.dstport",
        "-e", "tcp.srcport",
        "-e", "tcp.window_size_value",
        "-e", "tcp.flags",
    ]

    # Open CSV file for writing
    with open("normal_traffic.csv", "w", newline="") as csvfile:
        fieldnames = ['date', 'time', 'ip.dst', 'ip.src', 'tcp.dstport', 'tcp.srcport', 'tcp.window_size_value', 'tcp.flags']  # Define CSV header field names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        # Continuously capture HTTP traffic and write to CSV
        try:
            while True:
                # Use subprocess.Popen to capture output
                process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, universal_newlines=True)
                
                # Skip the first line containing the field names
                next(process.stdout)
                
                for line in process.stdout:
                    fields = line.strip().split(',')
                    
                    # Fill in empty fields with "NaN"
                    for i in range(len(fieldnames)):
                        if i < len(fields):
                            fields[i] = fields[i].strip()
                        else:
                            fields.append("NaN")
                    
                    date_str = fields[0]
                    time_str = fields[1]
                    row = {"date": fields[0], "time": fields[1], "ip.dst": fields[2], "ip.src": fields[3], "tcp.dstport": fields[4], "tcp.srcport": fields[5], "tcp.window_size_value": fields[6], "tcp.flags": fields[7]}
                    writer.writerow(row)
                    csvfile.flush()  # Flush the buffer to ensure data is written to the file
                time.sleep(5)  # Sleep for 5 seconds before capturing again
        except KeyboardInterrupt:
            print("\ntraffic capture stopped.")

if __name__ == "__main__":
    capture_http_traffic()
