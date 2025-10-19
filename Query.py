import requests
import json

api_key = "cb26b1ff-7130-4efe-b07e-9657d325f28c"

jsonFormat = '''

{
  "quiz_title": "Sample Practice Quiz",
  "quiz_description": "This is a template for a multiple-choice practice quiz.",
  "questions": [
    {
      "id": 1,
      "question": "Question text goes here",
      "choices": ["A. Option A", "B. Option B", "B. Option C", "B. Option D"],
      "answer": "A.",
      "explanation": "Optional explanation for the correct answer."
    }

'''

def QueryAI(topic, numberQuestions):
    response = requests.post(
        url="https://api.awanllm.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "Meta-Llama-3.1-8B-Instruct",
            "messages": [
            {
                "role": "user",
                "content": f'''Generate a comprehensive practice quiz on {topic} based on AP Classroom practice exams. Include exactly {numberQuestions} questions. Each question must include "id", "question", "choices", "answer", and "explanation". Some questions should include real-life examples. And your allowed to have more than 4 answer choices.

                                Output strictly valid JSON using double quotes for all keys and strings. Do not include any extra text outside the JSON (no "Here is...", no ``` or extra quotes). Do not include image-based questions. The final JSON must follow this format {jsonFormat}'''
            }
            ],
            
        })
    )

    print("RAW RESPONSE TEXT:", response.text)

    quiz = response.json()["choices"][0]["message"]["content"]

    if quiz.startswith("```") and quiz.endswith("```"):
        quiz = quiz.strip("`").strip()
    elif quiz.startswith("'''") and quiz.endswith("'''"):
        quiz = quiz.strip("'").strip()

    return quiz
