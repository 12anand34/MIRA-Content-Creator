# MIRA Content Generation Platform

A web application that analyzes trending topics from reddit and generates multi-format content using AI. The platform leverages MIRA's AI capabilities to create blogs, reel scripts, and tweets from trending discussions.

## Features

- **Trend Analysis**: Fetches and analyzes trending topics from Reddit
- **Sentiment Analysis**: Evaluates the sentiment of trending content
- **Multi-format Content Generation**:
  - Blog posts
  - Reel scripts
  - Tweet content
- **Real-time Processing**: Asynchronous content generation with loading states
- **Error Handling**: Comprehensive error management with retry capabilities

## Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python, Flask
- **AI/ML**: 
  - MIRA SDK
  - Hugging Face Transformers
  - Sentiment Analysis Models[Distilbert]
  - Summarization Models[BART]
- **APIs**:
  - Reddit API
  - MIRA API

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd MIRA.app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
MIRA_API_KEY=your_api_key
```

4. Run the application:
```bash
python app.py
```

## Project Structure 