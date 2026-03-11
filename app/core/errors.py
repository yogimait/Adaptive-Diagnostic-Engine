class AppException(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class SessionNotFound(AppException):
    def __init__(self, message="Session not found"):
        super().__init__(message, status_code=404)


class QuestionNotFound(AppException):
    def __init__(self, message="Question not found"):
        super().__init__(message, status_code=404)


class TestCompletedError(AppException):
    def __init__(self, message="Test is already completed. Cannot submit more answers."):
        super().__init__(message, status_code=400)


class ResultNotReadyError(AppException):
    def __init__(self, message="Test is not yet completed. Cannot retrieve results."):
        super().__init__(message, status_code=400)


class InvalidAnswerError(AppException):
    def __init__(self, message="Submitted answer is not one of the valid options."):
        super().__init__(message, status_code=400)
