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

After getting the data and merging it together with merge.py, it will create the new label coloumn that has the binary encodeing,
for the nmap scan.

**merge.py**

![merge](https://github.com/Matthew-a-smith/capstone-project/assets/109995724/31c94e81-0146-4e79-a783-d055a4977d43)


Since im not useing a huge data set the the labled data was appended to the bottom to the bottom of my normal traffic,
then i would go into the csv and manually mix the data up with the nmap scan.

**Output datasest**

![data--set](https://github.com/Matthew-a-smith/capstone-project/assets/109995724/616adaab-819a-49e8-89a5-638faeff6bd9)


The file path and model parametres are configured thru the config.yaml make sure you change the values of,
feature space with the correct coloumn names from your data and adjust the feilds that are more important for the model,
to look at.

After adjuisting the values simply run wireshark_model.py

I also have a test script that your able to fine tune values and test the accuracy on diffrent results thru the config.yaml,
this way you dont have to test the models on a full csv file instead you can just fine tune the 3 diffrent samples and be able,
to test the models output on diffrent data more easier.

the 3 test with csv scripts are just takeing the newly created model and createing diffrent outputs of the data from the model.

## FlaskAPP

I combined all the fucntions from the scripts that I just disscused into a flask app Were the backend consits of useing the diffrent models to parse any pcap or pcapng file.

Just upload the pcap file to the main webapge of the flask apilication and choose the model you wish to use. Adding new models is straight forward as well after creaeteng said model useing the steps above just add the file path into the main app.py script and make a few slight adjuisments in the index.html to load the model.

**Load new model app.py**

 ![Screenshot_2024-03-27_08-49-37](https://github.com/Matthew-a-smith/capstone-project/assets/109995724/2c05f044-e29b-49fa-8c9e-6c5f0e93e1a0)

**index.html**

![Screenshot_2024-03-27_08-50-56](https://github.com/Matthew-a-smith/capstone-project/assets/109995724/f53d9d48-10cb-418c-8245-dd87c7b19975)

**webpage**

![webpage---results](https://github.com/Matthew-a-smith/capstone-project/assets/109995724/aa445848-c85e-4dc4-a31b-29bc043feaf4)



