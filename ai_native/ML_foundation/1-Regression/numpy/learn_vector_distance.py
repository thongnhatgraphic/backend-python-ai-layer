import numpy as np

cat = np.array([1,1])
dog = np.array([2,2])
car = np.array([8,8])

print(np.linalg.norm(cat - dog))

print(np.linalg.norm(cat - car))

bird = np.array([1.5, 1.7])

print(np.linalg.norm(bird - cat))
print(np.linalg.norm(bird - car))
print(np.linalg.norm(car - bird))