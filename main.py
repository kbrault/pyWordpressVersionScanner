import requests
import re

url = "https://blender.org"


def url_exist(url_to_test):
    """Return validity of an URL
    Args:
        url_to_test (String): URL to be tested
    Returns:
        Boolean: True if the URL exists, False else
    """
    if requests.get(url_to_test).status_code == 200:
        return True
    return False

def findall_regex(regex, url_to_test):
    """If regex pattern exist on the url_to_test.content, return the Group 1 match, "Undefined" else
    Args:
        regex (Raw): pattern to match
        url_to_test (String]): URL to test
    Returns:
        String: If exists, Wordpress version, "Undefined" else
    """
    matches = re.findall(regex, url_to_test.content.decode("utf-8"), re.MULTILINE)
    if matches:
        return matches[0] 
    return "Undefined"

def search_by_meta_generator(request):
    """If exists, return the meta generator Wordpress version. If not, return "Undefined"
    Args:
        request (requests.Response): HTTP response of the url
    Returns:
        String: If exists, Wordpress version, "Undefined" else
    """
    regex = r"<meta.*?name=\"generator\".*?content=\"WordPress (\*|\d+(?:\.\d+){0,2}(?:\.\*)?)"
    return findall_regex(regex, request)

def search_by_included_version():
    """If exists, return the included CSS Wordpress version. If not, return "Undefined"
    Returns:
        String: If exists, Wordpress version, "Undefined" else
    """
    install_url = url+'/wp-admin/install.php'
    if url_exist(install_url):
        regex = r"wp-admin\/css\/install\.min\.css\?ver\=(\*|\d+(?:\.\d+){0,2}(?:\.\*)?)"
        return findall_regex(regex, requests.get(install_url))
    return "Undefined"

def search_by_feed_meta_generator():
    """If exists, return the feed meta generator Wordpress version. If not, return "Undefined"
    Returns:
        String: If exists, Wordpress version, "Undefined" else
    """
    feed_url = url+'/feed/'
    if url_exist(feed_url):
        regex = r"<generator>https:\/\/wordpress.org\/\?v\=(\*|\d+(?:\.\d+){0,2}(?:\.\*)?)"
        return findall_regex(regex, requests.get(feed_url))
    return "Undefined"

if __name__ == "__main__":
    try: 
        r = requests.get(url,timeout=3)
        print(f'Meta Generator Version : '+search_by_meta_generator(r))
        print(f'Included CSS Version : '+search_by_included_version())
        print(f'Feed Meta Generator Version : '+search_by_feed_meta_generator())
    except requests.exceptions.HTTPError as error_http:
        print ("HTTP Error : ",error_http)
    except requests.exceptions.ConnectionError as error_connexion:
        print ("Connexion Error : ",error_connexion)
    except requests.exceptions.Timeout as error_timeout:
        print ("Timeout Error : ",error_timeout)
    except requests.exceptions.RequestException as error:
        print ("Undefined Error : ",error)