import pandas as pd
import pickle
from sklearn.metrics import pairwise_distances
from typing import Tuple


def read_dataset() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read the datasets.
    Returns:
        tuple containing DataFrames for furniture and user ratings
    """
    furniture = pd.read_csv("dataset/Furniture.csv", low_memory=False)
    ratings = pd.read_csv("dataset/Ratings.csv")

    return furniture, ratings


def save_data(rating_matrix, similarity_scores, furniture):
    """
    Saves rating matrix, furniture, furniture names, and similarity scores in pickle format.
    Parameters:
        rating_matrix: pandas.DataFrame - User rating for each furniture item
        similarity_scores: 
        furniture: pandas.DataFrame - Details of the furniture items
    """
    pickle.dump(
        list(rating_matrix.index), open("rec_data/furniture_names.pkl", "wb")
    )
    pickle.dump(rating_matrix, open("rec_data/furniture.pkl", "wb"))
    pickle.dump(furniture, open("rec_data/furniture_info.pkl", "wb"))
    pickle.dump(similarity_scores, open("rec_data/similarity_scores.pkl", "wb"))


def furniture_rec_init():
    """
    Computes the similarity scores based on collaborative filtering.
    Users that reviewed more than 200 furniture items and furniture items with 
    equal or more than 50 ratings are considered to improve the quality of recommendations.
    Similarity is measured based on cosine-similarity.
    """
    furniture, ratings = read_dataset()

    ratings_with_furniture = ratings.merge(furniture, on="Furniture-ID")
    print(ratings_with_furniture)

    # Finding users with more than 0 reviews.
    ratings_group = ratings_with_furniture.groupby("User-ID").count()["Furniture-Rating"]
    ratings_group = ratings_group[ratings_group > 0]

    print(ratings_group)

    ratings_filtered = ratings_with_furniture[
        ratings_with_furniture["User-ID"].isin(ratings_group.index)
    ]

    # Finding furniture items with equal or more than 3 ratings.
    filtered_group = ratings_filtered.groupby("Furniture-Name").count()["Furniture-Rating"]
    filtered_group = filtered_group[filtered_group >= 3]

    final_filtered_ratings = ratings_filtered[
        ratings_filtered["Furniture-Name"].isin(filtered_group.index)
    ]

    rating_matrix = final_filtered_ratings.pivot_table(
        index="Furniture-Name", columns="User-ID", values="Furniture-Rating"
    )
    rating_matrix.fillna(0, inplace=True)

    print("Shape of the rating_matrix:", rating_matrix.shape)
    print("Rating matrix content:")
    print(rating_matrix)

    similarity_scores = pairwise_distances(rating_matrix, metric="cosine")

    print("Shape of the similarity_scores:", similarity_scores.shape)

    save_data(rating_matrix, similarity_scores, furniture)


if __name__ == "__main__":
    furniture_rec_init()
