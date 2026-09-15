1. Sentence:
Redis
is
fast
↓
2. Embedding
X
[
 eRedis
 eis
 efast
]
↓

3. Nhân WQ
Q
[
 qRedis
 qis
 qfast
]
↓
4. Nhân WK
K
[
 kRedis
 kis
 kfast
]
↓
5. Transpose
K.T
↓
Matrix Multiplication
Scores = Q @ K.T
            Keys
        R     I     F

Q(R)    4     3     2

Q(I)    2     5     3

Q(F)    1     2     4
↓
Softmax theo từng hàng
Weights
[
 [0.58 0.28 0.14]
 [.... .... ....]
 [.... .... ....]
]
↓
Nhân với V
↓
New Representation Matrix