from sqlmodel import Session
from time import perf_counter
from app.eval.retrieval.scifact_retriever import (
    engine,
    embedding_service,
    search_by_embedding,
)
import numpy as np
from pathlib import Path
from app.eval.datasets.scifact.query_loader import load_queries
import random

BASE_DIR = Path(__file__).resolve().parents[1] / "datasets" / "scifact"
QUERIES_PATH = BASE_DIR / "queries.jsonl"
queries = load_queries(QUERIES_PATH)

query_items = list(queries.items())

random.seed(42)
random.shuffle(query_items)

evaluation_queries = [query for _, query in query_items[:300]]


def measure_search_latency(
    session,
    query_embedding,
    k: int,
    ef_search: int,
    runs: int = 20,
) -> tuple[float, float]:

    latencies = []

    search_by_embedding(
        session=session,
        query_embedding=query_embedding,
        limit=k,
        ef_search=ef_search,
    )

    for _ in range(runs):
        start = perf_counter()

        search_by_embedding(
            session=session,
            query_embedding=query_embedding,
            limit=k,
            ef_search=ef_search,
        )

        elapsed = perf_counter() - start
        latencies.append(elapsed * 1000)

    p50 = float(np.percentile(latencies, 50))
    p95 = float(np.percentile(latencies, 95))

    return p50, p95


# K_VALUES = [5, 10, 20, 50, 100]
K_VALUES = [20]
T_VALUES = [50, 95]
Ef_SEARCH = [40, 80]


def measure_latency(
    query, k: int, runs: int = 20, ef_search: int | None = None
) -> tuple[float, float]:
    query_embedding = embedding_service.embed_text(query)

    with Session(engine) as session:

        return measure_search_latency(
            session=session,
            query_embedding=query_embedding,
            k=k,
            runs=runs,
            ef_search=ef_search,
        )


mean_latency_by_ef = {ef: {t: [] for t in T_VALUES} for ef in Ef_SEARCH}


for ef in Ef_SEARCH:
    for k in K_VALUES:
        for query in evaluation_queries:
            latency = measure_latency(
                # query="0-dimensional biomaterials show inductive properties.",
                query=query,
                k=k,
                runs=20,
                ef_search=ef,
            )
            mean_latency_by_ef[ef][T_VALUES[0]].append(latency[0])
            mean_latency_by_ef[ef][T_VALUES[1]].append(latency[1])

            print(f"K={k}, EF = {ef} , P50:{latency[0]}ms, P95:{latency[1]}ms")

print("mean_latency_by_ef", mean_latency_by_ef)

for ef in Ef_SEARCH:
    for t in T_VALUES:
        print(f"K=20, EF = {ef} ,P{t}: {np.mean(mean_latency_by_ef[ef][t])}ms")

# K=5, P50: 64.97479999779898 ms
# K=5, P95: 71.37798999974622 ms
# K=10, P50: 64.35815000077127 ms
# K=10, P95: 66.62407499843539 ms
# K=20, P50: 63.903749998644344 ms
# K=20, P95: 66.93717999969522 ms
# K=50, P50: 64.86129999939294 ms
# K=50, P95: 81.32649000035599 ms
# K=100, P50: 64.3882999993366 ms
# K=100, P95: 68.02913999745215 ms


# 1query = "0-dimensional biomaterials show inductive properties."

# K=20, EF = 10 ,P50: 46.872849999999744ms
# K=20, EF = 10 ,P95: 51.119904999995924ms
# K=20, EF = 20 ,P50: 47.76609999998982ms
# K=20, EF = 20 ,P95: 52.31164999986504ms
# K=20, EF = 40 ,P50: 46.66244999953051ms
# K=20, EF = 40 ,P95: 50.05326999976205ms
# K=20, EF = 80 ,P50: 64.30905000024723ms
# K=20, EF = 80 ,P95: 69.86800499930723ms
# K=20, EF = 100 ,P50: 66.27074999960314ms
# K=20, EF = 100 ,P95: 75.13601499977085ms


# 10 queries
# K=20, EF = 40 , P50:49.1975499999171ms, P95:54.87110500021117ms
# K=20, EF = 40 , P50:47.491400000126305ms, P95:51.714239999728306ms
# K=20, EF = 40 , P50:49.65050000009796ms, P95:53.86450500027422ms
# K=20, EF = 40 , P50:49.413100000492705ms, P95:53.65103000031013ms
# K=20, EF = 40 , P50:48.79404999974213ms, P95:51.44086000000243ms
# K=20, EF = 40 , P50:49.30599999988772ms, P95:53.08694499981357ms
# K=20, EF = 40 , P50:49.87415000005058ms, P95:53.24192499933815ms
# K=20, EF = 40 , P50:48.54325000042081ms, P95:52.011889999948835ms
# K=20, EF = 40 , P50:48.31469999999172ms, P95:50.95759500004533ms
# K=20, EF = 40 , P50:48.900899999807734ms, P95:50.88730499928715ms

# K=20, EF = 80 , P50:65.33005000028425ms, P95:68.95028999924762ms
# K=20, EF = 80 , P50:65.46195000009902ms, P95:68.15961499960395ms
# K=20, EF = 80 , P50:66.06600000031904ms, P95:69.52007000022604ms
# K=20, EF = 80 , P50:65.58464999989155ms, P95:70.91989000027752ms
# K=20, EF = 80 , P50:66.59700000000157ms, P95:72.23411999993914ms
# K=20, EF = 80 , P50:66.41665000006469ms, P95:72.74472499962032ms
# K=20, EF = 80 , P50:66.07365000036225ms, P95:69.19779500012737ms
# K=20, EF = 80 , P50:65.34174999978859ms, P95:70.86275000051502ms
# K=20, EF = 80 , P50:66.0285499998281ms, P95:69.72461499958627ms
# K=20, EF = 80 , P50:66.03629999972327ms, P95:69.65687500028253ms


# 300 queries
# K=20, EF = 40 ,P50: 47.06139449994225ms
# K=20, EF = 40 ,P95: 51.239878650045284ms
# K=20, EF = 80 ,P50: 67.07643300016571ms
# K=20, EF = 80 ,P95: 71.37749501665166ms
