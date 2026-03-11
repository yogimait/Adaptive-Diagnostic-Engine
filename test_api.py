import ssl
import json
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "http://localhost:8000"

def post_json(url, data=None):
    req = urllib.request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    if data:
        data_bytes = json.dumps(data).encode("utf-8")
        req.data = data_bytes
        
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.read().decode()}")
        return None

def get_json(url):
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.read().decode()}")
        return None

def run_test():
    print("1. Starting Session...")
    data = post_json(f"{BASE_URL}/start-session")
    if not data:
        print("Failed to start session.")
        return
        
    print("Start result:")
    print(json.dumps(data, indent=2))
    
    session_id = data.get("session_id")
    next_question = data
    
    print("\n2. Submitting Answers...")
    for i in range(12): # try to do 12 to test TestCompleted exceptions
        print(f"--- Question {i+1} ---")
        if "difficulty" in next_question:
            print(f"Difficulty Served: {next_question['difficulty']}")
            
        # Select first option as dummy answer
        ans = next_question["options"][0]
        
        payload = {
            "session_id": session_id,
            "question_id": next_question["question_id"],
            "answer": ans
        }
        
        data_submit = post_json(f"{BASE_URL}/submit-answer", payload)
        if not data_submit:
            break
            
        print("Submit Result:")
        print(json.dumps(data_submit, indent=2))
            
        if data_submit.get("test_completed"):
            print("Test naturally completed after this submit.")
            break
            
        next_question = data_submit["next_question"]
        
    print("\n3. Getting Final Result...")
    res_final = get_json(f"{BASE_URL}/result/{session_id}")
    if res_final:
        print("Final Result:")
        print(json.dumps(res_final, indent=2))

if __name__ == "__main__":
    run_test()
