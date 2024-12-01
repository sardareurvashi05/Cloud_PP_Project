import json
import os

# Function to load the configuration file
def load_config():
    """Load configuration from a JSON file."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/config.json'))
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from the configuration file at {config_path}")

# Load configuration at the module level
config = load_config()

def calculate_stock_value(product_price, quantity_in_stock):
    """Calculate the total stock value for a given product."""
    return product_price * quantity_in_stock

def calculate_discounted_price(product_price, discount_percentage):
    """Calculate the price of a product after applying a discount."""
    return product_price - (product_price * (discount_percentage / 100))

def check_reorder_status(quantity_in_stock, reorder_threshold):
    """Check if the product stock is below the reorder threshold."""
    return quantity_in_stock < reorder_threshold

def generate_inventory_report(products, include_discounted_price=True):
    """Generate an inventory report with configurable reorder messages."""
    report = []
    for product in products:
        stock_value = product.calculate_stock_value()
        discounted_price = product.calculate_discounted_price() if include_discounted_price else None
        reorder_status = config['reorder_needed'] if product.check_reorder_status() else config['stock_sufficient']

        report.append({
            'product_name': product.name,
            'stock_value': stock_value,
            'discounted_price': discounted_price,
            'reorder_status': reorder_status
        })
    
    return report
