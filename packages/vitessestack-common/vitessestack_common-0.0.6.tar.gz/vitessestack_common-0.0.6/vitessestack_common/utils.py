import jwt


def empty_method(*args, **kwargs):
    return


def get_router_definition_string():
    with open("routes.json", "r") as file:
        result = file.read()
        file.close()

    return result


def get_token_payload(token: str):
    try:
        result = jwt.decode(token, options={"verify_signature": False}) or {}
    except Exception as e:
        result = {}

    return result


__all__ = ["empty_method", "get_router_definition_string"]
