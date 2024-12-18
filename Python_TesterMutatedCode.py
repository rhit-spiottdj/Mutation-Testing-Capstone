def helloWorld(self):
    print('Hello World!!!!')
    return 'Hello World'

def makeArray(self):
    testArray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rM = 100
    for x in testArray:
        print(x)
        rM += x
    print(rM)
    return rM