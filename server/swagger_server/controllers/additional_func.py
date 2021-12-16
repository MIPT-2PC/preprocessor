# Create function for mask generation for links


import random


def generateRandom32int():
    return random.randint(20194, pow(2, 32) - 10)

def generateInput(N):
    i = 0
    input = []
    for i in range(N):
        input.append(random.randint(0, 1))
    return input


"""##Create function for tables generation"""


def result_Creation():  # G = A
    result_A = []
    hashA0 = [0] * 4
    hashA1 = [0] * 4
    for i in range(4):
        result_A.append(random.randint(0, 1))
        hashA0[i] = generateRandom32int()
        hashA1[i] = generateRandom32int()
    return result_A, hashA0, hashA1


def get_result(c, d, out):
    if c == 0 and d == 0:
        return out[0]
    if c == 0 and d == 1:
        return out[1]
    if c == 1 and d == 0:
        return out[2]
    if c == 1 and d == 1:
        return out[3]


def matrix_B_Creation(result_A, keys_list, wires, operation):
    B = [[0, 0, 0],
         [0, 1, 0],
         [1, 0, 0],
         [1, 1, 0]]
    result_B = []
    hashB0 = [0] * 4
    hashB1 = [0] * 4
    operations = {
        "XOR": lambda x, y: x ^ y,
        "AND": lambda x, y: x & y,
        "INV": lambda x, y: 1 if (x == 0 and y == 0) else 0
    }

    if len(wires) == 3:
        for i in range(len(B)):
            B[i][2] = result_A[i] ^ (keys_list[int(wires[2])] ^ operations[operation](B[i][0] ^ keys_list[int(wires[0])], B[i][1] ^ keys_list[int(wires[1])]))
            result_B.append(B[i][2])
            hashB1[i] = generateRandom32int()
            hashB0[i] = generateRandom32int()
    if len(wires) == 2:
        for i in range(len(B)):
            B[i][2] = result_A[i] ^ (keys_list[int(wires[1])] ^ operations[operation](B[i][0] ^ keys_list[int(wires[0])], B[i][0] ^ keys_list[int(wires[0])]))
            result_B.append(B[i][2])
            hashB1[i] = generateRandom32int()
            hashB0[i] = generateRandom32int()
    return result_B, hashB0, hashB1
