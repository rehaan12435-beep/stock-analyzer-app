import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter
from textblob import TextBlob
import datetime

# ---- Streamlit UI ----
st.set_page_config(page_title="Short-Term Stock Analyzer", page_icon="📈")

st.title("📈 Short-Term Stock Analyzer (Auto)")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL")

# ---- Function to fetch stock data ----
def get_stock_data(ticker):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=30)
    data = yf.download(ticker, start=start, end=end, progress=False)
    return data

# ---- Function to scrape tweets ----
def get_tweets(query, limit=30):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{query} since:{(datetime.date.today()-datetime.timedelta(days=7))}').get_items()):
        if i > limit:
            break
        tweets.append(tweet.content)
    return tweets

# ---- Function to analyze sentiment ----
def analyze_sentiment(texts):
    if not texts:
        return 0
    polarity = [TextBlob(t).sentiment.polarity for t in texts]
    return np.mean(polarity)

# ---- Run analysis ----
if st.button("Analyze"):
    try:
        # Stock data
        df = get_stock_data(ticker)
        df['Returns'] = df['Close'].pct_change()
        last_week_change = (df['Close'][-1] - df['Close'][-5]) / df['Close'][-5] * 100
        volatility = df['Returns'].std() * 100

        # Tweets sentiment
        st.write("📡 Scraping Twitter data...")
        tweets = get_tweets(ticker, limit=50)
        sentiment_score = analyze_sentiment(tweets)

        # Combine into final score
        score = 50
        score += last_week_change / 2
        score += sentiment_score * 50
        score -= volatility / 4
        score = max(0, min(100, score))  # keep between 0–100

        # ---- Display results ----
        st.subheader(f"Results for {ticker}")
        st.write(f"📊 7-day Price Change: {last_week_change:.2f}%")
        st.write(f"📉 Volatility: {volatility:.2f}%")
        st.write(f"💬 Sentiment Score: {sentiment_score:.2f}")
        st.progress(int(score))
        st.success(f"Final Short-Term Opportunity Score: {score:.1f}%")

    except Exception as e:
        st.error(f"Error: {e}")
