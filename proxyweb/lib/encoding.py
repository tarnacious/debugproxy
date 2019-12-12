
class MultipleHeadersException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

def get_charset(headers):
    content_type = get_header_value("Content-Type", headers)
    if content_type == None:
        return None
    parts = list(map(lambda x: x.strip(), content_type.split(";")))
    charset = list(filter(lambda x: x.lower().startswith("charset"), parts))
    if len(charset) == 1:
        header_value = charset[0].split("=")
        if len(header_value) == 2:
            return header_value[1]
    return None

def get_content_type(headers):
    content_type = get_header_value("Content-Type", headers)
    if content_type == None:
        return None
    parts = list(map(lambda x: x.strip(), content_type.split(";")))
    return parts[0]

def get_header_value(header_name, headers):
    headers = list(filter(lambda x: x[0].lower() == header_name.lower(),
                   headers))

    if len(headers) == 1:
        return headers[0][1]

    if len(headers) == 0:
        return None

    if len(headers) > 1:
        raise MultipleHeadersException()
