import numpy as np
import scipy.io


class Differentiation:
    def __init__(self, atNum):
        # Number of antennas
        self.atNum = atNum

    # Convert the .mat file to numpy
    def matToNumpy(self, fileName):
        data = scipy.io.loadmat(fileName)
        data = abs(np.array(data['csiAll']))
        return np.squeeze(data)

    # Compute the threshold matrix based on data of human occupancy
    def computeThreshold(self, humanData):
        threshold = np.zeros((self.atNum, 30))
        right = 0

        while right < 100:
            right += 1
            for a in range(self.atNum):
                for subCarrier in range(30):
                    cur = humanData[right][a][subCarrier]
                    pre = humanData[right - 1][a][subCarrier]
                    threshold[a][subCarrier] += abs(cur - pre)

        res = threshold / 100
        print("threshold: ----------------")
        print(res)
        return res

    # Compare test data with the threshold matrix
    def compare(self, testData, threshold):
        sumRecord = np.zeros((self.atNum, 30))
        right = 0

        while right < 100:
            right += 1
            for a in range(self.atNum):
                for subCarrier in range(30):
                    cur = testData[right][a][subCarrier]
                    pre = testData[right - 1][a][subCarrier]
                    sumRecord[a][subCarrier] += abs(cur - pre)

        testRes = sumRecord / 100
        print("sumRecord: ----------------")
        print(testRes)
        atCount = 0
        for a in range(self.atNum):
            count = 0
            for subCarrier in range(30):
                if testRes[a][subCarrier] > threshold[a][subCarrier]:
                    count += 1
            if count >= 25:
                atCount += 1

        res = "Human"
        if atCount >= 3:
            res = "Dog"
        return res


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
