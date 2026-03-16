from recommender import data, tfidf_matrix
from sklearn.metrics.pairwise import cosine_similarity

def similar_projects(index):
    scores = cosine_similarity(tfidf_matrix[index], tfidf_matrix)
    indexes = scores.argsort()[0][-4:][::-1]
    return data.iloc[indexes]
