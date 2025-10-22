import requests
import json
import re

# ✅ Your Google Gemini API key
api_key = "AIzaSyAI-vjHKEcqrOCZZUJ-qMA-zVTdUBwGiIc"

jsonFormat = '''
{
  "quiz_title": "Sample Practice Quiz",
  "quiz_description": "This is a template for a multiple-choice practice quiz.",
  "questions": [
    {
      "id": 1,
      "question": "Question text goes here",
      "choices": ["A. Option A", "B. Option B", "C. Option C", "D. Option D"],
      "answer": "A.",
      "explanation": "Optional explanation for the correct answer."
    }
  ]
}
'''

def QueryAI(topic, numberQuestions):
    # ✅ Gemini 2.5 Flash (latest & free)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}

    prompt = f"""
    Generate a comprehensive practice quiz on {topic} based on AP Classroom practice exams.
    Include exactly {numberQuestions} questions.
    Each question must include "id", "question", "choices", "answer", and "explanation".
    Some questions should include real-life examples.
    You're allowed to have more than 4 answer choices.
    Output strictly valid JSON using double quotes for all keys and strings.
    Do not include any extra text outside the JSON (no "Here is...", no ``` or extra quotes).
    Do not include image-based questions.
    The final JSON must follow this format: {jsonFormat}
    """

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    print("RAW RESPONSE TEXT:", response.text)

    try:
        data = response.json()

        if "error" in data:
            print("❌ API Error:", data["error"]["message"])
            return None

        quiz = data["candidates"][0]["content"]["parts"][0]["text"]

        # ✅ Auto-remove code fences like ```json ... ```
        quiz = re.sub(r"^```(json)?", "", quiz.strip(), flags=re.IGNORECASE)
        quiz = re.sub(r"```$", "", quiz.strip())
        quiz = quiz.strip().lstrip("json").lstrip().strip("'").strip('"')

    except Exception as e:
        print("❌ Error parsing Gemini response:", e)
        return None

    return quiz
