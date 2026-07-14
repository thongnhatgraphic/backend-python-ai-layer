import numpy as np

a = np.array([1,1])
b = np.array([2,2])

print(np.dot(a, b))

cosine = np.dot(a, b) / (
    np.linalg.norm(a)
    * np.linalg.norm(b)
)

print(cosine)

a = np.array([1,1])
b = np.array([-1,-1])

cosine = np.dot(a, b) / (
    np.linalg.norm(a)
    * np.linalg.norm(b)
)

print(cosine)