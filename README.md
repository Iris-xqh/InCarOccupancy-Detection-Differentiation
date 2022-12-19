# Occupancy Motion Detection and Identification in Cars



## File Structure 

- **Data**        --- sample test data
  - emptyCar.mat     				--- sample data of an empty car 
  - emptyToOccupancy.mat   --- sample data of a human entering the car (from empty to occupied)
  - human_1.mat                      --- sample data of an human occupancy
  - human_2.mat                      --- sample data of an human occupancy
  - dog.mat                                --- sample data of a dog occupancy

- **OccupancyDetect.py**             --- code for occupancy detection algorithm
- **Differentiate.py**     --- code for occupancy differentiation algorithm



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