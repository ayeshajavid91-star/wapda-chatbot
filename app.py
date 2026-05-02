from flask import Flask, render_template, request, jsonify, send_from_directory, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import traceback
import json
import difflib

# Load QA database
try:
    with open('qa_database.json', 'r', encoding='utf-8') as f:
        QA_DATABASE = json.load(f)
        QA_QUESTIONS = list(QA_DATABASE.keys())
except FileNotFoundError:
    QA_DATABASE = {}
    QA_QUESTIONS = []

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
app.secret_key = 'wapda_secure_secret_key_2024' # Required for sessions

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(tempfile.gettempdir(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print('UPLOAD_FOLDER set to', app.config['UPLOAD_FOLDER'])

# Knowledge base for chatbot - Filled with 40+ items as requested
KNOWLEDGE_BASE = {
    "wapda": "Water and Power Development Authority of Pakistan, responsible for water and hydropower resources.",
    "mdc": "Meter Data Control/Collector, responsible for reading and managing consumer meter data.",
    "mepco": "Multan Electric Power Company, serving the southern Punjab region.",
    "lesco": "Lahore Electric Supply Company, serving Lahore and surrounding districts.",
    "fesco": "Faisalabad Electric Supply Company.",
    "gepco": "Gujranwala Electric Power Company.",
    "hesco": "Hyderabad Electric Supply Company.",
    "sepco": "Sukkur Electric Power Company.",
    "qesco": "Quetta Electric Power Company.",
    "tesco": "Tribal Electric Supply Company.",
    "smart meter": "An advanced meter that records electricity consumption in real-time and communicates with the utility.",
    "prepaid meter": "A meter where consumers pay for electricity before using it, similar to mobile top-ups.",
    "tariff": "The rate at which electricity is charged to different consumer categories (residential, commercial, industrial).",
    "nepra": "National Electric Power Regulatory Authority, the body that determines tariffs and regulates the sector.",
    "load shedding": "Planned power outages to manage electricity demand when it exceeds supply.",
    "feeder": "A high-voltage line that transmits power from a substation to a specific area.",
    "transformer": "A device used to step down high voltage to a lower voltage (220V) for consumer use.",
    "kunda": "Illegal direct hooks on power lines to steal electricity.",
    "meter tampering": "Illegal manipulation of a meter to slow it down or stop it from recording consumption.",
    "disconnection": "The act of cutting off power supply due to non-payment or illegal activity.",
    "reconnection": "Restoring power supply after clearing dues or fixing violations.",
    "units": "Electricity consumption measured in Kilowatt-hours (kWh). One unit equals 1 kWh.",
    "meter number": "A unique identification number printed on the electricity meter.",
    "reference number": "A 14-digit unique number on the bill used to identify the consumer and pay bills.",
    "bill payment": "Settling electricity charges through banks, apps, or collection centers.",
    "surcharge": "An additional fee or penalty added for late payment of bills.",
    "new connection": "The process of getting a fresh electricity supply for a home or business.",
    "load enhancement": "The process of increasing the sanctioned load for a connection.",
    "subdivision": "The local administrative unit of a DISCO (like MEPCO/LESCO) led by an SDO.",
    "sdo": "Sub-Divisional Officer, the administrative head of a local subdivision.",
    "xen": "Executive Engineer, the senior officer overseeing multiple subdivisions.",
    "lineman": "Technical staff responsible for maintaining power lines and fixing local faults.",
    "grid station": "A high-voltage facility where power is transformed and distributed to feeders.",
    "ppe": "Personal Protective Equipment, essential for safety (gloves, helmets, rubber shoes).",
    "reading route": "The specific path assigned to a meter reader to visit consumers.",
    "energy audit": "The process of calculating power supplied vs. power billed to detect theft.",
    "power theft": "Stealing electricity via bypass, kunda, or tampering, which is a criminal offense.",
    "fir": "First Information Report, filed with police against power thieves.",
    "helpline": "Contact 118 or SMS to 8118 for complaints and emergencies.",
    "pitc": "Power Information Technology Company, handling the billing and data of all DISCOs.",
    "surcharge": "Late payment surcharge is usually 10% of the bill amount.",
    "security deposit": "The refundable amount paid when applying for a new connection."
}

# Urdu Language Support Dictionary
URDU_KNOWLEDGE = {
    "میٹر": "میٹر بجلی کی کھپت کو ماپنے والا آلہ ہے۔ اسے صاف رکھیں اور چھیڑ چھاڑ سے گریز کریں۔",
    "بجلی": "بجلی ایک قیمتی اثاثہ ہے، اسے ضرورت کے وقت ہی استعمال کریں تاکہ بل کم آئے۔",
    "شکایت": "کسی بھی شکایت کے لیے آپ ہیلپ لائن 118 پر کال کر سکتے ہیں۔",
    "بل": "اپنا بل وقت پر ادا کریں تاکہ جرمانے اور کنکشن کٹنے سے بچ سکیں۔",
    "کنڈہ": "کنڈہ لگانا غیر قانونی ہے اور اس کی سزا بھاری جرمانہ اور جیل ہو سکتی ہے۔",
    "سلام": "وعلیکم السلام! میں آپ کا میٹر ریڈر اسسٹنٹ ہوں۔ میں آپ کی کیا مدد کر سکتا ہوں؟",
    "مدد": "میں میٹر ریڈنگ، بلنگ، اور واپڈا کے دیگر معاملات میں آپ کی مدد کر سکتا ہوں۔",
    "لوڈ شیڈنگ": "لوڈ شیڈنگ سسٹم کی بہتری یا بجلی کی کمی کی صورت میں کی جاتی ہے۔",
    "کنکشن": "نیا کنکشن حاصل کرنے کے لیے قریبی سب ڈویژن آفس میں درخواست جمع کروائیں۔",
    "ادائیگی": "آپ اپنا بل بینک، ایزی پیسہ، یا جاز کیش کے ذریعے ادا کر سکتے ہیں۔",
    "شکریہ": "آپ کا بہت شکریہ! اگر مزید کوئی سوال ہو تو ضرور پوچھیں۔",
    "معلومات": "میں آپ کو میٹر ریڈنگ، بلنگ، اور واپڈا کے قوانین کے بارے میں معلومات دے سکتا ہوں۔",
    "خراب": "اگر میٹر خراب ہے تو فوری طور پر اپنے قریبی دفتر میں رپورٹ کریں۔",
    "چوری": "بجلی چوری ایک بڑا جرم ہے، اس سے ہمیشہ بچیں۔"
}

# Feature 3b: Roman Urdu Support (Expanded)
ROMAN_URDU_KNOWLEDGE = {
    "matlab": "Matlab (Meaning): Kisi bhi cheez ki wazahat. Aap kis term ka matlab jan'na chahte hain?",
    "kia hai": "Ye aik technical term hai. WAPDA MDC AI Assistant aapko iski detail bata sakta hai.",
    "kaise": "Iska tareeqa kaar asaan hai. Kya aap meter reading ya bill check karne ka tareeqa poochna chahte hain?",
    "shukriya": "Bohat bohat shukriya! Agar mazeed koi madad chahiye to batayein.",
    "theek": "Jee bilkul! Main aapki mazeed kya madad kar sakta hoon?",
    "help": "Main meter reading, billing, aur WAPDA rules main aapki help kar sakta hoon.",
    "kunda": "Kunda (Illegal hook) lagana qanoonan jurm hai. Is se bachein.",
    "bijli": "Electricity (Bijli) ko ehtiyat se istemal karein taake bill kam aaye.",
    "kharab": "Agar meter kharab hai to foran subdivision office ko report karein.",
    "billing": "Billing ki details ke liye apna reference number check karein.",
    "check": "Main aapki meter reading ya compliance check karne main madad kar sakta hoon.",
    "masla": "Kya masla hai? Kya aap meter reading ya bill ke baray main batana chahte hain?",
    "malomat": "Main aapko WAPDA aur MDC ke baray main mukammal malomat de sakta hoon.",
    "kia hal hai": "Alhamdulillah, main theek hoon! Aap batayein, WAPDA MDC main main aapki kia madad kar sakta hoon?",
    "kia ho rha ha": "Kuch nahi, bas aapki help karne ke liye tayyar hoon. Aap batayein kia sawal hai?",
    "sunao": "Sab theek hai! Aap koi WAPDA ya meter reading se mutaliq masla batayein to main hal kar sakta hoon.",
    "kaise ho": "Main bilkul theek! Aap batayein aapka kaam kaisa chal rha hai?",
    "hey": "Hey! How can I help you with your WAPDA meter tasks today?"
}

def find_relevant_answer(user_query):
    """Find relevant answer from knowledge base or provide intelligent responses"""
    user_query_lower = user_query.lower().strip()

    # 3. Add Urdu Language Support - Check Urdu keywords first
    for u_word, u_resp in URDU_KNOWLEDGE.items():
        if u_word in user_query:
            return u_resp
            
    # 3b. Roman Urdu Logic
    for r_word, r_resp in ROMAN_URDU_KNOWLEDGE.items():
        if r_word in user_query_lower:
            # If query contains a knowledge base word + "matlab"
            for k_word, k_resp in KNOWLEDGE_BASE.items():
                if k_word in user_query_lower:
                    return f"💡 **{k_word.upper()}:** {k_resp}"
            return r_resp

    # 1. Fuzzy match against the 160 predefined QA database
    if QA_QUESTIONS:
        matches = difflib.get_close_matches(user_query_lower, [q.lower() for q in QA_QUESTIONS], n=1, cutoff=0.6)
        if matches:
            original_q = next(q for q in QA_QUESTIONS if q.lower() == matches[0])
            return f"💡 **Answer to:** *{original_q}*\n\n{QA_DATABASE[original_q]}"

    # Direct check in the new 40+ Knowledge Base items
    for k_word, k_resp in KNOWLEDGE_BASE.items():
        if k_word in user_query_lower:
            return f"📖 **{k_word.upper()}:** {k_resp}"

    # Meter reader task keywords (Existing)
    meter_reading_terms = ['meter reading', 'read meter', 'meter reader', 'reading route', 'readings', 'meter reading process']
    data_record_terms = ['record', 'data record', 'log', 'save data', 'entry', 'data entry', 'record reading', 'store reading']
    meter_check_terms = ['meter check', 'check meter', 'meter inspection', 'meter condition', 'faulty meter', 'meter verification', 'meter test']
    illegal_connection_terms = ['illegal connection', 'kunda', 'theft', 'unauthorized connection', 'bypass', 'wire theft', 'illegal hook']
    consumer_complaint_terms = ['complaint', 'consumer complaint', 'billing complaint', 'service complaint', 'report issue', 'problem with consumer', 'customer complaint']
    real_life_terms = ['problem', 'issue', 'situation', 'scenario', 'challenge', 'real-life', 'real life']
    
    # Specific problem situations (Existing)
    locked_terms = ['locked', 'inaccessible', 'gate closed', 'no access', 'cannot enter', 'taala', 'band']
    dog_terms = ['dog', 'animal', 'kutta', 'bite', 'dangerous animal', 'pet']
    weather_terms = ['weather', 'rain', 'storm', 'baarish', 'flood', 'pani']
    faulty_meter_terms = ['broken', 'faulty', 'tampered', 'kharab', 'jal gaya', 'burnt meter', 'screen off', 'blank screen', 'meter jala']
    dispute_terms = ['angry', 'dispute', 'gussa', 'larai', 'fight', 'argue', 'badtameezi']

    # 2. Add More Keyword Coverage (New Topics)
    billing_terms = ['billing', 'bill check', 'duplicate bill', 'bill payment', 'online bill', 'payment methods', 'average bill']
    tariff_terms = ['tariff', 'rates', 'unit price', 'nepra', 'charges per unit']
    connection_terms = ['new connection', 'apply for connection', 'load enhancement', 'increase load', 'application process']
    safety_terms = ['safety', 'ppe', 'gloves', 'helmet', 'lineman safety', 'emergency']
    helpline_terms = ['helpline', 'contact', 'complaint number', '118', '8118', 'emergency number']

    # Handle greetings
    if any(word in user_query_lower for word in ['hello', 'hi', 'hey', 'assalam', 'salaam']):
        return "👋 Hello! I'm your WAPDA Meter Reader Assistant. I can help you with meter reading, data recording, meter checking, illegal connection reporting, and consumer complaint handling. What would you like to know?"

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

❓ **Ask me anything related to meter reading or consumer service!"""

    # Existing scenario handlers
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

    # Specific Problem Scenarios (Existing)
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

    # New Category Handlers (Feature 2)
    if any(term in user_query_lower for term in billing_terms):
        return "💳 **Billing & Payments:**\n\n- You can check your bill online at the PITC or your DISCO website.\n- Bills can be paid via Banks, Post Offices, Omni, EasyPaisa, or JazzCash.\n- If you haven't received a bill, visit the subdivision office for a duplicate copy."

    if any(term in user_query_lower for term in tariff_terms):
        return "📉 **Tariff Information:**\n\n- Electricity rates (Tariffs) are determined by NEPRA.\n- Rates vary based on consumption slabs (e.g., 1-100 units, 101-200 units).\n- Off-peak and Peak hours apply to industrial and specific residential connections."

    if any(term in user_query_lower for term in connection_terms):
        return "🔌 **New Connection & Load:**\n\n- Apply for a new connection via the ENC (Electricity New Connection) portal.\n- For load enhancement, submit a request to the XEN/SDO with required documents.\n- Ensure all wiring meets safety standards before inspection."

    if any(term in user_query_lower for term in helpline_terms):
        return "☎️ **Important Helplines:**\n\n- General Complaints: 118\n- SMS Complaints: 8118\n- Power Theft Reporting: 0800-84338\n- Local Sub-division numbers are printed on your monthly bill."

    if any(term in user_query_lower for term in real_life_terms):
        return "⚠️ **General Real-Life Meter Reader Situations:**\n\nMeter readers face many field challenges: Locked gates, aggressive dogs, bad weather, faulty meters, and angry consumers. Ask me about a specific situation like 'locked gate', 'dog', 'burnt meter', or 'angry customer' for specific guidance!"

    # Handle thank you
    if any(word in user_query_lower for word in ['thank', 'thanks', 'shukriya']):
        return "🙏 You're welcome! I'm glad I could help. Feel free to ask me anything else about meter reading or service support."

    # Handle goodbye
    if any(word in user_query_lower for word in ['bye', 'goodbye', 'see you', 'allah hafiz']):
        return "👋 Goodbye! Have a great day. Come back anytime if you need assistance with meter reading or report handling!"

    # Handle direct questions about meter reader work
    if '?' in user_query and any(word in user_query_lower for word in meter_reading_terms + data_record_terms + meter_check_terms + illegal_connection_terms + consumer_complaint_terms):
        return f"🤔 You've asked: '{user_query}'\n\nI can answer meter reader questions about reading, recording, checking meters, illegal connection reporting, and consumer complaint handling. Ask me for step-by-step guidance!"

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questions', methods=['GET'])
def get_questions_list():
    """Return the list of all available questions for auto-suggest"""
    return jsonify(QA_QUESTIONS)

# Feature 4: Add Chat History Endpoints
@app.route('/api/history', methods=['GET'])
def get_history():
    """Returns the current session chat history"""
    return jsonify(session.get('chat_history', []))

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clears the session chat history"""
    session['chat_history'] = []
    return jsonify({'status': 'success', 'message': 'History cleared'})

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message.strip():
        return jsonify({'response': 'Please type a message.'})
    
    # Feature 4: Initialize and Save User Message to Session
    if 'chat_history' not in session:
        session['chat_history'] = []
    session['chat_history'].append({'role': 'user', 'content': user_message})
    
    # Find relevant answer
    answer = find_relevant_answer(user_message)
    
    if answer:
        bot_response = answer
    else:
        bot_response = f"⚠️ You ask a irrelevent question. I am a specialist WAPDA MDC Assistant. Please ask about meter reading, billing, or WAPDA operations."
    
    # Feature 4: Save Bot Response to Session and Limit to 20 messages
    session['chat_history'].append({'role': 'bot', 'content': bot_response})
    session['chat_history'] = session['chat_history'][-20:] # Keep last 20 messages
    session.modified = True # Ensure session is saved
    
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
