from misc.log import logger

log = logger.get_logger(__name__)


def get_response_dict(response, key_field=None, key_value=None):
    found_response = None
    try:
        if isinstance(response, list):
            if not key_field or not key_value:
                found_response = response[0]
            else:
                for result in response:
                    if isinstance(result, dict) and key_field in result and result[key_field] == key_value:
                        found_response = result
                        break

                if not found_response:
                    log.error("Unable to find a result with key %s where the value is %s", key_field, key_value)

        elif isinstance(response, dict):
            found_response = response
        else:
            log.error("Unexpected response instance type of %s for %s", type(response).__name__, response)

    except Exception:
        log.exception("Exception determining response for %s: ", response)
    return found_response


def backoff_handler(details):
    log.warning("Backing off {wait:0.1f} seconds afters {tries} tries "
                "calling function {target} with args {args} and kwargs "
                "{kwargs}".format(**details))


def dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        import collections

        if k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], collections.Mapping):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

    return dct
