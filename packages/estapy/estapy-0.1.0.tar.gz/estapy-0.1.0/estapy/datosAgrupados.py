import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class DatosAgrupados:
    """
    Clase para calcular estadísticos descriptivos para datos agrupados.
    """

    def __init__(self, datos):
        self.datos = np.array(datos)
        if len(self.datos) == 0:
            raise ValueError("La lista de datos no puede estar vacía.")
        if not np.issubdtype(self.datos.dtype, np.number):
            raise ValueError("Todos los datos deben ser numéricos.")
        if len(self.datos) < 2:
            raise ValueError(
                "Se requieren al menos dos datos para calcular estadísticos."
            )

        self.n = len(self.datos)
        self.k = int(np.ceil(1 + 3.322 * np.log10(self.n)))
        self.rango = max(self.datos) - min(self.datos)
        self.amplitud = self.rango / self.k

        # Limites como puntos de corte, no tuplas
        self.limites = np.linspace(
            round(min(self.datos), 3), round(max(self.datos), 3), self.k + 1
        )

    def tabla_frecuencias(self):
        """
        Devuelve la tabla de frecuencias de los datos agrupados.
        """
        muestra = {}
        muestra["limites"] = self.limites
        muestra["n"] = self.n

        # Clasificación por intervalos
        cortes = pd.cut(self.datos, bins=self.limites, include_lowest=True)
        muestra["nj"] = cortes.value_counts().sort_index()
        muestra["intervalos"] = cortes.astype(str)
        muestra["hj"] = muestra["nj"] / muestra["n"]
        muestra["Nj"] = muestra["nj"].cumsum()
        muestra["Hj"] = muestra["hj"].cumsum()

        # Marca de clase
        marca_clase = np.round((self.limites[:-1] + self.limites[1:]) / 2, 3)
        muestra["marca_clase"] = marca_clase

        # Armar tabla
        tabla = pd.DataFrame(
            {
                "Intervalo": muestra["nj"].index.astype(str),
                "Marca de clase": muestra["marca_clase"],
                "Frecuencia (nᵢ)": muestra["nj"].values,
                "Frecuencia relativa (hᵢ)": muestra["hj"].values,
                "Frecuencia acumulada (Nᵢ)": muestra["Nj"].values,
                "Frecuencia acumulada relativa (Hᵢ)": muestra["Hj"].values,
            }
        )

        self.tabla = tabla
        return tabla

    def media(self):
        """
        Calcula la media de los datos agrupados.
        """
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        f = self.tabla["Frecuencia (nᵢ)"]
        x = self.tabla["Marca de clase"]
        return (f * x).sum() / self.n

    def mediana(self):
        """Calcula la mediana de los datos agrupados."""
        return self.percentil(50)

    def moda(self):
        """
        Calcula la moda de los datos agrupados.
        """
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        max_frecuencia = self.tabla["Frecuencia (nᵢ)"].max()
        modas = self.tabla[self.tabla["Frecuencia (nᵢ)"] == max_frecuencia]

        if len(modas) == 1:
            return modas["Marca de clase"].values[0]
        else:
            return modas["Marca de clase"].values.tolist()

    def percentil(self, k, debug=False):
        """
        Calcula el percentil k para los datos agrupados.
        Si debug=True, imprime información interna del cálculo.
        """
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        frecuencias = self.tabla["Frecuencia (nᵢ)"].values
        acumuladas = self.tabla["Frecuencia acumulada (Nᵢ)"].values
        limites = self.limites
        pos = k * self.n / 100

        for i, Ni in enumerate(acumuladas):
            if Ni >= pos:
                Li = limites[i]  # Límite inferior del intervalo
                ai = limites[i + 1] - limites[i]  # Amplitud del intervalo
                Ni_prev = 0 if i == 0 else acumuladas[i - 1]
                fi = frecuencias[i]
                Pk = Li + ai * ((pos - Ni_prev) / fi)

                if debug:
                    print(f"[DEBUG] Percentil {k}")
                    print(f"Intervalo: {limites[i]} - {limites[i + 1]}")
                    print(f"Límite inferior (Li): {Li}")
                    print(f"Amplitud (ai): {ai}")
                    print(f"Nᵢ₋₁: {Ni_prev}")
                    print(f"fᵢ: {fi}")
                    print(f"Posición teórica: {pos}")
                    print(f"Pk = {Pk}")

                return Pk

        raise ValueError("No se pudo calcular el percentil.")

    def varianza(self):
        """
        Calcula la varianza de los datos agrupados.
        """
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        media = self.media()
        f = self.tabla["Frecuencia (nᵢ)"]
        x = self.tabla["Marca de clase"]
        varianza = sum(f * (x - media) ** 2) / (self.n - 1)
        return varianza

    def desviacion_estandar(self):
        """
        Calcula la desviación estándar de los datos agrupados.
        """
        return np.sqrt(self.varianza())

    def rango_intercuartil(self):
        """
        Calcula el rango intercuartil (IQR) de los datos agrupados.
        """
        Q1 = self.percentil(25)
        Q3 = self.percentil(75)
        return Q3 - Q1

    def coeficiente_variacion(self):
        """
        Calcula el coeficiente de variación de los datos agrupados.
        """
        return (self.desviacion_estandar() / self.media()) * 100

    def valores_atipicos(self):
        """
        Identifica los valores atípicos en los datos agrupados.
        """
        lim_inf = self.percentil(25) - 1.5 * self.rango_intercuartil()
        lim_sup = self.percentil(75) + 1.5 * self.rango_intercuartil()
        atipicos = self.datos[(self.datos < lim_inf) | (self.datos > lim_sup)]
        print("Límite Inferior:", lim_inf)
        print("Límite Superior:", lim_sup)

        if len(atipicos) == 0:
            print("No hay valores atípicos.")

    def resumen(self):
        """
        Devuelve un resumen estadístico de los datos agrupados.
        """
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        resumen = {
            "Min": min(self.datos),
            "Q1": self.percentil(25),
            "Media": self.media(),
            "Mediana": self.mediana(),
            "Moda": self.moda(),
            "Q3": self.percentil(75),
            "Max": max(self.datos),
        }
        return resumen

    def medidas_variacion(self):
        """
        Devuelve un resumen de las medidas de variación.
        """
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        medidas = {
            "Media": self.media(),
            "Varianza": self.varianza(),
            "Desviación Estándar": self.desviacion_estandar(),
            "Rango Intercuartil": self.rango_intercuartil(),
            "Rango": self.rango,
            "Coeficiente de Variación (%)": self.coeficiente_variacion(),
        }
        return medidas

    def boxplot(self):
        """
        Genera un boxplot aproximado con seaborn a partir de los datos agrupados.
        """
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        # Simular datos
        simulados = []
        for _, fila in self.tabla.iterrows():
            simulados.extend(
                [round(fila["Marca de clase"], 3)] * int(fila["Frecuencia (nᵢ)"])
            )

        # Gráfico con seaborn
        plt.figure(figsize=(7, 4))
        sns.boxplot(x=simulados, color="lightcoral", fliersize=5, width=0.4)
        plt.title("Boxplot de datos agrupados")
        plt.xlabel("Valor")
        plt.grid(axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def histograma(self):
        """
        Genera un histograma con densidad de datos agrupados usando seaborn.
        """
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        # Calcular densidad
        ancho = self.limites[1] - self.limites[0]
        densidades = self.tabla["Frecuencia (nᵢ)"] / (ancho * self.n)

        # Crear dataframe temporal para graficar
        df = pd.DataFrame(
            {"Clase": self.tabla["Marca de clase"], "Densidad": densidades}
        )

        # Gráfico bonito con seaborn
        plt.figure(figsize=(8, 5))
        sns.barplot(
            x="Clase", y="Densidad", data=df, color="skyblue", edgecolor="black"
        )

        plt.xlabel("Marca de clase")
        plt.ylabel("Densidad")
        plt.title("Histograma de densidad (datos agrupados)")
        plt.grid(True , linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def __str__(self):
        if not hasattr(self, "tabla"):
            self.tabla_frecuencias()

        resumen = self.resumen()
        medidas = self.medidas_variacion()

        resumen_str = "\n".join(
            [f"{key}: {format(value, '.3g')}" for key, value in resumen.items()]
        )
        medidas_str = "\n".join(
            [f"{key}: {format(value, '.3g')}" for key, value in medidas.items()]
        )

        return f"Resumen:\n{resumen_str}\n\nMedidas de variación:\n{medidas_str}\n\nTabla de frecuencias:\n{self.tabla.to_string(index=False)}"