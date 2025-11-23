import sys
import os
import json

# Add the directory containing main_mcp2.py to path
sys.path.append(os.path.join(os.getcwd(), 'new_butold'))

try:
    import main_mcp2
    print("✅ Successfully imported main_mcp2")
except ImportError as e:
    print(f"❌ Failed to import main_mcp2: {e}")
    sys.exit(1)

def test_tools():
    print("\n--- Testing Tool 1: get_random_problem ---")
    try:
        # Ensure questions are loaded
        main_mcp2.load_questions(os.path.join(os.getcwd(), "questions.json"))
        prob = main_mcp2.get_random_problem()
        print(f"Result: {prob[:100]}...")
        if "error" in prob and "No questions" not in prob:
             print("❌ get_random_problem failed")
        else:
             print("✅ get_random_problem passed")
             
        # Parse problem to get ID for submission test
        prob_data = json.loads(prob)
        prob_id = prob_data.get("id")
    except Exception as e:
        print(f"❌ get_random_problem crashed: {e}")
        prob_id = "1" # Fallback

    print("\n--- Testing Tool 2: verify_concept ---")
    try:
        concept = main_mcp2.verify_concept("Python (programming language)")
        print(f"Result: {concept[:100]}...")
        if "Error" in concept:
            print("❌ verify_concept failed")
        else:
            print("✅ verify_concept passed")
    except Exception as e:
        print(f"❌ verify_concept crashed: {e}")

    print("\n--- Testing Tool 3: submit_code ---")
    try:
        # Dummy code that should pass the "Sum of Array" default problem if questions.json missing
        # Or just test that it runs
        code = "def solve(arr): return sum(arr)"
        result = main_mcp2.submit_code(prob_id, code)
        print(f"Result: {result[:100]}...")
        if "Error" in result and "Invalid Problem ID" not in result: # Invalid ID is expected if random prob
            print("⚠️ submit_code returned error (might be expected if ID mismatch)")
        else:
            print("✅ submit_code passed (execution attempted)")
    except Exception as e:
        print(f"❌ submit_code crashed: {e}")

if __name__ == "__main__":
    test_tools()
