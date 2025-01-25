
# Mira Content Generator

## Project Overview

The Mira Content Generator is an AI-driven project designed to identify trending topics on Reddit, analyze their sentiment, and generate content for blogs, tweets, and reels scripts. The system integrates data scraping, machine learning, and natural language generation to provide a seamless workflow for generating high-quality, targeted content.

---

## Workflow Description

### 1. Data Scraping and Trend Analysis
- **Frontend Development**: A user-friendly frontend was created to display trending topics and popular news from Reddit.
- **Reddit API Integration**: The Reddit API was used to scrape and fetch data about the most popular and trendy topics currently being discussed on the platform.

### 2. Data Processing and Analysis
For each selected news or trending topic:
1. **Sentiment Analysis**:
   - A machine learning model analyzes the sentiment of the topic and assigns:
     - **Sentiment Label** (e.g., Positive, Negative, Neutral).
     - **Sentiment Score** (a numerical representation of sentiment intensity).
2. **Summarization**:
   - The topic is summarized into a concise, meaningful overview using ML models.

### 3. Mira Flow ‘a0’: Sentiment Analysis and Summarization
- **Purpose**: This flow performs sentiment analysis and generates a summary for the selected topic.
- **Technology**: Powered by GPT-4o using Mira SDK, the ‘a0’ flow ensures high accuracy and efficiency in content processing.
- **Output**:
  - Sentiment Label
  - Sentiment Score
  - Summary of the topic

### 4. Content Generation Flows
The processed data (sentiment label, sentiment score, and summary) from the ‘a0’ flow is transmitted to three distinct content generation flows:

#### 4.1 Blog Generator
- **Flow Name**: `blog-generator`
- **Input**: The summary and sentiment analysis data from ‘a0’ flow.
- **Output**: Engaging and insightful blogs relevant to the topic.
- **Technology**: Powered by GPT-4o using Mira SDK.

#### 4.2 Tweet Generator
- **Flow Name**: `tweet-generator`
- **Input**: The summary and sentiment analysis data from ‘a0’ flow.
- **Output**: Short, impactful, and shareable tweets.
- **Technology**: Powered by GPT-4o using Mira SDK.

#### 4.3 Reel Script Generator
- **Flow Name**: `reel-script-generator`
- **Input**: The summary and sentiment analysis data from ‘a0’ flow.
- **Output**: Creative and engaging scripts for reels.
- **Technology**: Powered by GPT-4o using Mira SDK.

---

## Project Architecture
1. **Frontend**: Displays trending topics and interacts with the backend.
2. **Backend**:
   - Integrates Reddit API for data scraping.
   - Runs ML models for sentiment analysis and summarization.
   - Uses Mira SDK for generating content via flows.
3. **Mira SDK Flows**:
   - `a0`: Sentiment Analysis and Summarization.
   - `blog-generator`: Blog content generation.
   - `tweet-generator`: Tweet content generation.
   - `reel-script-generator`: Reel script generation.

---

## Key Technologies Used
- **Reddit API**: Data collection and trend identification.
- **Machine Learning Models**: Sentiment analysis and summarization.
- **Mira SDK**: Workflow automation and content generation powered by GPT-4o.
- **GPT-4o**: Advanced natural language generation.

---

## How to Use
1. Clone this repository.
2. Set up the environment by installing the required dependencies listed in `requirements.txt`.
3. Configure your Reddit API credentials in the `config.py` file.
4. Run the application to:
   - View and select trending topics.
   - Analyze sentiments and summaries using the ‘a0’ flow.
   - Generate blogs, tweets, and reel scripts using the content generation flows.

---

## Future Enhancements
- Integrating more social media platforms for data scraping.
- Enhancing the accuracy of sentiment analysis with advanced models.
- Providing customization options for generated content.


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
git clone https://github.com/12anand34/MIRA-Content-Creator.git
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


---

## Contributors
Anand Bansal, Arnav Saini


