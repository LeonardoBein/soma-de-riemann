import matplotlib.pyplot as plt
import numpy as np
from time import time

class MegaRampa():
    """docstring for MegaRampa."""
    y = []
    x = []
    numeroJanelas = 3
    janela = 1
    aRiemann = {'left':0,'right':0,'center':0}
    aNumpy = None
    timeEnd = 0
    timeStart = 0

    def __init__(self, x):
        self.x = x
        self.y = self.curva(x)

    def config_plot(self):
        if self.janela > self.numeroJanelas:
            raise Exception("Numero de janela excedida %d" % self.janela)
        plt.subplot(self.numeroJanelas,1, self.janela)
        plt.axis([-2, 20, 0, 8])
        self.janela += 1


    def curva(self,x):
        c = []
        for i in x:
            if 0 <=  i < 2:
                c.append((5/2)*i)
            elif 2 <= i < 4:
                c.append(5)
            elif 4 <= i < 8:
                c.append(i**2-12*i+37)
            elif 8 <= i < 10:
                c.append(5)
            elif 10 <= i < 16:
                c.append(-(5/6)*i+(50/6)+5)
            else:
                c.append(0)
        return c
    def yCurve(self,x):
        return self.curva([x])[0]

    def plotCurva(self):
        plt.plot(self.x, self.y)

    def riemann(self,passo,left=False,right=False,center=False,left_plot=False,right_plot=False,center_plot=False):

        if passo > 1:
            self.warning("passo inserido muito grande!")

        self.timeStart = time()
        if left:
            self.info("Iniciando calculo pela esquerda")
            self.aRiemann['left'] = 0
            i = self.x[0]

            if left_plot:
                self.config_plot()
                self.plotCurva()

            while i < self.x[-1]:
                self.aRiemann['left'] += passo * self.yCurve(i)
                if left_plot:
                    plt.plot(i, self.yCurve(i), marker='o',color='black')
                    plt.bar(i, self.yCurve(i), width=passo, align='edge')
                i = i + passo
            if left_plot:
                plt.title('Área aprox. esq.: {:.4f}'.format(self.aRiemann['left']))
        if right:
            self.info("Iniciando calculo pela direita")
            self.aRiemann['right'] = 0
            i = self.x[0]

            if right_plot:
                self.config_plot()
                self.plotCurva()

            while i < self.x[-1]:
                px = i+passo
                self.aRiemann['right'] += passo * self.yCurve(px)
                if right_plot:
                    plt.plot(px, self.yCurve(px), marker='o',color='black')
                    plt.bar(px, self.yCurve(px), width=-passo, align='edge')
                i = i + passo
            if right_plot:
                plt.title('Área aprox. dir.: {:.4f}'.format(self.aRiemann['right']))

        if center:
            self.info("Iniciando calculo pelo centro")
            self.aRiemann['center'] = 0
            i = self.x[0]

            if center_plot:
                self.config_plot()
                self.plotCurva()

            while i < self.x[-1]:
                px = i+(passo/2)
                self.aRiemann['center'] += passo * self.yCurve(px)
                if center_plot:
                    plt.plot(px, self.yCurve(px), marker='o',color='black')
                    plt.bar(px, self.yCurve(px), width=passo, align='center')
                i = i + passo
            if center_plot:
                plt.title('Área aprox. centro.: {:.4f}'.format(self.aRiemann['center']))
        self.timeEnd = time()
        self.showInfo()

    def showInfo(self):
        print()
        erro = np.abs(self.integrate_numpy() - self.aRiemann['left']) / self.integrate_numpy() * 100
        print("Area pela esquerda: %f (Erro: %f%%)" % (self.aRiemann['left'],erro))
        erro = np.abs(self.integrate_numpy() - self.aRiemann['right']) / self.integrate_numpy() * 100
        print("Area pela direita: %f (Erro: %f%%)" % (self.aRiemann['right'],erro))
        erro = np.abs(self.integrate_numpy() - self.aRiemann['center']) / self.integrate_numpy() * 100
        print("Area pelo centro: %f (Erro: %f%%)" % (self.aRiemann['center'],erro))
        print("Area calculada pelo numpy %f" % self.integrate_numpy())
        print("Tempo de execução %.2fs" % (self.timeEnd - self.timeStart))

    def info(self, msg):
        print("INFO - %s" % msg)

    def warning(self, msg):
        print("WARNING - %s" % msg)


    def integrate_numpy(self):
        if not self.aNumpy:
            self.aNumpy = np.sum(self.y)*(self.x[-1]-self.x[0])/len(self.x)
        return self.aNumpy
    def render(self):
        plt.subplots_adjust(hspace=0.5)
        plt.show()


if __name__ == '__main__':
    try:
        mega = MegaRampa(x=np.linspace(0,16,1000))
        plot = input("Gráfico?[Y/n]")
        if plot.lower() == 'y' or plot.lower() == 's' or plot.lower() == 'yes' or plot.lower() == 'sim' :
            mega.riemann(float(input("insira um passo: ")),right=True,right_plot=True,left=True,left_plot=True,center=True,center_plot=True)
            mega.render()
        else:
            mega.riemann(float(input("insira um passo: ")),right=True,left=True,center=True)
    except KeyboardInterrupt:
        print()
    except Exception as e:
        print(e)
