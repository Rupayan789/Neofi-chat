import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def calculate_similarity(user1, user2):
    age_similarity = abs(user1['age'] - user2["age"])
    interest_similarity = 0

    # Calculate interest similarity based on common interests
    for interest, score1 in user1["interests"].items():
        if interest in user2["interests"]:
            score2 = user2["interests"][interest]
            interest_similarity += abs(score1 - score2)

    return age_similarity + interest_similarity


def get_suggested_friends_list(target_user):
    suggested_friends = []
    with open(os.path.join(BASE_DIR, 'static', 'users.json'), 'r') as json_file:
        users = json.load(json_file)['users']
        for user in users:
            if target_user['id'] != user['id']:
                similarity_score = calculate_similarity(target_user, user)
                suggested_friends.append({
                    'user': user,
                    'similarity_score': similarity_score
                })
        json_file.close()

    suggested_friends.sort(key=lambda x: x['similarity_score'])
    top_friends = suggested_friends[:5]
    return top_friends

def get_target_user(user1):
    with open(os.path.join(BASE_DIR, 'static', 'users.json'), 'r') as json_file:
        users = json.load(json_file)['users']
        for user in users:
            if user['id'] == user1.user_id:
                return user
        json_file.close()
        return None

