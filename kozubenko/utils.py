import random, string

class Utils:
    def get_randomized_string(str_length):
        return ''.join(random.choices(string.ascii_letters,
                                      k=str_length))