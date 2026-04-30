"""FraudShield - Synthetic Generator"""
import uuid, random
from datetime import datetime, timedelta, timezone
from core import settings

IST = timezone(timedelta(hours=5, minutes=30))

INDIAN_BANKS = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Punjab National Bank", "Axis Bank", "Kotak Mahindra Bank", "IndusInd Bank", "Canara Bank", "Bank of Baroda"]
INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur",
    "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara",
    "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Ranchi", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli", "Vasai-Virar",
    "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Prayagraj", "Howrah", "Gwalior", "Jabalpur",
    "Coimbatore", "Vijayawada", "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubballi-Dharwad", "Bareilly"
]
MERCHANT_CATEGORIES = ["Groceries", "Electronics", "Fuel", "Restaurants", "Travel", "Utilities", "Shopping", "Entertainment"]
INDIAN_MERCHANTS = {
    "Groceries": ["Big Bazaar", "DMart", "Reliance Fresh", "Nature's Basket", "More Retail"],
    "Electronics": ["Croma", "Reliance Digital", "Vijay Sales", "Apple Store BKC", "Samsung Plaza"],
    "Fuel": ["Indian Oil", "Bharat Petroleum", "HP", "Shell"],
    "Restaurants": ["Swiggy", "Zomato", "Haldirams", "Barbeque Nation", "Paradise Biryani"],
    "Travel": ["MakeMyTrip", "IRCTC", "RedBus", "Indigo", "Air India"],
    "Utilities": ["Jio Recharge", "Airtel Payments", "BESCOM", "MSEDCL", "Adani Electricity"],
    "Shopping": ["Amazon.in", "Flipkart", "Myntra", "Ajio", "Tata CLiQ"],
    "Entertainment": ["BookMyShow", "Netflix India", "Prime Video", "PVR Cinemas", "Inox"]
}
ACCOUNT_HOLDERS = [
    "Aarav Sharma", "Priya Patel", "Rohit Kumar", "Ananya Singh", "Sneha Nair",
    "Vikram Malhotra", "Meera Reddy", "Siddharth Gupta", "Kavita Rao", "Arjun Verma",
    "Sanya Kapur", "Rohan Das", "Ishita Chatterjee", "Rahul Bose", "Zoya Khan",
    "Aditya Joshi", "Riya Sen", "Amitabh Bachchan", "Deepika Padukone", "Virat Kohli"
]

def random_ist_timestamp(days_back=30):
    return datetime.now(IST) - timedelta(days=random.randint(0, days_back), hours=random.randint(0, 23), minutes=random.randint(0, 59))

def random_odd_hour_timestamp(days_back=30):
    return (datetime.now(IST) - timedelta(days=random.randint(0, days_back))).replace(hour=random.randint(0, 4), minute=random.randint(0, 59))

def random_merchant(cat=None):
    cat = cat or random.choice(MERCHANT_CATEGORIES)
    return random.choice(INDIAN_MERCHANTS.get(cat, ["Unknown"])), cat

def random_account_number():
    return "".join(str(random.randint(0, 9)) for _ in range(12))

def inject_anomalies(transactions, anomaly_count):
    if anomaly_count <= 0 or not transactions: return transactions
    weights = settings.ANOMALY_INJECTION_WEIGHTS
    idx = random.sample(range(len(transactions)), min(anomaly_count, len(transactions)))
    types = []
    for atype, w in weights.items(): types.extend([atype] * max(1, int(anomaly_count * w)))
    random.shuffle(types)
    for i, j in enumerate(idx):
        atype = types[i % len(types)]
        txn = transactions[j]
        if atype == "high_value": txn["amount"] = random.uniform(75000, 500000)
        elif atype == "odd_hours": txn["timestamp"] = random_odd_hour_timestamp()
        elif atype == "velocity": txn["_velocity_flag"] = True
        elif atype == "geo_anomaly": txn["city"] = random.choice([c for c in INDIAN_CITIES if c != txn.get("city")] or ["Unknown"])
        elif atype == "merchant_mismatch":
            txn["merchant_category"] = random.choice([c for c in MERCHANT_CATEGORIES if c != txn.get("merchant_category")])
            txn["merchant_name"] = f"Unusual-{txn['merchant_category']}"
        txn["is_flagged"] = True
    return transactions

def generate_transactions(count=None):
    count = count or settings.SYNTHETIC_TRANSACTION_COUNT
    anomaly_count = int(count * settings.ANOMALY_PERCENTAGE)
    accounts = [{"account_number": random_account_number(), "account_holder": random.choice(ACCOUNT_HOLDERS), "bank_name": random.choice(INDIAN_BANKS), "home_city": random.choice(INDIAN_CITIES), "preferred": random.sample(MERCHANT_CATEGORIES, k=2)} for _ in range(max(20, count // 50))]
    
    transactions = []
    for i in range(count):
        acc = random.choice(accounts)
        m_name, m_cat = random_merchant(random.choice(acc["preferred"]))
        transactions.append({
            "id": str(uuid.uuid4()), "account_number": acc["account_number"], "account_holder": acc["account_holder"],
            "amount": round(random.uniform(100, 45000), 2), "timestamp": random_ist_timestamp(),
            "city": acc["home_city"], "merchant_name": m_name, "merchant_category": m_cat,
            "bank_name": acc["bank_name"], "transaction_type": random.choice(["Credit", "Debit"]), "is_flagged": False
        })
    return inject_anomalies(transactions, anomaly_count)
