from flask import Flask, jsonify, Response
import json

app = Flask(__name__)

def load_products():
    with open('mcdonalds_products_full.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_products(products):
    with open('mcdonalds_products_full.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

@app.route('/all_products/', methods=['GET'])
def get_all_products():
    products = load_products()
    return Response(json.dumps(products, ensure_ascii=False), mimetype='application/json'), 200

@app.route('/products/<product_name>/', methods=['GET'])
def get_product(product_name):
    products = load_products()
    product = next((p for p in products if p['name'].lower() == product_name.lower()), None)
    if product:
        return Response(json.dumps(product, ensure_ascii=False), mimetype='application/json'), 200
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products/<product_name>/<product_field>/', methods=['GET'])
def get_product_field(product_name, product_field):
    products = load_products()
    product = next((p for p in products if p['name'].lower() == product_name.lower()), None)
    if product:
        field_value = product.get(product_field)
        if field_value is not None:
            return jsonify({product_field: field_value}), 200
        else:
            return jsonify({"error": "Field not found"}), 404
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
