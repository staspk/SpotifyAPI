
class Utils:
    
    def list_to_str(_list:list[str], char_separator = " "):
        """
        `list_to_str(['a', 'b', 'c'], ';') -> "a;b;c"`
        """
        return char_separator.join(_list)
    

def assert_list(var_name:str, _list:list, min_len:int=None, max_len:int=None, returnBool=False):
    """
    Use to enforce type annotations. Raises Exception, unless `returnBool=True`:
    * if _list is not a list
    * len(_list) < min_len (*optional*)
    * len(_list) > max_len (*optional*)
    * returnBool (*optional*)
    """
    if not returnBool:    
        if not isinstance(_list, list):
            raise Exception(f"assert_list({var_name}): must be a list, not: {type(_list)}")
        if(min_len) and len(_list) < min_len:
            raise Exception(f"assert_list({var_name}): length of list under min_len: {min_len}")
        if(max_len) and len(_list) > max_len:
            raise Exception(f"assert_list({var_name}): length of list exceeds max_len: {max_len}")
    else:
        if not isinstance(_list, list):
            return False
        if min_len is not None and len(_list) < min_len:
            return False
        if max_len is not None and len(_list) > max_len:
            return False
        return True