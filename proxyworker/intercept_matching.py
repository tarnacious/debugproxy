def intercept_request(request_data, session_id, database_session):
    intercepts = database_session.get_intercepts(session_id)
    return is_intercept_match(request_data, intercepts)


def is_match(data, query):
    host = data["flow"]["request"]["host"]
    path = data["flow"]["request"]["path"]
    url = host + path
    method = data["flow"]["request"]["method"]
    query_parts = query.split()

    if len(query_parts) == 0:
        return False

    # all parts must match

    for part in query_parts:
        match = False
        if part in url:
            match = True
        if part.lower() == method.lower():
            match = True
        if match == False:
            return False

    return True



def is_intercept_match(request_data, intercepts):
    matches = len(list(filter(lambda x: is_match(request_data, x.query), intercepts)))
    return matches > 0
