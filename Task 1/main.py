import string
from pprint import pprint
import collections


# Took from GitHubGist
#  User: angstwad
#  Function for merging nested dictionaries
def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def optimize_data(template, data):
    '''
    We will make new_data dictionary,and
    copy to it only data,that contains in
    template
    '''
    new_data = dict()
    # Parsing our template
    # Parser will return iterable object
    single_templates = string.Formatter().parse(template)
    for single_template in single_templates:
        # Data,that required in this template
        single_template_new_data = {}
        # Which data we need in this template
        target_keys = single_template[1]
        if target_keys is None:
            continue
        # Processing string to distinct names keys
        target_keys = target_keys.split('[')
        # Renmoving "[" from every splitted string
        target_keys = list(map(lambda string: string.strip(']'), target_keys))

        # Query to get reqired value from data
        # Query type would be such type
        # data["first_key"]["second_key"]...
        query_for_data = 'data' + (
            '["%s"]' * len(target_keys)
            ) % tuple(target_keys)
        query_result = eval(query_for_data)

        # Appending query result (value of this keys) to target_keys
        target_keys.append(query_result)
        target_keys = tuple(target_keys)

        # Query to add this data to new dictionary
        # Query would be such type:
        # new_data[first_key] = {second_key :{... :{last_key:query_result}}}
        query_for_new_data = (
            'single_template_new_data["%s"] = ' +
            # Our keys
            '{"%s":' * (len(target_keys) - 2) +
            # Query result
            '"%s"' +
            # Closing brackets
            '}' * (len(target_keys) - 2)
            ) % target_keys
        exec(query_for_new_data)

        # Appending data from this single template
        dict_merge(new_data, single_template_new_data)

    return new_data


def main():
    template = 'Python version: {languages[python][latest_version]}'
    template += '\nPython site: {languages[python][site]}'
    data = {
        'languages': {
            'python': {
                'latest_version': '3.6',
                'site': 'http://python.org',
            },
            'rust': {
                'latest_version': '1.17',
                'site': 'https://rust-lang.org',
            },
        },
    }
    print("Original data:")
    pprint(data)

    new_data = optimize_data(template, data)
    print("Optimized data:")
    pprint(new_data)


if __name__ == '__main__':
    main()
