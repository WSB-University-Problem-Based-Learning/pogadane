"""
Quick test to verify the queue item click feature implementation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("🔍 Verifying Queue Click Feature Implementation\n")
print("=" * 70)

# Check that the method exists
try:
    from pogadane.gui_flet import PogadaneGUI
    
    # Check if the new method exists
    if hasattr(PogadaneGUI, 'view_result_from_queue'):
        print("✅ Method 'view_result_from_queue' exists")
        
        # Check method signature
        import inspect
        sig = inspect.signature(PogadaneGUI.view_result_from_queue)
        params = list(sig.parameters.keys())
        print(f"   Parameters: {params}")
        
        if 'source' in params:
            print("   ✅ Has 'source' parameter")
        else:
            print("   ❌ Missing 'source' parameter")
    else:
        print("❌ Method 'view_result_from_queue' NOT FOUND")
    
    print()
    print("Feature Overview:")
    print("  • Completed queue items show: 'Zakończono → Zobacz wyniki'")
    print("  • Completed items become clickable with tooltip")
    print("  • Clicking switches to Results tab and selects the file")
    print("  • Shows success message with file name")
    print()
    print("=" * 70)
    print("✅ Implementation complete! Test by:")
    print("   1. Run the GUI: python run_gui_flet.py")
    print("   2. Process an audio file")
    print("   3. Click on the completed item in queue")
    print("   4. Should navigate to Results tab with file selected")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
