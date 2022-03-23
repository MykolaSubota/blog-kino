from main import all_posts_by_author, post_commentators, number_of_posts_by_author, categories_of_posts_by_author, \
    tag_posts


def convert_to_list(data):
    data_list = []
    for items in data:
        for item in items:
            data_list.append(str(item))
    return data_list


def test_all_posts_by_author():
    assert convert_to_list(all_posts_by_author('James Smith')) == ['November', 'Edge of Tomorrow 2 gets a new script?']


def test_post_comments():
    assert convert_to_list(post_commentators('88 minutes')) == ['James Smith', 'John Johnson']


def test_number_of_posts_by_author():
    assert list(number_of_posts_by_author('James Smith'))[0] == 2


def test_categories_of_posts_by_author():
    assert convert_to_list(categories_of_posts_by_author('James Smith')) == ['Thriller', 'Fantasy']


def test_tag_posts():
    assert convert_to_list(tag_posts('thriller')) == ['November', '88 minutes']
