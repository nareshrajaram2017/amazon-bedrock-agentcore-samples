# Import libraries
from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool

# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

# System prompt defining the agent's role and capabilities
SYSTEM_PROMPT = """You are a helpful and professional customer support assistant for TechCorp. 

Your role is to:
- Provide accurate information using the tools available to you
- Be friendly, patient, and understanding with customers
- Always offer additional help after answering questions
- If you can't help with something, direct customers to the appropriate contact

You have access to 4 main tools:
1. get_shipping_info() - Get shipping details for specific orders
2. get_return_policy() - Get return policy information by product category
3. get_product_info() - Get product specifications and details
4. get_order_status() - Check the current status of customer orders

Always use the appropriate tool to get accurate, up-to-date information rather than guessing."""

# Bedrock model configuration
MODEL = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.3,
    region_name="us-east-1",
)

# ============================================================================
# AGENT TOOLS
# ============================================================================


@tool
def get_shipping_info(order_id: str) -> str:
    """
    Get shipping information for a specific order.

    Args:
        order_id: The order ID to look up shipping information for

    Returns:
        Formatted string with shipping details including method, cost, and status
    """
    # Mock shipping database - in real implementation, this should query a real shipping system
    shipping_data = {
        "12345": {
            "method": "Standard Shipping",
            "estimated_delivery": "3-5 business days",
            "cost": "Free",
            "status": "Preparing for shipment",
        },
        "67890": {
            "method": "Express Shipping",
            "estimated_delivery": "1-2 business days",
            "cost": "$9.99",
            "tracking_number": "TRK123456789",
            "status": "In transit",
        },
        "11111": {
            "method": "Priority Shipping",
            "delivery_date": "Delivered on Jan 14, 2024",
            "cost": "$14.99",
            "status": "Delivered",
        },
    }

    shipping = shipping_data.get(order_id)
    if not shipping:
        return f"Order #{order_id} not found. Please verify the order number."

    # Format response based on shipping status
    if shipping["status"] == "Delivered":
        return f"Order #{order_id}: Delivered on {shipping['delivery_date']} via {shipping['method']} (${shipping['cost']})."
    elif "tracking_number" in shipping:
        return (
            f"Order #{order_id}: {shipping['method']} (${shipping['cost']})\n"
            f"Tracking: {shipping['tracking_number']}\n"
            f"Estimated delivery: {shipping['estimated_delivery']}\n"
            f"Status: {shipping['status']}"
        )
    else:
        return (
            f"Order #{order_id}: {shipping['method']} (${shipping['cost']})\n"
            f"Estimated delivery: {shipping['estimated_delivery']}\n"
            f"Status: {shipping['status']}"
        )


@tool
def get_return_policy(product_category: str) -> str:
    """
    Get return policy information for a specific product category.

    Args:
        product_category: The category of product (e.g., 'electronics', 'clothing', 'books')

    Returns:
        Formatted return policy details including timeframes and conditions
    """
    # Return policy database - in real implementation, this should be stored in a database
    policies = {
        "electronics": {
            "window": "30 days",
            "condition": "Items must be in original packaging with all accessories",
            "process": "Contact customer service to initiate return",
            "refund_time": "5-7 business days after we receive the item",
            "shipping": "Free return shipping on defective items",
        },
        "clothing": {
            "window": "60 days",
            "condition": "Items must be unworn, unwashed, and have tags attached",
            "process": "Use our online return portal or contact customer service",
            "refund_time": "3-5 business days after we receive the item",
            "shipping": "Customer pays return shipping unless item is defective",
        },
        "books": {
            "window": "14 days",
            "condition": "Books must be in original condition with no writing or damage",
            "process": "Contact customer service for return authorization",
            "refund_time": "3-5 business days after we receive the item",
            "shipping": "Customer pays return shipping",
        },
    }

    # Default policy for unlisted categories
    default_policy = {
        "window": "30 days",
        "condition": "Items must be in original condition and packaging",
        "process": "Contact customer service to initiate return",
        "refund_time": "5-7 business days after we receive the item",
        "shipping": "Return shipping policies vary by item",
    }

    policy = policies.get(product_category.lower(), default_policy)

    return (
        f"{product_category} Return Policy:\n\n"
        f"• Return Window: {policy['window']} from delivery\n"
        f"• Condition: {policy['condition']}\n"
        f"• Process: {policy['process']}\n"
        f"• Refund Time: {policy['refund_time']}\n"
        f"• Return Shipping: {policy['shipping']}"
    )


@tool
def get_product_info(product_type: str) -> str:
    """
    Get detailed information about a specific product type.

    Args:
        product_type: The type of product to get information about

    Returns:
        Formatted product information including warranty, features, and policies
    """
    # Product catalog - in production, this would query a product database
    catalog = {
        "laptops": {
            "warranty": "2-year comprehensive warranty",
            "models": "13-inch and 15-inch models available",
            "features": "High-performance processors, SSD storage, premium displays",
            "shipping": "Free shipping on all orders",
            "return_policy": "30-day return window",
        },
        "phones": {
            "warranty": "1-year manufacturer warranty",
            "models": "Multiple models with various storage options",
            "features": "Advanced cameras, 5G connectivity, long battery life",
            "shipping": "Free shipping on orders over $50",
            "return_policy": "14-day return window",
        },
        "tablets": {
            "warranty": "1-year warranty (extended coverage available)",
            "models": "10-inch and 12-inch sizes available",
            "features": "Touch screens, stylus support, lightweight design",
            "shipping": "Free shipping on all orders",
            "return_policy": "30-day return window",
        },
    }

    product = catalog.get(product_type.lower())
    if not product:
        return f"I don't have specific details for {product_type}. Please contact our product specialists for detailed information."

    return (
        f"{product_type.title()} Information:\n\n"
        f"• Warranty: {product['warranty']}\n"
        f"• Models: {product['models']}\n"
        f"• Key Features: {product['features']}\n"
        f"• Shipping: {product['shipping']}\n"
        f"• Returns: {product['return_policy']}"
    )


@tool
def get_order_status(order_id: str) -> str:
    """
    Get the current status of a customer order.

    Args:
        order_id: The order ID to check status for

    Returns:
        Formatted order status information with relevant details
    """
    # Order database - in real implementation, this would query a real order management system
    orders = {
        "12345": {
            "status": "processing",
            "date_ordered": "2024-01-15",
            "estimated_delivery": "2-3 business days",
        },
        "67890": {
            "status": "shipped",
            "date_shipped": "2024-01-16",
            "tracking_number": "TRK123456789",
            "estimated_delivery": "Tomorrow",
        },
        "11111": {
            "status": "delivered",
            "delivery_date": "2024-01-14",
            "delivered_to": "Front door",
        },
        "22222": {
            "status": "returned",
            "return_date": "2024-01-10",
            "refund_status": "Processed",
        },
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

    return f"Order #{order_id}: {status}"
