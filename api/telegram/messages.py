WELCOME_MESSAGE = (
    "I'm *Akiko* and i use coinmarketcap API\n"
    "To get the coin price, send me its name or ticker."
    "(e.g. `Dogecoin` | `Doge`, `Bitcoin` | `BTC`)\n"
    "For more information about coin, enter `info` or `i`"
)


def display_error_message(type_error: str) -> str:
    """
    This function takes an error type and returns an appropriate message.

    """
    return {
        "session": "Session error! Enter coin (e.g. bitcoin, doge) (‾◡◝)",
        "match": r"Match error! ¯\_(ツ)_/¯",
        "unknown": "Sorry! Unknown error!  ( . .)",
    }[type_error]
