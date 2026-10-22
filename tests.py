import unittest
from arimaa import *

# Las piezas se representan con las siguientes letras:
#   E : elefante
#   M : camello
#   H : caballo
#   D : perro
#   C : gato
#   R : ratón
# donde
#   mayúscula : dorado
#   minúscula : plateado

def tablero_8x8_vacio():
    return leer_tablero([
              '--------', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              '--------', #1
              '--------', #0
              #01234567
            ])

def tablero_8x8_inicial_ejemplo():
    return leer_tablero([
              'hcdmedch', #7
              'rrrrrrrr', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              'RRRRRRRR', #1
              'HCDMEDCH', #0
              #01234567
            ])

#### Ejercicio 1

class test_tablero_bien_formado(unittest.TestCase):

    def test_8x8_lleno(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(tablero_bien_formado(t))

    def test_tablero_mal_formado_cantidad_filas(self):
        t = leer_tablero([
            'hcdmedch',
            'rrrrrrrr',
            '--------',
            '--------',
            'RRRRRRRR', 
            'HCDMEDCH'
        ])
        self.assertFalse(tablero_bien_formado(t))
        
    def test_tablero_mal_formado_columnas(self):
        t = leer_tablero([
              'hcdmedc', #7
              'rrrrrrr', #6
              '-------', #5
              '-------', #4
              '-------', #3
              '-------', #2
              'RRRRRRR', #1
              'HCDMEDCH', #0 
              #01234567
            ])
        self.assertFalse(tablero_bien_formado(t))

class test_posicion_en_tablero(unittest.TestCase):

    def test_posicion_ok(self):
        self.assertTrue(posicion_en_tablero(Posicion(5, 3)))

class test_movimiento_bien_formado(unittest.TestCase):
    def test_mover_a_secas_valido(self):
        m = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertTrue(movimiento_bien_formado(m))

    def test_arrastrar_valido(self):
        m = Movimiento(ARRASTRAR, Posicion(3, 4), [NORTE, ESTE])
        self.assertTrue(movimiento_bien_formado(m))

    def test_empujar_valido(self):
        m = Movimiento(EMPUJAR, Posicion(5, 2), [NORTE, OESTE])
        self.assertTrue(movimiento_bien_formado(m))

    def test_mover_a_secas_dos_pasos(self):
        m = Movimiento(MOVER_A_SECAS, Posicion(3, 1), [SUR, OESTE])
        self.assertFalse(movimiento_bien_formado(m))

    def test_mover_a_secas_sin_pasos(self):
        m = Movimiento(MOVER_A_SECAS, Posicion(3, 1), [])
        self.assertFalse(movimiento_bien_formado(m))

    def test_mover_fuera_del_tablero(self):
        m = Movimiento(MOVER_A_SECAS, Posicion(9, 8), [NORTE])
        self.assertFalse(movimiento_bien_formado(m))

    def test_arrastrar_un_paso(self):
        m = Movimiento(ARRASTRAR, Posicion(2, 3), [SUR])
        self.assertFalse(movimiento_bien_formado(m))

class test_juego_bien_formado(unittest.TestCase):

    def test_juego_ok(self):
        j = Juego(tablero_8x8_vacio(), DORADO, 0)
        self.assertTrue(juego_bien_formado(j))

    def test_juego_pasos_excedidos(self):
        j = Juego(tablero_8x8_vacio(), DORADO, 6)
        self.assertFalse(juego_bien_formado(j))

    def test_juego_pasos_invalido_filas(self):
        tablero_invalido = leer_tablero([
              '--------', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '-------', #2
              '--------', #1
              '--------', #0
              #01234567
            ])
        j = Juego(tablero_invalido, DORADO, 0)
        self.assertFalse(juego_bien_formado(j))

    def test_juego_pasos_invalido_columnas(self):
        tablero_invalido = leer_tablero([
              '--------', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              '--------', #1
              #01234567
            ])
        j = Juego(tablero_invalido, DORADO, 0)
        self.assertFalse(juego_bien_formado(j))

#### Ejercicio 2

class test_posicion_vecina_hacia(unittest.TestCase):

    def test_vecina_al_norte(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), NORTE), Posicion(1, 0))

    def test_vecina_al_sur(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(3, 4), SUR), Posicion(2, 4))

    def test_vecina_al_este(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(3, 4), ESTE), Posicion(3, 5))

    def test_vecina_al_oeste(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(3, 4), OESTE), Posicion(3, 3))
        
class test_son_posiciones_vecinas(unittest.TestCase):

    def test_vecinas(self):
        self.assertTrue(son_posiciones_vecinas(Posicion(0, 0), Posicion(1, 0)))

class test_casilla_en_posicion(unittest.TestCase):

    def test_casilla_en_posicion(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertEqual(casilla_en_posicion(t, Posicion(0, 0)), Pieza(CABALLO, DORADO))

class test_hay_casilla_vacia(unittest.TestCase):

    def test_casilla_vacia(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(hay_casilla_vacia(t, Posicion(2, 1)))

class test_hay_pieza_de_color(unittest.TestCase):

    def test_hay_pieza_de_color_ok(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(hay_pieza_de_color(t, Posicion(1, 4), DORADO))

#### Ejercicio 3

class test_hay_casilla_vacia_hacia(unittest.TestCase):

    def test_hay_casilla_vacia_hacia_norte_verdadero(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(0, 0), NORTE))

    def test_hay_casilla_vacia_hacia_sur_verdadero(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(2, 6), SUR))

    def test_hay_casilla_vacia_hacia_este_verdadero(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(1, 1), ESTE))

    def test_hay_casilla_vacia_hacia_oeste_verdadero(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(1, 1), OESTE))

    def test_hay_casilla_vacia_hacia_falso(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertFalse(hay_casilla_vacia_hacia(t, Posicion(2, 3), SUR))

class test_hay_pieza_amiga_vecina(unittest.TestCase):

    def test_hay_pieza_amiga_vecina(self):
        t = leer_tablero([
              'R-hRD-Rr', #7
              'M----d--', #6
              '-h-rrCR-', #5
              'R-rcE---', #4
              '--drRR--', #3
              '-HD-H--m', #2
              '--r-RCc-', #1
              're---r--', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_amiga_vecina(t, Posicion(4, 3)))

class test_hay_pieza_enemiga_mas_debil_hacia(unittest.TestCase):

    def test_hay_pieza_enemiga_mas_debil_hacia(self):
        t = leer_tablero([
              '--Hdm---', #7
              'r--HhC--', #6
              'e---R-C-', #5
              'ME--d---', #4
              'h--RDcRr', #3
              'R-R-r--r', #2
              '-RRcrRD-', #1
              '--r---rr', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(1, 3), OESTE))

class test_hay_pieza_enemiga_mas_fuerte_vecina(unittest.TestCase):

    def test_hay_pieza_enemiga_mas_fuerte_vecina(self):
        t = leer_tablero([
              'R-e--mRr', #7
              '------dE', #6
              'h--Rr-RR', #5
              'c--R-C--', #4
              '-rCHDrr-', #3
              '----rc--', #2
              'h-R-M-R-', #1
              'rr-D-dH-', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_enemiga_mas_fuerte_vecina(t, Posicion(3, 1)))

class test_hay_pieza_congelada(unittest.TestCase):

    def test_hay_pieza_congelada(self):
        t = leer_tablero([
              '--d--H-D', #7
              '-hMc--r-', #6
              '--r--C-H', #5
              '--------', #4
              '-CeD----', #3
              '---R----', #2
              '--------', #1
              '--------', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_congelada(t, Posicion(6, 1)))

    def test_hay_pieza_congelada_falso(self):
        t = leer_tablero([
              '--d--H-D', #7
              '-hMc--r-', #6
              '--r--C-H', #5
              '--------', #4
              '-CeD----', #3
              '---R----', #2
              '--------', #1
              '--------', #0
              #01234567
            ])
        self.assertFalse(hay_pieza_congelada(t, Posicion(6, 6)))

#Ejercicio 4

class test_puede_realizar_movimiento(unittest.TestCase):

    def test_mover_a_secas_ok(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertTrue(puede_realizar_movimiento(j, m))

    def test_mover_a_secas_congelada(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-dM--mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_mover_a_secas_mala_direccion_norte(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-dM--mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(5, 6), [NORTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_mover_a_secas_mala_direccion_sur(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-dM--mDR', #0
              #01234567
            ])
        j = Juego(t, DORADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(5, 1), [SUR])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_mover_a_secas_supera_maximo_de_pasos(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-dM--mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, MAX_PASOS)
        m = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_no_puede_mover_a_secas(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '------r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '-R------', #1
              '-dM--mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_no_puede_arrastrar(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--mMd---', #3
              '-R-D----', #2
              '-r------', #1
              '-d-M-mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(ARRASTRAR, Posicion(1, 1), [NORTE, ESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))
        
    def test_no_puede_arrastrar(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              'R-------', #1
              '-d-M-mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(ARRASTRAR, Posicion(0, 1), [NORTE, ESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))
        
    def test_no_puede_empujar_pieza_mas_fuerte(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '-D------', #1
              '-r-M-mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(EMPUJAR, Posicion(0, 1), [NORTE, ESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))
        
    def test_no_puede_empujar_casilla_no_vacia(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--m-d---', #3
              '---D----', #2
              'MR------', #1
              '-d-M-mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(EMPUJAR, Posicion(0, 1), [NORTE, OESTE])
        self.assertFalse(puede_realizar_movimiento(j, m))


#### Ejercicio 5

class test_activar_trampas(unittest.TestCase):

    def test_activar_trampas_ok(self):
        t0 = leer_tablero([
               '-eRD--rd', #7
               '--------', #6
               'H-r--E--', #5
               '-H--r-Cr', #4
               'R-------', #3
               'R-H--m--', #2
               'R-------', #1
               'c-D---R-', #0
               #01234567
             ])
        t1 = leer_tablero([
               '-eRD--rd', #7
               '--------', #6
               'H-------', #5
               '-H--r-Cr', #4
               'R-------', #3
               'R-------', #2
               'R-------', #1
               'c-D---R-', #0
               #01234567
             ])
        t2 = activar_trampas(t0)
        self.assertNotEqual(t0, t1)
        self.assertEqual(t2, t1)

    def test_activar_trampas_protegidas(self):
        t0 = leer_tablero([
                   '-eRD--rd', #7
                   '--------', #6
                   'H-rr-E--', #5
                   '-H--r-Cr', #4
                   'R-------', #3
                   'R-H--mm-', #2
                   'R-------', #1
                   'c-D---R-', #0
                   #01234567
                 ])
        t1 = leer_tablero([
                   '-eRD--rd', #7
                   '--------', #6
                   'H-rr----', #5
                   '-H--r-Cr', #4
                   'R-------', #3
                   'R----mm-', #2
                   'R-------', #1
                   'c-D---R-', #0
                   #01234567
                 ])
        t2 = activar_trampas(t0)
        self.assertNotEqual(t0, t1)
        self.assertEqual(t2, t1)
    
    def test_activar_trampas_sin_cambios(self):
        t0 = leer_tablero([
                   '-eRD--rd', #7
                   '--------', #6
                   'H-RR-EE-', #5
                   '-H--r-Cr', #4
                   'R-------', #3
                   'R-HH-MM-', #2
                   'R-------', #1
                   'c-D---R-', #0
                   #01234567
                 ])
        t1 = leer_tablero([
                   '-eRD--rd', #7
                   '--------', #6
                   'H-RR-EE-', #5
                   '-H--r-Cr', #4
                   'R-------', #3
                   'R-HH-MM-', #2
                   'R-------', #1
                   'c-D---R-', #0
                   #01234567
                 ])
        t2 = activar_trampas(t0)
        self.assertEqual(t0, t1)
        self.assertEqual(t2, t1)

### Ejercicio 6

class test_movimientos_del_juego(unittest.TestCase):
    pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    def test_realizar_movimiento_a_secas(self):
        t = leer_tablero([
            'rr----Rr',
            'c-----me',
            '---Ed-R-',
            '-M---R--',
            '---R----',
            '-rrrr---',
            '-H---DCC',
            'R-----RR',
        ])

        tResultado = leer_tablero([
            'r-----Rr',
            'cr----me',
            '---Ed-R-',
            '-M---R--',
            '---R----',
            '-rrrr---',
            '-H---DCC',
            'R-----RR',
        ])

        juego = Juego(t, PLATEADO, 0)
        juegoNuevo = Juego(tResultado, PLATEADO, 1)

        movimiento = Movimiento(
            MOVER_A_SECAS,
            Posicion(7, 1),
            [SUR]
        )
        self.assertEqual(realizar_movimiento(juego, movimiento), juegoNuevo)

    def test_realizar_movimiento_arrastrar(self):
        t = leer_tablero([
            'rr----Rr',
            'c-----me',
            '---Ed-R-',
            '-M---R--',
            '---R----',
            '-rrrr---',
            '-H---DCC',
            'R-----RR'
        ])

        tResultado = leer_tablero([
            'rr----Rr',
            'c--E--me',
            '---d--R-',
            '-M---R--',
            '---R----',
            '-rrrr---',
            '-H---DCC',
            'R-----RR'
        ])

        juego = Juego(t, DORADO, 0)
        juegoNuevo = Juego(tResultado, DORADO, 2)

        movimiento = Movimiento(
            ARRASTRAR,
            Posicion(5, 3),
            [NORTE, OESTE]
        )

        self.assertEqual(realizar_movimiento(juego, movimiento), juegoNuevo)

    def test_realizar_movimiento_empujar(self):
        t = leer_tablero([
            'rr----Rr', #7
            'c-----me', #6
            '---Ed-R-', #5
            '-M---R--', #4
            '---R----', #3
            '-rrrr---', #2
            '-H---DCC', #1
            'R-----RR', #0
        ])

        tResultado = leer_tablero([
            'rr----Rr', #7
            'c-----me', #6
            '----E-R-', #5
            '-M---R--', #4
            '---R----', #3
            '-rrrr---', #2
            '-H---DCC', #1
            'R-----RR', #0
        ])

        juego = Juego(t, DORADO, 0)
        juegoNuevo = Juego(tResultado, DORADO, 2)

        movimiento = Movimiento(
            EMPUJAR,
            Posicion(5, 3),
            [ESTE, ESTE]
        )

        self.assertEqual(realizar_movimiento(juego, movimiento), juegoNuevo)
    
    def test_realizar_movimiento_cuatro_pasos(self):
        t = leer_tablero([
            'rr----Rr', #7
            'c-----me', #6
            '---Ed-R-', #5
            '-M---R--', #4
            '---R----', #3
            '-rrrr---', #2
            '-H---DCC', #1
            'R-----RR', #0
        ])

        tResultado = leer_tablero([
            'r-----Rr', #7
            'cr----me', #6
            '---Ed-R-', #5
            '-M---R--', #4
            '---R----', #3
            '-rrrr---', #2
            '-H---DCC', #1
            'R-----RR', #0
        ])

        # El jugador plateado ya consumió 3 pasos
        juego = Juego(t, PLATEADO, 3)

        # Al consumir el cuarto paso, cambia el turno
        juegoNuevo = Juego(tResultado, DORADO, 0)

        movimiento = Movimiento(
            MOVER_A_SECAS,
            Posicion(7, 1),
            [SUR]
        )

        self.assertEqual(
            realizar_movimiento(juego, movimiento),
            juegoNuevo
        )

#### Ejercicio 7
class test_ganador_del_juego(unittest.TestCase):
    def test_promueve_conejo_dorado_turno_del_oponente(self):
        t = leer_tablero([
              'rr----Rr', #7
              'c-----me', #6
              '---Ed-R-', #5
              '-M---R--', #4
              '---R----', #3
              '-rrrr---', #2
              '-H---DCC', #1
              'R-----RR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        self.assertTrue(hay_ganador_determinado(j))
        self.assertEqual(ganador_del_juego(j), DORADO)
        
    def test_no_hay_conejos_rival(self):
        t = leer_tablero([
              '--------', #7
              'c---R-me', #6
              '---Ed-R-', #5
              '-M---R--', #4
              '---R----', #3
              '--------', #2
              '-H---DCC', #1
              'R-----RR', #0
              #01234567
            ])
        j = Juego(t, DORADO, 0)
        self.assertTrue(hay_ganador_determinado(j))
        self.assertEqual(ganador_del_juego(j), DORADO)

    def test_reunen_ambos_condiciones_de_ganar(self):
        t = leer_tablero([
              '--------', #7
              'c-----me', #6
              '---Ed---', #5
              '-M------', #4
              '----r---', #3
              '--------', #2
              '-H---DCC', #1
              '--------', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        self.assertTrue(hay_ganador_determinado(j))
        self.assertEqual(ganador_del_juego(j), PLATEADO)
