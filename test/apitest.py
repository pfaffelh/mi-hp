import requests
import json

url = "https://www.math.uni-freiburg.de/nlehre/api/person/de/6679cf96c8213a519f337504/2025SS/"

def fetch_person_data(url):
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Fehler werfen bei HTTP-Fehler
        data = response.json()
        
        # Ausgabe schön formatiert
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None

if __name__ == "__main__":
    fetch_person_data(url)


