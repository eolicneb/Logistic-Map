import Tkinter as tk
from PIL import ImageTk, Image
import threading as thr

H111 = 256*256*256+256*256+256
minIt = 1000

class ventana():
  def __init__(self,ancho,alto,iteraciones):
    self.w = ancho
    self.h = alto
    self.s = alto/5
    self.iter = iteraciones
    self.map = []*alto*ancho
    self.ventana = tk.Tk()
    self.iniciar()

  def iniciar(self):
    self.R = [3.7,3.8]
    self.X = [0,1]
    # Pantalla de imagen
    self.c = tk.Canvas(self.ventana,
                       width=self.w,
                       height=self.h,
                       bg="#102010")
    self.c.grid(row=1,column=0,columnspan=5)
    self.im = tk.PhotoImage(width=self.w,height=self.h)
    self.c.create_image((self.w/2,self.h/2),image=self.im)
    # Pantalla de corte transversal
    # self.d = tk.Canvas(self.ventana,
    #                    width=self.w,
    #                    height=self.s,
    #                    bg="#102020")
    # self.d.grid(row=2,column=0,columnspan=5)
    self.jm = tk.PhotoImage(width=self.w,height=self.s)
    # self.d.create_image((self.w/2,self.s/2),image=self.jm)
    # Variables de control
    self.inIter = tk.IntVar()
    self.inIter.set(self.iter)
    self.inIter.trace('w',self.chIter) # Llama chIter cuando cambia el texto
    self.rPos = tk.StringVar()
    self.rPos.set(self.w/2)
    # Despiece de la ventana
    f = tk.Frame(self.ventana)
    f.grid(row=0,column=4)
    e = tk.Entry(f,textvariable=self.inIter)
    e.grid(row=0,column=1,sticky="EW")
    g = tk.Label(f,textvariable=self.rPos)
    g.grid(row=0,column=0,sticky="EW")
    bZoomIn = tk.Button(self.ventana,text="+",command=self.zoomIn)
    bZoomOut = tk.Button(self.ventana,text="-",command=self.zoomOut)
    bLeft = tk.Button(self.ventana,text="<<",command=self.Left)
    bRight = tk.Button(self.ventana,text=">>",command=self.Right)
    bZoomIn.grid(row=0,column=1,sticky="EW")
    bZoomOut.grid(row=0,column=2,sticky="EW")
    bLeft.grid(row=0,column=0,sticky="EW")
    bRight.grid(row=0,column=3,sticky="EW")
    # Funciones de la ventana
    self.activarFunciones(True)
    self.indice = self.c.create_line(self.w/2,0,self.w/2,self.h,fill="yellow")
    self.xDown = 0
    self.yDown = 0
    self.barSt = self.w/40
    self.barSp = 9
    self.barLg = self.w/4
    # self.barA = self.c.create_rectangle(self.barSt,
    #                                     self.barSt,
    #                                     self.barSt+self.barLg,
    #                                     self.barSt+4,
    #                                     width=0,
    #                                     fill='red')
    # self.barB = self.c.create_rectangle(self.barSt,
    #                                     self.barSt+self.barSp,
    #                                     self.barSt+self.barLg,
    #                                     self.barSt+self.barSp+4,
    #                                     width=0,
    #                                     fill='green')
    # self.barC = self.c.create_rectangle(self.barSt,
    #                                     self.barSt+self.barSp*2,
    #                                     self.barSt+self.barLg,
    #                                     self.barSt+self.barSp*2+4,
    #                                     width=0,
    #                                     fill='yellow')
    # for r in [ self.barA, self.barB, self.barC ]:
    #   self.barLargo(r,0)
    self.refreshing = False
    self.refresh()

  def activarFunciones(self,sino):
    if sino:
      self.c.bind('<Button-1>',self.lClick)
      self.c.bind('<ButtonRelease-1>',self.NolClick)
      self.c.bind('<Button-3>',self.rClick)
      self.c.bind('<ButtonRelease-3>',self.NorClick)
      self.c.bind('<Motion>',self.position)
    else:
      self.c.unbind('<Button-1>')
      self.c.unbind('<ButtonRelease-1>')
      self.c.unbind('<Button-3>')
      self.c.unbind('<ButtonRelease-3>')
      self.c.unbind('<Motion>')

  def perfilar(self,li):
    pass

  def barLargo(self,bar,f):
    x0,y0,x1,y1 = self.c.coords(bar)
    self.c.coords(bar,x0,y0,int(self.barSt+f*self.barLg),y1)

  def position(self,event):
    if not self.refreshing:
      x = self.c.canvasx(event.x)
      paso = float((self.R[1]-self.R[0])/(self.w - 1.0))
      r = self.R[0]+x*paso
      self.rPos.set('{0:.15f}'.format(r))
      self.c.coords(self.indice,x,0,x,self.h)

  def lClick(self,event):
    self.xDown = self.c.canvasx(event.x)
    self.yDown = self.c.canvasy(event.y)

  def NolClick(self,event):
    longPix = float(self.R[1]-self.R[0])/self.w
    longPiy = float(self.X[1]-self.X[0])/self.h
    r = self.c.canvasx(event.x)
    h = self.c.canvasy(event.y)
    r0 = min(r,self.xDown)
    r1 = max(r,self.xDown)
    h1 = min(h,self.yDown)
    h0 = max(h,self.yDown)
    self.R[1] = self.R[0] + r1*longPix
    self.R[0] = self.R[0] + r0*longPix
    self.X[0] = max(0, self.X[1] - h0*longPiy)
    self.X[1] = min(1, self.X[1] - h1*longPiy)
    print("zoom in to r = {}, {}".format(self.R[0],self.R[1]))
    print("           x = {}, {}".format(self.X[0],self.X[1]))
    self.refresh()

  def rClick(self,event):
    self.xDown = self.c.canvasx(event.x)
    self.yDown = self.c.canvasy(event.y)

  def NorClick(self,event):
    r = self.c.canvasx(event.x)
    h = self.c.canvasy(event.y)
    if r<>self.xDown and h<>self.yDown:
      r0 = min(r,self.xDown)
      r1 = max(r,self.xDown)
      h0 = max(h,self.yDown)
      h1 = min(h,self.yDown)
      longPix = float(self.R[1]-self.R[0])/(r1-r0)
      longPiy = float(self.X[1]-self.X[0])/(h0-h1)
      self.R[1] = min(4,self.R[1]+(self.w-r1)*longPix)
      self.R[0] = max(1,self.R[0]-r0*longPix)
      self.X[1] = min(1,self.X[1]+h1*longPiy)
      self.X[0] = max(0,self.X[0]-(self.h-h0)*longPiy)
      print("zoom out to r = {}, {}".format(self.R[0],self.R[1]))
      print("            x = {}, {}".format(self.X[0],self.X[1]))
      self.refresh()

  def chIter(self,*args):
    self.iter = self.inIter.get()
    self.refresh()

  def zoomIn(self):
    W = (self.R[1]-self.R[0])/10.0
    self.R[0] = self.R[0] + W
    self.R[1] = self.R[1] - W
    self.refresh()

  def zoomOut(self):
    W = (self.R[1]-self.R[0])/10.0
    self.R[0] = max([1,self.R[0] - W])
    self.R[1] = min([4,self.R[1] + W])
    self.refresh()

  def Left(self):
    W = (self.R[1]-self.R[0])/10.0
    self.R[0] = max([1,self.R[0] - W])
    self.R[1] = self.R[1] - W
    self.refresh()

  def Right(self):
    W = (self.R[1]-self.R[0])/10.0
    self.R[0] = self.R[0] + W
    self.R[1] = min([4,self.R[1] + W])
    self.refresh()

  def refresh(self):
    if thr.activeCount()<20:
      z = thr.Thread(target=self.llenarMatriz,name="llenarMatriz")
      z.start()

  def pintarPantalla(self):
    plano = []
    for y in range(self.h):
      plano.append('{')
      for x in range(self.w):
        plano.append(self.map[x*self.h+y])
        #self.barLargo(self.barA,((x*self.h+y)/self.w/self.h))
        plano.append('}')
    self.im.put(' '.join(plano))

  def pintarLinea(self,li):
    linea = []
    for y in range(self.h,0,-1):
      linea.append('{')
      linea.append(self.map[li*self.h+y-1])
      linea.append('}')
    self.im.put(' '.join(linea), to=(li,0))

  def llenarMatriz(self):
    self.activarFunciones(False)
    self.refreshing = True
    print('llenarMatriz')
    paso = float((self.R[1]-self.R[0])/(self.w - 1.0))
    for k in range(self.w):
      r = self.R[0]+k*paso
      self.map[k*self.h:(k+1)*self.h-1] = self.logMap(r)
      self.pintarLinea(k)
    print('Ro = {}, Rf = {}'.format(self.R[0],self.R[1]))
    self.activarFunciones(True)
    self.refreshing = False

  def logMap(self,r):
    alfa = 1.0/(self.X[1]-self.X[0])
    beta = self.X[0]*alfa
    x = 0.5
    col = [0]*self.h
    for n in range(minIt):
      x = self.f(x,r)
    cnt = cErr = 0
    while cnt<self.iter and cErr<self.iter/(self.X[1]-self.X[0]):
      x = self.f(x,r)
      j = int(((alfa*x-beta)*(self.h-1))+0.5)
      if j>=0 and j<self.h:
        col[j] = col[j] + 1
        cnt = cnt+1
      else:
        cErr = cErr+1
    pMax = 0
    for p in col:
      if (p>pMax):
        pMax = p
    row = []
    for p in col:
      if p>0:
        row.append( "#%02x%02x%02x" % (p*187/pMax+68,
                                       p*187/pMax+68,
                                       p*187/pMax+68) )
      else:
        row.append("#332222")
    return row

  def f(self,x,r):
    return float(r*x*(1-x))

aca = ventana(600,540,100)
aca.ventana.focus_force()
aca.ventana.mainloop()
