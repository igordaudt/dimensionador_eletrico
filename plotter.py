#Plotter
import matplotlib.pyplot as plt
# from scipy.interpolate import spline

def plotar(lista_curvas): # ([(datax, datay,name),(datax, datay,name),...])   
    rotacao=0
    # plt.plot()
    pos_legendas=[]
    for curva in lista_curvas:
        
        #If curve, use line. If point, use 'bo'
        datax,datay,number,name=curva
        if type(datax) is not list:
            datax=[datax]
        if type(datay) is not list:
            datay=[datay]
        if len(datax)<2 or len(datax)<2:
            plt.plot(datax,datay,'o', label=name) #plot points
            # plt.annotate(name,(datax[0],datay[0])) #insert label
            if (datax[0],datay[0]) in pos_legendas:
                pos_y=(datay[0])**1.25
            else:
                pos_y=datay[0]
            plt.text(datax[0],pos_y, f'({number})', rotation=rotacao)
            pos_legendas.append((datax[0],pos_y))
        else:
            plt.plot(datax,datay,label=name) #plot lines
            # plt.annotate(name,(datax[-1],datay[-1])) #insert label
            plt.text(datax[-1],datay[-1], f'({number})', rotation=rotacao)
        


    #PLOT CONFIG
    plt.xlabel('log(I(A))')
    plt.ylabel('log(T(s))')

    plt.yscale('log')
    plt.xscale('log')

    plt.legend(loc='upper right')

    plt.grid(color = 'lightgray', linestyle = '--', linewidth = 0.5, which='both')

    plt.show()
    pass
    

if __name__ == '__main__': #Start program
    """Usado para testar a plotagem"""

    # a = [pow(10, i) for i in range(10)]
    # fig = plt.figure()
    # ax = fig.add_subplot(2, 1, 1)
    # line, = ax.plot(a, color='blue', lw=2)

    #example curve #2
    # exponential function x = 10^y
    datax = [ 10**i for i in range(5)]
    datay = [ i for i in range(5)]
    label='Curva teste'
    # plt.plot(datax,datay)
    curva2=([3],[16],'teste')

    plotar([(datax, datay, label),curva2])    