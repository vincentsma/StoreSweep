import csv
import requests
from bs4 import BeautifulSoup

# Pseudocode:
# 1. Define a function to fetch items from a store's API.
# 2. Define the knapsack solver function.
# 3. Define a function to filter items based on user-selected categories.
# 4. Define a function to get user preferences for budget and categories.
# 5. Set up a dictionary with hypothetical API URLs for various stores.
# 6. Fetch and filter items from each store and solve the knapsack problem.
# 7. Display the results.

def fetch_items_from_website(url):
    """Fetch items from a website using web scraping."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        items = []

        for product in soup.find_all('div', class_='product'):
            name = product.find('span', class_='product-name').get_text()
            weight = product.find('span', class_='product-weight').get_text()
            value = product.find('span', class_='product-value').get_text()
            category = product.find('span', class_='product-category').get_text()

            items.append({
                'name': name.strip(),
                'weight': convert_to_number(weight),
                'value': convert_to_number(value),
                'category': category.strip().lower()
            })

        return items

    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

def convert_to_number(string):
    """Convert a string to a number. Implement this based on the expected format."""
    # Example implementation (modify as needed):
    return float(''.join(filter(str.isdigit, string)) or 0)


def knapsack_solver(items, max_weight):
    """Solve the knapsack problem given a list of items and a maximum weight."""
    n = len(items)
    K = [[0 for x in range(max_weight + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(max_weight + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif items[i-1]['weight'] <= w:
                K[i][w] = max(items[i-1]['value'] + K[i-1][w-items[i-1]['weight']],  K[i-1][w])
            else:
                K[i][w] = K[i-1][w]

    return K[n][max_weight]

def filter_items_by_categories(items, categories):
    """Filter items by the given list of categories."""
    return [item for item in items if item['category'].lower() in categories]

def get_user_preferences():
    """Get user input for budget and desired item categories."""
    budget = int(input("Enter your budget (max weight): "))
    desired_categories = input("Enter desired categories (comma-separated, e.g., meat, vegetables): ")
    desired_categories = desired_categories.split(',')
    return budget, [category.strip().lower() for category in desired_categories]

def write_items_to_csv(store, items):
    """Write items to a CSV file."""
    filename = f"{store}_items.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Weight', 'Value', 'Category'])
        for item in items:
            writer.writerow([item['name'], item['weight'], item['value'], item['category']])

website_urls = {
    "Walmart Supercenters": "https://www.walmart.com/browse/food/976759",
    "Kroger": "https://www.kroger.com/d/grocery",
    "Albertsons": "https://www.albertsons.com/shop/aisles.html",
    "Publix": "https://www.publix.com/shop-online",
    "Costco": "https://www.costco.com/grocery-household.html",
    "Aldi": "https://www.aldi.us/en/products/",
    "Target": "https://www.target.com/c/grocery/-/N-5xt1a",
    "Safeway": "https://www.safeway.com/shop/aisles.html",
    "Sam's Club": "https://www.samsclub.com/c/grocery/1444",
    "Whole Foods Market": "https://www.wholefoodsmarket.com/products/all-products"
}


budget, desired_categories = get_user_preferences()

store_baskets = {}
for store, url in website_urls.items():
    items = fetch_items_from_website(url)
    write_items_to_csv(store, items)  # Write items to CSV
    filtered_items = filter_items_by_categories(items, desired_categories)
    max_value = knapsack_solver(filtered_items, budget)
    store_baskets[store] = max_value

for store, value in store_baskets.items():
    print(f"Maximum value achievable at {store} within the budget: {value}")