from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import traceback

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(tempfile.gettempdir(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print('UPLOAD_FOLDER set to', app.config['UPLOAD_FOLDER'])

# Knowledge base for chatbot
KNOWLEDGE_BASE = {
    # Existing features removed as requested
}

def find_relevant_answer(user_query):
    """Find relevant answer from knowledge base"""
    # Knowledge base has been cleared as requested
    return "I'm a chatbot with no existing features loaded. Please suggest new features to implement!"

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image file found in request.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Unsupported image type.'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    image_url = f'/uploads/{filename}'
    return jsonify({'success': True, 'message': 'Image uploaded successfully.', 'filename': filename, 'url': image_url})

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

