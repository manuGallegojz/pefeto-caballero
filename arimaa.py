from definiciones import *

#### Algunas funciones ya dadas

def son_posiciones_vecinas(pos1 : Posicion, pos2 : Posicion) -> bool: # pragma: no cover
    return (pos1.fila == pos2.fila and abs(pos1.columna - pos2.columna) == 1) \
        or (pos1.columna == pos2.columna and abs(pos1.fila - pos2.fila) == 1)

def direccion_desde_hasta(pos1 : Posicion, pos2 : Posicion) -> Direccion: # pragma: no cover
    assert son_posiciones_vecinas(pos1, pos2)
    if pos1.fila < pos2.fila:
       return NORTE
    elif pos1.fila > pos2.fila:
       return SUR
    elif pos1.columna < pos2.columna:
       return ESTE
    else:
       return OESTE

def pasar_turno(j : Juego) -> Juego: # pragma: no cover
    return Juego(j.tablero, oponente(j.turno), 0)

#auxiliares

def hay_figura_de_color(t : Tablero, pos : Posicion, f : Figura, col : Color) -> bool:
    return not hay_casilla_vacia(t, pos) and t[pos.fila][pos.columna].figura == f and t[pos.fila][pos.columna].color == col

#### Ejercicio 1

def tablero_bien_formado(t: Tablero) -> bool:

    """
    Indica si el tablero tiene las dimensiones correctas.

    PRE: True

    Args:
        t (Tablero): El tablero que se quiere verificar.

    Returns:
        True si el tablero tiene ALTO filas y cada fila tiene ANCHO columnas, y False si no.
    """

    res :bool = len(t) == ALTO
    for fila in t:
        if len(fila) != ANCHO:
            res = False
    return res

def posicion_en_tablero(pos : Posicion) -> bool:
    """
    Indica si una posición pertenece al tablero.

    PRE: True

    Args:
        pos (Posicion): La posición que se quiere verificar.

    Returns:
        True si la fila y la columna de la posición están dentro de los límites del tablero, y False si no.
    """
        
    return 0 <= pos.fila < ALTO and 0 <= pos.columna < ANCHO

def movimiento_bien_formado(m : Movimiento) -> bool:
    """
    Indica si un movimiento está bien formado.

    PRE: True

    Args:
        m (Movimiento): El movimiento que se quiere verificar.

    Returns:
        True si el origen del movimiento está dentro del tablero y la acción tiene una cantidad válida de pasos, y False si no.
    """
        
    accion_1_valida : bool = m.accion == MOVER_A_SECAS and len(m.pasos) == 1
    accion_2_valida : bool = (m.accion == ARRASTRAR or m.accion == EMPUJAR) and len(m.pasos) == 2 

    return posicion_en_tablero(m.origen) and (accion_1_valida or accion_2_valida)

def juego_bien_formado(j : Juego) -> bool:
    """
    Indica si el juego está bien formado.

    PRE: True

    Args:
        j (Juego): El juego que se quiere verificar.

    Returns:
        True si el tablero del juego está bien formado y la cantidad de pasos consumidos está entre 0 y MAX_PASOS - 1, y False si no.
    """
        
    return tablero_bien_formado(j.tablero) and (0 <= j.pasos_consumidos < MAX_PASOS)

#Ejercicio 2

def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
    """
    Devuelve la posición vecina a *pos* en la dirección *d*.

    PRE: True
    Args:
        pos (Posicion): La posición desde la cual se busca la vecina.
        d (Direccion): La dirección en la que se busca la posición vecina.
    Returns:
        La posición vecina a *pos* en la dirección *d*.
    """
    fila : int = pos.fila
    columna : int = pos.columna

    if d == NORTE:
        fila += 1
    elif d == SUR:
        fila -= 1
    elif d == ESTE:
        columna += 1
    elif d == OESTE:
        columna -= 1
    
    return Posicion(fila, columna)

def casilla_en_posicion(t : Tablero, p : Posicion) -> Casilla:
    """
    Devuelve la casilla del tablero *t* ubicada en la posición *p*.

    PRE: True
    Args:
        t (Tablero): El tablero en el que se busca la casilla.
        p (Posicion): La posición de la casilla que se quiere obtener.
    Returns:
        La casilla del tablero *t* ubicada en la posición *p*.
    """
    return t[p.fila][p.columna]

def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si la posición pos del tablero t contiene una casilla vacía.

    PRE: True
    Args:
    t (Tablero): El tablero en el que se verifica si la casilla está vacía.
    pos (Posicion): La posición de la casilla que se quiere verificar.
    Returns:
    True si pos está dentro del tablero y la casilla correspondiente está vacía, y False si no.
    """
    return posicion_en_tablero(pos) and t[pos.fila][pos.columna] == VACIA

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    """
    devuelve True si en la casilla de la posición pos hay una pieza de determinado color col

    PRE: True
    Args:
        t (Tablero): El tablero en el que se verifica la presencia de la pieza.
        pos (Posicion): La posición de la casilla que se quiere verificar.
        col (Color): El color de la pieza que se busca.
    Returns:
        True si *pos* está dentro del tablero, la casilla no está vacía y la pieza es del color *col*, y False en caso contrario.

    """
    pieza:(Pieza | CasillaVacia) = t[pos.fila][pos.columna]

    return posicion_en_tablero(pos) and (not hay_casilla_vacia(t, pos)) and pieza.color == col
    
#### Ejercicio 3

def hay_pieza_enemiga_mas_fuerte_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    devuelve True si hay una pieza enemiga más fuerte a la que está en la posición pos en dirección d , en cualquier otro caso devuelve False
    PRE: True
    Args:
        t (Tablero): El tablero en el que se verifica la presencia de la pieza enemiga.
        pos (Posicion): La posición de la pieza a comparar.
        d (Direccion): La dirección en la que se busca la pieza enemiga.
    Returns:
        True si en la posición vecina hacia *d* hay una pieza enemiga más fuerte que la ubicada en *pos*, y False en cualquier otro caso.
    """
    pieza : (Pieza | CasillaVacia) = t[pos.fila][pos.columna]
    pos2 : Posicion = posicion_vecina_hacia(pos, d)
    
    if not posicion_en_tablero(pos2):
        return False

    pieza2 : (Pieza | CasillaVacia) = t[pos2.fila][pos2.columna]
    return pieza != VACIA and pieza2 != VACIA and hay_pieza_de_color(t, pos2, oponente(pieza.color)) and fuerza(pieza2.figura) > fuerza(pieza.figura)


def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Devuelve True si la casilla en determinada dirección d desde una posicion pos está vacía. No modifica los valores de entrada.

    PRE: True
    Args:
        t (Tablero): El tablero en el que se verifica si la casilla está vacía.
        pos (Posicion): La posición desde la que se busca la casilla vecina.
        d (Direccion): La dirección en la que se busca la casilla.
    Returns:
        True si la posición vecina hacia la dirección indicada está dentro del tablero y su casilla está vacía, y False en caso contrario.
    """
    posicion2 = posicion_vecina_hacia(pos, d)
    return posicion_en_tablero(posicion2) and t[posicion2.fila][posicion2.columna] == VACIA

def hay_pieza_amiga_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Devuelve el resultado booleano de ver si hay o no una ficha vecina del mismo color.
    PRE: True
    Args:
        t(Tablero): El tablero donde se evaluará la busqueda.
        pos(Posicion): Posicion del tablero en el que se analizan los vecinos para ver los colores.
        d(Direccion): Hacia donde se quiere ver el mismo color.
    Returns:
        True si es el mismo color, la posicion de la ficha esta dentro del tablero en juego y no es una casilla vacia.
    """
    if hay_casilla_vacia(t,pos):
        return False
    
    color : Color = t[pos.fila][pos.columna].color
    pos2 : Posicion = posicion_vecina_hacia(pos, d)

    return (posicion_en_tablero(pos2) and not hay_casilla_vacia(t, pos2)) and t[pos2.fila][pos2.columna].color == color

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si hay una pieza amiga en alguna casilla vecina. No modifica los valores de entrada.

    PRE: True
    Args:
        t (Tablero): El tablero en el que se buscan piezas amigas.
        pos (Posicion): La posición a partir de la cual se buscan casillas vecinas.
    Returns:
        True si hay una pieza amiga en alguna de las casillas vecinas a pos, y False en caso contrario.
    """
    return (hay_pieza_amiga_hacia(t, pos, NORTE) or
            hay_pieza_amiga_hacia(t, pos, SUR) or
            hay_pieza_amiga_hacia(t, pos, ESTE) or
            hay_pieza_amiga_hacia(t, pos, OESTE))

def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Devuelve True si hay una pieza enemiga más débil que la ubicada en la posición pos, en determinada dirección d, y False en cualquier otro caso. No modifica los valores de entrada.

    PRE: True
    Args:
        t (Tablero): El tablero en el que se busca la pieza enemiga.
        pos (Posicion): La posición de la pieza que se quiere comparar.
        d (Direccion): La dirección en la que se busca la pieza enemiga.
    Returns:
        True si en la posición vecina hacia la dirección indicada hay una pieza enemiga más débil que la ubicada en pos, y False en caso contrario.
    """
    pieza : (Pieza | CasillaVacia) = t[pos.fila][pos.columna]
    pos2 : Posicion = posicion_vecina_hacia(pos, d)

    if not posicion_en_tablero(pos2):
        return False

    pieza2 : (Pieza | CasillaVacia) = t[pos2.fila][pos2.columna] 
    return pieza != VACIA and pieza2 != VACIA and hay_pieza_de_color(t, pos2, oponente(pieza.color)) and fuerza(pieza2.figura) < fuerza(pieza.figura)

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    """
    Devuelve True si hay una pieza enemiga más fuerte en alguna casilla vecina a la casilla con posicion pos, y False en cualquier otro caso. No modifica los valores de entrada.

    PRE: True
    Args:
        t (Tablero): El tablero en el que se buscan piezas enemigas.
        pos (Posicion): La posición a partir de la cual se buscan casillas vecinas.
    Returns:
        True si hay una pieza enemiga más fuerte en alguna de las casillas vecinas a pos, y False en caso contrario.
    """
    return (hay_pieza_enemiga_mas_fuerte_hacia(t, pos, NORTE) or
            hay_pieza_enemiga_mas_fuerte_hacia(t, pos, SUR) or
            hay_pieza_enemiga_mas_fuerte_hacia(t, pos, ESTE) or
            hay_pieza_enemiga_mas_fuerte_hacia(t, pos, OESTE))
            

def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    """
    Analiza si la pieza no tiene posibilidad de movimiento hacia los costados SUR, ESTE, OESTE o NORTE.

    PRE:  tablero_bien_formado (t) ∧ posicionEnTablero (pos)
    Args:
        t(Tablero): El tablero en el que se evaluaran las posiciones alrededor de pos.
        pos(Posicion): la posicion donde se ubica mi ficha.
    Returns:
        True si esta al lado de una pieza mas fuerte que no puede empujar y no hay una ficha del mismo color.
    """
    
    return hay_pieza_enemiga_mas_fuerte_vecina(t,pos) and not hay_pieza_amiga_vecina(t,pos)

#Ejercicio 4

def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    """
    evalúa si puede hacer un movimiento, al analizar las siguientes condiciones:
    > Si el color de la pieza es el color correspondiente al jugador.
    > Si no está congelada, es decir, tiene posibilidad de moverse.
    > tiene posibilidad de moverse en la direccion del movimiento propuesta.
    > los pasos consumidos hasta el momento en el juego mas los que va a hacer (en la cantidad de cosas que quiere hacer en movimiento) no excede los pasos maximos que tiene permitido el jugador
    > si la jugada que se quiere hacer realmente es posible (analisis de mover a secas, arrastrar o empujar).
    PRE: juego_bien_formado (j) ∧ movimiento_bien_formado (m)
    Args: 
        j(Juego): Tripla del estado del tablero, el color de jugador y los pasos que se hicieron.
        m(Movimiento): La posicion que se quiere mover y la dirección.
    Returns:
        True si se puede asegurar todas las condiciones expuestas.
    """
    return hay_pieza_de_color(j.tablero, m.origen, j.turno) and not hay_pieza_congelada(j.tablero, m.origen) and direccion_de_movimiento_habilitada(j.tablero, m.origen, m.pasos[0]) and j.pasos_consumidos + len(m.pasos) <= MAX_PASOS and puede_realizar_accion(j.tablero, m)

def direccion_de_movimiento_habilitada(t: Tablero, pos: Posicion, d: Direccion) -> bool:
    pieza: (Pieza | CasillaVacia) = t[pos.fila][pos.columna]
    res:bool = True

    if pieza.figura == CONEJO and pieza.color == DORADO:
        res = d != SUR

    elif pieza.figura == CONEJO and pieza.color == PLATEADO:
        res = d != NORTE

    return res

def puede_realizar_accion(t : Tablero, m : Movimiento) -> bool:
    """
    Dependiendo la accion que se quiera hacer, se desea averiguar si es realmente posible llevar a cabo.
    PRE:
        tablero_bien_formado(t) y movimiento_bien_formado (m) 
    Args:
        t(Tablero): donde se evalúa el movimiento:
        m(Movimiento): Contiene la accion que se quiere llevar a cabo, la posicion donde esta ubicado y la lista de movimientos
    Returns:
        True si cumple las condiciones para la accion que quiere hacer el usuario.
    """
    res = False
    
    if m.accion == MOVER_A_SECAS:
        res = hay_casilla_vacia_hacia(t, m.origen, m.pasos[0])
    elif m.accion == ARRASTRAR:
        res = hay_casilla_vacia_hacia(t, m.origen, m.pasos[0]) and hay_pieza_enemiga_mas_debil_hacia(t, m.origen, opuesta(m.pasos[1]))
    elif m.accion == EMPUJAR: 
        pos_enemiga = posicion_vecina_hacia(
            m.origen, m.pasos[0]
        )
        res = hay_pieza_enemiga_mas_debil_hacia(t, m.origen, m.pasos[0]) and hay_casilla_vacia_hacia(t, pos_enemiga, m.pasos[1])
    
    return res

#### Ejercicio 5

def activar_trampas(t : Tablero) -> Tablero:
    """
    Busca en las posiciones trampa hacer vacias las fichas(en caso de que las haya) si es que no tienen amigas vecinas.
    PRE: tablero_bien_formado (t)
    Args:
        t(Tablero): es el tablero que hay en juego para ver en las posiciones trampa que fichas hay y evaluar la respectiva transformacion a VACIA.
    Returns:
        Copia del tablero pasado como arg pero habiendo transformado a VACIA las posiciones trampa en caso de necesitar activar las trampas.
    """
    res = []
    for fila in t:
        res.append(fila.copy())

    for pos in POSICIONES_TRAMPA:
        if not hay_pieza_amiga_vecina(res, pos):
            res[pos.fila][pos.columna] = VACIA

    return res

### Ejercicio 6

def nuevoT(t: Tablero) -> Tablero:
    """
    Copia el tablero para generar uno nuevo.
    PRE: tablero_bien_formado(t)
    Args:
        t(Tablero): el tablero a copiar.
    Returns:
        El tablero duplicado.
    """
    res : Tablero = []
    for fila in t:
        res.append(fila.copy())
    return res

def moverSecas(j:Juego, movimiento: Movimiento) -> Tablero:
    """
        Se realiza un movimiento a una casilla vacia.
        PRE: juego_bien_formado (j) y movimiento_bien_formado (m)
        Args:
            j(Juego): Tripla con el tablero que tiene el jugador enfrente.
            m(Movimiento): El movimiento con los pasos que quiere hacer el jugador
        Returns:
            El tablero final con el movimiento hecho.
    """
    posOriginal:Posicion = movimiento.origen
    tableroCopia:Tablero = nuevoT(j.tablero)
    posDestino:Posicion = posicion_vecina_hacia(posOriginal, movimiento.pasos[0])
    tableroCopia[posDestino.fila][posDestino.columna] = j.tablero[posOriginal.fila][posOriginal.columna]
    tableroCopia[posOriginal.fila][posOriginal.columna] = VACIA
    return tableroCopia

def moverArrastre(j:Juego, movimiento:Movimiento) -> Tablero:
    """
        Se realiza un movimiento a una casilla donde esta la ficha contraria y se desplaza la ficha contraria a un sitio del movimiento en pasos[1].
        PRE: juego_bien_formado (j) y movimiento_bien_formado (m)
        Args:
            j(Juego): Tripla con el tablero que tiene el jugador enfrente.
            m(Movimiento): El movimiento con los pasos que quiere hacer el jugador (en este caso seran 2 a donde quiero ir en el sitio contrincante y donde el contrincante mueve su fi).
        Returns:
           El tablero final con el movimiento hecho.
    """
    posOriginal:Posicion = movimiento.origen
    tableroCopia:Tablero = nuevoT(j.tablero)
    posDestino:Posicion = posicion_vecina_hacia(posOriginal, movimiento.pasos[0])
    posContrario:Posicion = posicion_vecina_hacia(posOriginal, opuesta(movimiento.pasos[1]))
    tableroCopia[posDestino.fila][posDestino.columna] = j.tablero[posOriginal.fila][posOriginal.columna]
    tableroCopia[posOriginal.fila][posOriginal.columna] = j.tablero[posContrario.fila][posContrario.columna]
    tableroCopia[posContrario.fila][posContrario.columna] = VACIA
    return tableroCopia

def moverEmpuje(j:Juego, movimiento:Movimiento) -> Tablero:
    """
        Se realiza un movimiento a una casilla vacia y se arrastra a una pieza mas debil.
        PRE: juego_bien_formado (j) y movimiento_bien_formado (m)
        Args:
            j(Juego): Tripla con el tablero que tiene el jugador enfrente.
            m(Movimiento): El movimiento con los pasos que quiere hacer el jugador (en este caso seran 2 a donde quiero ir y como quiero arrastrar la ficha contraria).
        Returns:
           El tablero final con el movimiento hecho.
    """    
    posOriginal:Posicion = movimiento.origen
    tableroCopia:Tablero = nuevoT(j.tablero)
    posDestino:Posicion = posicion_vecina_hacia(posOriginal, movimiento.pasos[0])
    posContrario:Posicion = posicion_vecina_hacia(posDestino, movimiento.pasos[1])
    tableroCopia[posContrario.fila][posContrario.columna]  = j.tablero[posDestino.fila][posDestino.columna]
    tableroCopia[posDestino.fila][posDestino.columna]  = j.tablero[posOriginal.fila][posOriginal.columna]
    tableroCopia[posOriginal.fila][posOriginal.columna] = VACIA
    return tableroCopia

# al realizar el movimiento
def realizacionDeMovimiento(juegoInicial:Juego, mov: Movimiento) -> Juego:
    """
        Segun la accion que quiere hacer el user, se lleva a cabo la funcion de movimiento.
        PRE: juego_bien_formado (j) y movimiento_bien_formado (m)
        Args:
            j(Juego): Tripla con el tablero que tiene el jugador enfrente, el color y los pasos hechos.
            m(Movimiento): El movimiento con los pasos que quiere hacer el jugador.
        Returns:
           El juego final nuevo con el tablero modificado tras el movimiento realizado, con los mismos datos que el juego inicial en tanto a color y pasos hechos.
    """
    if mov.accion == MOVER_A_SECAS:
        tableroNuevo : Tablero = moverSecas(juegoInicial,mov)
    elif mov.accion == ARRASTRAR:
        tableroNuevo = moverArrastre(juegoInicial,mov)
    elif mov.accion == EMPUJAR:
        tableroNuevo = moverEmpuje(juegoInicial,mov)
    return Juego(
            tableroNuevo,
            juegoInicial.turno,
            juegoInicial.pasos_consumidos
    )

#efectúa las trampas y devuelve el juego con tablero a la trampa aplicada
def efectuandoTrampas(juegoInicial:Juego, mov: Movimiento) -> Juego:
    """
        En el tablero del juego se busca hacer una copia de este y efectuar las trampas en las posiciones correspondientes.
        PRE: juego_bien_formado (j) y movimiento_bien_formado (m)
        Args:
            j(Juego): Tripla con el tablero que tiene el jugador enfrente, el color y los pasos hechos.
            m(Movimiento): El movimiento con los pasos que quiere hacer el jugador.
        Returns:
           El juego nuevo con el tablero final.
    """
    juegoI : Juego = realizacionDeMovimiento(juegoInicial, mov)

    return Juego(
        activar_trampas(juegoI.tablero),
        juegoI.turno,
        juegoI.pasos_consumidos
    )

def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    """
    Devuelve el color del jugador oponente al indicado.

    PRE: col == DORADO ∨ col == PLATEADO

    Args:
        col (Color): Color del jugador.

    Returns:
        El color del jugador oponente.
    """
    nuevoJ : Juego = Juego(nuevoT(j.tablero), j.turno, j.pasos_consumidos)

    nuevoJ = efectuandoTrampas(nuevoJ, m)

    nuevoJ = Juego(
        nuevoJ.tablero,
        nuevoJ.turno,
        nuevoJ.pasos_consumidos + len(m.pasos)
    )

    if nuevoJ.pasos_consumidos == MAX_PASOS:
        nuevoJ = pasar_turno(nuevoJ)

    return nuevoJ

#### Ejercicio 7

#funciones auxiliares

def oponente_color(col : Color) -> Color:
    """
    Busca si hay un conejo del color indicado en la fila inicial del jugador oponente.

    PRE: juego_bien_formado(j) y (col == DORADO o col == PLATEADO)

    Args:
        j (Juego): Juego en el que se busca el conejo.
        col (Color): Color del conejo que se busca.

    Returns:
        True si hay un conejo del color indicado en la fila inicial del oponente, False en caso contrario.
    """
    
    oponente = DORADO

    if col == DORADO:
        oponente = PLATEADO

    return oponente

def hay_conejo_en_fila_inicial_oponente(j : Juego, col : Color):
    """
    Busca si hay un conejo del color indicado en el tablero.

    PRE: juego_bien_formado(j) y (col == DORADO o col == PLATEADO)

    Args:
        j (Juego): Juego cuyo tablero se analiza.
        col (Color): Color del conejo que se busca.

    Returns:
        True si hay al menos un conejo del color indicado en el tablero, False en caso contrario.
    """

    res = False
    oponente = oponente_color(col)

    posicion_fila_inicial = 0
    
    if oponente == PLATEADO:
        posicion_fila_inicial = 7

    for i in range(ANCHO):
        if hay_figura_de_color(j.tablero, Posicion(posicion_fila_inicial, i), CONEJO, col):
            res = True

    return res

def hay_conejo_en_tablero(j : Juego, col : Color):
    """
    Determina si el jugador del color indicado cumple alguna de las
    condiciones para ganar el juego.

    PRE: juego_bien_formado(j) y (col == DORADO o col == PLATEADO)

    Args:
        j (Juego): Juego en el que se evalúan las condiciones de victoria.
        col (Color): Color del jugador que se evalúa.

    Returns:
        True si el jugador cumple alguna condición de victoria, False en caso contrario.
    """

    res = False

    for x in range(ALTO):
        for y in range(ANCHO):
            casilla : Casilla = j.tablero[x][y]
            if casilla != VACIA and casilla.figura == CONEJO and casilla.color == col:
                res = True
    
    return res

def reune_condiciones_de_ganar(j : Juego, col : Color):
    """
    Determina si el jugador cumple las condiciones de victoria
    y su oponente no cumple esas mismas condiciones.

    PRE: juego_bien_formado(j) y (col == DORADO o col == PLATEADO)

    Args:
        j (Juego): Juego en el que se evalúan las condiciones de victoria.
        col (Color): Color del jugador que se evalúa.

    Returns:
        True si el jugador cumple las condiciones de victoria de forma exclusiva, False en caso contrario.
    """
    
    return hay_conejo_en_fila_inicial_oponente(j, col) or not hay_conejo_en_tablero(j, oponente_color(col))

def reune_condiciones_de_ganar_exclusivas(j : Juego, col : Color):
    return reune_condiciones_de_ganar(j, col) and not reune_condiciones_de_ganar(j, oponente_color(col))

def es_inicio_de_turno(j: Juego, col : Color):
    """
    Determina si el juego está al inicio del turno del jugador indicado.

    PRE: juego_bien_formado(j) y (col == DORADO o col == PLATEADO)

    Args:
        j (Juego): Juego cuyo turno se analiza.
        col (Color): Color del jugador que se evalúa.

    Returns:
        True si es el inicio del turno del jugador indicado, False en caso contrario.
    """

    return j.turno == col and j.pasos_consumidos == 0

def es_jugador_ganador(j : Juego, col : Color) -> bool:
    """
    Determina si el jugador del color indicado es ganador del juego.

    PRE: juego_bien_formado(j) y (col == DORADO o col == PLATEADO)

    Args:
        j (Juego): Juego en el que se determina al ganador.
        col (Color): Color del jugador que se evalúa.

    Returns:
        True si el jugador indicado es ganador, False en caso contrario.
    """

    oponente = oponente_color(col)
    return (es_inicio_de_turno(j, oponente) and reune_condiciones_de_ganar(j, col)) or (es_inicio_de_turno(j, col) and reune_condiciones_de_ganar_exclusivas(j, col))

# funciones del ejercicio

def hay_ganador_determinado(j : Juego) -> bool:
    """
    Determina si existe un ganador en el estado actual del juego.

    PRE: juego_bien_formado(j)

    Args:
        j (Juego): Juego en el que se busca determinar si hay ganador.

    Returns:
        True si alguno de los jugadores es ganador, False en caso contrario.
    """

    return es_jugador_ganador(j, PLATEADO) or es_jugador_ganador(j, DORADO)

def ganador_del_juego(j: Juego) -> ( Color | None ):
    """
    Determina el ganador del juego, si existe uno único.

    PRE: juego_bien_formado(j)

    Args:
        j (Juego): Juego cuyo ganador se quiere determinar.

    Returns:
        El color del jugador ganador si existe uno único; None si no hay ganador o ambos jugadores figuran como ganadores.
    """

    gana_plateado = es_jugador_ganador(j, PLATEADO)
    gana_dorado = es_jugador_ganador(j, DORADO)

    if gana_plateado:
        return PLATEADO
    
    if gana_dorado:
        return DORADO

    return None