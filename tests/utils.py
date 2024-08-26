from bs4 import BeautifulSoup


def normalize_classes(soup):
    """Normalize the order of CSS classes in the BeautifulSoup object."""
    for tag in soup.find_all(class_=True):
        classes = tag.get("class", [])
        sorted_classes = sorted(classes)
        tag["class"] = " ".join(sorted_classes)
    return soup


def assert_dom_equal(expected_html, actual_html):
    """Assert that two HTML strings are equal, ignoring differences in class order."""
    expected_soup = BeautifulSoup(expected_html, "html.parser")
    actual_soup = BeautifulSoup(actual_html, "html.parser")

    # Normalize the class attribute order
    expected_soup = normalize_classes(expected_soup)
    actual_soup = normalize_classes(actual_soup)

    expected_str = expected_soup.prettify()
    actual_str = actual_soup.prettify()

    assert expected_str == actual_str
