import re
import difflib

# List of items for suggestions
items = ["apple", "banana", "orange", "pineapple", "grape", "kiwi", "mango"]

# Function to get suggestions based on user input
def get_suggestions(query, items):
    suggestions = []
    pattern = re.compile(query, re.IGNORECASE)
    for item in items:
        if re.search(pattern, item):
            suggestions.append(item)
    return suggestions

# Function to get similar items
def get_similar_items(query, items):
    return difflib.get_close_matches(query, items)

# Main function for searching
def search(query, items):
    suggestions = get_suggestions(query, items)
    if suggestions:
        return suggestions
    else:
        similar_items = get_similar_items(query, items)
        if similar_items:
            return similar_items
        else:
            return ["No matches found"]

# Example usage
query = input("Enter your search query: ")
results = search(query, items)
print("Search results:", results)

