import os
from flask import Flask, render_template, request, jsonify
import data_processing_script as dps
import test as tst
import json
import tensorflow as tf

app = Flask(__name__)

# Load the models outside of the functions
nmap_1 = "capstone/app/Models/Inferance/NMAP-inference_model.keras"
nmap_2 = "capstone/app/Models/Inferance/NMAP-inference_model.keras"
meterpreter = "capstone/app/Models/Inferance/metaspoilt-ftp-inference_model.keras"
metasploit = "capstone/app/Models/Inferance/meter-preter-movement-inference_model.keras"
http_model = "capstone/app/Models/Inferance/http-traffic.keras"
Webscanners_IPs = "capstone/app/Models/Inferance/Webscanners-IPs-2024-04-08.keras"

loaded_models = {
    '1': tf.keras.models.load_model(nmap_1),
    '2': tf.keras.models.load_model(nmap_2),
    '3': tf.keras.models.load_model(meterpreter),  
    '4': tf.keras.models.load_model(metasploit),
    '5': tf.keras.models.load_model(http_model),
    '6': tf.keras.models.load_model(Webscanners_IPs)

}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_pcap', methods=['POST'])
def process_pcap():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    output_option = request.form.get('output')
    filename = 'capstone/app/data/csv/data-.pcap'
    file.save(filename)

    try:
        if output_option in ['1', '3', '5']:
            csv_file, predictions_file = dps.process_pcap_to_csv(filename, loaded_models[output_option])
        elif output_option in ['2', '4']:
            csv_file, predictions_file = dps.process_pcap_to_csv1(filename, loaded_models[output_option])
        
        elif output_option in ['6']:
            csv_file, predictions_file = tst.process_pcap_to_csv(filename, loaded_models[output_option])
            # Assuming http model loading and processing is done within the http module
        else:
            return jsonify({'error': 'Invalid output option'})
        
        with open(predictions_file) as f:
            full_json_data = json.load(f)
        
        return jsonify({'full_json_data': full_json_data})
    
    except Exception as e:
        os.remove(filename)
        app.logger.error(f"Error processing pcap file: {str(e)}")
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
