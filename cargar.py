import struct

from obj import Obj

def char(c):
    # 1 byte
    return struct.pack('=c'. c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)


def color(r,g,b):
    # Creacion de Color (255 deja usar todos los colores)
    return bytes([int(b*255),
                int(g*255),
                int(r*255)])

#Constructor
class Render(object):
    
    def __init__(self):
        self.viewPortX = 0
        self.viewPortY = 0
        self.height = 0
        self.width = 0
        #los colores van de 0 a 1 
        self.clearColor = color(0, 0, 0)

        #aqui especificamos el color de los puntitos
        self.current_color = color(1, 1, 1)
        self.framebuffer = []
        
        self.glViewport(0,0,self.width, self.height)
        self.glClear() 


    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

     #Mapa de bits de un solo color
    def glClear(self):
        self.framebuffer = [[self.clearColor for x in range(self.width+1)]
                            for y in range(self.height+1)]

    #el color del fondo o pantalla
    def glClearColor(self, r, g, b):
        self.clearColor = color(r, b, g)
        self.glClear()

    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    def glVertex(self, x, y):
        if x <= 1 and x>= -1 and y >= -1 and y <= 1:
                
                if x > 0:
                        self.vx = self.x + round(round(self.vpx/2)*x) - 1
                if y > 0:
                        self.vy = self.y + round(round(self.vpy/2)*y) - 1
                if x <= 0:
                        self.vx = self.x + round(round(self.vpx/2)*x)
                if y <= 0:
                        self.vy = self.y + round(round(self.vpy/2)*y)
                
                self.glPoint(self.vx,self.vy, self.current_color)
        else:
                pass
    
    #Da el color al punto en pantalla 
    def glPoint(self, x, y, color):
        x = int(round((x+1) * self.width / 2))
        y = int(round((y+1) * self.height / 2))
        try:
                self.framebuffer[x][y] = color
        except IndexError:
                print("\nFuera de los límites de la imagen\n")

     #Funcion para linea 
    def glLine(self, x0, y0, x1, y1):
        #Convierte los valores entre -1 a 1 a cordenadas DMC
        x0 = int(round((x0 + 1) * self.width / 2))
        y0 = int(round((y0 + 1) * self.height / 2))
        x1 = int(round((x1 + 1) * self.width / 2))
        y1 = int(round((y1 + 1) * self.height / 2))

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx
        
        if steep:
            #intercambiamos cada una de las coordenadas
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if x0 > x1:
            #intercambia los puntos
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #puntos que formarán la línea
        offset = 0.5 * 2 * dx
        threshold = 0.5 * 2 * dx
        y = y0

        #Rellena la línea con puntos sin dejar espacios
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint((float(y)/(float(self.width)/2))-1,(float(x)/(float(self.height)/2))-1,self.current_color)
            else:
                self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.current_color)
            offset += dy

            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * dx


    #Lee y renderiza archivos .obj 
    def glObjModel(self, file_name, translate=(0,0), scale=(1,1)):
        #Lector .obj
        model = Obj(file_name)
        model.read()
        
        for face in model.faces:
            vertices_ctr = len(face)
            for j in range(vertices_ctr):
                f1 = face[j][0]
                f2 = face[(j+1) % vertices_ctr][0]
                
                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

                x1 = (v1[0] + translate[0]) * scale[0]
                y1 = (v1[1] + translate[1]) * scale[1]
                x2 = (v2[0] + translate[0]) * scale[0]
                y2 = (v2[1] + translate[1]) * scale[1]

                self.glLine(x1, y1, x2, y2)


    # Función para crear la imagen
    def glFinish(self, filename):
        with open(filename, 'bw') as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))

            # file size
            file.write(dword(14 + 40 + self.height * self.width * 3))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.framebuffer[x][y])
            file.close()
