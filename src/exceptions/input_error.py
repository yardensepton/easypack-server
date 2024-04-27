class InputError(ValueError):
    def __init__(self,message):
        super().__init__(message)