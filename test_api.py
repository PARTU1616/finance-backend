"""
Quick API test script to verify the backend is working.

Usage:
    python test_api.py
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_api():
    print("🧪 Testing Finance Backend API\n")
    
    # Test 1: Check if server is running
    print("1. Testing server health...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("   ✓ Server is running")
        else:
            print("   ✗ Server returned unexpected status")
            return
    except requests.exceptions.ConnectionError:
        print("   ✗ Cannot connect to server. Make sure it's running with: python app.py")
        return
    
    # Test 2: Login
    print("\n2. Testing login...")
    login_data = {
        "email": "admin@finance.com",
        "password": "admin123"
    }
    session = requests.Session()
    response = session.post(f"{BASE_URL}/auth/login/", json=login_data)
    
    if response.status_code == 200 and response.json().get('ok'):
        print("   ✓ Login successful")
        user_data = response.json().get('data')
        print(f"   User: {user_data.get('email')} (Role: {user_data.get('role')})")
    else:
        print(f"   ✗ Login failed: {response.json()}")
        return
    
    # Test 3: Get session
    print("\n3. Testing session retrieval...")
    response = session.get(f"{BASE_URL}/auth/session/")
    if response.status_code == 200 and response.json().get('ok'):
        print("   ✓ Session retrieved successfully")
    else:
        print(f"   ✗ Session retrieval failed: {response.json()}")
    
    # Test 4: Create transaction
    print("\n4. Testing transaction creation...")
    transaction_data = {
        "amount": 5000.00,
        "type": "income",
        "category": "Salary",
        "date": "2024-01-15",
        "notes": "Test transaction"
    }
    response = session.post(f"{BASE_URL}/transactions/create/", json=transaction_data)
    
    if response.status_code == 200 and response.json().get('ok'):
        print("   ✓ Transaction created successfully")
        txn_id = response.json().get('data').get('id')
    else:
        print(f"   ✗ Transaction creation failed: {response.json()}")
        txn_id = None
    
    # Test 5: List transactions
    print("\n5. Testing transaction listing...")
    response = session.get(f"{BASE_URL}/transactions/list/")
    if response.status_code == 200 and response.json().get('ok'):
        records = response.json().get('records', [])
        print(f"   ✓ Found {len(records)} transaction(s)")
    else:
        print(f"   ✗ Transaction listing failed: {response.json()}")
    
    # Test 6: Get dashboard summary
    print("\n6. Testing dashboard summary...")
    response = session.get(f"{BASE_URL}/dashboard/summary/")
    if response.status_code == 200 and response.json().get('ok'):
        data = response.json().get('data')
        print("   ✓ Dashboard summary retrieved")
        print(f"   Total Income: ${data.get('total_income', 0):.2f}")
        print(f"   Total Expenses: ${data.get('total_expenses', 0):.2f}")
        print(f"   Net Balance: ${data.get('net_balance', 0):.2f}")
    else:
        print(f"   ✗ Dashboard summary failed: {response.json()}")
    
    # Test 7: Delete transaction (cleanup)
    if txn_id:
        print(f"\n7. Testing transaction deletion (cleanup)...")
        response = session.post(f"{BASE_URL}/transactions/delete/{txn_id}/")
        if response.status_code == 200 and response.json().get('ok'):
            print("   ✓ Transaction deleted successfully")
        else:
            print(f"   ✗ Transaction deletion failed: {response.json()}")
    
    # Test 8: Logout
    print("\n8. Testing logout...")
    response = session.post(f"{BASE_URL}/auth/logout/")
    if response.status_code == 200 and response.json().get('ok'):
        print("   ✓ Logout successful")
    else:
        print(f"   ✗ Logout failed: {response.json()}")
    
    print("\n✅ All tests completed!")
    print("\nAPI is working correctly. You can now:")
    print("  - Build a frontend application")
    print("  - Test with Postman or cURL")
    print("  - Review API_DOCUMENTATION.md for full API details")

if __name__ == "__main__":
    test_api()
