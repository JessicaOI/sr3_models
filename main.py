from cargar import Render

w = 900
h = 900
rend = Render()
rend.glCreateWindow(w, h)

rend.glViewport(int(0),
                int(0), 
                int(w/1), 
                int(h/1))

def glInit():
    return rend

if __name__ == '__main__':

    rend = glInit()
    rend.glClear()

    #Colores de la imagen
    rend.glColor(0.2, 0.7, 0)

    #cargar .obj (posicion inicial), (escala)
    rend.glObjModel('planta.obj', (0, -15), (0.03, 0.03))
    
    rend.glFinish("imagen.bmp")