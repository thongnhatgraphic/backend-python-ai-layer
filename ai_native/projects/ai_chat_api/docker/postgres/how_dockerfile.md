DOCKERFILE : Chỉ là 1 cuốn sách hướng dẫn nấu ăn

1. Lấy cái gì từ đâu??? (FROM postgres:15 )


2. Chế biến như thế nào?? (RUN apt-get update)
apt-get update không cài gì cả. Nó chỉ tải về danh sách package mới nhất từ repository.

3. Tải package cần thiết phục vụ cho nhu cầu bài toán
RUN apt-get install ...


    pgvector được viết bằng C.

    C thì không thể chạy trực tiếp.

    Nó phải trải qua:
    Source Code (.c)
    ↓
    Trình phiên dịch Compiler (gcc)

    ↓
    Binary

Đó chính là quá trình compile.
| Package                    | Tại sao cần?                                 |
| -------------------------- | -------------------------------------------- |
| `build-essential`          | Compiler (`gcc`, `make`, ...) để build C     |
| `git`                      | Clone source code `pgvector`                 |
| `postgresql-server-dev-15` | Header/API của PostgreSQL để build extension |



RUN apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-15


RUN cd pgvector && make && make install
cd pgvector

↓

make
(compile)

↓

make install
(copy vector.so và các file SQL vào đúng vị trí PostgreSQL cần)