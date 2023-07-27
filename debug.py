
debug=True

def alert(message):
    print('\033[33m'+message+'\033[0;0m')
def error(message):
    print('\033[32m'+message+'\033[0;0m')
def debug(message):
    if debug is True:
        print('\033[33m'+message+'\033[0;0m')
def formulas(message):
    print('\033[35m'+message+'\033[0;0m')
def mostrar(nome, dados):
    if dados is not None and dados !='' and dados !=0:
        print(nome+': '+str(dados))
