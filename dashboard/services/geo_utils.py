"""
🌍 Geographic Utilities for FraudShield
Maps Indian city names to high-precision coordinates for Pydeck visuals.
"""

CITY_COORDINATES = {
    "Mumbai": [19.0760, 72.8777],
    "Delhi": [28.6139, 77.2090],
    "Bengaluru": [12.9716, 77.5946],
    "Hyderabad": [17.3850, 78.4867],
    "Ahmedabad": [23.0225, 72.5714],
    "Chennai": [13.0827, 80.2707],
    "Kolkata": [22.5726, 88.3639],
    "Surat": [21.1702, 72.8311],
    "Pune": [18.5204, 73.8567],
    "Jaipur": [26.9124, 75.7873],
    "Lucknow": [26.8467, 80.9462],
    "Kanpur": [26.4499, 80.3319],
    "Nagpur": [21.1458, 79.0882],
    "Indore": [22.7196, 75.8577],
    "Thane": [19.2183, 72.9781],
    "Bhopal": [23.2599, 77.4126],
    "Visakhapatnam": [17.6868, 83.2185],
    "Pimpri-Chinchwad": [18.6279, 73.8010],
    "Patna": [25.5941, 85.1376],
    "Vadodara": [22.3072, 73.1812],
    "Ghaziabad": [28.6692, 77.4538],
    "Ludhiana": [30.9010, 75.8573],
    "Agra": [27.1767, 78.0081],
    "Nashik": [19.9975, 73.7898],
    "Ranchi": [23.3441, 85.3096],
    "Faridabad": [28.4089, 77.3178],
    "Meerut": [28.9845, 77.7064],
    "Rajkot": [22.2735, 70.7513],
    "Kalyan-Dombivli": [19.2402, 73.1305],
    "Vasai-Virar": [19.3919, 72.8397],
    "Varanasi": [25.3176, 82.9739],
    "Srinagar": [34.0837, 74.7973],
    "Aurangabad": [19.8762, 75.3433],
    "Dhanbad": [23.7957, 86.4304],
    "Amritsar": [31.6340, 74.8723],
    "Navi Mumbai": [19.0330, 73.0297],
    "Prayagraj": [25.4358, 81.8463],
    "Howrah": [22.5958, 88.2636],
    "Gwalior": [26.2124, 78.1773],
    "Jabalpur": [23.1815, 79.9864],
    "Coimbatore": [11.0168, 76.9558],
    "Vijayawada": [16.5062, 80.6480],
    "Madurai": [9.9252, 78.1198],
    "Raipur": [21.2514, 81.6296],
    "Kota": [25.2138, 75.8648],
    "Guwahati": [26.1445, 91.7362],
    "Chandigarh": [30.7333, 76.7794],
    "Solapur": [17.6599, 75.9064],
    "Hubballi-Dharwad": [15.3647, 75.1240],
    "Bareilly": [28.3670, 79.4304]
}

def get_coords(city_name: str) -> list[float]:
    """Return [lat, lon] for a given city name, or a default center of India."""
    return CITY_COORDINATES.get(city_name, [20.5937, 78.9629])
