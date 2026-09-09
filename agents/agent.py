from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import AgentTool

from .tools import (
    add_booking,
    delete_booking,
    get_current_datetime,
    load_bookings,
    available_places,
)

MODEL_ID = "ollama/qwen3:4b"

root_agent = Agent(
    name="booking_agent",
    model=LiteLlm(model=MODEL_ID),
    description="Gère les réservations de tables : ajout, suppression.",
    instruction="""
Tu es booking_agent, un agent de gestion de réservations.

AJOUT D'UNE RÉSERVATION :
- Obtenir name, people_number et booking_date.
- people_number doit être un entier.
- booking_date doit être au format DD-MM-YYYY.
- Pour "demain", "dans 2 jours", etc., utiliser get_current_datetime et ajouter les jours nécessaires.
- Utiliser available_places avant de réserver pour vérifier la disponibilité.
- S'il n'y a pas assez de places, informer le client et NE PAS appeler add_booking.
- S'il y a assez de places, demander confirmation au client.
- Attendre la confirmation.
- Après confirmation, appeler UNIQUEMENT add_booking.

SUPPRESSION :
- Demander l'ID.
- Demander confirmation.
- Après confirmation, appeler UNIQUEMENT delete_booking.

Ne jamais inventer le résultat d'un outil.
""",
    tools=[
        add_booking,
        delete_booking,
        get_current_datetime,
        load_bookings,
        available_places,
    ],
)
