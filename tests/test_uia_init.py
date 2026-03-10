import comtypes.client
import time

print("Attempting to get UIAutomationCore module...")
start = time.time()
try:
    UIAutomationCore = comtypes.client.GetModule("UIAutomationCore.dll")
    print(f"Success in {time.time() - start:.2f}s")
except Exception as e:
    print(f"Failed: {e}")

print("Attempting to create IUIAutomation object...")
start = time.time()
try:
    IUIAutomation = comtypes.client.CreateObject("{ff48dba4-60ef-4201-aa87-54103eef594e}", interface=UIAutomationCore.IUIAutomation)
    print(f"Success in {time.time() - start:.2f}s")
except Exception as e:
    print(f"Failed: {e}")
