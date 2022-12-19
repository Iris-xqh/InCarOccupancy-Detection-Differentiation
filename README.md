# Occupancy Motion Detection and Identification in Cars



## File Structure 

- **Data**        **--- sample test data**
  - emptyCar.mat     				--- sample data of an empty car 
  - emptyToOccupancy.mat   --- sample data of a human entering the car (from empty to occupied)
  - human_1.mat                      --- sample data of an human occupancy
  - human_2.mat                      --- sample data of an human occupancy
  - dog.mat                                --- sample data of a dog occupancy

- **OccupancyDetect.py**             **--- code for occupancy detection algorithm**
- **Differentiate.py**     **--- code for occupancy differentiation algorithm**
- **MatLab**
  - process.m                         --- run this file to process raw CSI data
  - get_scaled_csi.m              --- read in the CSI trace file
  - read_bf_file.m                  --- parse CSI data for all





## Hardware Setup

We used 2 NUCs with 3 antennas each, one as transmitter and another as receiver. Each NUC is equipped with Linux 802.11n CSI Tool:

https://dhalperi.github.io/linux-80211n-csitool/index.html

They are both powered with a portable power bank. 
Run “ifconfig” and “iwconfig” retrieve their IP address.  A laptop is connected to both NUCs using a 5-port switch, also powered by a portable power bank. 

#### Detailed steps of how to conduct the experiment:

Change the IP address of the laptop so that we could use SSH to connect the laptop to both NUCs. 
Turn on both NUCs, use terminal to redirect to the correct directory, which is “CSIExperiments-ETH”.
First, on the receiver, run “sudo receive.sh” with one parameter, which is the name of the file to be saved. The receiver will enter a state to wait for the signals from transmitter.

Next, on the transmitter, run “sudo transmit.sh” with parameters. One parameter would be the total package count, another would be the time interval (in microsecond). It would automatically stop after the designated package count * time interval (e.g. 100 package, 100000 microsecond interval = 10s total time).
Lastly, press ctrl + c on the receiver to stop the process. A consecutive string of letter “r” would appear exactly package count times.

Repeat as many experiments as you like and get a bunch of files containing CSI data. Export them to the local machine and then process using MATLAB and Python.





## Pre-processing data with MATLAB

Run process.m file to process the raw data.

**Input**: CSI trace file from the previous data collecting step

**Output**: 1. save the parsed CSI data in .mat file

​			    2. a heat map figure presenting the CSI data for all subcarriers 

```matlab
csi_trace = read_bf_file("test_30_1_empty_to_one_03");

for i = 1:30
    csi_entry = csi_trace{i};
    csi = get_scaled_csi(csi_entry);
    csiAll(i,:,:,:) = csi;
end

save('ssss.mat','csiAll')
% plot a heat map figure
figure;imagesc(db(abs(squeeze(csiAll(:,1,:)))).')
```

#### 





## Python Code Instructions

#### 1.Occupancy Detection

**Input**: .mat file containing the parsed CSI data for all collected packets, see example in the **data** folder 

**Output**: an array including time when there is an occupancy

```python
if __name__ == '__main__':
    # if the input data shape: (30, 3, 30)
    detection = Detection(30, 3, 3, 3);
    emptyData = detection.matToNumpy('data/emptyCar.mat')
    testData = detection.matToNumpy('data/emptyToOccupancy.mat')

    # if the input data shape: (300, 3, 30)
    # emptyData = detection.sample(emptyData)
    # testData = detection.sample(testData)

    threshold = detection.computeThreshold(emptyData)
    time = detection.slidingWindow(testData, threshold)
    print(time)
```

#### 2.Occupancy Differentiation

**Input**: .mat file containing the parsed CSI data for all collected packets, see example in the **data** folder 

**Output**: the category of the target data (string)

```python
if __name__ == '__main__':
    differentiation = Differentiation(3)

    # shape: (300, 3, 30)
    baseData = differentiation.matToNumpy('data/human_1.mat')
    testData = differentiation.matToNumpy('data/dog.mat')
    # testData = differentiation.matToNumpy('data/human_2.mat')

    print("Running differentation algorithm...")
    threshold = differentiation.computeThreshold(baseData)
    differentiationRes = differentiation.compare(testData, threshold)
    print("The object's category is: ", differentiationRes)
```