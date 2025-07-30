import random

QUOTES = [
    "Keep calm and debug!",
    "You are one semicolon away from greatness.",
    "Code. Coffee. Conquer.",
    "Stack Overflow was not built in a day.",
    "Git push your limits!",
    "Even your bugs are proud of you.",
    "Code like a rockstar, debug like a detective.",
]

def get_random_quote():
    return random.choice(QUOTES)
