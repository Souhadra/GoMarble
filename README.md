# GoMarble
# Review Scraper and Analyzer

This project is a web application built with Streamlit for scraping and analyzing product reviews from e-commerce websites. The application dynamically extracts reviews using Playwright and utilizes OpenAI's GPT model to identify CSS selectors for review elements. Users can analyze the extracted reviews through visualizations and download the data as a CSV file.

---

## Features

- **Dynamic Review Extraction**: Extract reviews from product pages with support for dynamic content loading.
- **OpenAI Integration**: Use GPT models to identify CSS selectors for review containers.
- **Data Analysis**: Visualize review ratings, identify common words, and generate insights.
- **Downloadable Reports**: Export extracted reviews as a CSV file.
- **User-Friendly Interface**: Simple and intuitive Streamlit-based UI.

---

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/review-scraper.git
    cd review-scraper
    ```

2. **Set Up Environment**:
    - Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    - Create a `.env` file in the project root with the following content:
        ```plaintext
        OPENAI_API_KEY=your_openai_api_key
        ```

3. **Install Playwright**:
    ```bash
    playwright install
    ```

4. **Run the Application**:
    ```bash
    streamlit run app.py
    ```

---

## Usage

1. **Enter Product URL**:
    - Paste the URL of the product page in the input field.
2. **Extract Reviews**:
    - Click the "Extract Reviews" button.
    - The app dynamically loads and extracts reviews.
3. **Analyze Reviews**:
    - View key metrics like average rating and rating distribution.
    - Explore a table of reviews and download the data as a CSV.
4. **Perform Text Analysis**:
    - Check the most common words in review texts.

---

## Requirements

- Python 3.8+
- Dependencies (from `requirements.txt`):
    - `streamlit`
    - `playwright`
    - `openai`
    - `pandas`
    - `plotly`
    - `python-dotenv`

---

## File Structure

- **`app.py`**: Main application file for Streamlit UI and logic.
- **`extractor.py`**: Contains the `ReviewExtractor` class for scraping reviews.
- **`.env`**: Environment variables (e.g., OpenAI API key).
- **`requirements.txt`**: Python dependencies.

---

## Troubleshooting

- **OpenAI API Key Not Found**:
    - Ensure your `.env` file is correctly configured with `OPENAI_API_KEY`.

- **Unable to Extract Reviews**:
    - Verify that the provided URL points to a product page.
    - Ensure the website loads content dynamically (e.g., scroll or pagination).

- **Playwright Errors**:
    - Ensure Playwright is installed and properly configured.
    - Run `playwright install` if not already done.

---

## Future Enhancements

- Support for additional e-commerce platforms.
- Advanced NLP-based sentiment analysis.
- Caching for faster repeated extractions.
- Browser-based selector testing and validation.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request.

---

## Contact

For questions or feedback, please contact [souhadracool@gmail.com](mailto:souhadracool@gmail.com).

