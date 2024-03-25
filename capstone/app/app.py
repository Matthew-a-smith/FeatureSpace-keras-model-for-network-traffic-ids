import os
from flask import Flask, render_template, request, jsonify
import data_processing_script as dps
import data_processing_script_2 as dps2
import http_model as http
import json
app = Flask(__name__)

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
    filename = 'data/csv/data-.pcap'
    file.save(filename)

    try:
        if output_option == '1':
            csv_file, predictions_file = dps.process_pcap_to_csv(filename)
            with open(predictions_file) as f:
                full_json_data = json.load(f)
        elif output_option == '2':
            csv_file, json_file = dps.process_pcap_to_csv1(filename)
            with open(json_file) as f:
                full_json_data = json.load(f)
        elif output_option == '3':
            csv_file, predictions_file = dps2.process_pcap_to_csv(filename)
            with open(predictions_file) as f:
                full_json_data = json.load(f)
        elif output_option == '4':
            csv_file, json_file = dps2.process_pcap_to_csv2(filename)
            with open(json_file) as f:
                full_json_data = json.load(f)
        elif output_option == '5':
            csv_file, predictions_file = http.process_pcap_to_csv3(filename)
            with open(predictions_file) as f:
                full_json_data = json.load(f)
        else:
            return jsonify({'error': 'Invalid output option'})
        
        return jsonify({'full_json_data': full_json_data})
    
    except Exception as e:
        os.remove(filename)
        app.logger.error(f"Error processing pcap file: {str(e)}")
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True, host='192.168.4.143')
