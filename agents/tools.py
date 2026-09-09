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
        return json.load(f)

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

def get_available_places(booking_date: str) -> dict:
    """
    Retourne le nombre de places disponibles pour une date donnée (format DD-MM-YYYY).
    La capacité maximale est de 50 places.
    """
    
    bookings = _load_json(TABLE_BOOKINGS_FILE)
    reserved = sum(
        b["people_number"] for b in bookings if b["date"] == booking_date
    )
    available = MAX_CAPACITY - reserved
    return {
        "date": booking_date,
        "capacity": MAX_CAPACITY,
        "reserved": reserved,
        "available": available,
        "created_at": get_current_datetime(),
    }

def add_booking(name: str, people_number: int, booking_date: str) -> dict:
    """
    Ajoute une réservation de table.

    Args :
        name (str): Nom du client.
        people_number (int): Nombre de personnes pour la réservation.
        booking_date (str): Date de la réservation au format DD-MM-YYYY.
    
    Returns :
        dict: Détails de la réservation si réussie, sinon un message d'erreur.
    """
    
    availability = get_available_places(booking_date)
    if people_number > availability["available"]:
        return {
            "error": (
                f"Pas assez de places pour le {booking_date}. "
                f"Demandé : {people_number}, disponible : {availability['available']}"
            )
        }

    bookings = _load_json(TABLE_BOOKINGS_FILE)
    booking = {
        "id": _next_id(bookings),
        "name": name,
        "people_number": people_number,
        "date": booking_date,
    }
    bookings.append(booking)
    _save_json(TABLE_BOOKINGS_FILE, bookings)
    return {**booking, "places_restantes": availability["available"] - people_number}

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
