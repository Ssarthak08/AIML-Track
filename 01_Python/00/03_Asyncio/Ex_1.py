# Synchronous coding 

import time


def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)                             # now time.sleep() is non awaitable, that is its not asynchronous in nature so we cant't use await in front of it 
    print(f"Done with {param}")
    return f"Result of {param}"


def main():                               # This is where the function starts 
    result1 = fetch_data(1)
    print("Fetch 1 fully completed")
    result2 = fetch_data(2)
    print("Fetch 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = main()
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")