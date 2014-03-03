"""
Configuration class
"""


class Config:
    """
    Config class contains all but fields containing the app conf
    """
    SIGNUP_REQUIRES_CONFIRMATION = False
    # A timestamp for validity
    TOKEN_VALIDITY = 3600
