# Import libraries
from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool

@tool
def get_shipping_info(order_id: str) -> str:
    """Get shipping information for a specific order."""
    # Mock shipping database - in real implementation, this would query a shipping system
    shipping_info = {
        "12345": {
            "method": "Standard Shipping",
            "estimated_delivery": "3-5 business days",
            "cost": "Free",
            "status": "Preparing for shipment"
        },
        "67890": {
            "method": "Express Shipping", 
            "estimated_delivery": "1-2 business days",
            "cost": "$9.99",
            "tracking_number": "TRK123456789",
            "status": "In transit"
        },
        "11111": {
            "method": "Priority Shipping",
            "delivery_date": "Delivered on Jan 14, 2024",
            "cost": "$14.99", 
            "status": "Delivered"
        }
    }
    
    shipping = shipping_info.get(order_id)
    if not shipping:
        return f"I couldn't find shipping information for order #{order_id}. This might be because the order hasn't shipped yet or the order number is incorrect."
    
    if shipping["status"] == "Delivered":
        return f"Order #{order_id} was delivered using {shipping['method']} (${shipping['cost']}). {shipping['delivery_date']}."
    elif "tracking_number" in shipping:
        return f"Order #{order_id} is being shipped via {shipping['method']} (${shipping['cost']}). " \
               f"Tracking number: {shipping['tracking_number']}. " \
               f"Expected delivery: {shipping['estimated_delivery']}. Status: {shipping['status']}."
    else:
        return f"Order #{order_id} will be shipped using {shipping['method']} (${shipping['cost']}). " \
               f"Estimated delivery: {shipping['estimated_delivery']}. Current status: {shipping['status']}."

print("✅ Shipping Information Tool created!")
print("🎉 All customer support tools are ready!")

@tool
def get_return_policy(product_category: str) -> str:
    """Get return policy information for a product category."""
    # Mock return policy database - in real implementation, this would query policy database
    return_policies = {
        "electronics": {
            "window": "30 days",
            "condition": "Items must be in original packaging with all accessories",
            "process": "Contact customer service to initiate return",
            "refund_time": "5-7 business days after we receive the item",
            "shipping": "Free return shipping on defective items"
        },
        "clothing": {
            "window": "60 days", 
            "condition": "Items must be unworn, unwashed, and have tags attached",
            "process": "Use our online return portal or contact customer service",
            "refund_time": "3-5 business days after we receive the item",
            "shipping": "Customer pays return shipping unless item is defective"
        },
        "books": {
            "window": "14 days",
            "condition": "Books must be in original condition with no writing or damage", 
            "process": "Contact customer service for return authorization",
            "refund_time": "3-5 business days after we receive the item",
            "shipping": "Customer pays return shipping"
        }
    }
    
    # Default policy for unlisted categories
    default_policy = {
        "window": "30 days",
        "condition": "Items must be in original condition and packaging",
        "process": "Contact customer service to initiate return", 
        "refund_time": "5-7 business days after we receive the item",
        "shipping": "Return shipping policies vary by item"
    }
    
    policy = return_policies.get(product_category.lower(), default_policy)
    
    return f"Return policy for {product_category}:\\n\\n" \
           f"• Return window: {policy['window']} from delivery date\\n" \
           f"• Condition requirements: {policy['condition']}\\n" \
           f"• Return process: {policy['process']}\\n" \
           f"• Refund timeline: {policy['refund_time']}\\n" \
           f"• Return shipping: {policy['shipping']}"

print("✅ Return Policy Tool created!")

@tool
def get_product_info(product_type: str) -> str:
    """Get information about a specific product type."""
    # Mock product catalog - in real implementation, this would query a product database
    products = {
        "laptops": {
            "warranty": "2-year comprehensive warranty",
            "models": "Available in 13-inch and 15-inch models",
            "features": "High-performance processors, SSD storage, premium displays",
            "shipping": "Free shipping on all orders",
            "return_policy": "30-day return policy"
        },
        "phones": {
            "warranty": "1-year manufacturer warranty", 
            "models": "Multiple models available with various storage options",
            "features": "Latest cameras, 5G connectivity, long battery life",
            "shipping": "Free shipping on orders over $50",
            "return_policy": "14-day return policy"
        },
        "tablets": {
            "warranty": "1-year warranty with optional extended coverage",
            "models": "Available in 10-inch and 12-inch sizes",
            "features": "Touch screens, stylus support, lightweight design", 
            "shipping": "Free shipping on all orders",
            "return_policy": "30-day return policy"
        }
    }
    
    product = products.get(product_type.lower())
    if not product:
        return f"I don't have specific information about {product_type}. Let me connect you with a specialist who can help with detailed product information."
    
    return f"Here's what I can tell you about our {product_type}:\\n\\n" \
           f"• Warranty: {product['warranty']}\\n" \
           f"• Models: {product['models']}\\n" \
           f"• Features: {product['features']}\\n" \
           f"• Shipping: {product['shipping']}\\n" \
           f"• Returns: {product['return_policy']}"

print("✅ Product Information Tool created!")

@tool
def get_order_status(order_id: str) -> str:
    """Get the status of a customer order."""
    # Mock order database - in real implementation, this would query a database
    orders = {
        "12345": {
            "status": "processing",
            "date_ordered": "2024-01-15",
            "estimated_delivery": "2-3 business days"
        },
        "67890": {
            "status": "shipped", 
            "date_shipped": "2024-01-16",
            "tracking_number": "TRK123456789",
            "estimated_delivery": "Tomorrow"
        },
        "11111": {
            "status": "delivered",
            "delivery_date": "2024-01-14",
            "delivered_to": "Front door"
        },
        "22222": {
            "status": "returned",
            "return_date": "2024-01-10",
            "refund_status": "Processed"
        }
    }
    
    order_info = orders.get(order_id)
    if not order_info:
        return f"I couldn't find order #{order_id} in our system. Please check the order number and try again."
    
    status = order_info["status"]
    if status == "processing":
        return f"Order #{order_id} is currently being processed. It was placed on {order_info['date_ordered']} and will ship within {order_info['estimated_delivery']}."
    elif status == "shipped":
        return f"Great news! Order #{order_id} was shipped on {order_info['date_shipped']}. Your tracking number is {order_info['tracking_number']} and it should arrive {order_info['estimated_delivery']}."
    elif status == "delivered":
        return f"Order #{order_id} was successfully delivered on {order_info['delivery_date']} to your {order_info['delivered_to']}."
    elif status == "returned":
        return f"Order #{order_id} was returned on {order_info['return_date']}. Your refund has been {order_info['refund_status'].lower()}."
    
    return f"Order #{order_id} status: {status}"

print("✅ Order Status Tool created!")
