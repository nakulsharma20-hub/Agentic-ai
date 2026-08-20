from google import genai

# ==================================================
# 1. GEMINI API KEY
# ==================================================

API_KEY = "AIzaSyD7ldXB5YmAvl6wisOAk5tCqXkg7iHrryg"

print("🔑 Connecting to Gemini...")

client = genai.Client(api_key=API_KEY)

print("✅ Gemini client connected!")


# ==================================================
# 2. TOOL: ADD
# ==================================================

def add(a: float, b: float) -> float:
    """Add two numbers."""

    print("\n🛠️ ADD TOOL CALLED")
    print(f"   a = {a}")
    print(f"   b = {b}")

    result = a + b

    print(f"   {a} + {b} = {result}")

    return result


# ==================================================
# 3. TOOL: MULTIPLY
# ==================================================

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""

    print("\n🛠️ MULTIPLY TOOL CALLED")
    print(f"   a = {a}")
    print(f"   b = {b}")

    result = a * b

    print(f"   {a} × {b} = {result}")

    return result


# ==================================================
# 4. TOOL: SUBTRACT
# ==================================================

def subtract(a: float, b: float) -> float:
    """Subtract b from a."""

    print("\n🛠️ SUBTRACT TOOL CALLED")
    print(f"   a = {a}")
    print(f"   b = {b}")

    result = a - b

    print(f"   {a} - {b} = {result}")

    return result


# ==================================================
# 5. TOOL: DIVIDE
# ==================================================

def divide(a: float, b: float) -> float:
    """Divide a by b."""

    print("\n🛠️ DIVIDE TOOL CALLED")
    print(f"   a = {a}")
    print(f"   b = {b}")

    if b == 0:
        print("   ❌ Cannot divide by zero")
        return 0

    result = a / b

    print(f"   {a} ÷ {b} = {result}")

    return result


# ==================================================
# 6. REGISTER ALL TOOLS
# ==================================================

tools = [
    add,
    multiply,
    subtract,
    divide
]

print("\n🔧 Tools registered:")
print("   ✅ add()")
print("   ✅ multiply()")
print("   ✅ subtract()")
print("   ✅ divide()")


# ==================================================
# 7. CREATE GEMINI CHAT
# ==================================================

print("\n🤖 Starting Gemini 3.6 Flash...")

chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "tools": tools
    }
)

print("✅ Gemini 3.6 Flash ready!")


# ==================================================
# 8. USER LOOP
# ==================================================

print("\n==========================================")
print("       GEMINI TOOL CALLING AGENT")
print("==========================================")

print("Examples:")
print("  Add 20 and 30")
print("  Multiply 5 by 10")
print("  Subtract 25 from 100")
print("  Divide 100 by 4")
print("Type 'exit' to stop.")
print("==========================================\n")


while True:

    user_input = input("👤 You: ")

    if user_input.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    print("\n🤖 Gemini is thinking...")
    print("🔍 Selecting appropriate tool...")

    try:

        response = chat.send_message(user_input)

        print("\n------------------------------------------")
        print("🤖 GEMINI RESPONSE")
        print("------------------------------------------")
        print(response.text)
        print("------------------------------------------\n")

    except Exception as e:

        print("\n❌ ERROR OCCURRED")
        print(e)
        print()