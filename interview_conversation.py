from typing import Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime
from llm_evaluator import LLMEvaluator

@dataclass
class InterviewTurn:
    """Single Q&A exchange in interview."""
    turn_number: int
    question: str
    answer: str
    evaluation: Dict
    timestamp: str

class InterviewConversation:
    """Manages multi-turn interview conversation with LLM."""

    def __init__(self, topic: str, keywords: List[str] = None):
        self.topic = topic
        self.keywords = keywords or []
        self.evaluator = LLMEvaluator()
        self.turns: List[InterviewTurn] = []
        self.current_turn = 0
        self.total_score = 0

    def start_interview(self) -> str:
        """Begin the interview with first question."""
        self.current_turn = 1
        initial_question = self.evaluator.generate_response(
            f"Generate an interview question about: {self.topic}. "
            f"Return ONLY the question, no other text.",
            temperature=0.7
        )
        return initial_question

    def process_answer(self, question: str, answer: str) -> Dict:
        """Process answer and generate next question or followup."""
        self.current_turn += 1

        # Evaluate answer
        evaluation = self.evaluator.evaluate_answer(question, answer, self.keywords)

        # Store turn
        turn = InterviewTurn(
            turn_number=self.current_turn,
            question=question,
            answer=answer,
            evaluation=evaluation,
            timestamp=datetime.now().isoformat()
        )
        self.turns.append(turn)
        self.total_score += evaluation.get("score", 5)

        return {
            "evaluation": evaluation,
            "turn_number": self.current_turn
        }

    def get_next_question(self, previous_answer: str, num_questions: int = 1) -> str:
        """Generate next question based on previous answer."""
        if num_questions == 1:
            # Get follow-up question
            followups = self.evaluator.generate_followup_questions(
                self.turns[-1].question,
                previous_answer,
                num_questions=1
            )
            return followups[0] if followups else "Can you elaborate more on that?"
        else:
            # Generate new question on topic
            return self.evaluator.generate_response(
                f"Generate a different interview question about {self.topic} that explores a different aspect. "
                f"The previous question was: {self.turns[-1].question if self.turns else 'None'} "
                f"Return ONLY the question.",
                temperature=0.8
            )

    def get_interview_summary(self) -> Dict:
        """Generate comprehensive interview summary."""
        if not self.turns:
            return {"error": "No questions answered yet"}

        avg_score = self.total_score / len(self.turns)

        all_feedback = "\n".join([
            f"Q{i+1}: {turn.evaluation.get('overall_feedback', '')}"
            for i, turn in enumerate(self.turns)
        ])

        summary_prompt = f"""Provide a concise interview performance summary based on these feedbacks:

{all_feedback}

Include:
- Overall performance level (Beginner/Intermediate/Advanced)
- Key strengths demonstrated
- Main areas for improvement
- Specific recommendations for study/practice
- Final assessment (1-2 sentences)"""

        summary = self.evaluator.generate_response(summary_prompt, temperature=0.2)

        return {
            "num_questions": len(self.turns),
            "average_score": round(avg_score, 1),
            "scores": [turn.evaluation.get("score", 0) for turn in self.turns],
            "all_turns": [asdict(turn) for turn in self.turns],
            "summary": summary
        }

    def export_results(self) -> Dict:
        """Export full interview results."""
        return {
            "topic": self.topic,
            "keywords": self.keywords,
            "total_turns": len(self.turns),
            "average_score": round(self.total_score / len(self.turns), 1) if self.turns else 0,
            "turns": [asdict(turn) for turn in self.turns],
            "timestamp": datetime.now().isoformat()
        }
