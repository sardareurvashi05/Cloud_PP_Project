# your_project/libs/product_calculator.py

def calculate_stock_value(product_price, quantity_in_stock):
    """Calculate the total stock value for a given product."""
    return product_price * quantity_in_stock


def calculate_discounted_price(product_price, discount_percentage):
    """Calculate the price of a product after applying a discount."""
    return product_price - (product_price * (discount_percentage / 100))


def check_reorder_status(quantity_in_stock, reorder_threshold):
    """Check if the product stock is below the reorder threshold."""
    return quantity_in_stock < reorder_threshold


def generate_inventory_report(products):
    """Generate an inventory report, including stock value, reorder status, and discounted prices."""
    report = []
    for product in products:
        stock_value = calculate_stock_value(product.price, product.quantity_in_stock)
        discounted_price = calculate_discounted_price(product.price, product.discount)
        reorder_status = check_reorder_status(product.quantity_in_stock, product.reorder_threshold)

        report.append({
            'product_name': product.name,
            'stock_value': stock_value,
            'discounted_price': discounted_price,
            'reorder_status': 'Reorder Needed' if reorder_status else 'Stock Sufficient'
        })
    
    return report
