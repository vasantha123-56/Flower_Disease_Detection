"""
NLP Database Module - Flower Disease Advisor
Contains all symptom and disease data with keyword mappings
"""

# ==================== COMPLETE SYMPTOM DATABASE ====================

SYMPTOM_DB = {
    "Rose Powdery Mildew": {
        "name": "Rose Powdery Mildew",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "White powdery coating on flowers, distorted blooms, poor flower opening",
        "cause": "Fungal infection favored by warm days and cool nights",
        "treatment": "Remove affected buds, improve air circulation, apply fungicides if needed",
        "prevention": "Grow in sunny positions, water at base, avoid crowded flowers",
        "affected_parts": ["flowers", "petals", "buds"],
        "common_keywords": ["powdery", "white coating", "distorted", "roses"]
    },
    "Rose Black Spot": {
        "name": "Rose Black Spot",
        "category": "Fungal",
        "severity": "High",
        "symptoms": "Dark irregular patches on stems and flowers, weak undersized blooms",
        "cause": "Fungal infection spreading in wet weather",
        "treatment": "Remove affected stems, keep surface dry, apply fungicides",
        "prevention": "Maintain airflow, avoid overhead watering, remove spent flowers",
        "affected_parts": ["stems", "flowers", "leaves"],
        "common_keywords": ["black spot", "dark patches", "weak blooms", "roses"]
    },
    "Rose Rust": {
        "name": "Rose Rust",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "Rust-colored patches on stems and flower bases, weakened buds",
        "cause": "Rust fungus spreading in moist conditions",
        "treatment": "Prune affected shoots, dispose material, apply rust fungicides",
        "prevention": "Keep bushes open, avoid flower wetting, clean old stems",
        "affected_parts": ["stems", "flowers", "buds"],
        "common_keywords": ["rust", "rust colored", "orange patches", "roses"]
    },
    "Lily Botrytis Blight": {
        "name": "Lily Botrytis Blight",
        "category": "Fungal",
        "severity": "High",
        "symptoms": "Brown spots on petals, tan patches, flowers collapse or drop",
        "cause": "Botrytis fungus in cool wet conditions",
        "treatment": "Remove affected flowers, avoid wetting blooms, apply fungicides",
        "prevention": "Space lilies properly, water at base, remove spent flowers",
        "affected_parts": ["flowers", "petals", "buds"],
        "common_keywords": ["brown spots", "blight", "collapse", "lilies", "tan patches"]
    },
    "Tulip Fire": {
        "name": "Tulip Fire",
        "category": "Fungal",
        "severity": "High",
        "symptoms": "Brown/gray spots on petals, scorch lesions, distorted blooms",
        "cause": "Botrytis fungus on infected bulbs in cool wet spring",
        "treatment": "Remove distorted flowers and infected bulbs",
        "prevention": "Plant healthy bulbs, ensure drainage, rotate planting sites",
        "affected_parts": ["flowers", "petals", "buds"],
        "common_keywords": ["tulip fire", "brown spots", "scorch", "distorted", "tulips"]
    },
    "Chrysanthemum White Rust": {
        "name": "Chrysanthemum White Rust",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "Pale patches and blister-like pustules on flower supports",
        "cause": "Rust fungus in cool moist conditions",
        "treatment": "Remove affected shoots, apply rust fungicides",
        "prevention": "Use clean material, space stems well, avoid moisture on blooms",
        "affected_parts": ["stems", "flowers", "leaves"],
        "common_keywords": ["white rust", "pustules", "pale patches", "chrysanthemum"]
    },
    "Gerbera Powdery Mildew": {
        "name": "Gerbera Powdery Mildew",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "White powdery coating on stalks and petals, stunted blooms",
        "cause": "Powdery mildew in warm stagnant air",
        "treatment": "Increase airflow, remove affected stalks, apply fungicides",
        "prevention": "Avoid overcrowding, water at base, maintain moderate humidity",
        "affected_parts": ["flowers", "stems", "petals"],
        "common_keywords": ["powdery", "gerbera", "white coating", "stunted"]
    },
    "Orchid Black Rot": {
        "name": "Orchid Black Rot",
        "category": "Fungal",
        "severity": "High",
        "symptoms": "Water-soaked dark patches at spike base, flower death",
        "cause": "Fungal/water-mold in poor air movement",
        "treatment": "Cut back spikes to healthy tissue, use fungicides",
        "prevention": "Avoid water pooling, ensure ventilation, use clean media",
        "affected_parts": ["flowers", "spikes", "buds"],
        "common_keywords": ["black rot", "orchid", "water-soaked", "dark patches"]
    },
    "Hibiscus Powdery Mildew": {
        "name": "Hibiscus Powdery Mildew",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "White powdery patches on buds and petals, reduced flowering",
        "cause": "Powdery mildew in warm conditions with poor air movement",
        "treatment": "Remove affected buds, improve circulation, apply fungicides",
        "prevention": "Space shoots properly, avoid late watering, monitor regularly",
        "affected_parts": ["flowers", "buds", "petals"],
        "common_keywords": ["powdery", "hibiscus", "white patches", "reduced flowering"]
    }
}


# ==================== SYMPTOM KEYWORDS MAPPING ====================

SYMPTOM_KEYWORDS = {
    # Powdery mildew keywords
    "powdery": ["Rose Powdery Mildew", "Gerbera Powdery Mildew", "Hibiscus Powdery Mildew"],
    "white powdery": ["Rose Powdery Mildew", "Gerbera Powdery Mildew", "Hibiscus Powdery Mildew"],
    "white coating": ["Rose Powdery Mildew", "Gerbera Powdery Mildew", "Hibiscus Powdery Mildew"],
    "white powder": ["Rose Powdery Mildew", "Gerbera Powdery Mildew", "Hibiscus Powdery Mildew"],
    "white patches": ["Hibiscus Powdery Mildew", "Rose Powdery Mildew"],
    
    # Black spot keywords
    "black spot": ["Rose Black Spot"],
    "dark patches": ["Rose Black Spot", "Orchid Black Rot"],
    "dark irregular": ["Rose Black Spot"],
    
    # Rust keywords
    "rust": ["Rose Rust", "Chrysanthemum White Rust"],
    "rust colored": ["Rose Rust"],
    "orange patches": ["Rose Rust"],
    "white rust": ["Chrysanthemum White Rust"],
    "pustules": ["Chrysanthemum White Rust"],
    
    # Blight keywords
    "blight": ["Lily Botrytis Blight", "Tulip Fire"],
    "brown spots": ["Lily Botrytis Blight", "Tulip Fire"],
    "tan patches": ["Lily Botrytis Blight"],
    "collapse": ["Lily Botrytis Blight"],
    "scorch": ["Tulip Fire"],
    
    # Rot keywords
    "rot": ["Orchid Black Rot"],
    "black rot": ["Orchid Black Rot"],
    "water-soaked": ["Orchid Black Rot"],
    "wilting": ["Orchid Black Rot"],
    
    # General keywords
    "distorted": ["Rose Powdery Mildew", "Tulip Fire"],
    "weak blooms": ["Rose Black Spot"],
    "stunted": ["Gerbera Powdery Mildew"],
    "reduced flowering": ["Hibiscus Powdery Mildew"],
    
    # Flower-specific keywords
    "roses": ["Rose Powdery Mildew", "Rose Black Spot", "Rose Rust"],
    "lilies": ["Lily Botrytis Blight"],
    "tulips": ["Tulip Fire"],
    "gerbera": ["Gerbera Powdery Mildew"],
    "orchid": ["Orchid Black Rot"],
    "hibiscus": ["Hibiscus Powdery Mildew"],
    "chrysanthemum": ["Chrysanthemum White Rust"]
}


# ==================== HELPER FUNCTIONS ====================

def get_disease_by_name(disease_name):
    """
    Get disease information by exact name
    
    Args:
        disease_name (str): Name of the disease
    
    Returns:
        dict: Disease information or None if not found
    """
    return SYMPTOM_DB.get(disease_name)


def get_all_diseases():
    """
    Get all diseases in database
    
    Returns:
        list: List of all disease dictionaries
    """
    return list(SYMPTOM_DB.values())


def get_disease_names():
    """
    Get list of all disease names
    
    Returns:
        list: List of disease names
    """
    return list(SYMPTOM_DB.keys())


def search_by_keyword(keyword):
    """
    Search diseases by keyword
    
    Args:
        keyword (str): Search keyword
    
    Returns:
        list: List of matching disease objects
    """
    keyword = keyword.lower()
    results = []
    
    # Check exact keyword match
    if keyword in SYMPTOM_KEYWORDS:
        matched_names = SYMPTOM_KEYWORDS[keyword]
        results = [SYMPTOM_DB[name] for name in matched_names]
    
    return results


def find_matching_diseases(text):
    """
    Find diseases matching text input
    
    Args:
        text (str): User input text
    
    Returns:
        list: List of matching disease dictionaries
    """
    text = text.lower()
    matched = []
    matched_diseases = set()
    
    # Check for keyword matches
    for keyword, diseases in SYMPTOM_KEYWORDS.items():
        if keyword in text:
            matched_diseases.update(diseases)
    
    # Convert to disease objects
    for disease_name in matched_diseases:
        matched.append(SYMPTOM_DB[disease_name])
    
    return matched


def get_disease_by_severity(severity):
    """
    Get all diseases of a certain severity
    
    Args:
        severity (str): 'High' or 'Medium'
    
    Returns:
        list: List of matching diseases
    """
    return [d for d in get_all_diseases() if d['severity'] == severity]


def get_disease_by_affected_part(part):
    """
    Get diseases affecting specific plant part
    
    Args:
        part (str): Plant part (e.g., 'flowers', 'stems', 'leaves')
    
    Returns:
        list: List of diseases affecting that part
    """
    part = part.lower()
    return [d for d in get_all_diseases() if part in [p.lower() for p in d['affected_parts']]]


def get_disease_symptoms(disease_name):
    """
    Get symptoms for specific disease
    
    Args:
        disease_name (str): Name of disease
    
    Returns:
        str: Symptoms description or None
    """
    disease = get_disease_by_name(disease_name)
    return disease['symptoms'] if disease else None


def get_disease_treatment(disease_name):
    """
    Get treatment for specific disease
    
    Args:
        disease_name (str): Name of disease
    
    Returns:
        str: Treatment description or None
    """
    disease = get_disease_by_name(disease_name)
    return disease['treatment'] if disease else None


def get_disease_prevention(disease_name):
    """
    Get prevention tips for specific disease
    
    Args:
        disease_name (str): Name of disease
    
    Returns:
        str: Prevention tips or None
    """
    disease = get_disease_by_name(disease_name)
    return disease['prevention'] if disease else None


# ==================== STATISTICS ====================

def get_database_stats():
    """
    Get statistics about the disease database
    
    Returns:
        dict: Statistics
    """
    all_diseases = get_all_diseases()
    high_severity = get_disease_by_severity("High")
    medium_severity = get_disease_by_severity("Medium")
    
    return {
        "total_diseases": len(all_diseases),
        "high_severity_count": len(high_severity),
        "medium_severity_count": len(medium_severity),
        "total_keywords": len(SYMPTOM_KEYWORDS),
        "fungal_count": sum(1 for d in all_diseases if d['category'] == 'Fungal'),
        "categories": list(set([d['category'] for d in all_diseases]))
    }


# ==================== DEMO/TESTING ====================

if __name__ == "__main__":
    """Test the database"""
    print("🌸 Flower Disease Database")
    print("=" * 50)
    print(f"\nTotal diseases: {len(SYMPTOM_DB)}")
    print(f"Total keywords: {len(SYMPTOM_KEYWORDS)}")
    print("\nDiseases:")
    for disease_name in get_disease_names():
        disease = get_disease_by_name(disease_name)
        print(f"  - {disease_name} ({disease['severity']})")
    
    stats = get_database_stats()
    print(f"\nStatistics:")
    print(f"  Total: {stats['total_diseases']}")
    print(f"  High Severity: {stats['high_severity_count']}")
    print(f"  Medium Severity: {stats['medium_severity_count']}")
    print(f"  Fungal: {stats['fungal_count']}")