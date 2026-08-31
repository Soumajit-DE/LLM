"""Beginner-friendly doctor-patient chat agent.

This script demonstrates a simple health assistant that:
- Detects emergency symptoms and advises urgent care.
- Suggests basic, low-risk home remedies for common mild symptoms.
- Encourages professional medical consultation for diagnosis.

Important:
This is educational code, not a medical diagnosis system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


EMERGENCY_KEYWORDS = {
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "fainting",
    "unconscious",
    "seizure",
    "stroke",
    "severe bleeding",
    "suicidal",
}


SYMPTOM_REMEDIES: Dict[str, Dict[str, List[str]]] = {
    "fever": {
        "possible_causes": ["viral infection", "flu", "mild infection"],
        "remedies": [
            "Rest and stay hydrated with water or oral rehydration fluids.",
            "Use a lukewarm sponge bath if comfortable.",
            "Monitor temperature every 4-6 hours.",
            "Consider standard fever medicine only as directed by a licensed clinician.",
        ],
    },
    "cold": {
        "possible_causes": ["common cold", "allergy", "viral upper respiratory infection"],
        "remedies": [
            "Drink warm fluids like soup or herbal tea.",
            "Use steam inhalation for nasal congestion.",
            "Get enough sleep and avoid smoking exposure.",
            "Use saline nasal drops for blocked nose.",
        ],
    },
    "headache": {
        "possible_causes": ["tension headache", "dehydration", "lack of sleep"],
        "remedies": [
            "Drink water and rest in a quiet, dark room.",
            "Try a cold or warm compress on your forehead or neck.",
            "Reduce screen time and bright light exposure.",
            "Practice gentle breathing or relaxation exercises.",
        ],
    },
    "sore throat": {
        "possible_causes": ["viral infection", "throat irritation", "seasonal infection"],
        "remedies": [
            "Gargle with warm salt water 2-3 times daily.",
            "Drink warm fluids and keep your throat moist.",
            "Avoid very cold drinks and spicy foods.",
            "Use lozenges if suitable for your age group.",
        ],
    },
    "stomach pain": {
        "possible_causes": ["indigestion", "gas", "mild stomach infection"],
        "remedies": [
            "Eat light food and avoid oily/spicy meals.",
            "Sip water slowly to stay hydrated.",
            "Avoid lying down immediately after meals.",
            "Track pain pattern and food triggers.",
        ],
    },
}


@dataclass
class ChatTurn:
    role: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class DoctorPatientAgent:
    """Simple rule-based health chat assistant for beginners."""

    def __init__(self) -> None:
        self.history: List[ChatTurn] = []

    def chat(self, user_message: str) -> str:
        cleaned = user_message.strip().lower()
        self.history.append(ChatTurn(role="patient", message=user_message))

        if not cleaned:
            reply = "Please describe your symptoms in simple words so I can help."
            self.history.append(ChatTurn(role="agent", message=reply))
            return reply

        if self._has_emergency_signal(cleaned):
            reply = self._emergency_response()
            self.history.append(ChatTurn(role="agent", message=reply))
            return reply

        symptom = self._detect_symptom(cleaned)
        if symptom:
            reply = self._build_remedy_response(symptom)
        else:
            reply = self._fallback_response()

        self.history.append(ChatTurn(role="agent", message=reply))
        return reply

    def _has_emergency_signal(self, message: str) -> bool:
        return any(word in message for word in EMERGENCY_KEYWORDS)

    def _detect_symptom(self, message: str) -> str:
        for symptom in SYMPTOM_REMEDIES:
            if symptom in message:
                return symptom
        return ""

    def _build_remedy_response(self, symptom: str) -> str:
        details = SYMPTOM_REMEDIES[symptom]
        causes = ", ".join(details["possible_causes"])
        remedies = "\n".join(f"- {item}" for item in details["remedies"])

        return (
            f"I understand you may have {symptom}. Possible reasons can include {causes}.\n\n"
            f"You can try these basic remedies:\n{remedies}\n\n"
            "If symptoms worsen, persist beyond 2-3 days, or you have chronic conditions, "
            "please consult a licensed doctor for proper diagnosis."
        )

    def _emergency_response(self) -> str:
        return (
            "Your message may indicate an emergency symptom. "
            "Please contact local emergency services immediately or go to the nearest emergency room now. "
            "Do not rely on chat advice for urgent care."
        )

    def _fallback_response(self) -> str:
        known = ", ".join(sorted(SYMPTOM_REMEDIES.keys()))
        return (
            "I could not map your symptom confidently yet. "
            f"I currently support: {known}. "
            "Please share symptom duration, severity, age group, and any existing conditions, "
            "or consult a licensed doctor for accurate medical advice."
        )


if __name__ == "__main__":
    agent = DoctorPatientAgent()

    print("Doctor-Patient Chat Agent")
    print("Type 'exit' to stop.\n")

    while True:
        patient_input = input("Patient: ").strip()
        if patient_input.lower() in {"exit", "quit"}:
            print("Agent: Take care. Wishing you good health.")
            break

        response = agent.chat(patient_input)
        print(f"Agent: {response}\n")
