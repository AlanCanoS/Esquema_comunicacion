
class NodoHuffman:
    def __init__(self, simbolo=None, probabilidad=None, izquierda=None, derecha=None):
        self.simbolo = simbolo
        self.probabilidad = probabilidad
        self.izquierda = izquierda
        self.derecha = derecha

def construir_arbol(simbolos_probabilidades):
    nodos = [NodoHuffman(simbolo=s, probabilidad=p) for s, p in simbolos_probabilidades.items()]

    while len(nodos) > 1:
        nodos.sort(key=lambda x: x.probabilidad)
        izquierda = nodos.pop(0)
        derecha = nodos.pop(0)
        nuevo_nodo = NodoHuffman(probabilidad=izquierda.probabilidad + derecha.probabilidad, izquierda=izquierda, derecha=derecha)
        nodos.append(nuevo_nodo)

    return nodos[0]

def generar_codificacion(arbol, codigo_actual="", codificacion={}):
    if arbol.simbolo is not None:
        codificacion[arbol.simbolo] = codigo_actual
    if arbol.izquierda is not None:
        generar_codificacion(arbol.izquierda, codigo_actual + "0", codificacion)
    if arbol.derecha is not None:
        generar_codificacion(arbol.derecha, codigo_actual + "1", codificacion)

def huffman(simbolos_probabilidades):
    arbol_huffman = construir_arbol(simbolos_probabilidades)
    codificacion = {}
    generar_codificacion(arbol_huffman, "", codificacion)
    return codificacion