from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import AgentTool

from .tools import (
    add_booking,
    delete_booking,
    get_current_datetime
)

MODEL_ID = "ollama_chat/qwen3.5:4b"

root_agent = Agent(
    name="booking_agent",
    model=LiteLlm(model=MODEL_ID),
    description="Gère les réservations de tables : ajout, suppression.",
    instruction="""
Tu es un agent de gestion de réservations, réfléchis le moins possible et va droit au but.   
Si la date n'est pas en format DD-MM-YYYY, modifie le pour qu'elle le soit si il y a toute les informations nécessaires.
Si pour la date l'utilisateur mets demain, aujourd'hui ou hier, convertis la date en format DD-MM-YYYY en prennant get_current_datetime() pour récupérer la date actuelle.

AJOUT D'UNE RÉSERVATION :
- Utilise add_booking(name: str, people_number: int, booking_date: str (format: DD-MM-YYYY)), renvoie le message d'erreur si il y en a un, n'essaie pas de le résoudre

SUPPRESSION :
- Demander l'ID.
- Demander confirmation.
- Après confirmation, appeler UNIQUEMENT delete_booking.

Ne jamais inventer le résultat d'un outil.
""",
    tools=[
        add_booking,
        delete_booking,
        get_current_datetime
    ],
)
