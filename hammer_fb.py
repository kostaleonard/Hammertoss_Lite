#!/usr/bin/python3
import facebook


# TODO keys, tokens, etc.
APP_ID = '821222461720870'
APP_SECRET = ''
USER_SHORT_ACCESS_TOKEN = 'EAALq5cEcySYBAE3g1G9rOQjFAfy9wTyxVtepaVgsET5d1Fc7cHZBefVVY1bRGAvTxZBwDZBewyyvK7axGoU3S5hxNALIDLSHqLCOtZAA1Qsf59C3JTDZA2ekc62HEWGweWM7Bgca52rTjVtCSw9PIfKgxQslZA34ajMCW0AZBfcZAl4TBvqjQksCw6eeyeOT1KqUYpLmVhOeuZBclOJcmzQYLQCqUZBGSVZCqXQaKZBiVy4jZCQZDZD'
USER_LONG_ACCESS_TOKEN = 'EAALq5cEcySYBAOckvAQIm1ZC9NWXRepXEx9zclliZCQJOuMeWGlFJak8yx28KdVRoxOe2kcyNNahzoGadgXRf4OV4zfyXUkiapTdQY6kqnSuYKNTZAYb1UF84fRe5lLUUx23QG3ZBT6ChNvRyTRifnTqQZByHbIx3YcNQ1mEPTwZDZD'

PAGE_LONG_ACCESS_TOKEN = 'EAALq5cEcySYBADHemZAiRUqTHaJwjGZAh1pZCBbm3LnLovTgorO7dDPbXZAUu31l8k8TrYBJPaWivcsihd0PfnHTMgdTvNharhxAtToIUAOX4AdgZCJZCGiLLQKbOl5Gj8fkarbbr7K9FL6XY45e7XbpzbAymN5pU3doc3qmzFgwZDZD'
PAGE_USERNAME = 'Hammer_6f5902ac237024bdd0c176cb93063dc4'

# The static account to which the malware connects.
# TODO actually create this twitter account.
STATIC_C2_ACCOUNT = 'Sulla09366348'


def main():
    """Runs the program."""
    print('Hello world')
    graph = facebook.GraphAPI(
        access_token=PAGE_LONG_ACCESS_TOKEN,
        version='3.1')
    page_data = get_page_data(graph)
    print(page_data['data'][0]['id'])
    page_id = page_data['data'][0]['id']
    posts = graph.get_object(
        id=page_id,
        fields='posts')
    print(posts)


def get_page_data(graph):
    """Returns basic page data, either for testing connectivity, or for
    later use."""
    return graph.get_object("/me/accounts")



if __name__ == '__main__':
    main()

