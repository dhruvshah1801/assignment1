import threading
import heapq


class Job:
    def __init__(self, arrival, job_id, priority, duration, resources, order):
        self.arrival = arrival
        self.job_id = job_id
        self.priority = priority
        self.duration = duration
        self.resources = resources
        self.order = order

        self.worker = None
        self.start = None
        self.finish = None


def simulate_scheduler(workers, jobs):
    # Sort jobs according to arrival time
    jobs.sort(key=lambda j: (j.arrival, j.order))

    # Priority queue:
    # higher priority first
    # earlier arrival first
    # earlier input order as final tie breaker
    ready_queue = []

    # Worker availability
    worker_available = [0] * workers

    # Results
    completed = []

    # Lock for thread-safe access
    lock = threading.Lock()

    # Each worker has its own thread
    worker_threads = []

    # Condition used to synchronize worker threads
    condition = threading.Condition(lock)

    # State shared by workers
    state = {
        "next_job": 0,
        "current_time": 0,
        "stop": False
    }

    def worker_function(worker_index):
        worker_id = f"W{worker_index + 1}"

        while True:
            with condition:

                while not ready_queue and not state["stop"]:
                    condition.wait()

                if state["stop"] and not ready_queue:
                    return

                # Highest priority first
                _, _, _, job = heapq.heappop(ready_queue)

                # Start job
                start_time = max(
                    job.arrival,
                    worker_available[worker_index]
                )

                job.worker = worker_id
                job.start = start_time
                job.finish = start_time + job.duration

                worker_available[worker_index] = job.finish

                completed.append(job)

    # Create worker threads
    for i in range(workers):
        thread = threading.Thread(
            target=worker_function,
            args=(i + 0,)
        )

        worker_threads.append(thread)
        thread.start()

    # Simulate arrivals
    for job in jobs:

        with condition:

            state["current_time"] = job.arrival

            # PriorityQueue key:
            # negative priority -> higher priority first
            heapq.heappush(
                ready_queue,
                (
                    -job.priority,
                    job.arrival,
                    job.order,
                    job
                )
            )

            condition.notify()

    # Tell workers that no more jobs will arrive
    with condition:
        state["stop"] = True
        condition.notify_all()

    # Wait for all workers
    for thread in worker_threads:
        thread.join()

    # Sort results by job ID/order
    completed.sort(key=lambda j: j.order)

    # Print results
    total_wait = 0

    for job in completed:
        waiting_time = job.start - job.arrival
        total_wait += waiting_time

        print(
            job.job_id,
            job.worker,
            job.start,
            job.finish
        )

    if completed:
        average_wait = total_wait / len(completed)
    else:
        average_wait = 0

    print(f"AVG_WAIT {average_wait:.2f}")


def main():

    # First line:
    # w = workers
    # n = jobs
    w, n = map(int, input().split())

    jobs = []

    for i in range(n):

        arrival, job_id, priority, duration, resources = input().split()

        job = Job(
            int(arrival),
            job_id,
            int(priority),
            int(duration),
            int(resources),
            i
        )

        jobs.append(job)

    simulate_scheduler(w, jobs)


if __name__ == "__main__":
    main()