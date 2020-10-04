from django.core.exceptions import SuspiciousOperation


class ImmutableUserError(SuspiciousOperation):
    """the user tried to modify immutable user"""


class UnmatchedPkError(SuspiciousOperation):
    """
    The user tried to user different primary key for modify different account.
    i.e.: The user tried to modify the primary key inside the html form in the browser
    """
