import random
from PIL import Image
from random import randint
import numpy as np


class BuildImage():
    def __init__(self):
        self.image = np.zeros((0, 0, 0), dtype = np.uint8 )

    def __validate_params(self, width, height, color):
        if not isinstance(height, int) or not isinstance(width, int):
            raise Exception("Los parametros altura y anchura deben ser enteros")
        if type(color) is not tuple or (len(color) != 3 and len(color) != 4):
            raise Exception("El parametro color debe ser una tupla de tamaño 3 o 4")

    def set_new_image(self, width, height, color, return_image = True):
        """
        a) Implementa un método al que se le pase el ancho y el alto de la imagen y el color de la
        misma. El método debe devolver la imagen creada.
        """
        self.__validate_params(width, height, color)
        image = np.zeros((height, width, len(color)), dtype = np.uint8 )
        image[0:height, 0:width] = color
        return Image.fromarray(image) if return_image is True else image
    
    @staticmethod
    def switch_np_and_image(image, switch_to):
        if isinstance(image, (np.ndarray, np.generic)):
            if switch_to == 'image':
                return Image.fromarray(image)
            else:
                return image
        else:
            if switch_to == 'np':
                return np.asarray(image)
            else:
                return image
    
    def set_images_stacked(self, width, height, hor_img_count, ver_img_count, return_image = True):
        """
        b) Implementa un método al que se le pasa el número de elementos horizontales y
        verticales, así como el ancho y el alto de los elementos horizontales y verticales y que
        devuelva la imagen creada con un color de fondo diferente para cada elemento.
        Ejemplo: imagen con 8 por 8 elementos del mismo ancho y alto e imagen con 8 por 3
        elementos con diferente ancho y alto.
        """
        previous_hor_image = None
        final_image = None

        for x in range(0, hor_img_count):
            for y in range(0, ver_img_count):
                color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                new_image = self.set_new_image(width, height, color, False)
                if (previous_hor_image is not None):
                    previous_hor_image = np.hstack((new_image, previous_hor_image))
                else:
                    previous_hor_image = new_image
            if (final_image is not None):
                final_image = np.vstack((final_image, previous_hor_image))
            else:
                final_image = previous_hor_image
            previous_hor_image = None

        return self.switch_np_and_image(final_image, 'image' if return_image is True else 'np')
    
        """
        @staticmethod
          def mosaic(x = 10, y = 10, width = 10, height = 10):
              total_width = x * width
              total_height = y * height
              _data = np.zeros((total_height, total_width, 3), dtype = np.uint8)
              for i in range(0, total_width, width):
                  for j in range(0, total_height, height):
                      _data[j : j + height, i : i + width] =  (randint(0, 255), randint(0, 255), randint(0, 255))
              return Image.fromarray(_data)
        """
    
    def redimensionar(self, width, height, new_image = None, return_image = True):
        """
        c) Implementa un método que redimensiona una imagen al ancho y alto especificado, este
        método deforma la imagen si la relación de aspecto no es la misma.
        """
        image = None
        if (new_image is not None):
            image = self.switch_np_and_image(new_image, 'image')
        else:
            image = self.switch_np_and_image(self.image, 'image')
        image = image.resize((width, height))
        return self.switch_np_and_image(image, 'image' if return_image is True else 'np')
    
    def redimensionar_ancho(self, width, new_image = None, return_image = True):
        """
        d) Implementa un método que redimensiona una imagen al ancho especificado, sin
        deformar la imagen.
        """
        image = None
        if (new_image is not None):
            image = self.switch_np_and_image(new_image, 'image')
        else:
            image = self.switch_np_and_image(self.image, 'image')
        image = image.resize((width, self.image.height * width // self.image.width))
        return self.switch_np_and_image(image, 'image' if return_image is True else 'np')
    
    def redimensionar_alto(self, height, new_image = None, return_image = True):
        """
        e) Implementa un método que redimensiona una imagen al alto especificado, sin deformar
        la imagen.
        """
        image = None
        if (new_image is not None):
            image = self.switch_np_and_image(new_image, 'image')
        else:
            image = self.switch_np_and_image(self.image, 'image')
        image = image.resize((self.image.width * height // self.image.height, height))
        return self.switch_np_and_image(image, 'image' if return_image is True else 'np')
    
    def get_from_image(self, initial_hor, initial_ver, width, height, new_image = None, return_image = True):
        """
        f) Implementa un método que devuelva un trozo de una imagen especificando la posición
        horizontal y vertical y el ancho y el alto, si las dimensiones especificadas son superiores a la
        imagen original, debe devolver el recorte disponible.
        """
        image = None
        if (new_image is not None):
            image = self.switch_np_and_image(new_image, 'np')
        else:
            image = self.switch_np_and_image(self.image, 'np')
        image = image[initial_ver:initial_ver+height, initial_hor:initial_hor+width]
        return self.switch_np_and_image(image, 'image' if return_image is True else 'np')
    
    def stack(self, second_image, first_image = None, vertically = True, return_image = True):
        """
        g) Implementa un método que apile dos imágenes horizontal o verticalmente, sin
        deformarlas. El método debe especificar en sus argumentos qué dimensiones son las que
        se deben adaptar.
        """
        image = None
        if (first_image is None):
            image = self.switch_np_and_image(self.image, 'image')
        else:
            image = self.switch_np_and_image(first_image, 'image')
        second_image = self.switch_np_and_image(second_image, 'image')
        
        new_image = None
        
        if (vertically is False):
            if image.height == second_image.height:
                pass
            elif image.height > second_image.height:
                second_image = self.redimensionar_alto(image.height, second_image)
            else:
                image = self.redimensionar_alto(second_image.height, image)
            image = self.switch_np_and_image(image, 'np')
            second_image = self.switch_np_and_image(second_image, 'np')
            new_image = np.vstack((image, second_image))
        else:
            if image.width == second_image.width:
                pass
            if image.width > second_image.width:
                second_image = self.redimensionar_ancho(image.width, second_image)
            else:
                image = self.redimensionar_ancho(second_image.width, image)
            image = self.switch_np_and_image(image, 'np')
            second_image = self.switch_np_and_image(second_image, 'np')
            new_image = np.hstack((image, second_image))

        image = new_image
        return self.switch_np_and_image(image, 'image' if return_image is True else 'np')
        
    def stack_2(self, second_image, first_image = None, vertically = True, return_image = True):
        """
        h) Implementa un método que apile dos imágenes horizontal o verticalmente, si las
        dimensiones de las imágenes no coinciden, debe adaptarlas a la imagen más ancha o más
        alta, deformándolas si fuera necesario.
        """
        image = None
        if (first_image is None):
            image = self.switch_np_and_image(self.image, 'image')
        else:
            image = self.switch_np_and_image(first_image, 'image')
        second_image = self.switch_np_and_image(second_image, 'image')
        
        new_image = None
        
        if (vertically is True):
            if image.height == second_image.height:
                pass
            elif image.height > second_image.height:
                second_image = self.redimensionar(image.width, image.height)
            else:
                image = self.redimensionar(second_image.width, second_image.height)
            image = self.switch_np_and_image(image, 'np')
            second_image = self.switch_np_and_image(second_image, 'np')
            new_image = np.vstack((image, second_image))
        else:
            if image.width == second_image.width:
                pass
            if image.width > second_image.width:
                second_image = self.redimensionar(image.width, image.height, second_image)
            else:
                image = self.redimensionar(second_image.width, second_image.height, second_image)
            image = self.switch_np_and_image(image, 'np')
            second_image = self.switch_np_and_image(second_image, 'np')
            new_image = np.hstack((image, second_image))

        image = new_image
        return self.switch_np_and_image(image, 'image' if return_image is True else 'np')
    
    @staticmethod
    def insert_image(img_a, img_b, x, y):
        """
        i) Implementa un método que inserte una imagen dentro de otra imagen en la posición
        horizontal y vertical especificada. Si la imagen que se va a insertar no cabe entera, debe
        recortarla.
        """
        if(x < 0): x = 0
        if(y < 0): y = 0
        arr_a = np.copy(np.asarray(img_a))
        arr_b = np.asarray(img_b)
        shape_y_a = y + arr_b.shape[0]
        shape_x_a = x + arr_b.shape[1]
        shape_y_b = arr_a.shape[0] - y
        shape_x_b = arr_a.shape[1] - x
        if(shape_x_a > arr_a.shape[1]): shape_x_a = arr_a.shape[1]
        if(shape_y_a > arr_a.shape[0]): shape_y_a = arr_a.shape[0]
        arr_a[y:shape_y_a,x:shape_x_a] = arr_b[0:shape_y_b,0:shape_x_b]
        return Image.fromarray(arr_a)

    @staticmethod
    def insert_redim(img1, img2, pos_x, pos_y, ancho, alto):
        img2 = Image.fromarray(Imagen.redim_image(np.asarray(img2), ancho, alto))
        res = Imagen.insert_image(img1, img2, pos_x, pos_y)
        return res
        
    def i(first_image, second_image, x, y):
        """
        j) Implementa un método que inserte dentro de una imagen otra imagen en la posición
        horizontal y vertical especificada con el ancho y el alto especificado. Si la imagen que se va
        a insertar no cabe entera, debe recortarla.
        """
        if(x < 0): x = 0
        if(y < 0): y = 0
        arr_a = np.copy(np.asarray(first_image))
        arr_b = np.asarray(second_image)
        shape_x_a = x + arr_b.shape[0]
        shape_y_a = y + arr_b.shape[1]
        shape_x_b = arr_a.shape[0] - x
        shape_y_b = arr_a.shape[1] - y
        if(shape_x_a > arr_a.shape[0]): shape_x_a = arr_a.shape[0]
        if(shape_y_a > arr_a.shape[1]): shape_y_a = arr_a.shape[1]
        arr_a[x:shape_x_a,y:shape_y_a] = arr_b[0:shape_x_b,0:shape_y_b]
        return Image.fromarray(arr_a)


img = BuildImage()
#img.image = img.set_new_image(100, 600, (100, 200, 50))
# img.image.save('cuadrado.png')
# img.image = img.set_images_stacked(150, 80, 3, 2)
# img.image = img.redimensionar(100, 600)
# img.image = img.redimensionar_ancho(70)
# img.image = img.redimensionar_alto(120)
# img.image.save('cuadrado.png')
# second_image = Image.open('cuadrado.png')
# img.image = img.stack(second_image)
# img.image = img.stack_2(second_image, None, False)
# img.image = img.get_from_image(100, 100, 2000, 2000)
# img.image.save('cuadrado6.png')
