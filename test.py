import time
t0 = time.time()
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model load:", time.time() - t0)

t1 = time.time()
model.encode("warm up")
print("Warmup encode:", time.time() - t1)

t2 = time.time()
model.encode("test resume text")
print("Actual encode:", time.time() - t2)