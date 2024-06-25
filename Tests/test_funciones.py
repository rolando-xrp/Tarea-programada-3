import os
import unittest
from Tarea_programada_2_Rolando_Chiari.src.Funciones import numero_imagenes,imagen

class TestFunciones(unittest.TestCase):
    def test_verificar_numero(self):
        self.assertEqual(1,numero_imagenes(1))

    def test_verificar_string_error(self):
        self.assertEqual(None,numero_imagenes(-5))
    
    def test_imagen(self):
        lista_urls = ['https://images.pexels.com/photos/8259263/pexels-photo-8259263.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1','https://images.pexels.com/photos/25912562/pexels-photo-25912562/free-photo-of-madera-punto-de-referencia-nueva-york-puente.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1','https://images.pexels.com/photos/26125407/pexels-photo-26125407/free-photo-of-verano-animal-hoja-al-aire-libre.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1']
        imagen(lista_urls,0)
        existe = os.path.exists('imagenes/imagen_1.jpg')
        self.assertTrue(existe)
        

if __name__ == '__main__':
    unittest.main()