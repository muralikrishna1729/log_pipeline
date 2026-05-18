import tracemalloc
from src.pipeline.readers import read_lines, read_lines_as_list

LOG_FILE = "data/Linux_2k.log"
# gen = read_lines(LOG_FILE)
# for i,line in enumerate(gen):
#     print(line)
#     if i > 10:
#         break

gen2 = read_lines(LOG_FILE)
print(type(gen2))
print(next(gen2))

print(sum(1 for _ in read_lines(LOG_FILE)))

tracemalloc.start()
for line in read_lines(LOG_FILE):
    pass 
current, peak= tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"Current memory usage for generator: {current / 10**3} KB; Peak memory usage: {peak / 10**3} KB")

tracemalloc.start()
for line in read_lines_as_list(LOG_FILE):
    pass 
current, peak= tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"Current memory usage for list: {current / 10**3} KB; Peak memory usage: {peak / 10**3} KB")