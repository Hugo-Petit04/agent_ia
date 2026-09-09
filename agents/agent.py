from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import AgentTool
from tools import (
    add_booking,delete_booking, get_current_datetime
)

MODEL_ID = "llama3.2"


root_agent = Agent(
    name="booking_agent",
    model=LiteLlm(model=MODEL_ID),
    description="Gère les réservations de tables : ajout, suppression",
    instruction="""Tu es un agent spécialisé dans les réservations de tables.
Pour AJOUTER une réservation :
    - Si la date n'est pas dans un bon format (DD-MM-YYYY), modifie la et demande si c'est ce que le client souhaite.
    - Si le client dit (demain, dans 2 jours, dans 3 jours, etc.), fait get_current_datetime et ajoute le nombre de jours souhaité.
    - Utilise add_booking avec les informations nécessaires (nom, nombre de personnes, date(DD-MM-YYYY)).
 
Pour SUPPRIMER une réservation :
  - Demande l'ID de la réservation 
  - Utilise delete_booking avec l'ID confirmé

Pour CONSULTER : utilise load_bookings ou get_available_places.""",
    tools=[add_booking, delete_booking, get_current_datetime],
)
