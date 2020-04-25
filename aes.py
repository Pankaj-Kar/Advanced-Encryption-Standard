from pyfinite import ffield
import copy
import random
gf8 = ffield.FField(8)
sbox = [[] for i in range(16)]
inputString = ""
inputGrid = [[] for i in range(4)]
inputGrid22 = [[] for i in range(4)]
inputGrid2 = [[] for i in range(4)]


mixColMat = [[2, 3, 1, 1],
             [1, 2, 3, 1],
             [1, 1, 2, 3],
             [3, 1, 1, 2]]


mat = [[1, 0, 0, 0, 1, 1, 1, 1],
       [1, 1, 0, 0, 0, 1, 1, 1],
       [1, 1, 1, 0, 0, 0, 1, 1],
       [1, 1, 1, 1, 0, 0, 0, 1],
       [1, 1, 1, 1, 1, 0, 0, 0],
       [0, 1, 1, 1, 1, 1, 0, 0],
       [0, 0, 1, 1, 1, 1, 1, 0],
       [0, 0, 0, 1, 1, 1, 1, 1]]


mat2 = [1, 1, 0, 0, 0, 1, 1, 0]
tempMat = []
tempMat2 = []
temporaryMat = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 16]]

srow = [[]for i in range(4)]
srow2 = [[]for i in range(4)]
matrix = [[]for i in range(4)]
matrix2 = [[]for i in range(4)]


def Sbox():
    for i in range(16):
        for j in range(16):
            x = hex(i) + hex(j)
            x = x.replace('0x', "")
            invX = gf8.Inverse(int(x, 16))
            # print(type(invX))
            binn = toBin(invX)
            tempst = ""
            temp = 0
            # print(binn)
            for k in range(8):
                res = 0
                for l in range(8):
                    t = gf8.Multiply(mat[k][l], int(binn[l], 2))
                    res = res ^ t
                tempMat.append(res)
                tempMat2.append(tempMat[k] ^ mat2[k])
                tempst += str(tempMat2[k])
            tempst = "".join(reversed(tempst))
            # print(tempst)
            temp = hex(int(tempst, 2))
            sbox[i].append(temp)
            tempMat.clear()
            tempMat2.clear()
            # print(temp)


def shiftRow(MAT):
    srow[0].append(MAT[0][0])
    srow[0].append(MAT[0][1])
    srow[0].append(MAT[0][2])
    srow[0].append(MAT[0][3])
    srow[1].append(MAT[1][1])
    srow[1].append(MAT[1][2])
    srow[1].append(MAT[1][3])
    srow[1].append(MAT[1][0])
    srow[2].append(MAT[2][2])
    srow[2].append(MAT[2][3])
    srow[2].append(MAT[2][0])
    srow[2].append(MAT[2][1])
    srow[3].append(MAT[3][3])
    srow[3].append(MAT[3][0])
    srow[3].append(MAT[3][1])
    srow[3].append(MAT[3][2])


def shiftRow2(MAT):
    srow2[0].append(MAT[0][0])
    srow2[0].append(MAT[0][1])
    srow2[0].append(MAT[0][2])
    srow2[0].append(MAT[0][3])
    srow2[1].append(MAT[1][1])
    srow2[1].append(MAT[1][2])
    srow2[1].append(MAT[1][3])
    srow2[1].append(MAT[1][0])
    srow2[2].append(MAT[2][2])
    srow2[2].append(MAT[2][3])
    srow2[2].append(MAT[2][0])
    srow2[2].append(MAT[2][1])
    srow2[3].append(MAT[3][3])
    srow2[3].append(MAT[3][0])
    srow2[3].append(MAT[3][1])
    srow2[3].append(MAT[3][2])


def mixCol(MAT):
    for i in range(4):
        for j in range(4):
            res = 0
            for k in range(4):
                x = MAT[k][j]
                x = x.replace('0x', "")
                temp = int(x, 16)
                res = res ^ gf8.Multiply(mixColMat[i][k], temp)
            matrix[j].append(hex(res))


def mixCol2(MAT):
    for i in range(4):
        for j in range(4):
            res = 0
            for k in range(4):
                x = MAT[k][j]
                x = x.replace('0x', "")
                temp = int(x, 16)
                res = res ^ gf8.Multiply(mixColMat[i][k], temp)
            matrix2[j].append(hex(res))


def keyByte():
    kb = ''
    for i in range(8):
        kb += str(random.randint(0, 1))
    return kb


def g(w, sbox, j):
    rc = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']
    w = lshift(w)
    for i in range(4):
        num = w[i]
        hi = num[:4]
        low = num[4:]
        hi = int(hi, 2)
        low = int(low, 2)
        w[i] = sbox[hi][low]
        if i == 0:
            w[i] = bin(int(w[i], 16) ^ int(rc[j], 16))[2:]
        else:
            w[i] = bin(int(w[i], 16) ^ 0)[2:]
    return w


def generateKeys():
    global allKeys
    w = ['']*45
    initKey = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            initKey[i][j] = keyByte()
    for i in range(4):
        for j in range(4):
            w[j] += initKey[i][j]

    for i in range(4, 45):
        temp = w[i-1]
        if i == 4:
            temp = g(temp, sbox, i)
        s_temp = toString(temp)
        s_w = toString(w[i-4])
        w[i] = bin(int(s_temp, 2) ^ int(s_w, 2))[2:]

    allKeys = toString(w)


def lshift(s):
    arr = []
    temp = ''
    for i in range(len(s)):
        temp += s[i]
        if i % 8 == 7:
            arr.append(copy.deepcopy(temp))
            temp = ''
    ls = copy.deepcopy(arr)
    for i in range(4):
        arr[i] = ls[(i+1) % 4]
    return arr


def getRoundKey(round):
    base = round*128
    key = ''
    for i in range(base, base+128):
        key += allKeys[i]
    return key


def addRoundKey(grid, round):
    # if round == 9:
    # print(grid)
    key = getRoundKey(round)
    temp = ''
    keys = []
    for i in range(128):
        temp += key[i]
        if i % 8 == 7:
            keys.append(copy.deepcopy(temp))
            temp = ''
    keyNo = 0
    for i in range(4):
        for j in range(4):
            temp = copy.deepcopy(grid[i][j])
            temp = int(temp, 16)
            temp = bin(temp ^ int(keys[keyNo], 2))[2:]
            grid[i][j] = hex(int(temp, 2))
            keyNo += 1
    return grid


def toString(ls):
    s = ''
    for i in ls:
        s += str(i)
    return s


def createGrid(inputString):
    tempGrid = []
    s = ""

    for i in range(len(inputString)):
        s = s+str(inputString[i])
        if len(s) == 8:
            tempGrid.append(hex(int(s, 2)))
            s = ""

    inputGrid[0].append(tempGrid[0])
    inputGrid[0].append(tempGrid[1])
    inputGrid[0].append(tempGrid[2])
    inputGrid[0].append(tempGrid[3])
    inputGrid[1].append(tempGrid[4])
    inputGrid[1].append(tempGrid[5])
    inputGrid[1].append(tempGrid[6])
    inputGrid[1].append(tempGrid[7])
    inputGrid[2].append(tempGrid[8])
    inputGrid[2].append(tempGrid[9])
    inputGrid[2].append(tempGrid[10])
    inputGrid[2].append(tempGrid[11])
    inputGrid[3].append(tempGrid[12])
    inputGrid[3].append(tempGrid[13])
    inputGrid[3].append(tempGrid[14])
    inputGrid[3].append(tempGrid[15])


def subByte(inputGrid2):
    for i in range(4):
        for j in range(4):
            s = inputGrid2[i][j]
            # print(s)
            s = s.replace("0x", "")
            temp = toBin(int(s, 16))
            r = int(temp[:4], 2)
            c = int(temp[4:8], 2)
            inputGrid2[i][j] = sbox[r][c]
            #print(temp, r, c, inputGrid[0][0])


def subByte2(inputGrid22):
    for i in range(4):
        for j in range(4):
            s = inputGrid22[i][j]
            # print(s)
            s = s.replace("0x", "")
            temp = toBin(int(s, 16))
            r = int(temp[:4], 2)
            c = int(temp[4:8], 2)
            inputGrid22[i][j] = sbox[r][c]
            #print(temp, r, c, inputGrid[0][0])


def compare(mata, matb):
    tem1 = []
    tem2 = []
    a = ""
    b = ""
    v1 = 0
    v2 = 0
    for i in range(4):
        for j in range(4):
            tem1.append(mata[i][j])
            tem2.append(matb[i][j])

    for i in range(len(tem1)):
        a = a + toBin(int(tem1[i].replace("0x", ""), 16))
        b = b + toBin(int(tem2[i].replace("0x", ""), 16))

    v1 = int(a, 2)
    v2 = int(b, 2)
    temp = str(bin(v1 ^ v2))
    count = 0
    for i in temp:
        if i == '1':
            count += 1
    #a=a.replace("0x", "")
    #b=b.replace("0x", "")
    # print(count)
    return count


def main():
    # constructing the sbox
    Sbox()
    # print(sbox)
    generateKeys()
    inputString = "00000001001000110100010101100111100010011010101111001101111011111111111011011100101110101001100001110110010101000011001000010000"
    inputString2 = "00000000001000110100010101100111100010011010101111001101111011111111111011011100101110101001100001110110010101000011001000010000"
    createGrid(inputString)
    #print(f'Input Matrix: {inputGrid}')
    #print("Input Grid")
    inputGrid2 = copy.deepcopy(inputGrid)


    inputGrid[0].clear()
    inputGrid[1].clear()
    inputGrid[2].clear()
    inputGrid[3].clear()
    createGrid(inputString2)

    inputGrid22 = copy.deepcopy(inputGrid)
    print(
        f'Number of Unmatched Bits First : {compare(inputGrid2, inputGrid22)}')

    inputGrid2 = copy.deepcopy(addRoundKey(inputGrid2, 0))
    inputGrid22 = copy.deepcopy(addRoundKey(inputGrid22, 0))

    print(f'Number of Unmatched Bits 0 : {compare(inputGrid2, inputGrid22)}')

    for i in range(10):
        #print(i, inputGrid2)
        if i == 9:
            subByte(inputGrid2)
            subByte2(inputGrid22)
            # print("sub")
            #print(inputGrid2, "here")

            shiftRow(inputGrid2)
            shiftRow2(inputGrid22)
            # print("srow")

            # mixCol(srow)
            # print(matrix)

            inputGrid2 = copy.deepcopy(addRoundKey(srow, i))
            inputGrid22 = copy.deepcopy(addRoundKey(srow2, i))
            print(
                f'Number of Unmatched Bits {i+1} : {compare(inputGrid2, inputGrid22)}')

        else:
            subByte(inputGrid2)
            subByte2(inputGrid22)
            # print("sub")
            # print(inputGrid2)

            # print(inputGrid2)
            shiftRow(inputGrid2)
            shiftRow2(inputGrid22)
            # print("srow")
            # print(srow)

            mixCol(srow)
            mixCol2(srow2)
            # print("mix")
            srow[0].clear()
            srow[1].clear()
            srow[2].clear()
            srow[3].clear()
            srow2[0].clear()
            srow2[1].clear()
            srow2[2].clear()
            srow2[3].clear()
            # print(matrix)

            inputGrid2 = copy.deepcopy(addRoundKey(matrix, i))
            inputGrid22 = copy.deepcopy(addRoundKey(matrix2, i))
            # print("ig")
            matrix[0].clear()
            matrix[1].clear()
            matrix[2].clear()
            matrix[3].clear()
            matrix2[0].clear()
            matrix2[1].clear()
            matrix2[2].clear()
            matrix2[3].clear()

            print(
                f'Number of Unmatched Bits {i+1} : {compare(inputGrid2, inputGrid22)}')

    #print(f'OutPut Matrix: {inputGrid, inputGrid2, inputGrid22}')
    #print(f'Temporaray grid: {inputString, inputString2}')


def toBin(x):
    return f'{x:08b}'


main()
