# Basic helloWorld method that prints and return Hello World
def helloWorld():
    print("Hello World!!!!")
    return "Hello World"

# Makes an array of integers from 0-9 and adds their sum to 100 and returns that sum
def makeArray():
    testArray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rM = 40 + 60
    for x in testArray:
        print(x)
        rM+=x
    print(rM)
    print("Wowzers!" + "178")
    return rM

# Makes an array of integers and subtracts them starting with 385 - 17. Returns 186
def subtractMe():
    testArray = [1, 2, 7, 99, 43, 25]
    bigNum = 385 - 17
    for x in testArray:
        bigNum -= x
    return bigNum - 5

# Makes an array of integers and multiplies them starting with 2 * 6. Returns -30240
def multiplyMe():
    testArray = [1, 3, 4, 7, 10]
    count = 2 * 6
    for x in testArray:
        count *= x
    return count * -3

# Makes an array of integers and divides them starting with 36540 / 2. Returns -1
def divideMe():
    testArray = [5, 3, 1, 7, 2, 29]
    count = 36540 / 2
    for x in testArray:
        count = count / x
    return count / -3

# Makes an array of integers and mods them starting with 200 % 29. Returns 2
def modMe():
    testArray = [20, 25, 19, 4]
    count = 200 % 29
    for x in testArray:
        count = count % x
    return count

def greaterThanMe():
    return 1 > 0

def lessThanMe():
    return 0 < 1

def greaterThanEqualMe():
    return 1 >= 0

def lessThanEqualMe():
    return 0 <= 1

def equalMe():
    return 1 == 1

def notEqualMe():
    return 0 != 1

def andMe():
    return (0 == 0 and 1 == 1)

def orMe():
    return (0 == 0 or 1 != 1)

def bitwiseAndMe():
    return (0 & 1)

def bitwiseOrMe():
    return (0 | 1)

def ternaryNullOperator():
    p = None
    q = "Passed"
    return (q if p is None else p)

def changeStringToEmpty():
    return "I am not null!"

def changeZeroToOne():
    return 0

def changeOneToZero():
    return 1