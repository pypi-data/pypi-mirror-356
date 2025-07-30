import json
import requests

from flask import make_response, Response

from vitessestack_common.test import gateway_signature


def check_authorization(authorizer_url: str):
    def check_decorator(func, *args, **kwargs):
        def execution(*args, **kwargs):
            result = make_response({"response": "Unauthorized"})
            result.status_code = 403

            signature = gateway_signature()
            response = requests.get(
                authorizer_url, headers=signature.get("headers", {})
            )

            response_content = json.loads(response.content.decode())

            if (
                response.status_code == 200
                and response_content.get("policyDocument", {})
                .get("Statement", [{}])[0]
                .get("Effect", "")
                == "Allow"
            ):
                if response_content.get("context", {}).get("replace_client"):
                    to_client = response_content.get("context", {}).get(
                        "replace_client"
                    )
                    result = func(
                        *args,
                        authorizer_data={
                            "requestContext": {"authorizer": {"to_client": to_client}}
                        },
                        **kwargs
                    )
                else:
                    result: Response = func(*args, **kwargs)

            return result

        return execution

    return check_decorator
