import hashlib
import json

def hash_obj(obj):
    """
    Compute a hash for a given object (dict, list, tuple, str).
    
    :param obj: Object to hash.
    :return: Hash string.
    """
    try:
        obj_str = json.dumps(obj, sort_keys=True)  # Ensure deterministic serialization
    except TypeError:
        obj_str = str(obj)  # Fallback for non-serializable objects
    return hashlib.md5(obj_str.encode()).hexdigest()


def is_same(obj1, obj2):
    """
    Compare two objects (dict, list, tuple, str) using a hash function.
    
    :param obj1: First object.
    :param obj2: Second object.
    :return: True if objects are the same, False otherwise.
    """
    return hash_obj(obj1) == hash_obj(obj2)


def unique_objects(obj_list, return_idx=False):
    """
    Get the unique set of objects from a list, where objects can be dict, list, tuple, or str.
    
    :param obj_list: List of objects.
    :return: List of unique objects, maintaining order.
    """
    seen_hashes = set()
    unique_list = []
    idx_lst = []
    
    for idx, obj in enumerate(obj_list):
        obj_hash = hash_obj(obj)
        
        if obj_hash not in seen_hashes:
            seen_hashes.add(obj_hash)
            unique_list.append(obj)
            idx_lst.append(idx)

    if return_idx:
        return unique_list, idx_lst
    return unique_list


if __name__ == "__main__":
    data = [
        {"a": 1, "b": {"a": 1, "b": "c"}},
        {"a": 1, "b": [2, 3]},
        {"b": [2, 3], "a": 1},  # Same as first dict (order does not matter)
        [1, 2, 3],
        [1, 2, 3],  # Duplicate list
        (4, 5),
        (4, 5),  # Duplicate tuple
        "hello",
        "hello"  # Duplicate string
    ]

    unique_data = unique_objects(data)
    print(unique_data)
