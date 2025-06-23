"""Modul omogućava parsiranje aritmetičkih izraza."""
import re


__author__ = 'mijicd'


REGEX = r'(?:\d*\.\d+)|(?:\d+)|(?:[()+\-\^/*])'

class ExpressionNotStringError(Exception):
    pass

class UnknownCharacterError(Exception):
    pass

def tokenize(expression):
    """Funkcija kreira tokene na osnovu zadatog izraza.

    Postupak formiranja liste tokena koristi regularni izraz
    zadat putem REGEX varijable. Omogućeno je pronalaženje
    sledećih tipova tokena:
        - floating-point vrednosti
        - celobrojne vrednosti
        - operatori +, -, *, /, ^
        - zagrade

    Args:
        expression (string): Izraz koji se parsira.

    Returns:
        list: Lista pronađenih tokena.

    Raises:
        AssertionError: Ako izraz nije zadat kao string.
    """
    if isinstance(expression, str):
        pass
    else:
        raise ExpressionNotStringError("Izraz mora biti tipa string.")
    tokens = re.findall(REGEX, expression)
    final_tokens = []
    for i, token in enumerate(tokens):
        if token == '-' and (i == 0 or tokens[i - 1] in ['(', '+', '-', '*', '/', '^']):
            final_tokens.append('_')
        else:
            final_tokens.append(token)
    if expression.replace(" ", "") != "".join(tokens):
        raise UnknownCharacterError("Izraz sadrži neprihvatljiv(e) krakter(e).")
    return final_tokens