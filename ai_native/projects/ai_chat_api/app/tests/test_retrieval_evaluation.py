# | Memory                                                               | Relevant? |
# | -------------------------------------------------------------------- | --------- |
# | Bạn thích Python và đang học về AI, ML                               | ✅         |
# | Mục tiêu trở thành phát triển trí tuệ nhân tạo trong tương lai       | ❌         |
# | User wants to be a Python programmer and is willing to learn it.     | ✅         |
# | User wants to become a Python programmer and is willing to learn it. | ✅         |
# | Learning goals: Learn Python and become a Python developer           | ✅         |
# | Learning goals: Python, AI-native, ML                                | ✅         |
# | Các memory về tên/nickname                                           | ❌         |
# | Profession: AI developer                                             | ❌         |


# query1 = "Tôi đang học Python"
# query2 = "Python là ngôn ngữ tôi đang tập trung học"
# query3 = "Tôi muốn mua một chiếc xe"


# Bạn thích Python và đang học về AI, ML                 ✅
# User wants to be a Python programmer...              ✅
# User wants to become a Python programmer...          ✅
# Learning goals: Learn Python...                       ✅
# Learning goals: Python, AI-native, ML                ✅

# Precision@K = relevant retrieved / total retrieved


# Recall@K = relevant retrieved / total relevant
from uuid import UUID

from app.tests.test_semantic_search import (
    embedding1,
    embedding2,
    embedding3,
    semantic_search1,
    semantic_search2,
    semantic_search3,
    semantic_search,
)

# for result in semantic_search2:
#     print(result.memory.content, result.score, result.memory.id)
# retrieved_ids = {str(result.memory.id) for result in semantic_search2}

threshold = 0.5

# experiment 1
retrieved_ids_of_embedding1 = semantic_search(
    UUID("43371a56-0d6b-454a-87c9-5c78b593122b"), embedding1, limit=10
)
retrieved_ids2_of_exp1 = {
    str(result.memory.id)
    for result in retrieved_ids_of_embedding1
    if result.score >= threshold
}
print("K = 10 of experiment 1", retrieved_ids2_of_exp1)

# experiment 2
retrieved_ids_of_embedding2 = semantic_search(
    UUID("43371a56-0d6b-454a-87c9-5c78b593122b"), embedding2, limit=10
)
retrieved_ids2_of_exp2 = {f"""{result.memory.id} 
        \n {result.memory.content} 
        \n {result.score}
""" for result in retrieved_ids_of_embedding2 if result.score >= threshold}
print("K = 10 of experiment 2", retrieved_ids2_of_exp2)


# cfab9ccf-a537-4d10-b4c9-de9447cc840e Tên của user là Nhất.
# 6b020aa3-7465-428b-b5cd-c8f90ce1b0e0 User wants to become a Python programmer and is willing to learn it.
# 8cb391ff-dc6f-4a9c-af11-fdb477a5b655 User prefers responses in Vietnamese.
# adbbd8aa-d3e4-4911-9381-b469ccebca8e User wants to be a Python programmer and is willing to learn it.
# 9040679a-a637-43fc-9ac0-249b411a35df User's name: Nhất
# 653a72ac-b837-4eba-a620-59a73a26ec41 User plays carom 3C billiards and is interested in studying and improving their skills.
# ccf6d763-a42e-4112-8462-3435856925e3 Tên của user là Nhất.
# cc48235f-c2f4-4ecd-8aff-4afed20db9ef User's name is Nhất.
# 33bfc30f-2488-4a6d-918c-26bb000d1d8a Tên của user là Nhât
# 6f96724f-89f9-4865-9512-308253de116a Learning goals: Learn Python and become a Python developer
# c1329c5a-468f-416a-82de-ff21b2e722a2 User name: Nhât
# e8d25658-094a-40cc-a976-d9f38c6bc609 Ngot
# b4a48608-7125-473b-99d8-e9185b9a5c0d User's name: Ngọt
# a9022fdc-ca1d-4fa2-abef-861c9178a78c Learning goals: Python, AI-native, ML
# d7c00874-bd64-4557-a2a2-e6af56b45cb7 Profession: AI developer
# f04e0f92-9c87-4ac3-8101-fc5faa758354 Nickname của tôi là Ngọt
# 177ad754-1726-4438-8d7e-9a4f6336901c Mục tiêu trở thành phát triển trí tuệ nhân tạo trong tương lai
# c02e1595-b121-4c73-8600-18e2aa3248c3 Bạn thích Python và đang học về AI, ML
# 07043ef4-28b7-42da-9d64-b68010ec09e5 User's name: nhất
# 2e5db002-c280-4e97-b0f5-2e1899861d63 User's name: nhất

relevant_ids = {
    "6b020aa3-7465-428b-b5cd-c8f90ce1b0e0",
    "adbbd8aa-d3e4-4911-9381-b469ccebca8e",
    "6f96724f-89f9-4865-9512-308253de116a",
    "a9022fdc-ca1d-4fa2-abef-861c9178a78c",
    "c02e1595-b121-4c73-8600-18e2aa3248c3",
}


def precision_at_k(
    retrieved_ids: set[UUID],
    relevant_ids: set[UUID],
) -> float:
    if not retrieved_ids:
        return 0.0

    hits = retrieved_ids & relevant_ids

    return len(hits) / len(retrieved_ids)


def recall_at_k(
    retrieved_ids: set[UUID],
    relevant_ids: set[UUID],
) -> float:
    if not relevant_ids:
        return 0.0

    hits = retrieved_ids & relevant_ids

    return len(hits) / len(relevant_ids)


precision10_exp1 = precision_at_k(retrieved_ids2_of_exp1, relevant_ids)
recall10_exp1 = recall_at_k(retrieved_ids2_of_exp1, relevant_ids)

print(f"Precision@10 experiment 1: {precision10_exp1}")
print(f"Recall@10 experiment 1: {recall10_exp1}")

precision10_exp2 = precision_at_k(retrieved_ids2_of_exp2, relevant_ids)
recall10_exp2 = recall_at_k(retrieved_ids2_of_exp2, relevant_ids)

print(f"Precision@10 experiment 2: {precision10_exp2}")
print(f"Recall@10 experiment 2: {recall10_exp2}")
