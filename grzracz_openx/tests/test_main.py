import unittest
from grzracz_openx import *


class TestMain(unittest.TestCase):
    def setUp(self):
        self.users_url = "https://jsonplaceholder.typicode.com/users"
        self.posts_url = "https://jsonplaceholder.typicode.com/posts"
        self.valid_users = [
            {
                "id": 1,
                "username": "One",
                "address": {
                    "geo": {
                        "lat": "10",
                        "lng": "20"
                    }
                },
            },
            {
                "id": 2,
                "username": "Two",
                "address": {
                    "geo": {
                        "lat": "-10",
                        "lng": "-20"
                    }
                },
            },
            {
                "id": 3,
                "username": "Three",
                "address": {
                    "geo": {
                        "lat": "10",
                        "lng": "21"
                    }
                },
            }
        ]
        self.invalid_objects = [
            {
                "test": 1
            },
            {
                "test": 2
            }
        ]
        self.valid_posts = [
            {
                "userId": 1,
                "id": 1,
                "title": "Title 1",
            },
            {
                "userId": 3,
                "id": 2,
                "title": "Title 2",
            },
            {
                "userId": 2,
                "id": 3,
                "title": "Title 3",
            }
        ]
        self.duplicated_posts = [
            {
                "userId": 1,
                "id": 1,
                "title": "Title 1",
            },
            {
                "userId": 1,
                "id": 1,
                "title": "Title 1",
            },
            {
                "userId": 1,
                "id": 1,
                "title": "Title 1",
            }
        ]

    def test_get_data_from_url_exceptions(self):
        with self.assertRaises(ValueError):
            get_data_from_url("test")
        with self.assertRaises(URLError):
            get_data_from_url("https://test.test")

    def test_get_data_from_url_data(self):
        self.assertEqual(type(get_data_from_url(self.users_url)), list)
        self.assertEqual(type(get_data_from_url(self.posts_url)), list)

    def test_get_user_by_id_exceptions(self):
        with self.assertRaises(KeyError):
            get_user_by_id(None, None)
        with self.assertRaises(KeyError):
            get_user_by_id(None, 1)

    def test_get_user_by_id_data(self):
        self.assertEqual(get_user_by_id(self.valid_users, 1), self.valid_users[0])
        self.assertEqual(get_user_by_id(self.valid_users, 100), None)

    def test_assign_posts_to_users_exceptions(self):
        self.assertEqual(assign_posts_to_users(self.invalid_objects, self.invalid_objects), False)

    def test_assign_posts_to_users_assignment(self):
        assign_posts_to_users(self.valid_users, self.valid_posts)
        self.assertEqual(self.valid_users[1]["posts"][0], self.valid_posts[2])

    def test_get_users_posts_amount_string_list_exceptions(self):
        strings, status = get_users_posts_amount_string_list(self.invalid_objects)
        self.assertEqual(strings, [])
        self.assertEqual(status, False)

    def test_get_users_posts_amount_string_list_data(self):
        strings, status = get_users_posts_amount_string_list(self.valid_users)
        self.assertEqual(strings, [])
        self.assertEqual(status, False)
        assign_posts_to_users(self.valid_users, self.valid_posts)
        strings, status = get_users_posts_amount_string_list(self.valid_users)
        self.assertTrue("One napisal(a) 1 postow" in strings)
        self.assertTrue("Two napisal(a) 1 postow" in strings)
        self.assertEqual(status, True)

    def test_post_titles_unique_exceptions(self):
        with self.assertRaises(KeyError):
            post_titles_unique(self.invalid_objects)
        with self.assertRaises(KeyError):
            post_titles_unique(None)

    def test_post_titles_unique_result(self):
        are_unique, titles = post_titles_unique(self.valid_posts)
        self.assertEqual(are_unique, True)
        self.assertTrue(len(titles) == len(self.valid_posts))
        are_unique, titles = post_titles_unique(self.duplicated_posts)
        self.assertEqual(are_unique, False)
        self.assertTrue(len(titles) == 3)

    def test_get_duplicates(self):
        with self.assertRaises(TypeError):
            self.assertEqual(get_duplicates(None), [])
        are_unique, titles = post_titles_unique(self.valid_posts)
        self.assertEqual(get_duplicates(titles), [])
        are_unique, titles = post_titles_unique(self.duplicated_posts)
        self.assertTrue(len(get_duplicates(titles)) == 1)

    def test_distance_Haversine(self):
        cracow = [50.049683, 19.944544]
        warsaw = [52.237049, 21.017532]
        distance = 254.3
        self.assertAlmostEqual(distance_Haversine(cracow[0], cracow[1],
                                                  warsaw[0], warsaw[1]), distance, 0)

    def test_assign_closest_user_to_users_exceptions(self):
        status = assign_closest_user_to_users(self.invalid_objects)
        self.assertEqual(status, False)

    def test_assign_closest_user_to_users_data(self):
        status = assign_closest_user_to_users(self.valid_users)
        self.assertEqual(status, True)
        self.assertEqual(self.valid_users[0]["closestUserId"], 3)

    def test_main(self):
        self.assertEqual(main('s'), False)
        self.assertEqual(main(self.posts_url, self.users_url), True)
        self.assertEqual(main(), True)


if __name__ == '__main__':
    unittest.main()
