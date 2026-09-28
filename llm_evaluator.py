import requests
import json
from typing import Dict, List
import time

class LLMEvaluator:
    """Evaluates interview responses using Ollama local LLM."""

    def __init__(self, model: str = "mistral", ollama_url: str = "http://localhost:11434"):
        self.model = model
        self.ollama_url = ollama_url
        self.check_connection()

    def check_connection(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                print(f"✓ Connected to Ollama at {self.ollama_url}")
                return True
        except requests.exceptions.RequestException:
            print(f"✗ Could not connect to Ollama at {self.ollama_url}")
            print("  Download Ollama from https://ollama.ai and run: ollama serve")
            return False

    def generate_response(self, prompt: str, temperature: float = 0.3) -> str:
        """Generate response from LLM."""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                },
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            print(f"Error calling LLM: {e}")
        return ""

    def evaluate_answer(self, question: str, answer: str, expected_keywords: List[str] = None) -> Dict:
        """Evaluate an answer using LLM."""
        keywords_text = ", ".join(expected_keywords) if expected_keywords else "General knowledge"

        prompt = f"""You are an expert interviewer evaluating a candidate's response.

QUESTION: {question}

CANDIDATE'S ANSWER: {answer}

KEY CONCEPTS TO COVER: {keywords_text}

Evaluate this answer and respond in JSON format with:
- score (1-10 integer)
- accuracy (was it correct? brief)
- completeness (did they cover main points? brief)
- strengths (list 2-3 strong points)
- areas_for_improvement (list 2-3 areas to improve)
- overall_feedback (1-2 sentences on performance)

Respond ONLY with valid JSON, no other text."""

        response_text = self.generate_response(prompt, temperature=0.1)

        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                return result
        except json.JSONDecodeError:
            pass

        return {
            "score": 5,
            "accuracy": "Unable to parse evaluation",
            "completeness": "Error in evaluation",
            "strengths": ["Response was provided"],
            "areas_for_improvement": ["Could not evaluate properly"],
            "overall_feedback": "LLM evaluation error. Please check Ollama connection."
        }

    def generate_followup_questions(self, question: str, answer: str, num_questions: int = 3) -> List[str]:
        """Generate follow-up questions based on the answer."""
        prompt = f"""Based on this interview exchange, generate {num_questions} follow-up questions to test deeper understanding.

ORIGINAL QUESTION: {question}

CANDIDATE'S ANSWER: {answer}

Generate {num_questions} thoughtful follow-up questions that probe deeper into their understanding.
Return ONLY the questions as a JSON array of strings, no other text.

Format: ["Question 1?", "Question 2?", "Question 3?"]"""

        response_text = self.generate_response(prompt, temperature=0.5)

        try:
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                questions = json.loads(json_str)
                return questions[:num_questions]
        except (json.JSONDecodeError, ValueError):
            pass

        return [
            "Can you provide more details about that concept?",
            "How would you apply that in a real-world scenario?",
            "What are the limitations or edge cases to consider?"
        ]

    def generate_ideal_answer(self, question: str, keywords: List[str] = None) -> str:
        """Generate what an ideal answer would look like."""
        keywords_text = ", ".join(keywords) if keywords else "relevant concepts"

        prompt = f"""Generate an ideal, comprehensive answer to this interview question.

QUESTION: {question}

KEY CONCEPTS TO INCLUDE: {keywords_text}

Provide a well-structured answer that covers all key concepts. Make it detailed but concise (3-4 sentences).
Start with the main answer, then add important details."""

        return self.generate_response(prompt, temperature=0.2)

    def compare_answers(self, user_answer: str, ideal_answer: str) -> Dict:
        """Compare user answer against ideal answer."""
        prompt = f"""Compare these two answers and identify key differences.

USER'S ANSWER: {user_answer}

IDEAL ANSWER: {ideal_answer}

Respond in JSON format with:
- correct_elements (what the user got right)
- missing_elements (what the user missed)
- extra_elements (correct extra info added by user)
- key_differences (main gaps between answers)

Respond ONLY with valid JSON."""

        response_text = self.generate_response(prompt, temperature=0.1)

        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return {
            "correct_elements": ["Answer was provided"],
            "missing_elements": ["Unable to determine"],
            "extra_elements": [],
            "key_differences": "Comparison failed"
        }
