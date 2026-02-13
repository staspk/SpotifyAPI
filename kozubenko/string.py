

def whitespace(amount:int) -> str:
    return " " * amount


class Str(str):

    def pad(self, amount:str, indent_size=2) -> str:
        string = ""
        for line in self.splitlines(keepends=True):
            string += whitespace(amount * indent_size) + line

        return string

    @staticmethod
    def From(items:list, separator="\n\n") -> str:
        """ Transforms list into a pretty string. """
        string = ""
        for item in items:
            string += f'{item}{separator}'

        return string[:-1]
