from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import AgentTool

from .tools import (
    add_booking,
    delete_booking,
)

MODEL_ID = "ollama_chat/qwen3.5:4b"

root_agent = Agent(
    name="booking_agent",
    model=LiteLlm(model=MODEL_ID),
    description="Gère les réservations de tables : ajout, suppression.",
    instruction="""
Tu es un agent de gestion de réservations, réfléchis le moins possible et va droit au but.   

AJOUT D'UNE RÉSERVATION :
- Utilise add_booking(name: str, people_number: int, booking_date: str (format: DD-MM-YYYY))

SUPPRESSION :
- Demander l'ID.
- Demander confirmation.
- Après confirmation, appeler UNIQUEMENT delete_booking.

Ne jamais inventer le résultat d'un outil.
""",
    tools=[
        add_booking,
        delete_booking,
    ],
)
