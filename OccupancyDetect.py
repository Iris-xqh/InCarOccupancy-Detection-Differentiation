import numpy as np
import scipy.io
import scipy.io as io

class Detection:
    def __init__(self, pkgNum, atNum, windowSize, ignoreNum):
        # Number of all packets
        self.pkgNum = pkgNum
        # Number of antennas
        self.atNum = atNum
        # Size of the sliding window
        self.windowSize = windowSize
        # Number of the packets needed to be ignored
        # Because in the first few seconds, we performed an action of closing the car door, which may have an impact on the data
        self.ignoreNum = ignoreNum

    # Convert the .mat file to numpy
    def matToNumpy(self, fileName):
        data = scipy.io.loadmat(fileName)
        data = abs(np.array(data['csiAll']))
        print(data)
        return np.squeeze(data)

    # Sample the high-frequency data to low-frequency one
    # (300, 3, 30) --> (30, 3, 30)
    def sample(self, allData):
        newData = allData[0: 150:5]
        return newData
        # matFileName = "box1_60.mat"
        # io.savemat(matFileName, {'csiAll': newData})

    # Compute the threshold matrix based on data of an empty car
    def computeThreshold(self, emptyCarData):
        # (antennas num, subcarriers num)
        # Reocrd the accumulated differences within a window, change over time
        sumRecord = np.zeros((self.atNum, 30))

        # (antennas num, subcarriers num, number of accumulated differences needed to be calculated)
        threshold = np.zeros(([self.atNum, 30, self.pkgNum - self.ignoreNum - self.windowSize]))

        # The start of the sliding window
        left = self.ignoreNum
        right = self.ignoreNum

        # Sliding window algorithm
        while right < self.pkgNum - 1:
            right += 1
            if (right - left) > self.windowSize:
                left += 1
            for a in range(self.atNum):
                for subCarrier in range(30):
                    cur = emptyCarData[right][a][subCarrier]
                    pre = emptyCarData[right - 1][a][subCarrier]
                    sumRecord[a][subCarrier] += abs(cur - pre)
                    if (right - left) >= self.windowSize and (left - 1) != 0:
                        sumRecord[a][subCarrier] -= abs(
                            emptyCarData[left][a][subCarrier] - emptyCarData[left - 1][a][subCarrier])
                        threshold[a][subCarrier][left - self.ignoreNum] = sumRecord[a][subCarrier]

        # For every subcarrier, the accumulated differences for all window are calculated
        # Calculate the mean value for every subcarrier, get the threshold
        res = np.mean(threshold, axis=2)
        return res

    # Sliding window on test data, compare with the threshold matrix
    def slidingWindow(self, allData, threshold):
        sumRecord = np.zeros((self.atNum, 30))

        # The array of recorded time(s) when there is an occupancy
        occupancyTime = []
        left = self.ignoreNum
        right = self.ignoreNum

        while right < self.pkgNum - 1:
            atCount = 0
            right += 1
            if (right - left) > self.windowSize:
                left += 1
            for j in range(self.atNum):
                count = 0
                for subCarrier in range(30):
                    # absolute value
                    sumRecord[j][subCarrier] += abs(allData[right][j][subCarrier] - allData[right - 1][j][subCarrier])
                    if (right - left) >= self.windowSize and (left - 1) != 0:
                        sumRecord[j][subCarrier] -= abs(allData[left][j][subCarrier] - allData[left - 1][j][subCarrier])
                        a = sumRecord[j][subCarrier]
                        b = threshold[j][subCarrier]
                        if sumRecord[j][subCarrier] > threshold[j][subCarrier]:
                            count += 1
                # If there are over 25 subcarriers' larger than the threshold,
                # we say this antennas' data larger than the threshold
                if count > 25:
                    atCount += 1
            # If there are over 1 antennas' data larger than the threshold
            # we say detect the occupancy and record the time
            if atCount >= 2:
                # An argument that correct the time
                timeArguement = 2.2
                occupancyTime.append(((left + right) + timeArguement)/ 2)
        return occupancyTime


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

