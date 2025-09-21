import streamlit as st
import yfinance as yf
from textblob import TextBlob
import pandas as pd

st.title("Short-Term Stock Analyzer 📈")

# Step 1: User inputs
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):")
social_sentiment = st.text_area("Paste Recent Social Media Sentiment Text:")

# Step 2: Fetch stock data
if ticker:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")  # last 1 month
    st.subheader(f"Price Data for {ticker}")
    st.line_chart(hist['Close'])

# Step 3: Analyze social sentiment
if social_sentiment:
    blob = TextBlob(social_sentiment)
    sentiment_score = blob.sentiment.polarity  # -1 to 1
    st.subheader("Social Media Sentiment Score")
    st.write(f"{sentiment_score:.2f}")

# Step 4: Simple short-term signal
if ticker and social_sentiment:
    recent_trend = (hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0]  # % change
    score = 0.5 * recent_trend + 0.5 * sentiment_score  # weighted average
    st.subheader("Short-Term Investment Score")
    st.write(f"{score*100:.1f}% chance this stock is good for short-term investment")