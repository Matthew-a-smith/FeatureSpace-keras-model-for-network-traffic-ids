# otx plugin
# use with merge.py to create seprate models from diffrent pulses
# capture.py should be used to create the normal traffic for the models datas
# 
import csv

# Your code to retrieve indicators goes here
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes

otx = OTXv2("--API Key--")
# Get all the indicators associated with a pulse
indicators = otx.get_pulse_indicators("--Pulse ID--")

# Define the file name for the CSV file
output_file = "output_indicators.csv"

# Write the output data to a CSV file
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write each indicator to the CSV file
    for indicator in indicators:
        writer.writerow([indicator["indicator"]])

print("Output saved to", output_file)

# Get everything OTX knows about google.com
#otx.get_indicator_details_full(IndicatorTypes.DOMAIN, "google.com")