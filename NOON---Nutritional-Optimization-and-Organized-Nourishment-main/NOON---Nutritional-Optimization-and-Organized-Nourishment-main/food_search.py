from textblob import TextBlob
from nltk.corpus import wordnet
import requests
import nltk

# Ensure required NLTK data is downloaded
nltk.download('wordnet')
nltk.download('omw-1.4')

def correct_spelling(term):
    """
    Correct the spelling of a search term using TextBlob.
    :param term: The term to correct.
    :return: The corrected term.
    """
    blob = TextBlob(term)
    return str(blob.correct())

def get_synonyms(word):
    """
    Get a list of synonyms for a given word using WordNet.
    :param word: The word to find synonyms for.
    :return: A list of synonyms.
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))  # Replace underscores with spaces for readability
    return list(synonyms)

def search_food(search_term):
    """
    Search for food items using the OpenFoodFacts API, correcting spelling errors and expanding the search term with synonyms.
    :param search_term: The term to search for (e.g., "apple", "banana").
    :return: A list of food products with name, calories, protein, etc.
    """
    if not search_term.strip():
        return []  # Don't make an API call for empty or whitespace search terms

    # Correct the spelling of the search term
    corrected_term = correct_spelling(search_term).strip()

    # Get synonyms for the corrected term
    synonyms = get_synonyms(corrected_term)

    # Include both the original term and its synonyms in the search
    search_terms = [corrected_term] + synonyms

    food_list = []
    
    # Loop through each search term (including synonyms)
    for term in search_terms:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={term}&search_simple=1&action=process&json=1&page_size=10"  # Limit to 10 results

        try:
            response = requests.get(url, timeout=30)  # Add timeout to prevent long waits
            response.raise_for_status()  # Raises HTTPError if the response code is not 200 (OK)

            data = response.json()
            products = data.get('products', [])

            # Extract relevant nutritional data for each product
            for product in products:
                product_name = product.get('product_name', 'Unknown Product')
                calories = product.get('nutriments', {}).get('energy-kcal_100g', 'N/A')
                proteins = product.get('nutriments', {}).get('proteins_100g', 'N/A')
                carbs = product.get('nutriments', {}).get('carbohydrates_100g', 'N/A')
                fats = product.get('nutriments', {}).get('fat_100g', 'N/A')

                food_item = {
                    'name': product_name,
                    'calories': calories,
                    'proteins': proteins,
                    'carbs': carbs,
                    'fats': fats,
                }
                food_list.append(food_item)

        except requests.exceptions.RequestException as e:
            print(f"Error during API request for '{term}': {e}")

    return food_list

