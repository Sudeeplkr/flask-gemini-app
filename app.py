from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Google Gemini API details
LLM_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
LLM_API_KEY = "AIzaSyAj0eC7BXR54chuvgd1vqPiuLj3DleECGg"  # Replace with your Gemini key!

@app.route("/", methods=["GET", "POST"])
def home():
    generated_code = None
    if request.method == "POST":
        product_desc = request.form["description"]
        
        try:
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
            # Gemini uses the API key as a query parameter, not in headers
            response = requests.post(f"{LLM_API_URL}?key={LLM_API_KEY}", json=payload, headers=headers, timeout=10)
            response.raise_for_status()  # Raises an error for bad status codes
            
            generated_code = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except requests.exceptions.RequestException as e:
            generated_code = f"API error: {str(e)}"
        except KeyError:
            generated_code = "API response missing expected data"
        except Exception as e:
            generated_code = f"Unexpected error: {str(e)}"
    
    return render_template("index.html", code=generated_code)

if __name__ == "__main__":
    app.run(debug=True)  # Debug mode for detailed errors