from flask import Flask, url_for

def generate_map_view(url_map_list):

    links = list()
    found_routes = list()

    links_divided = {}
    
    for rule in url_map_list():
        if "GET" in rule.methods and has_no_empty_params(rule):
            splitted_endpoint = rule.endpoint.split(".")
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if len(splitted_endpoint) == 1:
                splitted_endpoint[0] = ""
            if splitted_endpoint[0] not in links_divided:
                links_divided[splitted_endpoint[0]] = list()
            links_divided[splitted_endpoint[0]].append([url, rule.endpoint])
    
    return links_divided

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)