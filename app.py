import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import symbols, sympify, lambdify
import time

# CONFIGURACIÓN
st.set_page_config(
    page_title="Sumas de Riemann",
    page_icon="📘",
    layout="wide"
)

# ESTILO PERSONALIZADO
st.markdown("""
<style>

/* FONDO TOTAL */
html, body, [class*="css"]  {
    background-color: #050816;
    color: white;
}
header {
    background-color: #050816 !important;
}

input {

    background-color: #111827 !important;

    color: white !important;
}


/* APP */
.stApp {
    background-color: #050816;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #0B1120;
    border-right: 1px solid #00FFFF;
}

/* TÍTULOS */
h1 {
    color: #00FFFF;
    text-align: center;
    font-size: 52px;
    font-weight: 800;
}

h2, h3, h4 {
    color: white;
}

/* TEXTO */
p, label, div {
    color: white;
}

/* BOTONES */
.stButton>button {

    background-color: #00FFFF;
    color: black;

    border-radius: 12px;

    border: none;

    font-weight: bold;

    transition: 0.3s;
}

.stButton>button:hover {

    background-color: #00CCFF;
    transform: scale(1.05);
}

/* INPUTS */
.stNumberInput input {

    background-color: #111827;
    color: white;
}

/* SELECTBOX */

div[data-baseweb="select"] > div {

    background-color: #111827 !important;

    color: white !important;

    border: 1px solid #00FFFF;

    border-radius: 10px;
}

/* TEXTO */

div[data-baseweb="select"] span {

    color: white !important;
}

/* MENÚ DESPLEGABLE */

div[role="listbox"] {

    background-color: #111827 !important;

    color: white !important;
}

/* OPCIONES */

div[role="option"] {

    background-color: #111827 !important;

    color: white !important;
}

/* HOVER */

div[role="option"]:hover {

    background-color: #00FFFF !important;

    color: black !important;
}
ul {

    background-color: #111827 !important;
}

li {

    background-color: #111827 !important;

    color: white !important;
}

/* OPCIÓN SELECCIONADA */

li:hover {

    background-color: #00FFFF !important;

    color: black !important;
}
/* TEXTO DEL SELECT */

div[data-baseweb="select"] span {

    color: white !important;
}
/* SLIDER */
.stSlider {

    color: #00FFFF;
}

/* MÉTRICAS */
[data-testid="stMetricValue"] {

    color: #00FFFF;
    font-size: 32px;
}

/* GRÁFICO */
.js-plotly-plot {

    border-radius: 20px;
    overflow: hidden;
    border: 1px solid #00FFFF;
}
/* TOOLBAR */

[data-testid="stToolbar"] {

    background-color: #050816;
}

/* MAIN */

.main {

    background-color: #050816;
}

</style>
""", unsafe_allow_html=True)
# TÍTULO
st.title("Software Interactivo de Sumas de Riemann")


st.markdown("""
<div style='text-align:center;'>

<h3 style='color:#A0AEC0;'>

Simulador matemático interactivo para el análisis
de aproximaciones integrales mediante sumas de Riemann.

</h3>

</div>
""", unsafe_allow_html=True)

# PESTAÑAS
tab1, tab2 = st.tabs([
    "📚 Fundamentación Teórica",
    "🧮 Simulador"
])
with tab1:

    st.header("¿Qué son las sumas de Riemann?")

    st.write("""
    Las sumas de Riemann son un método utilizado para aproximar
    el área bajo una curva mediante rectángulos.
    """)

    st.latex(r"\Delta x = \frac{b-a}{n}")

    st.latex(r"\sum_{i=0}^{n-1} f(x_i)\Delta x")

    st.write("""
    A medida que aumenta el número de rectángulos,
    la aproximación se acerca al valor exacto de la integral definida.
    """)
    
with tab2: 
# SIDEBAR
st.sidebar.header("Configuración")

funciones = {

    "Parábola → x²": "x**2",

    "Cúbica → x³": "x**3",

    "Seno → sin(x)": "sin(x)",

    "Coseno → cos(x)": "cos(x)",

    "Exponencial → e^x": "exp(x)",

    "Lineal → x": "x",

    "Polinómica → x³ - 4x": "x**3 - 4*x",

    "Trigonométrica → sin(x)": "sin(x)",

    "Gaussiana → e^(-x²)": "exp(-x**2)"
}

opcion = st.sidebar.selectbox(
    "Seleccione una función",
    list(funciones.keys())
)

funcion_texto = funciones[opcion]

a = st.sidebar.number_input(
    "Inicio del intervalo",
    value=0.0
)

b = st.sidebar.number_input(
    "Final del intervalo",
    value=5.0
)

n = st.sidebar.slider(
    "Número máximo de rectángulos",
    1,
    100,
    20
)

tipo = st.sidebar.selectbox(
    "Tipo de suma",
    [
        "Izquierda",
        "Derecha",
        "Punto medio"
    ]
)

animar = st.sidebar.button("▶ Iniciar animación")

# ECUACIONES
st.latex(r"\Delta x = \frac{b-a}{n}")

st.latex(r"\sum_{i=0}^{n-1} f(x_i)\Delta x")

# CONVERTIR FUNCIÓN
x = symbols('x')

try:

    expr = sympify(funcion_texto)
    f = lambdify(x, expr, "numpy")

    # DATOS
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)

    # CONTENEDOR
    grafica = st.empty()

    # CREAR FIGURA
    def crear_figura(k):

        dx = (b - a) / k

        fig = go.Figure()

        # CURVA
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                name='f(x)',
                line=dict(
                    color='#00FFFF',
                    width=4
                )
            )
        )

        suma = 0

        # RECTÁNGULOS
        for i in range(k):

            if tipo == "Izquierda":
                xi = a + i * dx

            elif tipo == "Derecha":
                xi = a + (i + 1) * dx

            else:
                xi = a + (i + 0.5) * dx

            altura = f(xi)

            suma += altura * dx

            x_rect = [
                xi if tipo != "Derecha" else xi - dx,
                xi if tipo != "Derecha" else xi - dx,
                xi + dx if tipo != "Derecha" else xi,
                xi + dx if tipo != "Derecha" else xi,
                xi if tipo != "Derecha" else xi - dx
            ]

            y_rect = [0, altura, altura, 0, 0]

            fig.add_trace(
                go.Scatter(
                    x=x_rect,
                    y=y_rect,
                    fill="toself",
                    mode='lines',
                    fillcolor='rgba(0,255,170,0.35)',
                    line=dict(color='#00FFAA'),
                    showlegend=False
                )
            )

        # ESTILO DEL GRÁFICO
        fig.update_layout(

            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',

            font=dict(color='white'),

            title={
                'text': f'Suma de Riemann ({tipo})',
                'x':0.5
            },

            xaxis=dict(
                gridcolor='gray',
                zerolinecolor='white'
            ),

            yaxis=dict(
                gridcolor='gray',
                zerolinecolor='white'
            ),

            height=650
        )

        return fig, suma

    # ANIMACIÓN
    if animar:

        for k in range(1, n + 1):

            fig, suma = crear_figura(k)

            grafica.plotly_chart(
                fig,
                use_container_width=True
            )

            time.sleep(0.15)

    else:

        fig, suma = crear_figura(n)

        grafica.plotly_chart(
            fig,
            use_container_width=True
        )

    # RESULTADOS
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Área aproximada",
        round(suma, 6)
    )

    col2.metric(
        "Rectángulos",
        n
    )

    col3.metric(
        "Método",
        tipo
    )

except:

    st.error("Error en la función ingresada")