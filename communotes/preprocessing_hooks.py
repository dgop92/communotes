def ignore_auth_urls(endpoints):
    endpoints = filter(lambda e: e[0].find("auth") == -1, endpoints)
    return endpoints
