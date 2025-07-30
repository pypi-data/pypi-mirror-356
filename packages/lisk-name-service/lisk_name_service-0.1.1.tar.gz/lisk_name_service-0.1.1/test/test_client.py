from src.client import LNSClient

client = LNSClient("2370a32fae91c2077a24f60bb6bbb288e16240bbae814bf52d424cc54f4a7efb")

try:
    address = client.resolve("testname")
    print(f"✅ Resolved address: {address}")
except Exception as e:
    print(f"❌ Error: {e}")
    