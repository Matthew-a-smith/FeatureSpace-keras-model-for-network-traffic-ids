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
        "-e", "tcp.window_size_value",
        "-e", "tcp.flags",
        "-e", "tcp.options.mss_val",
    ]

    # Capture TCP traffic using subprocess
    process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, universal_newlines=True)

    # Open CSV file for writing
    with open(csv_file, "w", newline="") as csvfile:
        fieldnames = ["tcp.window_size_value", "tcp.flags", "tcp.options.mss_val"]  # Define CSV header field names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        # Skip the first line containing the field names
        next(process.stdout)
                
        for line in process.stdout:
            fields = line.strip().split(',')
            # Fill empty fields with 0
            fields = [field if field else "0" for field in fields]
            row = {"tcp.window_size_value": fields[0], "tcp.flags": fields[1], "tcp.options.mss_val": fields[2]}
            writer.writerow(row)
            csvfile.flush()  # Flush the buffer to ensure data is written to the file

    # Close the subprocess after capturing is done
    process.terminate()

    print("PCAP to CSV conversion completed.")

if __name__ == "__main__":
    pcap_file = "mixed-normal-march10.pcap"  # Replace with your pcap file path
    csv_file = "mixed-normal-march10.csv"   # Specify the output CSV file path
    process_pcap_to_csv(pcap_file, csv_file)
