

Giả sử
z = a1x1 + a2x2 + a3x3 + b



công thức tính: 
linear_regress = z
1/(1 + e^( đối xứng linear_regress qua 0 ))

- Với z = 1000--------------------------------------
    ta có: -z = -1000
    và e^(-1000) ~ 0 => 1/(1 + ~0) ~ = 1
-z = -7.23
e^(-7.23) 
- Với z = -1000--------------------------------------
    ta có -z = 1000
    và e^(1000) ~ rất lớn => 1/(1 + rất lớn) ~ = 0

- Với z = 0 -----------------------------------------
    ta co -z = 0
    và e^(0) = 1 =? 1/(1 + 1 ) = 0.5

==============================================
                Input Features
                │
                ▼
            Linear Combination
            (z)
                │
                ▼
            Sigmoid
                │
                ▼
            Probability
                │
                ▼
            Decision Boundary
                │
                ▼
            Class (0 hoặc 1)