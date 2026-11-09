
# ============================================================
# PROJETO: CRÉDITO
# SISTEMA DE ANÁLISE DE GERAÇÃO E CRÉDITOS ENERGÉTICOS
#
# Arquivo: app.py
# Descrição: Aplicação principal Flask
# ============================================================

from flask import Flask, render_template, request

from backend.calculos import realizar_calculos


# ------------------------------------------------------------
# 1. CONFIGURAÇÃO DA APLICAÇÃO
# ------------------------------------------------------------

app = Flask(__name__)

app.config["SECRET_KEY"] = "credito-chave-local"


# ------------------------------------------------------------
# 2. PARÂMETROS PADRÃO
# ------------------------------------------------------------

DADOS_PADRAO = {

    "A0": 2010,
    "At": 2025,

    "C0": 3000,
    "CA": 3600,

    "Payback": 3,

    "PN": 500,
    "N": 4,

    "H": 2,
    "Classe": 1,

    "validade": 5

}


# ------------------------------------------------------------
# 3. CONVERSÃO DOS DADOS DO FORMULÁRIO
# ------------------------------------------------------------

def obter_dados_formulario(formulario):

    dados = {

        "A0": int(formulario["A0"]),
        "At": int(formulario["At"]),

        "C0": float(formulario["C0"]),
        "CA": float(formulario["CA"]),

        "Payback": float(formulario["Payback"]),

        "PN": float(formulario["PN"]),
        "N": int(formulario["N"]),

        "H": int(formulario["H"]),
        "Classe": int(formulario["Classe"]),

        "validade": int(formulario["validade"])

    }

    return dados


# ------------------------------------------------------------
# 4. ROTA PRINCIPAL
# ------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    # Inicialização
    resultados = None
    tabela = None
    indicadores = None
    erro = None

    # Valores inicialmente apresentados no formulário
    dados = DADOS_PADRAO.copy()

    # --------------------------------------------------------
    # Recebimento do formulário
    # --------------------------------------------------------

    if request.method == "POST":

        try:

            # Obter parâmetros enviados pelo usuário
            dados = obter_dados_formulario(request.form)

            # Executar o backend matemático
            resultados = realizar_calculos(dados)

            # Extrair resultados
            tabela = resultados["tabela"]

            indicadores = resultados["indicadores"]

        except ValueError as e:

            erro = str(e)

        except (KeyError, TypeError, OverflowError):

            erro = (
                "Verifique os campos preenchidos. "
                "Todos os parâmetros devem possuir valores válidos."
            )

        except Exception:

            app.logger.exception(
                "Erro inesperado durante a simulação."
            )

            erro = (
                "Ocorreu um erro inesperado durante o processamento. "
                "Verifique os parâmetros e tente novamente."
            )

    # --------------------------------------------------------
    # Renderização da página
    # --------------------------------------------------------

    return render_template(

        "index.html",

        dados=dados,

        tabela=tabela,

        indicadores=indicadores,

        resultados=resultados,

        erro=erro

    )


# ------------------------------------------------------------
# 5. EXECUÇÃO DA APLICAÇÃO
# ------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=3011)
