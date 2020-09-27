class OperationError(Exception):
    def __init__(self, what):
        super().__init__(what)