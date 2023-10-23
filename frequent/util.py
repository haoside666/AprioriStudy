

def standard_str(obj):
    s = f'{obj.__class__}: \n'
    for attribute, value in obj.__dict__.items():
        s += f'\t {attribute}: {value}\n'
    return s

def standard_eq(obj1, obj2):
    if not obj1.__class__ == obj2.__class__:
        return False
    return vars(obj1) == vars(obj2)

def return_empty_list_if_none_else_itself(arg):
    if arg is None:
        return []
    else:
        return arg

def item_union(item1,item2):
    return sorted(list(set(item1 + item2)))

def list_add_item_not_order(item,item_list):
    if item not in item_list:
        item_list.append(item)

