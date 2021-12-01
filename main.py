import requests
import re

url = "https://blender.org"
r = requests.get(url)


def search_by_meta_generator():
    # How about some beautifulsoup to avoid these naughty regex ?
    regex = r"<meta.*?name=\"generator\".*?content=\"WordPress (.*?)\".*?>"

    matches = re.findall(regex, r.content.decode("utf-8"), re.MULTILINE)
    if not matches:
        pass
    else:
        print(re.findall(regex, r.content.decode("utf-8"), re.MULTILINE)[0])

# TODO :
# def search_by_readme():
# def search_by_feed_meta_generator():
# def search_by_included_version():
# def search_by_md5_files():


if __name__ == "__main__":
    search_by_meta_generator()
