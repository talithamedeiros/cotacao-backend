import re

def validateEmail(email):
    p = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
    if len(email) > 7:
        if re.match(p, email) is not None:
            return 1
    return 0