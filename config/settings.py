# File: config/settings.py

# Konfigurasi Model LLM
MODEL_SCORING = "llama3-70b-8192"
MODEL_NARRATIVE = "llama3-70b-8192"
MODEL_SUMMARY = "llama3-8b-8192"       # <-- TAMBAHKAN INI
MODEL_RECOMMENDATION = "llama3-70b-8192" # <-- TAMBAHKAN INI
MODEL_COMPARISON = "llama3-70b-8192"   # <-- TAMBAHKAN INI

# Konfigurasi Performa
MAX_CONCURRENT_WORKERS = 5
# File: src/config/settings.py
DOMAINS = ["it", "hr", "finance", "marketing", "sales", "operations", "general"]
CRITERIA_MAP = {
    "hr": ["People Management", "Communication", "Work Experience", "Education", "Certifications", "Strategic Thinking"],
    "it": ["Technical Skills", "Problem Solving", "Work Experience", "Education", "Certifications", "Project Management"],
    "finance": ["Analytical Skills", "Attention to Detail", "Work Experience", "Education", "Certifications", "Compliance Knowledge"],
    "general": ["Problem Solving", "Communication", "Work Experience", "Leadership"]
}
WEIGHTS_MAP = {
    "it": {"Technical Skills": 10, "Problem Solving": 9, "Work Experience": 8, "Project Management": 7, "Certifications": 6, "Education": 5},
    "hr": {"People Management": 10, "Strategic Thinking": 9, "Work Experience": 8, "Communication": 7, "Certifications": 6, "Education": 5},
    "finance": {"Analytical Skills": 10, "Compliance Knowledge": 9, "Work Experience": 8, "Attention to Detail": 8, "Certifications": 6, "Education": 5},
    "general": {"Work Experience": 10, "Problem Solving": 9, "Leadership": 8, "Communication": 7}
}