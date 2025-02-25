from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Google Gemini API details
LLM_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
LLM_API_KEY = os.getenv("GEMINI_API_KEY")  # Get key from environment

@app.route("/", methods=["GET", "POST"])
def home():
    generated_code = None
    if request.method == "POST":
        product_desc = request.form["description"]
        
        try:
            if not LLM_API_KEY:
                raise ValueError("GEMINI_API_KEY is not set in environment variables")
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"Generate code for: {product_desc}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": 500
                }
            }
            response = requests.post(f"{LLM_API_URL}?key={LLM_API_KEY}", json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            generated_code = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except requests.exceptions.RequestException as e:
            generated_code = f"API error: {str(e)}"
        except KeyError:
            generated_code = "API response missing expected data"
        except Exception as e:
            generated_code = f"Unexpected error: {str(e)}"
    
    return render_template("index.html", code=generated_code)

if __name__ == "__main__":
    app.run(debug=True)