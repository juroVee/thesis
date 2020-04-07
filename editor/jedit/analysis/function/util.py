def transform_title(title: str) -> str:
    if title == '':
        return ''
    start = title.find('$')
    end = title.rfind('$')
    result = r'' + title[start:end + 1]
    return result
