from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import traceback

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(tempfile.gettempdir(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print('UPLOAD_FOLDER set to', app.config['UPLOAD_FOLDER'])

# Knowledge base for chatbot
KNOWLEDGE_BASE = {
    # Existing features removed as requested
}

def find_relevant_answer(user_query):
    """Find relevant answer from knowledge base or provide intelligent responses"""
    user_query_lower = user_query.lower().strip()

    # Meter reader task keywords
    meter_reading_terms = ['meter reading', 'read meter', 'meter reader', 'reading route', 'readings', 'meter reading process']
    data_record_terms = ['record', 'data record', 'log', 'save data', 'entry', 'data entry', 'record reading', 'store reading']
    meter_check_terms = ['meter check', 'check meter', 'meter inspection', 'meter condition', 'faulty meter', 'meter verification', 'meter test']
    illegal_connection_terms = ['illegal connection', 'kunda', 'theft', 'unauthorized connection', 'bypass', 'wire theft', 'illegal hook']
    consumer_complaint_terms = ['complaint', 'consumer complaint', 'billing complaint', 'service complaint', 'report issue', 'problem with consumer', 'customer complaint']
    real_life_terms = ['problem', 'issue', 'situation', 'scenario', 'challenge', 'real-life', 'real life']
    
    # Specific problem situations
    locked_terms = ['locked', 'inaccessible', 'gate closed', 'no access', 'cannot enter', 'taala', 'band']
    dog_terms = ['dog', 'animal', 'kutta', 'bite', 'dangerous animal', 'pet']
    weather_terms = ['weather', 'rain', 'storm', 'baarish', 'flood', 'pani']
    faulty_meter_terms = ['broken', 'faulty', 'tampered', 'kharab', 'jal gaya', 'burnt meter', 'screen off', 'blank screen', 'meter jala']
    dispute_terms = ['angry', 'dispute', 'gussa', 'larai', 'fight', 'argue', 'badtameezi']

    # Handle greetings
    if any(word in user_query_lower for word in ['hello', 'hi', 'hey', 'assalam', 'salaam']):
        return "👋 Hello! I'm your WAPDA Meter Reader Assistant. I can help you with meter reading, data recording, meter checking, illegal connection reporting, and consumer complaint handling. What would you like to know?"

    # Handle voice-related queries
    if any(word in user_query_lower for word in ['voice', 'speak', 'speech', 'audio', 'sound']):
        return "🔊 I support voice input and output! Click the microphone button to speak your questions, and enable voice responses to hear my answers. Try asking about meter reading tasks or complaint handling."

    # Handle file upload queries
    if any(word in user_query_lower for word in ['upload', 'file', 'image', 'pdf', 'document']):
        return "📁 I can help you upload images and PDF files. Click the upload button to select and send files. I can process both images and documents!"

    # Handle feature questions
    if any(word in user_query_lower for word in ['feature', 'what can you do', 'capabilities', 'help']):
        return """🤖 Here's what I can do:

📌 **Meter Reader Tasks:**
• Explain how meter reading works
• Help with meter reading route planning
• Describe accurate data recording steps
• Guide meter checking and fault inspection
• Explain illegal connection reporting (kunda, bypass)
• Describe consumer complaint handling process

🔊 **Voice Features:**
• Speak your questions using the microphone
• Listen to my responses with voice output
• Toggle voice on/off anytime

📁 **File Upload:**
• Upload images (PNG, JPG, JPEG, GIF, BMP)
• Upload PDF documents
• Automatic file processing

❓ **Ask me anything related to meter reading or consumer service!"""

    # Specific meter reader responses
    if any(term in user_query_lower for term in meter_reading_terms):
        return "📊 **Meter Reading Guide:**\n\n1. Verify the assigned route and meter list.\n2. Visit each meter carefully with PPE.\n3. Read the meter accurately and note the digits.\n4. Record readings clearly in the app or ledger.\n5. Report missing or inaccessible meters immediately."

    if any(term in user_query_lower for term in data_record_terms):
        return "📝 **Data Recording Best Practices:**\n\n- Record meter numbers and readings immediately.\n- Use clear, legible notes or mobile entry.\n- Save data in the app or logbook at the same time.\n- Verify entries before submission to avoid mistakes."

    if any(term in user_query_lower for term in meter_check_terms):
        return "🔎 **Meter Checking Process:**\n\n- Inspect the meter for damage or tampering.\n- Check seals, meter number, and connection wires.\n- Compare the reading with the previous record.\n- Report any faults or abnormal behavior to your supervisor."

    if any(term in user_query_lower for term in illegal_connection_terms):
        return "🚨 **Illegal Connection Reporting:**\n\n- Look for unauthorized wires, bypasses, or meter tampering.\n- Note the exact location and meter details.\n- Take a photo if it is safe and allowed.\n- Report the issue to the field office and follow official procedures."

    if any(term in user_query_lower for term in consumer_complaint_terms):
        return "📞 **Consumer Complaint Handling:**\n\n- Listen carefully to the consumer's issue.\n- Record complaint details clearly.\n- Inspect the meter and service connection if needed.\n- Report the complaint through the system and follow up until resolution."

    # Specific Problem Scenarios
    if any(term in user_query_lower for term in locked_terms):
        return "🔒 **Locked or Inaccessible Meter Scenario:**\n\n- Do not attempt to climb walls or enter without permission.\n- Try calling out or ringing the bell again.\n- If no response, clearly note the exact location and access issue (e.g., 'House Locked').\n- Take a photo of the locked gate for proof if required.\n- Schedule a revisit or report to the supervisor."

    if any(term in user_query_lower for term in dog_terms):
        return "🐕 **Aggressive Animals / Dogs Scenario:**\n\n- Safety first! Do not enter premises if a dangerous dog is loose.\n- Ask the owner to tie up the dog before you enter.\n- Maintain a safe distance and do not make sudden movements.\n- Note 'Inaccessible due to dog' in your log if the owner is unavailable.\n- Report the situation to your supervisor."

    if any(term in user_query_lower for term in weather_terms):
        return "⛈️ **Bad Weather / Rain Scenario:**\n\n- Do not risk electrocution. Avoid touching wet meters or exposed wires.\n- Wear proper rain gear and rubber-soled, non-slip shoes.\n- Protect your recording device (mobile/logbook) from water damage.\n- Document any delays caused by the weather and resume safely."

    if any(term in user_query_lower for term in faulty_meter_terms):
        return "⚠️ **Broken / Burnt / Faulty Meter Scenario:**\n\n- Do not touch a burnt or heavily damaged meter.\n- If the screen is blank/off, try pressing the display button if safe.\n- Take a clear picture of the damaged or blank meter.\n- Record it as 'Defective/Burnt' in your system.\n- Immediately report the exact location to the maintenance team."

    if any(term in user_query_lower for term in dispute_terms):
        return "😠 **Angry Consumer / Dispute Scenario:**\n\n- Stay calm and polite. Do not argue back.\n- Listen to their concern (often about high bills or readings).\n- Explain that you are only recording the current reading.\n- Advise them to visit the local subdivision office with their bill for complaints.\n- If you feel unsafe, leave the premises immediately and report to your supervisor."

    if any(term in user_query_lower for term in real_life_terms):
        return "⚠️ **General Real-Life Meter Reader Situations:**\n\nMeter readers face many field challenges: Locked gates, aggressive dogs, bad weather, faulty meters, and angry consumers. Ask me about a specific situation like 'locked gate', 'dog', 'burnt meter', or 'angry customer' for specific guidance!"

    # Handle thank you
    if any(word in user_query_lower for word in ['thank', 'thanks', 'shukriya']):
        return "🙏 You're welcome! I'm glad I could help. Feel free to ask me anything else about meter reading or service support."

    # Handle goodbye
    if any(word in user_query_lower for word in ['bye', 'goodbye', 'see you', 'allah hafiz']):
        return "👋 Goodbye! Have a great day. Come back anytime if you need assistance with meter reading or report handling!"

    # Handle direct questions about meter reader work
    if '?' in user_query or any(word in user_query_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which']):
        return f"🤔 You've asked: '{user_query}'\n\nI can answer meter reader questions about reading, recording, checking meters, illegal connection reporting, and consumer complaint handling. Ask me for step-by-step guidance!"

    # Default response for other inputs
    return f"💬 I received your message: '{user_query}'\n\nI'm here to help with meter reading, data recording, meter checking, illegal connection reports, and consumer complaint handling. What would you like to do next?"

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files and 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No file found in request.'}), 400

    # Check for both 'file' and 'image' keys for backward compatibility
    file = request.files.get('file') or request.files.get('image')
    
    if not file or file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Unsupported file type. Please upload images (PNG, JPG, JPEG, GIF, BMP) or PDF files.'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    file_url = f'/uploads/{filename}'
    
    # Determine file type for response
    file_type = "file"
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        file_type = "image"
    elif filename.lower().endswith('.pdf'):
        file_type = "PDF"
    
    return jsonify({
        'success': True, 
        'message': f'{file_type.capitalize()} uploaded successfully.', 
        'filename': filename, 
        'url': file_url,
        'type': file_type
    })

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message.strip():
        return jsonify({'response': 'Please type a message.'})
    
    # Find relevant answer
    answer = find_relevant_answer(user_message)
    
    if answer:
        bot_response = answer
    else:
        bot_response = f"I'm a specialist chatbot about WAPDA meter reading and MDC (Meter Data Controller) operations. Your question '{user_message}' seems unrelated to my expertise. Please ask me about:\n- Meter reading processes\n- WAPDA operations\n- MDC responsibilities\n- Billing procedures\n- Meter types\n- Consumer categories\n- Any issues related to meter data and WAPDA"
    
    return jsonify({'response': bot_response})

@app.errorhandler(Exception)
def handle_exception(e):
    error_message = traceback.format_exc()
    app.logger.error('Unhandled exception:\n%s', error_message)
    if request.path.startswith('/api'):
        return jsonify({'success': False, 'message': 'Server error', 'error': str(e)}), 500
    return 'Internal Server Error', 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

