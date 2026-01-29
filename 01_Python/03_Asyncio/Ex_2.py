import asyncio
import time


async def fetch_data(param):                   # any function that is async and that can pause and resume itself is called a courintine function 
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():      # Couritine function
    task1 = fetch_data(1)  # Could be awaited directly
    task2 = fetch_data(2)  # Could be awaited directly
    result1 = await task1
    print("Task 1 fully completed")
    result2 = await task2
    print("Task 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())    # event loop, we always put main() in the event loop only 
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")

# whenever await is called that particular function is suspended untill and unless that task is not completed, after the fucntion has been suspended the control goes to the event loop
# and then event loop starts executing the already scheduled task and starts completing it 