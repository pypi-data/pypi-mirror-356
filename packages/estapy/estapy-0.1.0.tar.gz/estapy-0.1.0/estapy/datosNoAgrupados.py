import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class DatosNoAgrupados:
    """
    Clase para calcular estadísticos descriptivos para datos no agrupados.
    """

    def __init__(self, datos):
        self.datos = np.array(datos)
        if len(self.datos) == 0:
            raise ValueError("La lista de datos no puede estar vacía.")
        if not np.issubdtype(self.datos.dtype, np.number):
            raise ValueError("Todos los datos deben ser numéricos.")
        self.n = len(self.datos)
        
    def tabla_frecuencias(self):
        """
        Retorna una tabla de frecuencias para datos no agrupados.
        """
        valores, cuentas = np.unique(self.datos, return_counts=True)
        relativas = cuentas / self.n
        tabla = pd.DataFrame({
            "Valor": valores,
            "Frecuencia absoluta": cuentas,
            "Frecuencia relativa": np.round(relativas, 3)
        })
        return tabla

    def media(self):
        return np.mean(self.datos)

    def mediana(self):
        return np.median(self.datos)

    def moda(self):
        valores, cuentas = np.unique(self.datos, return_counts=True)
        max_frec = np.max(cuentas)
        modas = valores[cuentas == max_frec]
        return modas.tolist() if len(modas) > 1 else modas[0]

    def varianza(self):
        return np.var(self.datos, ddof=1)

    def desviacion_estandar(self):
        return np.std(self.datos, ddof=1)

    def rango(self):
        return np.max(self.datos) - np.min(self.datos)

    def percentil(self, k):
        return np.percentile(self.datos, k)

    def rango_intercuartil(self):
        return self.percentil(75) - self.percentil(25)

    def coeficiente_variacion(self):
        return (self.desviacion_estandar() / self.media()) * 100

    def valores_atipicos(self):
        Q1 = self.percentil(25)
        Q3 = self.percentil(75)
        IQR = Q3 - Q1
        lim_inf = Q1 - 1.5 * IQR
        lim_sup = Q3 + 1.5 * IQR
        atipicos = self.datos[(self.datos < lim_inf) | (self.datos > lim_sup)]
        print("Límite Inferior:", lim_inf)
        print("Límite Superior:", lim_sup)
        return atipicos.tolist()

    def resumen(self):
        return {
            "Min": np.min(self.datos),
            "Q1": self.percentil(25),
            "Media": self.media(),
            "Mediana": self.mediana(),
            "Moda": self.moda(),
            "Q3": self.percentil(75),
            "Max": np.max(self.datos),
        }

    def medidas_variacion(self):
        return {
            "Media": self.media(),
            "Varianza": self.varianza(),
            "Desviación Estándar": self.desviacion_estandar(),
            "Rango Intercuartil": self.rango_intercuartil(),
            "Rango": self.rango(),
            "Coeficiente de Variación (%)": self.coeficiente_variacion(),
        }

    def boxplot(self):
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=self.datos, color="lightgreen", fliersize=5, width=0.4)
        plt.title("Boxplot de datos no agrupados")
        plt.grid(axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def histograma(self, bins='auto', kde=False):
        plt.figure(figsize=(7, 4))
        sns.histplot(self.datos, bins=bins, kde=kde, color="steelblue", edgecolor="black", stat='density')
        plt.title("Histograma de densidad (datos no agrupados)")
        plt.xlabel("Valor")
        plt.ylabel("Densidad")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def __str__(self):
        resumen = self.resumen()
        medidas = self.medidas_variacion()

        # ⚠️ Solución: usar str(v) si el valor es una lista
        resumen_str = "\n".join([
            f"{k}: {format(v, '.3g') if isinstance(v, (int, float)) else str(v)}"
            for k, v in resumen.items()
        ])
        medidas_str = "\n".join([
            f"{k}: {format(v, '.3g')}" for k, v in medidas.items()
        ])

        return f"Resumen:\n{resumen_str}\n\nMedidas de variación:\n{medidas_str}"
