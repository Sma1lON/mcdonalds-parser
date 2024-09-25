# McDonald's Parser

This repository contains a Python script for scraping the McDonald's menu from the official website. The script utilizes Playwright for web automation and BeautifulSoup for parsing HTML content. It collects detailed nutritional information for various products, including calories, fats, carbohydrates, and proteins, and stores the data in a JSON file for easy access and analysis.

## Flask API Endpoints

Additionally, the repository includes a Flask-based API with the following endpoints:

- **GET /all_products/**: Returns detailed information about all products on the menu.
- **GET /products/{product_name}**: Returns information about a specific product by name.
- **GET /products/{product_name}/{product_field}**: Returns information about a specific field (e.g., calories, fats) for one particular product.

## Setup and Usage

To run this project, you'll need to have Python installed along with the necessary libraries. You can install the required packages using pip:

```bash
pip install playwright beautifulsoup4 flask
```
After installing the dependencies, you can run the script to scrape the McDonald's menu:

```bash
python parsingMC.py
```
Then, start the Flask API server:
```bash
python endpointMC.py
```
You can access the API endpoints at http://127.0.0.1:5000/.
