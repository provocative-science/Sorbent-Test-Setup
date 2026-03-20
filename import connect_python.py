# test_import.py
try:
    import connect_python
    print("✅ connect_python module is available.")
except ImportError as e:
    print("❌ connect_python module NOT found.")
    print(e)