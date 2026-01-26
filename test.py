import requests
import json

BASE = "http://localhost:5000"

print("\n=== Test 1: Check API is running ===")
r = requests.get(BASE)
print(r.json())

print("\n=== Test 2: Try to get joke without payment ===")
r = requests.get(f"{BASE}/joke")
print(f"Status: {r.status_code}")
print(r.json())

print("\n=== Test 3: Send real payment ===")
print("Now open MetaMask and send 0.01 ETH to your API address")
print("Then paste the transaction hash here:")
tx_hash = input("Transaction Hash: ")

print("\n=== Test 4: Verify payment ===")
r = requests.post(f"{BASE}/verify", 
                  json={"transactionHash": tx_hash})
print(r.json())

print("\n=== Test 5: Get joke with payment proof ===")
r = requests.get(f"{BASE}/joke", 
                 headers={"X-Payment-Proof": tx_hash})
print(r.json())

print("\n=== Test 6: Check stats ===")
r = requests.get(f"{BASE}/stats")
print(r.json())