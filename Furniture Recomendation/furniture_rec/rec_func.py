import pickle
from .furniture import Furniture
import numpy as np
from typing import List

class FurnitureRecommender:
    def __init__(self):
        """
        Creates an instance of the furniture recommender system after loading the data.
        """
        self.furniture_info = pickle.load(
            open("furniture_rec/rec_data/furniture_info.pkl", "rb")
        )
        self.furniture = pickle.load(open("furniture_rec/rec_data/furniture.pkl", "rb"))
        self.similarity_scores = pickle.load(
            open("furniture_rec/rec_data/similarity_scores.pkl", "rb")
        )
        self.furniture_names = pickle.load(open("furniture_rec/rec_data/furniture_names.pkl", "rb"))
        

    def recommend(self, furniture_name: str) -> List[Furniture]:
        """
        Find similar furniture items to the given furniture name.
        Parameters:
            furniture_name: str - name of the furniture item.
        If the furniture item is not found, an exception will be raised.
        Returns:
            list of recommended furniture items.
        """
        print(self)
        furniture_idx = np.where(self.furniture_info.index == furniture_name)[0]
        print("Furniture Name:", furniture_name)
        print("Furniture Index:", furniture_idx)
        similar_items = list(enumerate(self.similarity_scores[furniture_idx]))
        print("Similar Items:", similar_items)
        similar_items.sort(reverse=True, key=lambda x: x[1])
        print("Sorted Similar Items:", similar_items)

        recommended_furniture = []
        for i in similar_items[1:6]:
            furniture_match_df = self.furniture[
                self.furniture["Furniture-Name"] == self.furniture_info.index[i]
            ].drop_duplicates("Furniture-Name")

            furniture_item = Furniture(
                furniture_match_df["Furniture-Name"].values,
                furniture_match_df['Furniture-ID'].values,
                furniture_match_df["Category"].values,
                furniture_match_df["Price"].values,
                furniture_match_df["Material"].values,
                furniture_match_df["Image-URL"].values,
            )
            recommended_furniture.append(furniture_item)
            
        print("Recommended Furniture:", recommended_furniture)
        return recommended_furniture


furniture_recommender = FurnitureRecommender()
