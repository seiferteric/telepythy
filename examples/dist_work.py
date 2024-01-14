from telepythy import Remote
import random

def do_hard_work(seed):
    # Simulate long running task...
    import time
    import random
    time.sleep(random.randint(1,10))
    return seed+random.randint(1,100)

# Pretend we have 10 different remotes...
remotes = [Remote('localhost') for i in range(0,10)]
results = []
# Run remote jobs
for r in remotes:
    r.run_async(do_hard_work, random.randint(1,100))
# Collect Results
for r in remotes:
    results.append(r.return_async())
# Process results
total = sum(results)
print(f'Total: {total}')
