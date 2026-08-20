# 🤖 Gemini Agentic AI Studio (Tool Calling Web UI)

A full-stack, real-time Web UI and Python application powered by **Gemini Flash (`gemini-2.5-flash` / `gemini-3.7-flash`)** and the official **`google-genai` SDK**. 

The AI agent dynamically chooses and executes custom Python tools based on user prompts:
- 🎨 **`get_art_info` (Art Recommendation Tool)**: Curates color palette swatches, artistic styles (Impressionism, Cyberpunk, Surrealism, Minimalism), techniques, and painting ideas.
- 🛍️ **`get_product_info` (Product Catalog Tool)**: Searches hardware specifications, prices, ratings, and stock status (Gaming Laptops, Studio Headphones, Keyboards, etc.).
- 💬 **Direct Conversation**: Responds normally when no tool execution is needed.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Set your Gemini API Key in Environment
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"

# Linux / macOS
export GEMINI_API_KEY="your_api_key_here"
```
*(Note: You can also enter or change your API key directly in the Web UI sidebar settings).*

### 3. Run the Web Application
```bash
python app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🌟 Key Features

1. **Autonomous Tool Selection**: Gemini analyzes the user's intent and automatically dispatches calls to the Art or Product tool.
2. **Visual Tool Call Cards**:
   - 🎨 **Color Swatches Preview**: Renders interactive color swatches with hex codes for art inquiries.
   - 🛍️ **Product Spec Cards**: Renders price tags, stock badges, and feature lists.
   - 🔍 **Inspect Raw JSON**: Collapsible developer inspector to view the exact payload returned by tools.
3. **Glassmorphic Dark UI**: Built with Tailwind CSS, Lucide icons, and code syntax highlighting.
4. **Interactive Prompt Chips**: One-click quick test buttons for instant demonstrations.
5. **Model Switcher**: Easily switch between `gemini-2.5-flash` and `gemini-3.7-flash`.
