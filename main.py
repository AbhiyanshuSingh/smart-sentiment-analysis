from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob

# Create a FastAPI app instance
app = FastAPI(
    title="Project Sentinel: Sentiment Analysis API",
    description="A simple API to analyze the sentiment of a given text.",
    version="0.1.0",
)

# Pydantic model to define the structure of the request body
class SentimentRequest(BaseModel):
    text: str

# Pydantic model to define the structure of the response
class SentimentResponse(BaseModel):
    text: str
    polarity: float
    subjectivity: float
    sentiment: str

def get_sentiment(polarity: float) -> str:
    """
    Categorizes the polarity score into 'Positive', 'Negative', or 'Neutral'.
    """
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

@app.get("/")
def read_root():
    """
    Root endpoint to welcome users to the API.
    """
    return {"message": "Welcome to the Sentiment Analysis API. Send a POST request to /analyze with your text."}

@app.post("/analyze", response_model=SentimentResponse)
def analyze_sentiment(request: SentimentRequest):
    """
    Analyzes the sentiment of the text provided in the request.
    - Polarity: A float between -1.0 (negative) and 1.0 (positive).
    - Subjectivity: A float between 0.0 (objective) and 1.0 (subjective).
    """
    # Create a TextBlob object
    blob = TextBlob(request.text)
    
    # Get the polarity and subjectivity
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine the sentiment category
    sentiment = get_sentiment(polarity)
    
    # Return the response
    return SentimentResponse(
        text=request.text,
        polarity=polarity,
        subjectivity=subjectivity,
        sentiment=sentiment
    )
