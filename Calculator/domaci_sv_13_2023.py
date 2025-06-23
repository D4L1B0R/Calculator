# OVE TRI METODE ĆE BITI POZIVANE KROZ AUTOMATSKE TESTOVE. NEMOJTE MENJATI NAZIV, PARAMETRE I POVRATNU VREDNOST.
#Dozvoljeno je implementirati dodatne, pomoćne metode, ali isključivo u okviru ovog modula.

from tokenizer import tokenize

class InfixToPostfixError(Exception):
    pass

class PostfixEvalError(Exception):
    pass

class Stek(object):
    def __init__(self):
        self._izlaz = []
        self._stek_sa_operatorima = []
        self._prioritet_operacija = {'_': 3,
                                     '^': 5,
                                     '*': 4,
                                     '/': 4,
                                     '+': 2,
                                     '-': 2,
                                     '(': 1}
        self._operacije = '+-*/^_'

    def je_operacija(self, token):
        return token in self._operacije

    def prioritet(self, op1, op2):
        return self._prioritet_operacija[op1] >= self._prioritet_operacija[op2]

    def dužina_izlaza(self):
        return len(self._izlaz)

    @property
    def stek_sa_operatorima(self):
        return self._stek_sa_operatorima

    @property
    def izlaz(self):
        return self._izlaz

    def poslednja_operacija_sa_steka(self):
        return self._stek_sa_operatorima[-1]

    def poslednja_vrednost_sa_izlaza(self):
        return self._izlaz[-1]

    def push_vrednosti(self, value):
        self._izlaz.append(value)

    def pop_vrednosti(self):
        return self._izlaz.pop()

    def push_operacije(self, value):
        self._stek_sa_operatorima.append(value)

    def pop_operacije(self):
        return self._stek_sa_operatorima.pop()

def infix_to_postfix(expression):

    tokens = tokenize(expression)
    obj = Stek()
    prošli_token = "?"
    if not tokens:
        raise InfixToPostfixError("Unet je prazan token!")
    for token in tokens:
        if token.isdigit():
            obj.push_vrednosti(int(token))
        elif token.replace(".", "", 1).isdigit():
            obj.push_vrednosti(float(token))
        elif token == "(":
            obj.push_operacije(token)
        elif token == ")":
            while obj.stek_sa_operatorima and obj.poslednja_operacija_sa_steka() != "(":
                obj.push_vrednosti(obj.pop_operacije())
            if not obj.stek_sa_operatorima:
                raise InfixToPostfixError("Nije pronadjena odgovarajuća otvorena zagrada!")
            obj.pop_operacije()
        elif obj.je_operacija(token):
            while (obj.stek_sa_operatorima and obj.poslednja_operacija_sa_steka() != "(" and obj.prioritet(obj.poslednja_operacija_sa_steka(), token)):
                if obj.je_operacija(token) and token != "_" and (obj.je_operacija(prošli_token) or prošli_token == "?" or prošli_token == "("):
                    raise InfixToPostfixError("Nevalidan izraz!")
                elif obj.dužina_izlaza() < 2 and token == "_":
                    raise InfixToPostfixError("Nevalidan izraz!")
                obj.push_vrednosti(obj.pop_operacije())
            obj.push_operacije(token)
        if token == "_" and obj.je_operacija(prošli_token):
            raise InfixToPostfixError("Nevalidan izraz!")
        if obj.je_operacija(token) and token != "_" and (obj.je_operacija(prošli_token) or prošli_token == "?" or prošli_token == "("):
            raise InfixToPostfixError("Nevalidan izraz!")
        prošli_token = token
    while obj.stek_sa_operatorima:
        if obj.poslednja_operacija_sa_steka() == "(":
            raise InfixToPostfixError("Nije pronadjena odgovarajuća zatvorena zagrada!")
        obj.push_vrednosti(obj.pop_operacije())
    return obj.izlaz

def calculate_postfix(token_list):
    """Funkcija izračunava vrednost izraza zapisanog u postfiksnoj notaciji

    Args:
        token_list (list): Lista tokena koja reprezentuje izraz koji se izračunava. Izraz može da sadrži cifre, zagrade,
         znakove računskih operacija.
        U slučaju da postoji problem sa brojem parametara, potrebno je baciti odgovarajući izuzetak.

    Returns:
        result: Broj koji reprezentuje konačnu vrednost izraza

    Primer:
        Ulaz [6.11, 74, 2, '*', '-'] se pretvara u izlaz -141.89
    """
    obj = Stek()
    for token in token_list:
        if str(token).isdigit():
            obj.push_vrednosti(int(token))
        elif str(token).replace(".", "", 1).isdigit():
            obj.push_vrednosti(float(token))
        elif token == "_":
            a = obj.pop_vrednosti()
            obj.push_vrednosti(-a)
        elif token in "+-*/^_":
            if obj.dužina_izlaza() < 2:
                raise PostfixEvalError("Nevalidan izraz!")
            b = obj.pop_vrednosti()
            a = obj.pop_vrednosti()
            if token == '+':
                obj.push_vrednosti(a + b)
            elif token == '-':
                obj.push_vrednosti(a - b)
            elif token == '*':
                obj.push_vrednosti(a * b)
            elif token == '/':
                if b == 0:
                    raise PostfixEvalError("Deljenje nulom nije dozvoljeno!")
                obj.push_vrednosti(a / b)
            elif token == '^':
                if a == 0 and b <= 0:
                    raise PostfixEvalError("Neispravan izraz, nije moguć njegov proračun!")
                if type(a**b) == complex:
                    raise PostfixEvalError("Nije moguće izvršiti proračun nad kompleksnim brojem!")
                obj.push_vrednosti(a ** b)
    if obj.dužina_izlaza() != 1:
        raise PostfixEvalError("Nevalidan izraz!")
    if obj.poslednja_vrednost_sa_izlaza() == int(obj.poslednja_vrednost_sa_izlaza()):
        return int(obj.pop_vrednosti())
    else:
        return obj.pop_vrednosti()

def calculate_infix(expression):
    """Funkcija izračunava vrednost izraza zapisanog u infiksnoj notaciji

    Args:
        expression (string): Izraz koji se parsira. Izraz može da sadrži cifre, zagrade, znakove računskih operacija.
        U slučaju da postoji problem sa formatom ili sadržajem izraza, potrebno je baciti odgovarajući izuzetak.

        U slučaju da postoji problem sa brojem parametara, potrebno je baciti odgovarajući izuzetak.
        

    Returns:
        result: Broj koji reprezentuje konačnu vrednost izraza

    Primer:
        Ulaz '' se pretvara u izlaz -141.89
    """
    postfix_izraz = infix_to_postfix(expression)
    rezultat = calculate_postfix(postfix_izraz)
    return rezultat