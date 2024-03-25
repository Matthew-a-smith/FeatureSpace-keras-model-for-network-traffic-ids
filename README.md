# Project built on kali linux

Dependencys
```
pip install tensorflow==2.15.0 
```

## Createing the model 

I broke up everything into multiply small scripts instead of of createing one huge script to take care of all the diffrent data,

**Wireshark_model.py**

This is the main script used to create the models slightly altered from the oringal version of the keras website,

https://keras.io/examples/structured_data/structured_data_classification_with_feature_space/

to make things more easy and streamline the process I created a config.yaml file to adjust the values from the model along with the file,
paths to the datasets to be used.

Each mode is created the sames as a typical IDS would be you first want to figure out what excect type of traffic,
it is you want to the model to look for.

the following example im going to use is nmap scan.

First I would gather the data in wireshark with a single address being monitored and just capture the nmap scan,
I captured the full handshake for a normal nmap scan of the top 1000 ports.

After getting the full scan from wire shark I then turned the pcap data into csv for my model and parsed it thru my processing script
pcap-processing.py, this script uses tshark to extract, more detailed and specfic feilds from the data then turns it into a csv format.

After getting the attack data i then needed just normal traffic to mix in with it for my model I dident need A massive amount of traffic just regular traffic that happens normallly,
across your network without the scan mixed in yet.

I created another script called capture.py and this is what i used to capture my normal traffic, it uses the same tshark feilds as my processing script,
but collects the data and saves it to csv as it runs so i dont  have to run wireshark and rerun the processing script.

(ITS EAISER TO SINGLE OUT MY SPECIFC IP ADDRESS FOR MY NMAP THRU WIRESHARK AND JUST GET THAT DATA ASCOTIED WITH,
 ITS REALLY IMPORTANT NOT TO CONTAMANTE YOUR DATA WITH DIFFRENT VALUES OUTSIDE OF WHAT YOU WANT TO CAPTURE (AKA NORMAL TRAFFIC MIXED IN WITH THE SCAN))

After getting the data and merging it together with merge.py, it will create the new label coloumn that has the binary encodeing,
for the nmap scan.

Since im not usieng a huge data set the the labled data was appended to the bottom to the bottom of my normal traffic,
then i would go into the csv and manually mix the data up with the nmap scan.

The file path and model parametres are configured thru the config.yaml make sure you change the values of,
feature space with the correct coloumn names from your data and adjust the feilds that are more important for the model,
to look at.

After adjuisting the values simply run wireshark_model.py

I also have a test script that your able to fine tune values and test the accuracy on diffrent results thru the config.yaml,
this way you dont have to test the models on a full csv file instead you can just fine tune the 3 diffrent samples and be able,
to test the models output on diffrent data more easier.

the 3 test with csv scripts are just takeing the newly created model and createing diffrent outputs of the data from the model.



