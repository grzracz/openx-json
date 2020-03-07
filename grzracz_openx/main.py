import json
from collections import defaultdict, Counter
from numpy import unique, radians, sin, cos, arcsin, sqrt
from urllib.request import urlopen
from urllib.error import URLError


def get_data_from_url(url):
    """
    Returns dict with data parsed from JSON code
    On failure: returns None
    :param url: source
    :return: data dict
    """
    try:
        with urlopen(url) as url:
            return json.loads(url.read().decode())
    except URLError as e:
        raise URLError("Can't connect to: \"" + str(url) + "\", " + str(e.reason))
    except ValueError as e:
        raise ValueError("URL invalid: \"" + str(url) + "\", " + str(e))


def get_user_by_id(users, user_id):
    """
    Returns user dict with given user id
    On failure (bad users list): raises KeyError
    :param users: list of all users to search through
    :param user_id: user identifier
    :return: user dict or None if not found
    """
    try:
        return next((user for user in users if user["id"] == user_id), None)
    except (KeyError, TypeError) as e:
        raise KeyError("Error: Bad users list: " + str(e))


def assign_posts_to_users(users, posts):
    """
    Appends posts to the dict of their user at user["posts"]
    :param users: list of all users
    :param posts: list of all posts
    :return: status bool
    """
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
    """
    Returns a list of formatted strings about the amount of posts made by each user
    :param users: list of all users
    :return: string list, status bool
    """
    string_list = []
    no_errors = True
    for user in users:
        try:
            string_list.append(str(user["username"]) + " napisal(a) " + str(len(user["posts"])) + " postow")
        except KeyError as e:
            print("User invalid, ignoring:\n", user)
            print("Error: Invalid key", e)
            no_errors = False
    return string_list, no_errors


def post_titles_unique(posts):
    """
    Checks if all posts have unique titles
    On failure: raises KeyError
    :param posts: list of all posts
    :return: bool, list of post titles
    """
    try:
        post_titles = [post["title"] for post in posts]
        return unique(post_titles).size == len(posts), post_titles
    except (KeyError, TypeError) as e:
        raise KeyError("Error: Bad posts list: Invalid key" + str(e))


def get_duplicates(object_list):
    """
    Returns all duplicates of objects in a given list
    :param object_list: list of objects
    :return: list of duplicates
    """
    return [item for item, count in Counter(list(object_list)).items() if count > 1]


def distance_Haversine(first_latitude, first_longitude, second_latitude, second_longitude):
    """
    Calculates the distance between two coordinates in km using Haversine formula
    :param first_latitude
    :param first_longitude
    :param second_latitude
    :param second_longitude
    :return: float distance
    """
    lat1, lng1, lat2, lng2 = map(radians,
                                 [float(first_latitude),
                                  float(first_longitude),
                                  float(second_latitude),
                                  float(second_longitude)])
    distance_in_km = 12734 * arcsin(sqrt(sin((lat2 - lat1) / 2.0) ** 2 +
                                         cos(lat1) * cos(lat2) * sin((lng2 - lng1) / 2.0) ** 2))
    return distance_in_km


def assign_closest_user_to_users(users):
    """
    Appends the id of the closest user to the dict of each user at user["closestUserId"]
    :param users: list of all users
    :return: status bool
    """
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


def main(posts_url="https://jsonplaceholder.typicode.com/posts",
         users_url="https://jsonplaceholder.typicode.com/users"):
    try:
        posts = get_data_from_url(posts_url)
        users = get_data_from_url(users_url)
    except (URLError, ValueError) as e:
        print("Something went wrong while trying to connect to the Internet.")
        print(e)
        return False
    else:
        assign_posts_to_users(users, posts)

        strings, status = get_users_posts_amount_string_list(users)
        for string in strings:
            print(string)

        print()
        all_unique, titles = post_titles_unique(posts)
        if all_unique:
            print("Wszystkie tytuly postow sa unikalne")
        else:
            print("Te tytuly postow nie sa unikalne:")
            for duplicate in get_duplicates(titles):
                print(duplicate)

        print()
        assign_closest_user_to_users(users)
        for user in users:
            print(user["username"], "mieszka najblizej uzytkownika:",
                  get_user_by_id(users, user["closestUserId"])["username"])
    return True


if __name__ == '__main__':
    if not main():
        exit(1)
