class TakeoffException(Exception):
    """The takeoff error class"""

    def __init__(self, status_code: int, message: str, *args, **kwargs):
        """Create a new takeoff error

        Args:
            status_code (int): the http status code (from the takeoff server) that triggered the error
            message (str): the string message describing the error
        """
        super().__init__(message, *args, **kwargs)
        self.status_code = status_code
