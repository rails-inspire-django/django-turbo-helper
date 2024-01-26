from bs4 import BeautifulSoup


def assert_dom_equal(expected_html, actual_html):
    expected_soup = BeautifulSoup(expected_html, "html.parser")
    actual_soup = BeautifulSoup(actual_html, "html.parser")

    expected_str = expected_soup.prettify()
    actual_str = actual_soup.prettify()

    assert expected_str == actual_str
