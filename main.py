import requests
import re

url = "https://blender.org"

def search_by_meta_generator(request):
    """
    search_by_meta_generator : If exist, return the XXX wordpress version value of <meta name="generator" content="Wordpress XXX"/> 
    :return: If exist, return the Wordpress version of the meta generator
    """
    # How about some beautifulsoup to avoid these naughty regex ?
    regex = r"<meta.*?name=\"generator\".*?content=\"WordPress (.*?)\".*?>"
    matches = re.findall(regex, request.content.decode("utf-8"), re.MULTILINE)
    if matches:
        return matches[0] 
    else:
        return "Undefined"


def search_by_included_version(request):
    """
    search_by_included_version : If exist, return the Wordpress version of the included CSS file of the /wp-admin/install.php URI
    :return: If exist, return the Wordpress version of the included CSS file
    """
    response_install_file = requests.get(url+'/wp-admin/install.php')
    if response_install_file.status_code == 200:
        regex = r"wp-admin\/css\/install\.min\.css\?ver\=(.*?)'"
        matches = re.findall(regex, response_install_file.content.decode("utf-8"), re.MULTILINE)
        if matches:
            return matches[0]
        else:
            return "Undefined"
    else:
            return "Undefined"
        
# TODO :
# def search_by_feed_meta_generator():
# def search_by_readme_file():
# def search_by_md5_files():

if __name__ == "__main__":
    try: 
        r = requests.get(url,timeout=3)
        print(f'Meta Generator Version : '+search_by_meta_generator(r))
        print(f'Included CSS Version : '+search_by_included_version(r))
    except requests.exceptions.HTTPError as error_http:
        print ("HTTP Error :",error_http)
    except requests.exceptions.ConnectionError as error_connexion:
        print ("Connexion Error :",error_connexion)
    except requests.exceptions.Timeout as error_timeout:
        print ("Timeout Error :",error_timeout)
    except requests.exceptions.RequestException as error:
        print ("OOps: Something Else",error)