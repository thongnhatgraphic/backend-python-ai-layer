import numpy as np

v1 = np.array([1,2,3,4,5])

v2 = np.array([4,5,6,7,8])

print(v1)
print(v2)
print(v1 - v2)



v1 = np.array([1, 2])
v2 = np.array([4, 6])
distance = np.linalg.norm(v1 - v2)

print(distance)