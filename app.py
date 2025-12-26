from flask import Flask, render_template, request, jsonify, session, redirect
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid
import cv2
import hashlib
from difflib import get_close_matches


# ==================== INITIALIZE FLASK ====================
app = Flask(__name__)
app.secret_key = os.urandom(24)


# ==================== CONFIGURATION ====================
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


# ==================== FLOWER DISEASE DATABASE ====================
SYMPTOM_DB = {
    "Rose Powdery Mildew": {
        "name": "Rose Powdery Mildew",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "White powdery coating on flowers, distorted blooms, poor flower opening",
        "cause": "Fungal infection favored by warm days and cool nights",
        "treatment": "Remove affected buds, improve air circulation, apply fungicides if needed",
        "prevention": "Grow in sunny positions, water at base, avoid crowded flowers",
        "affected_parts": ["flowers", "petals", "buds"]
    },
    "Rose Black Spot": {
        "name": "Rose Black Spot",
        "category": "Fungal",
        "severity": "High",
        "symptoms": "Dark irregular patches on stems and flowers, weak undersized blooms",
        "cause": "Fungal infection spreading in wet weather",
        "treatment": "Remove affected stems, keep surface dry, apply fungicides",
        "prevention": "Maintain airflow, avoid overhead watering, remove spent flowers",
        "affected_parts": ["stems", "flowers", "leaves"]
    },
    "Rose Rust": {
        "name": "Rose Rust",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "Rust-colored patches on stems and flower bases, weakened buds",
        "cause": "Rust fungus spreading in moist conditions",
        "treatment": "Prune affected shoots, dispose material, apply rust fungicides",
        "prevention": "Keep bushes open, avoid flower wetting, clean old stems",
        "affected_parts": ["stems", "flowers", "buds"]
    },
    "Lily Botrytis Blight": {
        "name": "Lily Botrytis Blight",
        "category": "Fungal",
        "severity": "High",
        "symptoms": "Brown spots on petals, tan patches, flowers collapse or drop",
        "cause": "Botrytis fungus in cool wet conditions",
        "treatment": "Remove affected flowers, avoid wetting blooms, apply fungicides",
        "prevention": "Space lilies properly, water at base, remove spent flowers",
        "affected_parts": ["flowers", "petals", "buds"]
    },
    "Tulip Fire": {
        "name": "Tulip Fire",
        "category": "Fungal",
        "severity": "High",
        "symptoms": "Brown/gray spots on petals, scorch lesions, distorted blooms",
        "cause": "Botrytis fungus on infected bulbs in cool wet spring",
        "treatment": "Remove distorted flowers and infected bulbs",
        "prevention": "Plant healthy bulbs, ensure drainage, rotate planting sites",
        "affected_parts": ["flowers", "petals", "buds"]
    },
    "Chrysanthemum White Rust": {
        "name": "Chrysanthemum White Rust",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "Pale patches and blister-like pustules on flower supports",
        "cause": "Rust fungus in cool moist conditions",
        "treatment": "Remove affected shoots, apply rust fungicides",
        "prevention": "Use clean material, space stems well, avoid moisture on blooms",
        "affected_parts": ["stems", "flowers", "leaves"]
    },
    "Gerbera Powdery Mildew": {
        "name": "Gerbera Powdery Mildew",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "White powdery coating on stalks and petals, stunted blooms",
        "cause": "Powdery mildew in warm stagnant air",
        "treatment": "Increase airflow, remove affected stalks, apply fungicides",
        "prevention": "Avoid overcrowding, water at base, maintain moderate humidity",
        "affected_parts": ["flowers", "stems", "petals"]
    },
    "Orchid Black Rot": {
        "name": "Orchid Black Rot",
        "category": "Fungal",
        "severity": "High",
        "symptoms": "Water-soaked dark patches at spike base, flower death",
        "cause": "Fungal/water-mold in poor air movement",
        "treatment": "Cut back spikes to healthy tissue, use fungicides",
        "prevention": "Avoid water pooling, ensure ventilation, use clean media",
        "affected_parts": ["flowers", "spikes", "buds"]
    },
    "Hibiscus Powdery Mildew": {
        "name": "Hibiscus Powdery Mildew",
        "category": "Fungal",
        "severity": "Medium",
        "symptoms": "White powdery patches on buds and petals, reduced flowering",
        "cause": "Powdery mildew in warm conditions with poor air movement",
        "treatment": "Remove affected buds, improve circulation, apply fungicides",
        "prevention": "Space shoots properly, avoid late watering, monitor regularly",
        "affected_parts": ["flowers", "buds", "petals"]
    }
}


# Symptom keywords mapping
SYMPTOM_KEYWORDS = {
    "powdery": ["Rose Powdery Mildew", "Gerbera Powdery Mildew", "Hibiscus Powdery Mildew"],
    "black spot": ["Rose Black Spot"],
    "rust": ["Rose Rust", "Chrysanthemum White Rust"],
    "blight": ["Lily Botrytis Blight", "Tulip Fire"],
    "rot": ["Orchid Black Rot"],
    "white": ["Chrysanthemum White Rust"],
    "brown spots": ["Lily Botrytis Blight", "Tulip Fire"],
    "patches": ["Rose Black Spot", "Rose Powdery Mildew"],
    "wilting": ["Orchid Black Rot"],
    "collapse": ["Lily Botrytis Blight"],
    "rose": ["Rose Powdery Mildew", "Rose Black Spot", "Rose Rust"],
    "lily": ["Lily Botrytis Blight"],
    "tulip": ["Tulip Fire"],
    "chrysanthemum": ["Chrysanthemum White Rust"],
    "gerbera": ["Gerbera Powdery Mildew"],
    "orchid": ["Orchid Black Rot"],
    "hibiscus": ["Hibiscus Powdery Mildew"],
    "spots": ["Rose Black Spot", "Lily Botrytis Blight", "Tulip Fire"],
    "coating": ["Rose Powdery Mildew", "Gerbera Powdery Mildew", "Hibiscus Powdery Mildew"],
    "distorted": ["Rose Powdery Mildew", "Tulip Fire"],
    "scorch": ["Tulip Fire"],
    "pustules": ["Chrysanthemum White Rust"],
    "pale": ["Chrysanthemum White Rust"],
    "dark patches": ["Orchid Black Rot"],
    "stunted": ["Gerbera Powdery Mildew"]
}


# ==================== HELPER FUNCTIONS ====================


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def find_disease_by_symptoms(symptom_text):
    """Find disease matching symptom keywords"""
    symptom_text = symptom_text.lower().strip()
    matched_diseases = set()
    
    for keyword, diseases in SYMPTOM_KEYWORDS.items():
        if keyword in symptom_text:
            matched_diseases.update(diseases)
    
    if matched_diseases:
        return [SYMPTOM_DB[d] for d in matched_diseases]
    
    # Fuzzy matching if no keyword match
    disease_names = list(SYMPTOM_DB.keys())
    close_matches = get_close_matches(symptom_text, disease_names, n=2, cutoff=0.6)
    if close_matches:
        return [SYMPTOM_DB[d] for d in close_matches]
    
    return list(SYMPTOM_DB.values())[:3]


def predict_image_disease(image_path):
    """Analyze image and predict disease"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None, "Invalid image format"
        
        # Use hash to select disease (for demo)
        h = hashlib.md5(image_path.encode()).hexdigest()
        diseases = list(SYMPTOM_DB.keys())
        selected_disease = diseases[int(h, 16) % len(diseases)]
        return selected_disease, SYMPTOM_DB[selected_disease]
    except Exception as e:
        return None, f"Error: {str(e)}"


def get_chat_history():
    """Get chat history from session"""
    return session.get('chat_history', [])


def add_to_history(role, content, image_url=None):
    """Add message to chat history"""
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    history_item = {
        'role': role,
        'content': content,
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'type': 'image' if image_url else 'text'
    }
    
    if image_url:
        history_item['image_url'] = image_url
    
    session['chat_history'].append(history_item)
    session.modified = True


def clear_chat_history():
    """Clear chat history"""
    session['chat_history'] = []
    session.modified = True


def get_database_stats():
    """Get database statistics"""
    return {
        'total_diseases': len(SYMPTOM_DB),
        'total_keywords': len(SYMPTOM_KEYWORDS),
        'high_severity': len([d for d in SYMPTOM_DB.values() if d['severity'] == 'High']),
        'medium_severity': len([d for d in SYMPTOM_DB.values() if d['severity'] == 'Medium']),
        'categories': list(set([d['category'] for d in SYMPTOM_DB.values()]))
    }


# ==================== ROUTES ====================


@app.route('/')
def index():
    """Home page"""
    if 'user' in session:
        return redirect('/dashboard')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            session['user'] = username
            session['chat_history'] = []
            return redirect('/dashboard')
        return render_template('login.html', error='Please enter a username')
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect('/login')


@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    if 'user' not in session:
        return redirect('/login')
    
    return render_template(
        'dashboard.html',
        user=session['user'],
        diseases=SYMPTOM_DB,
        chat_history=get_chat_history(),
        stats=get_database_stats()
    )


# ==================== API ENDPOINTS ====================


@app.route('/api/chat-message', methods=['POST'])
def chat_message():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Add user message to history
        add_to_history('user', user_message)
        
        # Find matching disease based on symptoms
        matched_diseases = find_disease_by_symptoms(user_message)
        
        if matched_diseases:
            bot_response = f"🌺 Based on your symptoms, here are possible diseases:\n\n"
            for disease in matched_diseases[:3]:
                bot_response += f"**{disease['name']}** - Severity: {disease['severity']}\n"
                bot_response += f"Symptoms: {disease['symptoms']}\n\n"
        else:
            bot_response = "😊 Please provide more details about the symptoms you see on your flowers."
        
        # Add bot response to history
        add_to_history('bot', bot_response)
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'history': get_chat_history()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/upload-image-chat', methods=['POST'])
def upload_image_chat():
    """Upload image in chat and analyze"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        user_input = request.form.get('description', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Predict disease from image
        disease_name, disease_info = predict_image_disease(filepath)
        
        if disease_name is None:
            return jsonify({'error': disease_info}), 500
        
        # Prepare response
        image_url = f'/static/uploads/{filename}'
        user_msg = f"📸 Image uploaded"
        if user_input:
            user_msg += f": {user_input}"
        
        # Add user message with image
        add_to_history('user', user_msg, image_url)
        
        # Generate structured response with baby pink background
        affected_parts_html = ', '.join(disease_info['affected_parts'])
        severity_color = '#FF6B6B' if disease_info['severity'] == 'High' else '#FFA500'

        bot_response = f"""<div style="background:#FFE4E1;border-radius:10px;padding:20px;border-left:5px solid #FF69B4;">
  <h2 style="color:#C71585;margin-bottom:15px;">🔍 Disease Analysis Results</h2>

  <div style="background:#FFFFFF;border-radius:8px;padding:15px;margin-bottom:15px;">
    <h3 style="color:#FF1493;margin-bottom:10px;">{disease_info['name']}</h3>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:5px;">
      <div><strong>Category:</strong> {disease_info['category']}</div>
      <div>
        <strong>Severity:</strong>
        <span style="background:{severity_color};color:#FFFFFF;padding:3px 8px;border-radius:3px;font-weight:bold;">
          {disease_info['severity']}
        </span>
      </div>
    </div>
  </div>

  <div style="background:#FFF0F5;border-radius:8px;padding:12px 15px;margin-bottom:10px;">
    <h4 style="color:#C71585;margin-bottom:6px;">📋 Symptoms</h4>
    <p style="margin:0;color:#333333;line-height:1.6;">{disease_info['symptoms']}</p>
  </div>

  <div style="background:#FFF0F5;border-radius:8px;padding:12px 15px;margin-bottom:10px;">
    <h4 style="color:#C71585;margin-bottom:6px;">🔎 Cause</h4>
    <p style="margin:0;color:#333333;line-height:1.6;">{disease_info['cause']}</p>
  </div>

  <div style="background:#FFF0F5;border-radius:8px;padding:12px 15px;margin-bottom:10px;">
    <h4 style="color:#C71585;margin-bottom:6px;">💊 Treatment</h4>
    <p style="margin:0;color:#333333;line-height:1.6;">{disease_info['treatment']}</p>
  </div>

  <div style="background:#FFF0F5;border-radius:8px;padding:12px 15px;margin-bottom:10px;">
    <h4 style="color:#C71585;margin-bottom:6px;">🛡️ Prevention</h4>
    <p style="margin:0;color:#333333;line-height:1.6;">{disease_info['prevention']}</p>
  </div>

  <div style="background:#FFF0F5;border-radius:8px;padding:12px 15px;">
    <h4 style="color:#C71585;margin-bottom:6px;">🌿 Affected Parts</h4>
    <p style="margin:0;color:#333333;line-height:1.6;">{affected_parts_html}</p>
  </div>
</div>"""
        
        # If user provided description, also analyze it
        if user_input:
            matched = find_disease_by_symptoms(user_input)
            if matched and matched[0]['name'] != disease_name:
                bot_response += f"\n\n⚠️ **Note:** Based on your description, this could also be **{matched[0]['name']}**. Please verify by checking the symptoms carefully."
        
        # Add bot response
        add_to_history('bot', bot_response)
        
        return jsonify({
            'success': True,
            'disease': disease_name,
            'disease_info': disease_info,
            'image_url': image_url,
            'response': bot_response,
            'history': get_chat_history()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-image-tab', methods=['POST'])
def upload_image_tab():
    """Upload image from upload tab and analyze"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        user_description = request.form.get('description', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Predict disease
        disease_name, disease_info = predict_image_disease(filepath)
        
        if disease_name is None:
            return jsonify({'error': disease_info}), 500
        
        # Also check user description if provided
        alternate_matches = []
        if user_description:
            alternate_matches = find_disease_by_symptoms(user_description)
        
        return jsonify({
            'success': True,
            'disease': disease_name,
            'disease_info': disease_info,
            'image_url': f'/static/uploads/{filename}',
            'alternate_matches': [d for d in alternate_matches if d['name'] != disease_name][:2]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search-symptoms', methods=['POST'])
def search_symptoms():
    """Search diseases by symptoms"""
    try:
        data = request.get_json()
        symptom_text = data.get('symptom', '').strip()
        
        if not symptom_text:
            return jsonify({'error': 'Please enter symptoms'}), 400
        
        # Find matching diseases
        matched_diseases = find_disease_by_symptoms(symptom_text)
        
        return jsonify({
            'success': True,
            'results': matched_diseases,
            'count': len(matched_diseases)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get all diseases"""
    return jsonify(list(SYMPTOM_DB.values()))


@app.route('/api/disease/<disease_name>', methods=['GET'])
def get_disease(disease_name):
    """Get specific disease"""
    if disease_name in SYMPTOM_DB:
        return jsonify(SYMPTOM_DB[disease_name])
    return jsonify({'error': 'Disease not found'}), 404


@app.route('/api/chat-history', methods=['GET'])
def get_history():
    """Get chat history"""
    return jsonify(get_chat_history())


@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history"""
    try:
        clear_chat_history()
        return jsonify({
            'success': True,
            'message': 'Chat history cleared',
            'history': get_chat_history()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        return jsonify({
            'success': True,
            'stats': get_database_stats()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/search-keyword', methods=['POST'])
def search_keyword():
    """Search diseases by keyword"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip().lower()
        
        if not keyword:
            return jsonify({'error': 'Please enter a keyword'}), 400
        
        # Search in keywords
        results = []
        if keyword in SYMPTOM_KEYWORDS:
            for disease_name in SYMPTOM_KEYWORDS[keyword]:
                results.append(SYMPTOM_DB[disease_name])
        
        # Also search in disease names
        for disease_name, disease_info in SYMPTOM_DB.items():
            if keyword in disease_name.lower() and disease_info not in results:
                results.append(disease_info)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ==================== ERROR HANDLERS ====================


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(413)
def request_too_large(error):
    """Handle file too large errors"""
    return jsonify({'error': 'File too large. Maximum 16MB allowed.'}), 413


# ==================== MAIN ====================


if __name__ == '__main__':
    print("=" * 60)
    print("🌸 FLOWER DISEASE ADVISOR - STARTING")
    print("=" * 60)
    print("✅ Database loaded: 9 flower diseases")
    print("✅ Keywords loaded: 25+ symptom keywords")
    print("✅ Upload folder: " + UPLOAD_FOLDER)
    print("✅ Max file size: 16MB")
    print("=" * 60)
    print("🌐 Open browser: http://localhost:5000")
    print("📸 Features: Chat, Image Upload, Search, Browse, History")
    print("🎤 Voice: Microphone Input & Text-to-Speech Output")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)