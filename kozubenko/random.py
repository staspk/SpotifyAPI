import string, random


class Random():
    def string(len:int, of=string.ascii_letters+string.digits) -> str:
        """
        returns a randomized string
        """
        return ''.join(random.choices(of, k=len))