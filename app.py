import streamlit as st
import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import openai
from typing import Dict, List, Optional
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Settings
class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-3.5-turbo"
    MAX_RETRIES = 3
    TIMEOUT = 30


settings = Settings()

# Review Extractor Class
class ReviewExtractor:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def get_selectors(self, html: str) -> Dict[str, str]:
        try:
            response = await openai.ChatCompletion.acreate(
                model=settings.MODEL_NAME,
                messages=[{
                    "role": "user",
                    "content": f"""
                    Analyze this HTML and return CSS selectors for review elements.
                    HTML: {html[:2000]}...

                    Return only a JSON object with these selectors:
                    - review_container: main container for each review
                    - title: review title
                    - body: review text
                    - rating: rating element
                    - reviewer: reviewer name
                    - next_page: next page button/link
                    """
                }],
                temperature=0
            )
            css_selectors = json.loads(response.choices[0].message.content)
            required_keys = {"review_container", "title", "body", "rating", "reviewer", "next_page"}
            if not required_keys.issubset(css_selectors.keys()):
                raise ValueError("Missing required CSS selectors.")
            return css_selectors
        except Exception as e:
            logger.error(f"Error getting selectors: {str(e)}")
            raise

    async def extract_review_data(self, element, selectors: Dict[str, str]) -> Dict:
        async def get_text(selector: str) -> str:
            try:
                el = await element.query_selector(selector)
                return (await el.text_content()).strip() if el else ""
            except:
                return ""

        async def get_rating(selector: str) -> float:
            try:
                el = await element.query_selector(selector)
                if not el:
                    return 0.0
                text = await el.text_content()
                numbers = re.findall(r"\d+\.?\d*", text)
                return float(numbers[0]) if numbers else 0.0
            except:
                return 0.0

        return {
            "title": await get_text(selectors["title"]),
            "body": await get_text(selectors["body"]),
            "rating": await get_rating(selectors["rating"]),
            "reviewer": await get_text(selectors["reviewer"]),
        }

    async def extract_reviews(self, url: str, progress_callback=None) -> List[Dict]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            reviews = []

            try:
                await page.goto(url, timeout=settings.TIMEOUT * 1000)
                await page.wait_for_load_state("networkidle")

                html = await page.content()
                selectors = await self.get_selectors(html)

                page_num = 1
                while True:
                    if progress_callback:
                        progress_callback(f"Processing page {page_num}")

                    review_elements = await page.query_selector_all(selectors["review_container"])
                    if not review_elements:
                        logger.warning("No review elements found.")
                        break

                    for element in review_elements:
                        review_data = await self.extract_review_data(element, selectors)
                        if review_data["body"]:
                            reviews.append(review_data)

                    next_button = await page.query_selector(selectors["next_page"])
                    if not next_button or not await next_button.is_visible():
                        break

                    try:
                        await next_button.click()
                        await page.wait_for_load_state("networkidle")
                        page_num += 1
                    except PlaywrightTimeoutError:
                        logger.error("Next page click timed out.")
                        break

                return reviews

            except PlaywrightTimeoutError as e:
                logger.error(f"TimeoutError during page load: {str(e)}")
                raise

            except Exception as e:
                logger.error(f"Error during review extraction: {str(e)}")
                raise

            finally:
                await browser.close()


# Streamlit UI
st.set_page_config(page_title="Review Scraper", layout="wide")

st.title("📊 Product Reviews Analyzer")

url = st.text_input("Enter product URL:", placeholder="https://example.com/product")


def update_progress(message):
    if "progress_bar" not in st.session_state:
        st.session_state.progress_bar = st.empty()
    st.session_state.progress_bar.text(message)


if "reviews_df" not in st.session_state:
    st.session_state.reviews_df = None

if url and st.button("Extract Reviews"):
    try:
        with st.spinner("Extracting reviews..."):
            extractor = ReviewExtractor()
            reviews = asyncio.run(extractor.extract_reviews(url, update_progress))

            if reviews:
                df = pd.DataFrame(reviews)
                st.session_state.reviews_df = df
                st.write(f"Extracted {len(df)} reviews.")
                st.dataframe(df)

            else:
                st.error("No reviews found on the page.")

    except Exception as e:
        st.error(f"Error extracting reviews: {str(e)}")
