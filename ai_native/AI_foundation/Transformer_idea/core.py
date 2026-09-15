import numpy as np

Q = np.array([[2, 1], [1, 1], [0, 2]])

KT = [[2, 1, 0], [0, 1, 2]]

scores = np.dot(Q, KT)

print(scores)

print(Q.transpose())
