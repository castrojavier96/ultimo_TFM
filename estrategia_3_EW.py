# ESTRATEGIA Volumen EW

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

activos_volumen= pd.read_csv('etf_data_volumen.csv',index_col=0)
activos_volumen.index = pd.to_datetime(activos_volumen.index)
new_index = pd.date_range(start=activos_volumen.index.min(), end=activos_volumen.index.max(), freq='B')
activos_volumen = activos_volumen.reindex(new_index, method='ffill')
activos_volumen = activos_volumen.loc[:'2023-06-30']
activos_volumen

#activos_close = activos_close.loc['2015-08-24':'2023-06-30']

#etiquetas = prueba.loc['2013-08-19':'2023-08-18',['Theme']]
#word_to_number = {'Recovery': 0, 'Reflection': 1, 'Overheat': 2, 'Stagflation': 3}
#etiquetas = etiquetas.replace(word_to_number)
#etiquetas = etiquetas.iloc[-2050:,:]

def obtener_precios_EW(activos_close, activos_volumen,n_activos,capital_inicial,com, etiquetas):

    # creamos listas a rellenar
    serie_EW = []
    comision_total = 0# inicializamos la comision
    for i in range(22,len(activos_close)):# for que va leyendo el dataframe de datos
        if i==22 or (etiquetas.iloc[i,0] != etiquetas.iloc[i-1,0]): # si hay cambio de mes se rebalancea
            if i==22:# si es el primer dia del dataframe se utiliza el capital inicial, sino la valorizacion de la serie de precios de la estrategia
                capital = capital_inicial
            else:
                capital = delta + (n_acciones*activos_close[activos_EW].iloc[i-1]).sum() 

            volu_activos = activos_volumen[i-30:i-1].sum() # calculo el volumen de los ultimos 20 dias de cada activo
            activos_EW = volu_activos.sort_values(ascending = False)[0:n_activos].index # me quedo con los 10 que mas volumen hayan tenido en los ultimos 20 dias
            n_acciones = (capital/10)//activos_close[activos_EW].iloc[i-1] # se calculan la cantidad de acciones a comprar de cada uno
            capital_invertido = (n_acciones*activos_close[activos_EW].iloc[i]).sum() # se calcula cuanto capital queda invertido realmente ya que no se pueden comprar fracciones de una accion
            delta = capital - capital_invertido # calculamos el diferencial entre el capital disponible al que realmente se invirtio
            comision = capital_invertido*com # se calcula la comision
            comision_total = comision_total + comision# se agrega esta comision al costo de comision total acumulada de la estrategia

        serie_EW.append((n_acciones*activos_close[activos_EW].iloc[i]).sum() + delta) # se obtiene el valor de hoy de la estrategia y se une a la lista para crear la serie de precios

    #Aqui se grafica la serie hitorica de la estrategia junto con la volatilidad de la misma
    serie_EW = pd.DataFrame(serie_EW)
    serie_EW.set_index(activos_close.index[22:], inplace=True)
    # Se grafica la serie historica de la estrategia    
    plt.figure()
    plt.plot(serie_EW, label = 'Serie Volumen')
    plt.title('Serie Precios Volumen')
    plt.xlabel('Fechas')
    plt.ylabel('Precio')
    plt.legend()

    
    rent_EW = np.log(serie_EW).diff().dropna(axis=0)
    vol_EW = rent_EW.rolling(window=20).std()
    # Se grafica la volatilidad historica de la estrategia
    plt.figure()
    plt.plot(vol_EW, label = 'Volatilidad Serie Volumen')
    plt.title('Volatilidad Volumen')
    plt.xlabel('Fechas')
    plt.ylabel('Volatilidad')
    plt.legend()    


    return serie_EW
