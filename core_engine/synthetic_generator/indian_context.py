"""
FraudShield - Indian Context Data Pools
Localized bank names, merchant names, cities, and categories for synthetic data.
"""

import random
from datetime import datetime, timedelta, timezone

# IST offset
IST = timezone(timedelta(hours=5, minutes=30))

INDIAN_BANKS = [
    "State Bank of India", "HDFC Bank", "ICICI Bank", "Punjab National Bank",
    "Bank of Baroda", "Axis Bank", "Canara Bank", "Union Bank of India",
    "Indian Bank", "Bank of India", "Central Bank of India", "Kotak Mahindra Bank",
    "IndusInd Bank", "Yes Bank", "IDBI Bank", "Federal Bank",
]

INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Kochi",
    "Surat", "Nagpur", "Indore", "Bhopal", "Patna", "Vadodara",
    "Coimbatore", "Visakhapatnam", "Thiruvananthapuram", "Guwahati",
]

MERCHANT_CATEGORIES = [
    "Groceries", "Electronics", "Fuel", "Restaurants", "Travel",
    "Healthcare", "Education", "Entertainment", "Clothing", "Utilities",
    "Insurance", "Jewellery", "Real Estate", "Automobile", "Online Shopping",
]

INDIAN_MERCHANTS = {
    "Groceries": ["Big Bazaar", "DMart", "Reliance Fresh", "More Supermarket", "Star Bazaar"],
    "Electronics": ["Croma", "Reliance Digital", "Vijay Sales", "Poorvika Mobiles"],
    "Fuel": ["Indian Oil", "Bharat Petroleum", "Hindustan Petroleum", "Shell India"],
    "Restaurants": ["Swiggy Partner", "Zomato Partner", "Haldirams", "Barbeque Nation", "Saravana Bhavan"],
    "Travel": ["MakeMyTrip", "IRCTC", "Yatra", "Goibibo", "RedBus"],
    "Healthcare": ["Apollo Pharmacy", "Medplus", "Practo", "1mg", "PharmEasy"],
    "Education": ["Byju's", "Unacademy", "Vedantu", "Coursera India"],
    "Entertainment": ["BookMyShow", "PVR Cinemas", "Netflix India", "Hotstar"],
    "Clothing": ["Myntra", "Ajio", "Fabindia", "Raymond", "Allen Solly"],
    "Utilities": ["Jio Recharge", "Airtel Payments", "BESCOM", "Tata Power"],
    "Insurance": ["LIC", "HDFC Life", "SBI Life", "ICICI Prudential"],
    "Jewellery": ["Tanishq", "Kalyan Jewellers", "Malabar Gold", "PC Jeweller"],
    "Real Estate": ["NoBroker", "MagicBricks", "99acres", "Housing.com"],
    "Automobile": ["Maruti Suzuki", "Hyundai India", "Tata Motors", "Mahindra"],
    "Online Shopping": ["Amazon India", "Flipkart", "Meesho", "Snapdeal", "JioMart"],
}

ACCOUNT_HOLDERS = [
    "Aarav Sharma", "Priya Patel", "Rohit Kumar", "Ananya Singh", "Vijay Reddy",
    "Sneha Nair", "Arjun Gupta", "Divya Iyer", "Karthik Menon", "Pooja Deshpande",
    "Rahul Verma", "Meera Krishnan", "Suresh Yadav", "Lakshmi Pillai", "Aditya Joshi",
    "Neha Agarwal", "Manish Tiwari", "Kavitha Rajan", "Sanjay Mishra", "Deepa Moorthy",
]


def random_ist_timestamp(days_back: int = 30) -> datetime:
    """Generate a random IST timestamp within the last N days."""
    now = datetime.now(IST)
    delta = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    return now - delta


def random_odd_hour_timestamp(days_back: int = 30) -> datetime:
    """Generate a random timestamp specifically between midnight and 5 AM IST."""
    now = datetime.now(IST)
    day_offset = timedelta(days=random.randint(0, days_back))
    target_date = (now - day_offset).replace(
        hour=random.randint(0, 4),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )
    return target_date


def random_merchant(category: str = None) -> tuple[str, str]:
    """Return a random (merchant_name, merchant_category) tuple."""
    if category is None:
        category = random.choice(MERCHANT_CATEGORIES)
    merchants = INDIAN_MERCHANTS.get(category, ["Unknown Merchant"])
    return random.choice(merchants), category


def random_account_number() -> str:
    """Generate a random 12-digit Indian bank account number."""
    return "".join([str(random.randint(0, 9)) for _ in range(12)])
