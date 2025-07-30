#!/usr/bin/env python3
"""
Quick test for GitHub Actions
"""

def test_basic_functionality():
    """Test basic functionality without requiring API keys"""
    try:
        from multipromptify import MultiPromptifyAPI
        import pandas as pd
        
        # Test 1: Basic import
        print("✅ Import successful")
        
        # Test 2: Create instance
        mp = MultiPromptifyAPI()
        print("✅ Instance creation successful")
        
        # Test 3: Load data
        data = [{'question': 'Test?', 'answer': 'Yes'}]
        mp.load_dataframe(pd.DataFrame(data))
        print("✅ Data loading successful")
        
        # Test 4: Set template (without AI variations)
        template = {
            'instruction_template': 'Q: {question}\nA: {answer}',
            'question': ['surface'],  # Non-AI variation
            'gold': 'answer'
        }
        mp.set_template(template)
        print("✅ Template setting successful")
        
        # Test 5: Configure
        mp.configure(max_rows=1, variations_per_field=1)
        print("✅ Configuration successful")
        
        print("🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1) 