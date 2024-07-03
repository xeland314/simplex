from advanced_simplex import *

# Ejecución por datos

simplex = Simplex(
    numero_de_variables=12,
    funcion_objetivo=FuncionObjetivo(
        "z = 16*x1 + 10*x2 + 12*x3 + 13*x4 + 26*x5 + 20*x6 + 30*x7 + 21*x8 + 22*x9 + 15*x10 + 23*x11 + 14x12"
    ),
    metodo=Simplex.MINIMIZAR,
    restricciones=[
        ExpresionAlgebraica("x1 + x2 + x3 + x4 <= 30"),
        ExpresionAlgebraica("x5 + x6 + x7 + x8 <= 15"),
        ExpresionAlgebraica("x9 + x10 + x11 + x12 <= 25"),
        ExpresionAlgebraica("x1 + x5 + x9 >= 15"),
        ExpresionAlgebraica("x2 + x6 + x10 >= 25"),
        ExpresionAlgebraica("x3 + x7 + x11 >= 10"),
        ExpresionAlgebraica("x4 + x8 + x12 >= 20"),
    ],
)
simplex.resolver_problema()
simplex.mostrar_resultados()
