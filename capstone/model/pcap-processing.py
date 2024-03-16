import subprocess
import csv

def process_pcap_to_csv(pcap_file, csv_file):
    # Define the tshark command to read pcap file and output as CSV
    tshark_cmd = [
        "tshark",
        "-r", pcap_file,  # Specify the input pcap file
        "-Y", "tcp",      # Filter for TCP traffic
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
        "-e", "tcp.checksum",

    ]

    # Capture TCP traffic using subprocess
    process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, universal_newlines=True)

    # Open CSV file for writing
    with open(csv_file, "w", newline="") as csvfile:
        fieldnames = ["date", "time", "ip.dst", "ip.src", "tcp.dstport", "tcp.srcport", "tcp.window_size_value", "tcp.flags", "tcp.checksum"]  # Define CSV header field names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        # Skip the first line containing the field names
        next(process.stdout)
                
        for line in process.stdout:
            fields = line.strip().split(',')
            date_str = fields[0]
            time_str = fields[1]
            row = {"date": fields[0],"time": fields[1], "ip.dst": fields[2], "ip.src": fields[3], "tcp.dstport": fields[4], "tcp.srcport": fields[5], "tcp.window_size_value": fields[6], "tcp.flags": fields[7], "tcp.checksum": fields[8]}
            writer.writerow(row)
            csvfile.flush()  # Flush the buffer to ensure data is written to the file


    # Close the subprocess after capturing is done
    process.terminate()

    print("PCAP to CSV conversion completed.")

if __name__ == "__main__":
    pcap_file = "smb-connection.pcap"  # Replace with your pcap file path
    csv_file = "smb-connection.csv"   # Specify the output CSV file path
    process_pcap_to_csv(pcap_file, csv_file)

