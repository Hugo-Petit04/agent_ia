from datetime import datetime
import json
import os

INVENTORY_FILE = "inventory.json"
TABLE_BOOKINGS_FILE = "bookings.json"
ORDERS_FILE = "orders.json"
RECIPES_FILE = "recipes.json"
MAX_CAPACITY = 50

def get_current_datetime():
    return datetime.now().strftime("%d-%m-%Y")

def _load_json(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

def _save_json(file_path: str, data: list[dict]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _next_id(items: list[dict]) -> int:
    if not items:
        return 1
    return max(item["id"] for item in items) + 1

def load_bookings() -> list[dict]:
    """Retourne toutes les réservations existantes."""
    return _load_json(TABLE_BOOKINGS_FILE)

def available_places(booking_date: str, people_number: int) -> bool:
    """
    Retourne True si suffisamment de places sont disponibles pour une date donnée.
    """
    bookings = _load_json(TABLE_BOOKINGS_FILE)

    reserved = sum(
        int(b["people_number"])
        for b in bookings
        if b["date"] == booking_date
    )

    available = MAX_CAPACITY - reserved

    return available >= people_number

def add_booking(name: str, people_number: int, booking_date: str) -> dict:
    valid, message = validate_booking_variables(name, people_number, booking_date)
    if not valid:
        return {"error": message}

    if not available_places(booking_date, people_number):
        return {"error": "Pas assez de places disponibles pour cette date."}

    bookings = _load_json(TABLE_BOOKINGS_FILE)

    booking = {
        "id": _next_id(bookings),
        "name": name,
        "people_number": people_number,
        "date": booking_date,
    }

    bookings.append(booking)
    _save_json(TABLE_BOOKINGS_FILE, bookings)

    return {"success": True, "message": "Réservation ajoutée avec succès.", "booking": booking}

def validate_booking_variables(name: str, people_number: int, booking_date: str) -> tuple[bool, str]:
    """
    Valide les variables de réservation.
    
    Args :
        name (str): Le nom du client.
        people_number (int): Le nombre de personnes.
        booking_date (str): La date de réservation au format DD-MM-YYYY.
    
    Returns :
        tuple: (bool, str) où le booléen indique si la validation est réussie et la chaîne fournit un message d'erreur si nécessaire.
    """
    if not name:
        return False, "Le nom est requis."
    
    if not isinstance(people_number, int) or people_number <= 0:
        return False, "Le nombre de personnes doit être un entier positif."
    
    try:
        datetime.strptime(booking_date, "%d-%m-%Y")
    except ValueError:
        return False, "La date doit être au format DD-MM-YYYY."
    
    return True, ""

def delete_booking(booking_id: int) -> dict:
    """
    Supprime une réservation par son ID.
   
    Args :
        booking_id (int): L'ID de la réservation à supprimer.
    
    Returns :
        dict: Un message de succès ou d'erreur.
    """
    bookings = _load_json(TABLE_BOOKINGS_FILE)
    target = next((b for b in bookings if b["id"] == booking_id), None)

    if not target:
        return {"error": f"Aucune réservation trouvée avec l'ID {booking_id}"}

    bookings = [b for b in bookings if b["id"] != booking_id]
    _save_json(TABLE_BOOKINGS_FILE, bookings)
    return {"success": True, "deleted": target}
