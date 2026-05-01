# WAPDA MDC Chatbot - Meter Reading Assistant

A web-based chatbot specialized in WAPDA meter reading and Meter Data Controller (MDC) operations. Built as a semester final project.

## Features

✨ **Specialized Knowledge**: Focuses on WAPDA meter reading, billing processes, MDC responsibilities, and related topics.

💬 **Smart Responses**: Redirects off-topic questions back to relevant WAPDA/MDC topics.

🎨 **Modern UI**: Beautiful, responsive web interface with smooth animations.

🖼️ **Image Upload**: Upload WAPDA equipment or meter photos directly for contextual support.

⚡ **Real-time Chat**: Fast message processing with typing indicators.

## Project Structure

```
chatbot/
├── app.py                 # Flask backend with chatbot logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Chat interface (HTML/CSS/JS)
├── static/               # Static files (CSS, JS if needed)
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Locally

```bash
python app.py
```

The chatbot will be available at: **http://localhost:5000**

## Usage

1. Open the chatbot in your browser
2. Type any question about:
   - Meter reading processes
   - WAPDA operations
   - MDC (Meter Data Controller) responsibilities
   - Billing procedures
   - Meter types and consumer categories
3. The chatbot will provide relevant answers
4. Off-topic questions will be redirected to WAPDA/MDC topics

## Knowledge Base Topics

The chatbot currently covers:
- **Meter Reading**: Recording consumption data
- **MDC**: Meter Data Controller roles and responsibilities
- **WAPDA**: Water and Power Development Authority
- **Billing**: Bill generation and calculation processes
- **Meter Types**: Single phase, three phase, smart meters
- **Consumer Categories**: Residential, commercial, industrial, agricultural
- **Anomalies**: Identifying unusual meter readings
- **Disputes**: Handling billing complaints and meter disputes

## Deployment on Vercel

### Step 1: Prepare for Deployment

Create a `vercel.json` file in the root directory:

```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Step 2: Prepare for Production

Update `app.py` to handle Vercel environment:

Replace the last line with:
```python
if __name__ == '__main__':
    app.run(debug=False)
```

### Step 3: Push to GitHub

1. Create a GitHub repository
2. Push your code:
```bash
git init
git add .
git commit -m "Initial WAPDA MDC Chatbot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 4: Deploy on Vercel

1. Go to https://vercel.com
2. Sign up/Login
3. Click "New Project"
4. Select your GitHub repository
5. Deploy (Vercel auto-detects Flask)

Your chatbot will be live!

## How to Extend

### Add More Topics to Knowledge Base

Edit `app.py` in the `KNOWLEDGE_BASE` dictionary:

```python
"new_topic": {
    "questions": ["question keyword 1", "question keyword 2"],
    "answer": "Your answer here"
}
```

### Integrate with OpenAI/ChatGPT (Advanced)

For more advanced responses, you can integrate OpenAI API:

1. Install: `pip install openai`
2. Add your API key to environment
3. Modify the `find_relevant_answer()` function to use OpenAI

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel
- **Styling**: Custom CSS with gradients and animations

## Troubleshooting

**Problem**: Port 5000 already in use
**Solution**: 
```bash
python app.py --port 5001
```

**Problem**: ModuleNotFoundError
**Solution**: Make sure you've installed requirements
```bash
pip install -r requirements.txt
```

## Future Enhancements

- [ ] Integration with OpenAI API for more intelligent responses
- [ ] Multi-language support (Urdu)
- [ ] User authentication and history
- [ ] Analytics dashboard
- [ ] Mobile app version
- [ ] Voice input/output
- [ ] Image upload for meter reading verification

## Author

Developed as a semester final project for understanding WAPDA meter reading operations and MDC responsibilities.

## License

This project is for educational purposes.

---

**Questions?** Feel free to modify the knowledge base and add more topics as needed!
