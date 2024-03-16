import csv
import subprocess
import time

def capture_http_traffic():
    # Define the tshark command to capture HTTP traffic and output as CSV
    tshark_cmd = [
        "tshark",
        "-i", "wlan0",  # Specify the interface you want to capture traffic on
        "-Y", "http",  # Filter for HTTP traffic
        "-E", "header=y",  # Add header to output
        "-T", "fields",  # Output fields
        "-E", "separator=,",  # CSV separator
        "-e", "frame.time",  # Add frame time
        "-e", "ip.dst",
        "-e", "ip.src",
        "-e", "http.request.method",  # Include HTTP request method
        "-e", "http.request.uri",  # Include HTTP request URI
        "-e", "http.response.code",  # Include HTTP response code
        "-e", "http.user_agent",  # Include user agent
    ]

    # Open CSV file for writing
    with open("http_traffic.csv", "w", newline="") as csvfile:
        fieldnames = ["date", "time", "ip.dst", "ip.src", "http.request.method", "http.request.uri", "http.response.code", "http.user_agent"]  # Define CSV header field names
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
                    row = {"date": fields[0],"time": fields[1], "ip.dst": fields[2], "ip.src": fields[3], "http.request.method": fields[4], "http.request.uri": fields[5], "http.response.code": fields[6], "http.user_agent": fields[7]}
                    writer.writerow(row)
                    csvfile.flush()  # Flush the buffer to ensure data is written to the file
                time.sleep(5)  # Sleep for 5 seconds before capturing again
        except KeyboardInterrupt:
            print("\nHTTP traffic capture stopped.")

if __name__ == "__main__":
    capture_http_traffic()
