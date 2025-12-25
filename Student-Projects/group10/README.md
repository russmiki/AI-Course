# Group 10
## YouTube Comments Sentiment Analyzer
# Group members:
1. Sogol Shariatzadeh Shirazi (leader)
2. Rahil Tondghadaman
3. Minoo Sadat Hoseini Hasan Abadi
4. Kiana Negahban
5. Nadia Khaghani Joo


## overview

This project provides a fully automated pipeline for collecting, filtering, and analyzing the sentiment of YouTube video comments. It uses the YouTube Data API to retrieve comments, filters out irrelevant entries based on predefined keywords, and applies a hybrid sentiment analysis system that combines:
  - Emoji-based sentiment detection
  - Gibberish detection (nonsense text identification)
  - NLP-based sentiment classification using a fine-tuned Transformer model
The goal is to produce highly accurate sentiment labels, even for comments containing emojis, short informal text, or noisy patterns.
The final output is exported as a .csv file for further data analysis, visualization, and machine learning tasks.



## Key Features
   1. Retrieve up to 500 YouTube Comments:
      - Uses pagination automatically with the YouTube Data API.
   2. Keyword-Based Comment Filtering:
      - Comments containing unwanted terms (e.g., “wallpaper”, “intro”, “which”, etc.) are excluded.
      - This helps remove repetitive questions, irrelevant chatbot-like comments, and off-topic messages.
   3. Emoji Sentiment Detection:
      - A dedicated emoji sentiment engine identifies clear emotional signals such as:
         Positive: 😂 🤣 😍 ❤️ 🔥 😁
         Negative: 😡 🤬 😢 😞 👎
      - If the emoji sentiment is strong enough, the system avoids unnecessary NLP processing.
   4. Gibberish Detection:
      - The system identifies meaningless or low-quality text such as:
         asdasdasd
         brbrbrbr
         ksjdfhksjh
         sdfkjh
         qwerty
      - Patterns used include:
         No vowels
         Repetitive patterns
         Low character diversity
         Consonant-only sequences
         Missing real English words
         Detected gibberish is automatically labeled NEUTRAL.
    5. NLP Sentiment Analysis
      - If no strong emoji-based sentiment is detected and the text is not gibberish, the pipeline uses:
         distilbert-base-uncased-finetuned-sst-2-english
      - to classify the comment as:
         POSITIVE
         NEGATIVE
    6. CSV Export
      - All results are saved to:
         youtube_comments_sentiment.csv
         containing each cleaned comment and its associated sentiment.



## Dependencies
- Required Python Version: Python 3.8+



## Required Libraries:
- google-api-python-client
- pandas
- transformers
- emoji
- torch
- re



## Install all dependencies using:

- pip install google-api-python-client pandas transformers emoji torch


## Setup Instructions:
1. Obtain a YouTube Data API Key

Create an API key from
Google Cloud Console → APIs & Services → Credentials

2. Insert Your API Key

Replace your API key inside the script:
API_Key = "YOUR_API_KEY_HERE"

3. Set the Target YouTube Video

Modify the following line:
video_id = "YOUR_VIDEO_ID"

4. Run the Script
python main.py


# The script fetches comments, filters them, performs sentiment analysis, and saves the output CSV file.


# System Architecture

                ┌───────────────────────────┐
                │  YouTube Data API (v3)    │
                └───────────────┬───────────┘
                                │
                                ▼
                   ┌──────────────────────┐
                   │  Comment Collector   │
                   └────────────┬─────────┘
                                │
                                ▼
                   ┌──────────────────────┐
                   │  Keyword Filter      │
                   └────────────┬─────────┘
                                │
                                ▼
       ┌───────────────────────────────────────────────────┐
       │               Hybrid Sentiment Engine             │
       │                                                   │
       │  ┌──────────────┐  ┌────────────────┐  ┌────────┐│
       │  │ Emoji Module  │→│ Gibberish Check │→│ NLP ML  ││
       │  └──────────────┘  └────────────────┘  └────────┘│
       └───────────────────────────────────────────────────┘
                                │
                                ▼
                   ┌──────────────────────┐
                   │     CSV Export       │
                   └──────────────────────┘




## Output Format
 - The generated CSV contains two columns:
     Column	    Description
     comment    Cleaned filtered YouTube comment
     sentiment	POSITIVE / NEGATIVE
  - Example output row:
     "Great video man!", POSITIVE



## Algorithm Architecture:
1. Comment Extraction
  - Uses pagination with nextPageToken
  - Retrieves plaintext comments only
  - Collects up to 500 comments
2. Keyword Filtering
  - Removes comments containing any of the predefined keywords.
  - This helps reduce noise.
3. Emoji-First Sentiment Detection
  - If a comment contains strong positive or negative emoji presence, the model decides based on emojis alone.
4. Gibberish Detection
  - The cleaner removes comments with extremely low linguistic validity.
5. Transformer-Based Sentiment Analysis
  - Only properly structured text is sent to the NLP model.
6. CSV Export
  - Data is saved in UTF-8 format for maximum compatibility.



## Project Goals
 1. Improve the accuracy of sentiment analysis for social media content
 2. Handle informal text, emojis, slang, and noisy characters
 3. Provide a clean dataset suitable for further research or ML modeling
 4. Offer a customizable script for YouTube comment analysis



## Customization
  - You can easily modify:
     Keyword Filters
  - Add or remove keywords in the keywords list.
     Emoji Sentiment Lists
  - Extend positive_emojis or negative_emojis depending on your use-case.
  - NLP Model
  - Replace the model with any Hugging Face sentiment model:
     pipeline("sentiment-analysis", model="your-model")



## Future Improvements:
- If desired, the system can be expanded to include:
- Graphical sentiment analysis (matplotlib visualizations)
- YouTube replies analysis (nested comments)
- Real-time monitoring of new comments
- Language detection + multilingual sentiment models
- GUI or web dashboard version
- Database integration (MongoDB / SQLite)


## Frequently Asked Questions

### What does this project do?
This project collects comments from a YouTube video, filters out irrelevant or noisy entries, and analyzes the sentiment of the remaining comments using a hybrid AI approach.  
The final output is a clean CSV file containing comments labeled as **POSITIVE** or **NEGATIVE**.

### What design principles does it follow?
The project is built with the following considerations:
- Handling real-world noisy social media text  
- Prioritizing emojis when sentiment is obvious  
- Detecting and neutralizing gibberish or meaningless input  
- Limiting text length for stable NLP inference  
- Keeping the pipeline modular and easy to extend  

### What are the requirements?
- Python **3.8 or higher**  
- A valid **YouTube Data API v3 key**  
- Internet access for API calls and model downloads  

### Which API does it use?
The project uses the **YouTube Data API v3** to retrieve video comments via Google’s official API.

### Why are these libraries used?
- **google-api-python-client**: YouTube Data API communication  
- **transformers**: Transformer-based sentiment analysis  
- **torch**: Deep learning backend  
- **pandas**: Data processing and CSV export  
- **emoji**: Emoji detection and normalization  
- **re**: Text cleaning and gibberish detection

## Additional Information

### Limitations & Known Issues
- The sentiment model is optimized for English comments only.
- Emoji-based sentiment is rule-based and may not capture sarcasm or complex context.
- Neutral sentiment is intentionally minimized to focus on clear positive/negative polarity.
- YouTube API quota limits may restrict large-scale data collection.

### Ethical Considerations
- Only publicly available YouTube comments are analyzed.
- No personal user data is stored or redistributed.
- Predictions may contain model bias; they should not be used for moderation or decision-making without human review.

### Reproducibility
- Use the same model versions listed in `requirements.txt`.
- Run the notebook or script with the same video ID.
- Ensure stable internet connection for API calls and model downloads.

### Project Scope
**In Scope:**
- English-language YouTube comments
- Top-level comments only
- Binary sentiment classification (POSITIVE / NEGATIVE)

**Out of Scope:**
- Sarcasm or nuanced sentiment detection
- Multilingual support
- Automated comment moderation or spam removal

### Changelog
**v1.0.0**
- Initial release with hybrid sentiment analysis system
- CSV export support
- Jupyter Notebook demo included




