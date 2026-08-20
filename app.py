import os
import json
from flask import Flask, render_template, request, jsonify, session
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ==========================================
# 1. Custom Tools / Functions
# ==========================================

def get_art_info(art_style: str, artist_name: str = None) -> dict:
    """Retrieves curated art suggestions, techniques, and color palettes.

    Args:
        art_style: The art movement or style (e.g., 'Impressionism', 'Cyberpunk', 'Surrealism', 'Minimalism').
        artist_name: Optional name of an artist for style inspiration (e.g., 'Van Gogh', 'Monet', 'Dali').

    Returns:
        A dictionary containing artwork recommendations, technique breakdown, and suggested palettes.
    """
    database = {
        "impressionism": {
            "style_name": "Impressionism",
            "technique": "Visible brush strokes, emphasis on accurate depiction of natural light and ordinary subject matter.",
            "palette": ["#007BA7", "#FCE205", "#E32636", "#40826D"],
            "palette_names": ["Cerulean Blue", "Cadmium Yellow", "Rose Madder", "Viridian Green"],
            "suggested_ideas": [
                "Sunlit water lilies pond with shimmering reflections",
                "Bustling street cafe in the rain with glowing yellow lanterns"
            ]
        },
        "cyberpunk": {
            "style_name": "Cyberpunk",
            "technique": "High-contrast neon lighting, rainy dark metallic surfaces, futuristic holograms, and dystopian atmosphere.",
            "palette": ["#FF007F", "#00F0FF", "#120024", "#7928CA"],
            "palette_names": ["Neon Magenta", "Cyan Glow", "Deep Obsidian", "Electric Purple"],
            "suggested_ideas": [
                "Nighttime high-tech alleyway with towering holographic billboards",
                "Cyborg artisan crafting mechanical cyber-prosthetics"
            ]
        },
        "surrealism": {
            "style_name": "Surrealism",
            "technique": "Dreamlike and bizarre scenes, illogical juxtaposition of objects, hyper-detailed fantasy landscapes.",
            "palette": ["#E2725B", "#4A5D4E", "#D4AF37", "#1C2833"],
            "palette_names": ["Terracotta", "Forest Slate", "Melted Gold", "Abyss Black"],
            "suggested_ideas": [
                "Melting clocks draped over desert crystal formations",
                "Floating islands with upside-down waterfalls under a double moon"
            ]
        },
        "minimalism": {
            "style_name": "Minimalism",
            "technique": "Stripped down to essential elements, geometric shapes, monochromatic tones, and vast negative space.",
            "palette": ["#FFFFFF", "#E5E7EB", "#6B7280", "#111827"],
            "palette_names": ["Pure White", "Soft Gray", "Graphite", "Pitch Black"],
            "suggested_ideas": [
                "Single geometric monolith casting a lone shadow across an endless white plane",
                "Overlapping translucent circular layers with subtle gradients"
            ]
        }
    }

    key = art_style.strip().lower()
    art_data = database.get(key, {
        "style_name": art_style.title(),
        "technique": f"Expressive visual blend exploring forms, emotions, and concepts in {art_style.title()} style.",
        "palette": ["#2C3E50", "#ECF0F1", "#E67E22", "#9B59B6"],
        "palette_names": ["Midnight Blue", "Cloud White", "Warm Amber", "Amethyst"],
        "suggested_ideas": [
            f"Experimental composition capturing the fundamental essence of {art_style.title()}"
        ]
    })

    if artist_name:
        art_data["inspiration"] = f"Mastery elements and stylistic nuances inspired by {artist_name.title()}."

    return art_data


def get_product_info(product_name: str, category: str = "all") -> dict:
    """Searches for product specifications, stock status, pricing, and ratings.

    Args:
        product_name: The name or keyword of the product (e.g., 'Gaming Laptop', 'Wireless Headphones', 'Mechanical Keyboard').
        category: The category of the product (e.g., 'Electronics', 'Gaming', 'Audio', 'Home').

    Returns:
        A dictionary containing product details, price, rating, stock status, and features.
    """
    catalog = {
        "laptop": {
            "item_name": "TitanBook Ultra 16 Gaming Laptop",
            "category": "Computers & Gaming",
            "price": "$1,499.00",
            "original_price": "$1,799.00",
            "in_stock": True,
            "rating": 4.9,
            "reviews_count": 328,
            "features": [
                "NVIDIA GeForce RTX 4070 (8GB GDDR6)",
                "Intel Core i9 14-Core Processor",
                "32GB DDR5 RAM (5600MHz)",
                "1TB NVMe PCIe 4.0 SSD",
                "16-inch QHD+ 240Hz OLED Display"
            ]
        },
        "headphones": {
            "item_name": "SonicPro ANC Wireless Studio Headphones",
            "category": "Audio & Electronics",
            "price": "$199.99",
            "original_price": "$249.99",
            "in_stock": True,
            "rating": 4.8,
            "reviews_count": 812,
            "features": [
                "Hybrid Active Noise Cancellation (ANC)",
                "40-Hour Extended Battery Life with Fast Charge",
                "Lossless Spatial Audio & Custom EQ",
                "Ultra-soft Memory Foam Earcups"
            ]
        },
        "keyboard": {
            "item_name": "ApexType RGB Hot-Swappable Mechanical Keyboard",
            "category": "Gaming & Peripherals",
            "price": "$129.50",
            "original_price": "$149.00",
            "in_stock": True,
            "rating": 4.7,
            "reviews_count": 450,
            "features": [
                "Gateron Linear Red Switches (Hot-Swappable)",
                "Per-Key RGB Lighting with 20 Presets",
                "Solid CNC Anodized Aluminum Base",
                "Tri-mode: 2.4GHz Wireless, Bluetooth 5.2, USB-C"
            ]
        },
        "camera": {
            "item_name": "Lumina 4K Mirrorless Creator Camera",
            "category": "Photography & Video",
            "price": "$899.00",
            "original_price": "$999.00",
            "in_stock": False,
            "rating": 4.6,
            "reviews_count": 190,
            "features": [
                "24.2 MP Full-Frame Exmor Sensor",
                "4K 60fps Uncompressed Video Recording",
                "Real-time Eye AutoFocus Tracking",
                "Flip-out 3.2-inch Touchscreen"
            ]
        }
    }

    query = product_name.strip().lower()
    for key, item in catalog.items():
        if key in query:
            return item

    return {
        "item_name": product_name.title(),
        "category": category.title(),
        "price": "Market Price Upon Inquiry",
        "in_stock": False,
        "rating": 4.2,
        "reviews_count": 45,
        "features": [
            "Standard Manufacturer 1-Year Warranty",
            "Global Shipping Available",
            "Verified Authentic Distribution"
        ],
        "notice": "Item currently not cataloged in instant inventory; standard order fulfillment applies."
    }

TOOL_REGISTRY = {
    "get_art_info": {
        "func": get_art_info,
        "name": "Art Recommendation & Palette Tool",
        "icon": "palette",
        "description": "Generates artistic concepts, color swatches, and technical art style breakdowns.",
        "params": ["art_style (str)", "artist_name (str, optional)"]
    },
    "get_product_info": {
        "func": get_product_info,
        "name": "Product & Inventory Search Tool",
        "icon": "shopping-bag",
        "description": "Retrieves real-time product specifications, prices, reviews, and stock availability.",
        "params": ["product_name (str)", "category (str, optional)"]
    }
}

# ==========================================
# 2. Routes & Gemini Interaction Handler
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tools", methods=["GET"])
def list_tools():
    tools_info = []
    for name, data in TOOL_REGISTRY.items():
        tools_info.append({
            "id": name,
            "name": data["name"],
            "icon": data["icon"],
            "description": data["description"],
            "params": data["params"]
        })
    return jsonify({"tools": tools_info})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    api_key = data.get("api_key", "").strip() or os.environ.get("GEMINI_API_KEY", "")
    model_name = data.get("model", "gemini-3.7-flash")

    if not user_message:
        return jsonify({"error": "Please provide a message."}), 400

    if not api_key:
        return jsonify({
            "error": "Gemini API key is required. Please set it in the top settings bar or as GEMINI_API_KEY environment variable."
        }), 401

    try:
        # Initialize Gemini Client
        client = genai.Client(api_key=api_key)
        
        # Tools to offer to the model
        tools = [get_art_info, get_product_info]

        # Execute conversation with tool execution capture
        # We use manual / automated dispatch tracking
        tool_executions = []

        # Intercept tool calls to send visual details to the frontend
        def track_art_info(art_style: str, artist_name: str = None) -> dict:
            result = get_art_info(art_style, artist_name)
            tool_executions.append({
                "tool_name": "get_art_info",
                "display_name": "Art Knowledge & Palette Tool",
                "icon": "palette",
                "args": {"art_style": art_style, "artist_name": artist_name},
                "result": result
            })
            return result

        def track_product_info(product_name: str, category: str = "all") -> dict:
            result = get_product_info(product_name, category)
            tool_executions.append({
                "tool_name": "get_product_info",
                "display_name": "Product Catalog & Pricing Tool",
                "icon": "shopping-bag",
                "args": {"product_name": product_name, "category": category},
                "result": result
            })
            return result

        # Session history in Flask session
        chat_session_history = session.get("chat_history", [])

        # Try the requested model first, with fallback if 503 high demand occurs
        candidate_models = [model_name]
        if model_name != "gemini-3.5-flash-lite":
            candidate_models.append("gemini-3.5-flash-lite")

        response = None
        last_error = None
        used_model = model_name

        for target_model in candidate_models:
            try:
                chat = client.chats.create(
                    model=target_model,
                    config=types.GenerateContentConfig(
                        tools=[track_art_info, track_product_info],
                        temperature=0.7,
                        system_instruction=(
                            "You are an intelligent multimodal AI assistant equipped with dynamic tools:\n"
                            "1. 'get_art_info': Call this whenever the user asks for art ideas, styles, techniques, color palettes, or artistic guidance.\n"
                            "2. 'get_product_info': Call this whenever the user asks about products, laptops, gadgets, electronics, pricing, specs, or shopping.\n"
                            "When a tool returns information, synthesize it cleanly, highlight key details (like color palettes, specs, and prices), and be engaging and conversational."
                        )
                    )
                )
                response = chat.send_message(user_message)
                used_model = target_model
                break
            except Exception as ex:
                err_str = str(ex)
                last_error = ex
                # If 503 (high demand) or 429, try the next model
                if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                    continue
                else:
                    raise ex

        if response is None:
            if last_error:
                raise last_error
            return jsonify({"error": "Service temporarily unavailable. Please try again."}), 503

        response_text = response.text or ""

        # Update history
        chat_session_history.append({"role": "user", "content": user_message})
        chat_session_history.append({
            "role": "model",
            "content": response_text,
            "tool_calls": tool_executions
        })
        session["chat_history"] = chat_session_history

        return jsonify({
            "response": response_text,
            "tool_calls": tool_executions,
            "model": used_model
        })

    except Exception as e:
        error_msg = str(e)
        return jsonify({"error": error_msg}), 500

@app.route("/api/clear", methods=["POST"])
def clear_history():
    session.pop("chat_history", None)
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    print("==================================================")
    print(" Gemini Agent Web UI starting on http://127.0.0.1:5000")
    print("==================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)
