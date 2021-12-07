#Create function for mask generation for links


import random

def generateInput(N):
  i = 0
  input=[]
  for i in range(N):
    input.append(random.randint(0, 1))
  return input

"""##Create function for tables generation"""

def matrix_Creation():# G = A
  A = [[0,0,0],
       [0,1,0],
       [1,0,0],
       [1,1,0]]
  result_A = []
  for i in range (len(A)):
    A[i][2] = random.randint(0, 1)
    result_A.append(A[i][2])
  return A,result_A

def get_result(c,d,out):
  if c == 0 and d == 0:
    return out[0]
  if c == 0 and d == 1:
    return out[1]
  if c == 1 and d == 0:
    return out[2]
  if c == 1 and d == 1:
    return out[3]

result_G = matrix_Creation()[1]
result_A = matrix_Creation()[1]

def matrix_B_Creation(result_A, secret_keys, result_G):
  B = [[0,0,0],
       [0,1,0],
       [1,0,0],
       [1,1,0]]
  result_B = []
  for i in range (len(B)):
    B[i][2] = result_A[i]^(secret_keys[0]^get_result(B[i][0]^secret_keys[1],B[i][1]^secret_keys[2],result_G))
    result_B.append(A[i][2])
  return B,result_B

B,result_B = matrix_B_Creation(result_A,[1,0,1],result_G)