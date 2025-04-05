import os
import httpx # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")  # Your OpenRouter key

async def get_recommendations(user_info: dict, schemes: list) -> str:
    import json  # Just in case for debug printing

  # (same as your full custom prompt above)
    prompt = """
You are an assistant that helps elderly citizens in the U.S. discover personalized benefits according to the state in which they reside.

Given the user's personal details, provide:
1. A list of **government schemes** they are **specifically eligible for** (do NOT give generic or unrelated schemes). Give schemes according to various fields like health, finance, food, housing, and tax. Just give the fields that are relevant to the user info provided. Give links for the specific schemes if possible.
2. A list of **discounts or offers** on **merchandise, groceries, or restaurants** that apply to them.

Please ensure:
- Each scheme includes its name and a short reason why it applies to the user.
- Each discount includes a store/brand name and what the offer is.
- Keep the output direct and easy to read.

User Info:

Please return the response in the following **JSON format**:

{
  "state": "<User's state>",
  "gov_schemes": [
    {
      "name": "...",
      "description": "...",
      "link": "..."
    }
  ],
  "discounts": [
    {
      "name": "...",
      "description": "...",
      "link": "..."
    }
  ]
}

Only include relevant schemes and discounts.
"""



    for key, value in user_info.items():
        prompt += f"- {key}: {value}\n"

    prompt += "\nAvailable Schemes:\n"
    for s in schemes:
        prompt += f"- {s['name']}: {s['description']}\n"

    prompt += "\nOnly include schemes and discounts that are relevant to the user's info above."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "google/gemini-pro",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for elderly users seeking benefits."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return f"Error from OpenRouter: {response.status_code} - {response.text}"

        result = response.json()
        print("Raw OpenRouter response:", json.dumps(result, indent=2))  # ?? Debug print

        try:
            content = result["choices"][0].get("message", {}).get("content")
            if content:
                try:
                    structured = json.loads(content)
                    return structured
                except json.JSONDecodeError:
                    print("Raw content (not JSON):", content)
                    return {"raw_text": content}
            else:
                return "Response received but no content was generated."
        except Exception as e:
            print("Exception while parsing:", e)
            return "Could not parse OpenRouter response."
