# Store Management System - Backend

This is a backend-focused **Store Management System** built using Python, Flask, and SQLite.

## Features
- Product CRUD: Create, Read, Update, Delete products
- Inventory Management: Track stock quantity automatically
- Sales Management: (optional extension)
- Modular Code Structure
- Error Handling and Input Validation

## Tech Stack
- Python 3
- Flask
- SQLite

## How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Access endpoints via Postman or browser

## Example API Endpoints

### Add Product
POST /add_product
Body (JSON): 
{
  "name": "Apple",
  "price": 100,
  "quantity": 10
}

## Validation & Error Handling

- The system ensures that:
  - Product names are not empty
  - Prices and quantities are positive numbers
  - Updating or deleting a product that doesn’t exist returns an error message
- Example error response when product ID not found:
{
  "error": "Product not found"
}
- Example error response when invalid input is given:
{
  "error": "Price must be a positive number"
}

### View Products
GET /view_products

### Update Product
PUT /update_product/<product_id>
Body (JSON):
{
  "name": "Apple",
  "price": 120,
  "quantity": 15
}

### Delete Product
DELETE /delete_product/<product_id>
 
## Author
Shivangi Biswas
