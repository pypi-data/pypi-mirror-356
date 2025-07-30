import logging
from typing import Any, List

logger = logging.getLogger(__name__)


def remove_properties(obj: Any, properties_to_remove: List[str]) -> Any:
    """
    Recursively remove specified properties from a nested object (dict or list).

    :param obj: The object to process (dict or list).
    :param properties_to_remove: A list of property names (keys) to remove.
    :return: The modified object.
    """
    if isinstance(obj, dict):
        # Keys to remove from the current dictionary
        keys_in_obj = set(obj.keys())
        properties_set = set(properties_to_remove)
        keys_to_remove_from_current_obj = keys_in_obj & properties_set

        if keys_to_remove_from_current_obj:
            logger.debug(
                f"Removing properties: {', '.join(sorted(keys_to_remove_from_current_obj))}"
            )
            obj = {k: v for k, v in obj.items() if k not in properties_to_remove}

        # Recursively process values
        return {k: remove_properties(v, properties_to_remove) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [remove_properties(item, properties_to_remove) for item in obj]
    else:
        return obj
