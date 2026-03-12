import urllib.request
import urllib.parse
import urllib.error
import json
import sys

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
        print(f"\n[Error] HTTP {e.code}: {e.read().decode()}")
        return None
    except urllib.error.URLError:
        print(f"\n[Error] Could not connect to {BASE_URL}. Is the server running?")
        sys.exit(1)

def get_json(url):
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"\n[Error] HTTP {e.code}: {e.read().decode()}")
        return None

def main():
    print("=" * 50)
    print("🎓 Starting Adaptive Diagnostic Test 🎓")
    print("=" * 50)
    
    data = post_json(f"{BASE_URL}/start-session")
    if not data:
        return
        
    session_id = data.get("session_id")
    next_question = data
    question_count = 1
    
    while True:
        print(f"\n📝 Question {question_count}")
        print("-" * 50)
        print(next_question["question"])
        print()
        
        options = next_question["options"]
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")
            
        print()
        
        # Keep asking until valid input
        while True:
            choice = input(f"Select option (1-{len(options)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                selected_answer = options[int(choice) - 1]
                break
            print("Invalid selection. Please try again.")
            
        payload = {
            "session_id": session_id,
            "question_id": next_question["question_id"],
            "answer": selected_answer
        }
        
        result = post_json(f"{BASE_URL}/submit-answer", payload)
        if not result:
            break
            
        print("\n" + ("✅ Correct!" if result.get("correct") else "❌ Incorrect."))
        print(f"Current Ability Score: {result.get('ability'):.2f}")
        
        if result.get("test_completed"):
            break
            
        print("\nLoading Next Question...")
        next_question = result.get("next_question")
        question_count += 1
        
    print("\n" + "=" * 50)
    print("🎉 Test Completed! Generating Results 🎉")
    print("=" * 50)
    
    final_result = get_json(f"{BASE_URL}/result/{session_id}")
    if final_result:
        print(f"\nFinal Ability Score : {final_result.get('ability_score'):.2f}")
        print(f"Accuracy            : {final_result.get('accuracy'):.1f}%")
        
        weak_topics = final_result.get('weak_topics', [])
        print(f"Weak Topics         : {', '.join(weak_topics) if weak_topics else 'None'}")
        
        print("\n" + "-" * 50)
        print("🤖 AI Study Plan")
        print("-" * 50)
        print(final_result.get("study_plan"))
        print("-" * 50)

if __name__ == "__main__":
    main()
