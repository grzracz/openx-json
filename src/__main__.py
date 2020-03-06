from urllib.request import urlopen
from urllib.error import URLError
import json
from collections import defaultdict, Counter
from numpy import unique, radians, sin, cos, arcsin, sqrt


def get_data_from_url(url):
    try:
        with urlopen(url) as url:
            return json.loads(url.read().decode())
    except URLError as e:
        print("Something went wrong while trying to connect to:", url)
        print("Error:", e)
        return None


def get_user_by_id(users, user_id):
    try:
        return next((user for user in users if user["id"] == user_id), None)
    except KeyError as e:
        print("Some users are invalid, can not continue")
        print("Error: Invalid key", e)
        return None


def assign_posts_to_users(users, posts):
    user_posts = defaultdict(list)
    no_errors = True
    for post in posts:
        try:
            user_posts[post["userId"]].append(post)
        except KeyError as e:
            print("Post invalid, ignoring:\n", post)
            print("Error: Invalid key", e)
            no_errors = False
    for index in user_posts:
        get_user_by_id(users, user_posts[index][0]["userId"])["posts"] = user_posts[index]
    return no_errors


def get_users_posts_amount_string_list(users):
    string_list = []
    for user in users:
        try:
            string_list.append(str(user["username"]) + " napisał(a) " + str(len(user["posts"])) + " postów")
        except KeyError as e:
            print("User invalid, ignoring:\n", user)
            print("Error: Invalid key", e)
    return string_list


def post_titles_unique(posts):
    try:
        post_titles = [post["title"] for post in posts]
        return unique(post_titles).size == len(posts), post_titles
    except KeyError as e:
        print("Some posts are invalid, can not continue")
        print("Error: Invalid key", e)
        return None, None


def get_duplicates(object_list):
    return [item for item, count in Counter(object_list).items() if count > 1]


def distance_Haversine(first_latitude, first_longitude, second_latitude, second_longitude):
    lat1, lng1, lat2, lng2 = map(radians, [float(first_latitude), float(first_longitude), float(second_latitude), float(second_longitude)])
    distance_in_km = 12734 * arcsin(sqrt(sin((lat2 - lat1) / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin((lng2 - lng1) / 2.0) ** 2))
    return distance_in_km


def assign_closest_user_to_users(users):
    no_errors = True
    for user in users:
        min_distance = 20040
        closest_user_id = -1
        try:
            lat = user["address"]["geo"]["lat"]
            lng = user["address"]["geo"]["lng"]
        except KeyError as e:
            print("User coordinates unknown, ignoring:", user)
            print("Error: Invalid key", e)
            no_errors = False
            continue
        for user_temp in users:
            if user == user_temp:
                continue
            try:
                temp_distance = distance_Haversine(lat, lng,
                                                   user_temp["address"]["geo"]["lat"],
                                                   user_temp["address"]["geo"]["lng"])
            except KeyError:
                continue
            if temp_distance < min_distance:
                min_distance = temp_distance
                closest_user_id = user_temp["id"]
        user["closestUserId"] = closest_user_id
    return no_errors


def main(args=None):
    posts = get_data_from_url("https://jsonplaceholder.typicode.com/posts")
    users = get_data_from_url("https://jsonplaceholder.typicode.com/users")
    print(users)
    for user in users:
        print(user["address"]["geo"])
    assign_posts_to_users(users, posts)

    for string in get_users_posts_amount_string_list(users):
        print(string)

    print()
    all_unique, titles = post_titles_unique(posts)
    if all_unique:
        print("Wszystkie tytuły postów są unikalne")
    else:
        print("Te tytuły postów nie są unikalne:")
        for duplicate in get_duplicates(titles):
            print(duplicate)

    print()
    assign_closest_user_to_users(users)
    for user in users:
        print(user["username"], "mieszka najblizej uzytkownika:",
              get_user_by_id(users, user["closestUserId"])["username"])


if __name__ == '__main__':
    main()
