"""
NLP Bot Module - Flower Disease Advisor
Advanced chatbot for disease diagnosis with NLP capabilities
"""

from difflib import get_close_matches
from nlp_db import SYMPTOM_DB, SYMPTOM_KEYWORDS, find_matching_diseases


# ==================== FLOWER DISEASE NLP BOT CLASS ====================

class FlowerDiseaseNLPBot:
    """
    Advanced NLP Bot for Flower Disease Diagnosis
    Handles natural language queries and returns disease information
    """
    
    def __init__(self):
        """Initialize the NLP Bot"""
        self.symptom_db = SYMPTOM_DB
        self.symptom_keywords = SYMPTOM_KEYWORDS
        self.conversation_history = []
        self.current_disease = None
    
    # ==================== MAIN RESPONSE METHOD ====================
    
    def get_response(self, user_text):
        """
        Get response based on user input
        
        Args:
            user_text (str): User's input text
        
        Returns:
            str: Bot's response
        """
        
        if not user_text or not user_text.strip():
            return "😊 Please describe your flower's symptoms or ask about flower diseases."
        
        text = user_text.lower().strip()
        
        # Add to conversation history
        self.conversation_history.append({
            'user': user_text,
            'bot': None,
            'timestamp': None
        })
        
        # Handle greetings
        if self._is_greeting(text):
            response = self._handle_greeting(text)
        
        # Handle help requests
        elif self._is_help_request(text):
            response = self._handle_help()
        
        # Handle exit requests
        elif self._is_exit_request(text):
            response = self._handle_exit()
        
        # Check for disease names directly
        elif self._check_disease_name(text):
            disease_name = self._check_disease_name(text)
            response = self._format_disease_response(self.symptom_db[disease_name])
            self.current_disease = disease_name
        
        # Check for symptom keywords
        elif self._find_diseases_by_symptoms(text):
            matched_diseases = self._find_diseases_by_symptoms(text)
            response = self._format_multiple_results(matched_diseases)
        
        # Fuzzy matching
        else:
            response = self._handle_unknown_input(text)
        
        # Store bot response in history
        if self.conversation_history:
            self.conversation_history[-1]['bot'] = response
        
        return response
    
    # ==================== GREETING HANDLERS ====================
    
    def _is_greeting(self, text):
        """Check if user is greeting"""
        greeting_words = ["hi", "hello", "hey", "greetings", "hiya", "welcome", "good morning",
                         "good afternoon", "good evening", "howdy", "sup"]
        return any(word in text for word in greeting_words)
    
    def _handle_greeting(self, text):
        """Handle greeting messages"""
        greetings = [
            "Hello 🌸 I can help you identify flower diseases and provide treatment recommendations. "
            "Please describe your flower's symptoms or ask about specific diseases.",
            "Hi there! 🌺 Welcome to the Flower Disease Advisor. Tell me about your flower's symptoms "
            "and I'll help identify the disease.",
            "Greetings! 🌼 I'm here to help diagnose flower diseases. What symptoms are you seeing?",
            "Welcome! 🌹 I specialize in identifying flower diseases. Describe what you see on your flowers."
        ]
        return greetings[hash(text) % len(greetings)]
    
    # ==================== HELP HANDLERS ====================
    
    def _is_help_request(self, text):
        """Check if user is asking for help"""
        help_words = ["help", "what can you do", "how do you work", "capabilities",
                     "what do you do", "how can you help", "guide", "tutorial"]
        return any(word in text for word in help_words)
    
    def _handle_help(self):
        """Handle help requests"""
        return (
            "🌸 I can help with:\n\n"
            "1️⃣ Identify flower diseases from symptoms\n"
            " Example: 'white powdery on my rose'\n\n"
            "2️⃣ Provide treatment recommendations\n"
            " Example: 'how to treat rose black spot'\n\n"
            "3️⃣ Suggest prevention methods\n"
            " Example: 'prevent lily blight'\n\n"
            "4️⃣ Answer disease-specific questions\n"
            " Example: 'what is tulip fire'\n\n"
            "5️⃣ Search all available diseases\n"
            " Example: 'list all fungal diseases'\n\n"
            "Just describe your flower's symptoms or ask about a disease! 🌺"
        )
    
    # ==================== EXIT HANDLERS ====================
    
    def _is_exit_request(self, text):
        """Check if user wants to exit"""
        exit_words = ["exit", "quit", "bye", "goodbye", "see you", "farewell"]
        return any(word in text for word in exit_words)
    
    def _handle_exit(self):
        """Handle exit requests"""
        return "Goodbye! 🌸 Hope your flowers get better soon. See you next time!"
    
    # ==================== DISEASE NAME DETECTION ====================
    
    def _check_disease_name(self, text):
        """
        Check if user mentioned a disease name directly
        
        Args:
            text (str): User input text
        
        Returns:
            str: Disease name if found, None otherwise
        """
        for disease_name in self.symptom_db.keys():
            if disease_name.lower() in text:
                return disease_name
        return None
    
    # ==================== SYMPTOM MATCHING ====================
    
    def _find_diseases_by_symptoms(self, text):
        """
        Find diseases matching user symptoms
        
        Args:
            text (str): User's symptom description
        
        Returns:
            list: List of matching disease objects
        """
        matched_diseases = set()
        
        # Check keywords
        for keyword, diseases in self.symptom_keywords.items():
            if keyword in text:
                matched_diseases.update(diseases)
        
        if matched_diseases:
            return [self.symptom_db[d] for d in matched_diseases]
        
        # Try fuzzy matching if no keyword match
        disease_names = list(self.symptom_db.keys())
        close_matches = get_close_matches(text, disease_names, n=2, cutoff=0.6)
        
        if close_matches:
            return [self.symptom_db[d] for d in close_matches]
        
        return None
    
    # ==================== UNKNOWN INPUT HANDLER ====================
    
    def _handle_unknown_input(self, text):
        """Handle input that doesn't match any pattern"""
        return (
            "😊 I couldn't identify the disease from your description.\n\n"
            "Please provide more details about:\n"
            "• Color and location of the affected areas\n"
            "• Type of flower (rose, lily, tulip, etc.)\n"
            "• When the problem started\n"
            "• Any other unusual signs\n\n"
            "Or try asking about a specific disease! "
            "Type 'help' to see what I can do."
        )
    
    # ==================== RESPONSE FORMATTING ====================
    
    def _format_disease_response(self, disease_info):
        """
        Format disease information for display
        
        Args:
            disease_info (dict): Disease information dictionary
        
        Returns:
            str: Formatted response
        """
        return (
            f"🌺 **Disease:** {disease_info['name']}\n"
            f"**Category:** {disease_info['category']}\n"
            f"**Severity:** {disease_info['severity']}\n\n"
            f"🔍 **Symptoms:**\n"
            f"{disease_info['symptoms']}\n\n"
            f"🦠 **Cause:**\n"
            f"{disease_info['cause']}\n\n"
            f"💊 **Treatment:**\n"
            f"{disease_info['treatment']}\n\n"
            f"🛡️ **Prevention:**\n"
            f"{disease_info['prevention']}\n\n"
            f"📍 **Affected Parts:** {', '.join(disease_info['affected_parts'])}"
        )
    
    def _format_multiple_results(self, diseases):
        """
        Format multiple disease results
        
        Args:
            diseases (list): List of disease dictionaries
        
        Returns:
            str: Formatted response
        """
        if not diseases:
            return "No matching diseases found."
        
        if len(diseases) == 1:
            return self._format_disease_response(diseases[0])
        
        response = "🌺 I found several possible diseases:\n\n"
        
        for i, disease in enumerate(diseases[:5], 1):
            response += (
                f"{i}. **{disease['name']}**\n"
                f" Severity: {disease['severity']}\n"
                f" Symptoms: {disease['symptoms'][:60]}...\n\n"
            )
        
        response += "📝 Please provide more details or tell me which one looks most similar."
        return response
    
    # ==================== DATABASE QUERIES ====================
    
    def get_all_diseases(self):
        """Get all available diseases"""
        return list(self.symptom_db.values())
    
    def get_disease_by_name(self, disease_name):
        """Get specific disease information"""
        if disease_name in self.symptom_db:
            return self.symptom_db[disease_name]
        return None
    
    def search_diseases(self, query):
        """
        Search diseases by name or symptoms
        
        Args:
            query (str): Search query
        
        Returns:
            list: Matching diseases
        """
        query = query.lower()
        results = []
        
        # Search by disease name
        for disease_name, disease_info in self.symptom_db.items():
            if query in disease_name.lower():
                results.append(disease_info)
        
        # Search by symptoms
        if not results:
            for disease_name, disease_info in self.symptom_db.items():
                if query in disease_info['symptoms'].lower():
                    results.append(disease_info)
        
        # Fuzzy matching
        if not results:
            disease_names = list(self.symptom_db.keys())
            close_matches = get_close_matches(query, disease_names, n=3, cutoff=0.6)
            
            for disease_name in close_matches:
                results.append(self.symptom_db[disease_name])
        
        return results
    
    # ==================== CONVERSATION MANAGEMENT ====================
    
    def get_conversation_history(self):
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_current_disease(self):
        """Get currently discussed disease"""
        return self.current_disease
    
    def set_current_disease(self, disease_name):
        """Set current disease context"""
        if disease_name in self.symptom_db:
            self.current_disease = disease_name
            return True
        return False
    
    # ==================== UTILITY METHODS ====================
    
    def get_database_stats(self):
        """Get database statistics"""
        total = len(self.symptom_db)
        high_severity = sum(1 for d in self.symptom_db.values() if d['severity'] == 'High')
        medium_severity = sum(1 for d in self.symptom_db.values() if d['severity'] == 'Medium')
        
        return {
            'total_diseases': total,
            'high_severity': high_severity,
            'medium_severity': medium_severity,
            'total_keywords': len(self.symptom_keywords),
            'fungal_diseases': sum(1 for d in self.symptom_db.values() if d['category'] == 'Fungal')
        }
    
    def get_disease_treatment_steps(self, disease_name):
        """Get treatment steps for disease"""
        disease = self.get_disease_by_name(disease_name)
        if disease:
            return disease['treatment'].split(',')
        return []
    
    def get_disease_prevention_tips(self, disease_name):
        """Get prevention tips for disease"""
        disease = self.get_disease_by_name(disease_name)
        if disease:
            return disease['prevention'].split(',')
        return []


# ==================== HELPER FUNCTIONS ====================

def create_bot():
    """Create and return a new bot instance"""
    return FlowerDiseaseNLPBot()


def check_symptom(user_text):
    """
    Quick function to check symptoms
    
    Args:
        user_text (str): User's symptom description
    
    Returns:
        list: List of matching diseases
    """
    bot = FlowerDiseaseNLPBot()
    return bot._find_diseases_by_symptoms(user_text.lower())


def get_disease_info(disease_name):
    """
    Quick function to get disease info
    
    Args:
        disease_name (str): Name of disease
    
    Returns:
        dict: Disease information
    """
    bot = FlowerDiseaseNLPBot()
    return bot.get_disease_by_name(disease_name)


def search_diseases(query):
    """
    Quick function to search diseases
    
    Args:
        query (str): Search query
    
    Returns:
        list: Matching diseases
    """
    bot = FlowerDiseaseNLPBot()
    return bot.search_diseases(query)


# ==================== DEMO/TESTING ====================

if __name__ == "__main__":
    """Test the bot"""
    bot = FlowerDiseaseNLPBot()
    
    print("🌸 Flower Disease Advisor NLP Bot 🌸")
    print("=" * 70)
    print(f"\nBot initialized with {len(bot.symptom_db)} diseases and {len(bot.symptom_keywords)} keywords\n")
    
    # Test messages
    test_messages = [
        "hello",
        "white powdery coating on my rose",
        "brown spots on lily petals",
        "What is rose black spot?",
        "help",
        "how to prevent tulip fire",
        "goodbye"
    ]
    
    print("Testing bot responses:\n")
    print("-" * 70)
    
    for message in test_messages:
        print(f"\nUser: {message}")
        response = bot.get_response(message)
        print(f"Bot: {response}")
        print("-" * 70)
    
    # Show statistics
    stats = bot.get_database_stats()
    print("\nDatabase Statistics:")
    print(f" Total Diseases: {stats['total_diseases']}")
    print(f" High Severity: {stats['high_severity']}")
    print(f" Medium Severity: {stats['medium_severity']}")
    print(f" Total Keywords: {stats['total_keywords']}")
    print(f" Fungal Diseases: {stats['fungal_diseases']}")