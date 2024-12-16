import pandas as pd
import numpy as np


def myIBCF(newuser):
    # Read the similarity matrix
    S_matrix = pd.read_csv("updated_similarity_matrix.csv", index_col=0)
    all_movies = pd.read_csv("all_movies_with_stats.csv")
    # Initialize predictions vector
    predictions = np.full(S_matrix.shape[1], np.nan)

    # Iterate over each movie in the similarity matrix
    for i in range(S_matrix.shape[0]):
        S_i = S_matrix.iloc[i, :]

        # Find the rated movies for the new user
        rated_movies = newuser[~newuser["Rating"].isna()]

        # Get the similarity scores for the rated movies
        S_i_intersect = S_i[rated_movies["MovieID"].values]

        # Get the ratings for the rated movies
        W_intersect = rated_movies["Rating"].values

        # Compute the weighted sum
        valid_indices = ~np.isnan(S_i_intersect)

        numerator = np.sum(S_i_intersect[valid_indices] * W_intersect[valid_indices])
        denominator = np.sum(S_i_intersect[valid_indices])

        if denominator != 0:
            predictions[i] = numerator / denominator

    # Create a DataFrame for predictions with movie IDs
    predictions_df = pd.DataFrame(
        predictions, index=S_matrix.columns, columns=["predicted_rating"]
    )

    # Sort predictions in descending order
    predictions_df = predictions_df.sort_values(by="predicted_rating", ascending=False)

    # Get the top 10 movie recommendations
    top_10_recommendations = predictions_df.head(10).index

    # Filter out already rated movies before selecting top 10 recommendations
    rated_movie_ids = rated_movies["MovieID"].values
    predictions_filtered = predictions_df[~predictions_df.index.isin(rated_movie_ids)]

    # Get the top 10 non-rated movie recommendations
    top_10_recommendations = predictions_filtered.head(10).index

    # Handle case with fewer than 10 non-NA predictions
    if len(top_10_recommendations) < 10:
        remaining_movies = all_movies.columns[~S_matrix.columns.isin(rated_movie_ids)]
        additional_recommendations = remaining_movies[
            : 10 - len(top_10_recommendations)
        ]
        top_10_recommendations = top_10_recommendations.append(
            pd.Index(additional_recommendations)
        )

    return top_10_recommendations
