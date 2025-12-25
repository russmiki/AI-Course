     ######################################################################################################################
     #                            YouTube comment sentiment analysis about iphone 16 using API                            #
     #                        lecture : Artificial intelligence / lecturer: Dr.Maryam hajiesameili                        #
     #  Group members: Sogol Shariatzadehshirazi / Nadia Khaghanijo / Kiana Negahban / Rahil Tondghadaman / Minoo Hoseini #
     ######################################################################################################################

from googleapiclient.discovery import build
import pandas as pd
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import emoji
import re

# API Key for accessing YouTube data API
API_Key = "your-API-key"

# Create Youtube API client
youtube = build("youtube","v3",developerKey=API_Key)

# List of the keywords we want to filter
keywords = ["which","wallpaper","wallpapers","confused",
            "dubbing","intro", "intros", "lottery", "marques",
              "viewers","content", "shirt", "MKBHD", "mustache",
                "he", "guy","or","choice","watching"]

# Function: fetch comments from YouTube
def getComments(video_id,max_comments = 500):
    comments = []
    next_page = None

    while(len(comments) < max_comments):
        request = youtube.commentThreads().list(
            part = 'snippet',
            videoId=video_id,
            maxResults =100,
            pageToken = next_page,
            textFormat = "plainText"
        )
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        next_page = response.get("nextPageToken")
        if not next_page:
            break
    return comments

# Function: filter comments using keywords
def filterComments(comments,keywords):
    filteredComments = [c for c in comments if not any(k.lower() in c.lower() for k in keywords)]
    return filteredComments


# Emoji Sentiment System
positive_emojis = set(["😂", "🤣", "😍", "❤️", "🔥", "😁", "😊", "😃", "👍", "🙂"])     # positive emoji set
negative_emojis = set(["😡", "🤬", "😢", "😭", "👎", "😠", "🙁", "😞"])                 # negative empji set
def emoji_sentiment_score(text): 
    pos = sum(ch in positive_emojis for ch in text)
    neg = sum(ch in negative_emojis for ch in text)

    if pos == 0 and neg == 0:
        return None                                                                        # no emoji sentiment

    if pos > neg:
        return "POSITIVE"
    elif neg > pos:
        return "NEGATIVE"
    else:
        return None
    

# detect gibberish ( meaningless text) 
def is_gibberish(text):
    # remove all non-letters (emojis, spaces, punctuation)
    cleaned = re.sub(r'[^a-zA-Z]', '', text)

    cleaned = cleaned.lower()

    # too short -> not gibberish
    if len(cleaned) < 5:
        return False

    # no vowels at all (very strong gibberish signal)
    if not re.search(r'[aeiou]', cleaned):
        return True

    # repeating pattern like brbrbr / asdasd / kjkjkj
    # find half-length repeating
    half = len(cleaned) // 2
    if cleaned[:half] == cleaned[half:]:
        return True

    # extremely low character variety (aaaabaaa, bbbbbbb)
    if len(set(cleaned)) <= 2:
        return True

    # no English word in it
    if not re.search(r'(the|and|good|bad|wow|love|like|hate|you|this)', cleaned):
        # if it's just random consonant clusters
        if re.match(r'^[bcdfghjklmnpqrstvwxyz]+$', cleaned):
            return True

    return False

# Load Better Sentiment Model using NLP

model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
# Standard sentiment pipline
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


# Hybrid Sentiment Analyzer
def analyze_comment(text):
    # Check emoji-only or strong emoji sentiment
    emoji_label = emoji_sentiment_score(text)
    if emoji_label:
        return emoji_label

    # Clean + demojize for improved NLP
    cleaned = emoji.demojize(text, delimiters=(" ", " "))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Run NLP model
    result = sentiment_model(cleaned[:256])[0]
    label = result['label']

    # Convert roberta labels to POS/NEG
    if label.lower() in ["positive"]:
        return "POSITIVE"
    elif label.lower() in ["negative"]:
        return "NEGATIVE"
    

    # detect nonsense text first
    if is_gibberish(text):
        return "NEUTRAL"

# analyze list of comments
def analyze_comments(comments):
    return [analyze_comment(c) for c in comments]

def analyze_comments(comments):
    """Analyze sentiment of a list of comments."""
    results = []
    for c in comments:
        res = sentiment_model(c[:512])[0]  # limit text length to avoid model issues
        results.append(res["label"])
    return results

# --- Example usage ---
video_id = "rng_yUSwrgU"

# Fetch comments
all_comments = getComments(video_id)

# Filter comments using keywords
filtered_comments = filterComments(all_comments, keywords)

# Analyze sentiment only on filtered comments
sentiments = analyze_comments(filtered_comments)

# Save results
df = pd.DataFrame({
    "comment": filtered_comments,
    "sentiment": sentiments
})
df.to_csv("youtube_comments_sentiment.csv", index=False)
print(df.head(100))

# Display all 100 comments 
pd.set_option('display.max_rows', 100)