import pandas as pd
import random

# List of meaningful furniture names
furniture_names = ['Table', 'Sofa', 'Chair', 'Bed', 'Cabinet', 'Wardrobe', 'Desk', 'Dresser', 'Bookshelf', 'Bench']

# Generate random Furniture data with meaningful names
def generate_furniture_data(num_rows):
    furniture_data = []
    for i in range(num_rows):
        furniture_name = random.choice(furniture_names)
        furniture_id = f'FID{i + 1}'
        category = furniture_name
        price = round(random.uniform(100, 1000), 2)
        material = random.choice(['Wood', 'Metal', 'Fabric', 'Leather', 'Plastic'])
        image_url = f'https://example.com/furniture/{furniture_id}.jpg'
        furniture_data.append([furniture_name, furniture_id, category, price, material, image_url])
    return furniture_data

# Generate random Ratings data with matching Furniture-ID values
def generate_ratings_data(num_rows, num_users, furniture_ids):
    ratings_data = []
    for i in range(num_rows):
        user_id = f'User{i + 1}'
        furniture_id = random.choice(furniture_ids)
        rating = random.randint(1, 5)
        ratings_data.append([user_id, furniture_id, rating])
    return ratings_data

# Generate Furniture data and save to CSV
furniture_data = generate_furniture_data(100)
furniture_df = pd.DataFrame(furniture_data, columns=['Furniture-Name', 'Furniture-ID', 'Category', 'Price', 'Material', 'Image-URL'])
furniture_df.to_csv('../Furniture.csv', index=False)

# Get the Furniture-ID values from the Furniture DataFrame
furniture_ids = furniture_df['Furniture-ID'].tolist()

# Generate Ratings data with matching Furniture-ID values and save to CSV
ratings_data = generate_ratings_data(500, 20, furniture_ids)
ratings_df = pd.DataFrame(ratings_data, columns=['User-ID', 'Furniture-ID', 'Furniture-Rating'])
ratings_df.to_csv('../Ratings.csv', index=False)
