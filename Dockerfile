FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

# Hugging Face Spaces requires running on port 7860
ENV PORT=7860
EXPOSE 7860

# Command to run the application using Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
