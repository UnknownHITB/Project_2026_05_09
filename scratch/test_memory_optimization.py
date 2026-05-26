import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.curdir))

from app.core.memory import memory

def test_context_consistency():
    print("Testing memory context consistency...")

    # Setup test data
    memory.store_fact("test_user", "hobby", "speed")
    memory.add_episode("Test episode summary", "test")
    memory.set_rule("Test rule", "Be consistent.")

    # Get data individually
    facts = memory.get_facts(entity='test_user')
    episodes = memory.get_recent_episodes(limit=3)
    rules = memory.get_all_rules()

    # Get data consolidated
    context = memory.get_full_context(entity='test_user', episodic_limit=3)

    # Compare
    assert facts == context["facts"], f"Facts mismatch: {facts} != {context['facts']}"
    assert episodes == context["episodes"], f"Episodes mismatch: {episodes} != {context['episodes']}"
    assert "Be consistent." in context["rules"], "Rule missing from context"

    print("✅ Memory context consistency test passed!")

if __name__ == "__main__":
    try:
        test_context_consistency()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
