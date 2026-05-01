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
    
    # Handle greetings
    if any(word in user_query_lower for word in ['hello', 'hi', 'hey', 'assalam', 'salaam']):
        return "👋 Hello! I'm your AI assistant. I can help you with voice input, file uploads, and answering questions. What would you like to know?"
    
    # Handle voice-related queries
    if any(word in user_query_lower for word in ['voice', 'speak', 'speech', 'audio', 'sound']):
        return "🔊 I support voice input and output! Click the microphone button to speak your questions, and enable voice responses to hear my answers. Try asking me something!"
    
    # Handle file upload queries
    if any(word in user_query_lower for word in ['upload', 'file', 'image', 'pdf', 'document']):
        return "📁 I can help you upload images and PDF files. Click the upload button to select and send files. I can process both images and documents!"
    
    # Handle feature questions
    if any(word in user_query_lower for word in ['feature', 'what can you do', 'capabilities', 'help']):
        return """🤖 Here's what I can do:

🔊 **Voice Features:**
• Speak your questions using the microphone
• Listen to my responses with voice output
• Toggle voice on/off anytime

📁 **File Upload:**
• Upload images (PNG, JPG, JPEG, GIF, BMP)
• Upload PDF documents
• Automatic file processing

💬 **Chat Features:**
• Answer questions intelligently
• Support for multiple languages
• Real-time conversation

❓ **Ask me anything!** I'm here to help with information, assistance, or just chat!"""

    # Handle thank you
    if any(word in user_query_lower for word in ['thank', 'thanks', 'shukriya']):
        return "🙏 You're welcome! I'm glad I could help. Feel free to ask me anything else!"
    
    # Handle goodbye
    if any(word in user_query_lower for word in ['bye', 'goodbye', 'see you', 'allah hafiz']):
        return "👋 Goodbye! Have a great day. Come back anytime if you need assistance!"
    
    # Handle general questions
    if '?' in user_query or any(word in user_query_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which']):
        return f"🤔 That's an interesting question: '{user_query}'\n\nI'm an AI assistant with voice and file upload capabilities. While I don't have specific knowledge about that topic yet, I can help you find information or assist with uploading files. What else would you like to know?"
    
    # Default response for other inputs
    return f"💬 I received your message: '{user_query}'\n\nI'm here to help! You can:\n• Ask me questions\n• Use voice input/output\n• Upload images or PDF files\n• Chat about various topics\n\nWhat would you like to do next?"

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

