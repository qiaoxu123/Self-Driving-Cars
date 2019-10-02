class CUtils(object):
    def __init__(self):
        pass

    def create_var(self, var_name, value):
        if not var_name in self.__dict__:
            self.__dict__[var_name] = value
