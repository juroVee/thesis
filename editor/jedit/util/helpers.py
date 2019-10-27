
def transform_title(title: str) -> str:
    start = title.find('$')
    end = title.rfind('$')
    return r'' + title[start:end + 1]