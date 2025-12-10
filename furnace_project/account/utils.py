from .result_names import RESULT_NAMES

def convert_result_keys(result: dict) -> dict:
    mapping = RESULT_NAMES

    readable = {}
    for key, value in result.items():
        readable[mapping.get(key, key)] = value  # если нет в словаре — оставляем как есть

    return readable