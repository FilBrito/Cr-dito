# ============================================================
# PROJETO: CRÉDITO
# MÓDULO: CÁLCULOS
# Arquivo: backend/calculos.py
# ============================================================

import numpy as np
import pandas as pd

from scipy.stats import gmean


# ------------------------------------------------------------
# 1. PARÂMETROS REGIONAIS
# ------------------------------------------------------------

IRRADIACAO_REGIONAL = {
    1: 5.2,  # Norte
    2: 5.8,  # Nordeste
    3: 5.5,  # Centro-Oeste
    4: 4.8,  # Sudeste
    5: 4.4   # Sul
}


# ------------------------------------------------------------
# 2. PARÂMETROS DAS CLASSES DOS SISTEMAS
# ------------------------------------------------------------

CLASSES = {
    1: {"y": 0.008148, "Y": 0.000679, "R": [25, 30]},
    2: {"y": 0.010519, "Y": 0.000877, "R": [15, 30]},
    3: {"y": 0.007544, "Y": 0.000629, "R": [25, 35]},
    4: {"y": 0.012883, "Y": 0.001074, "R": [10, 30]},
    5: {"y": 0.057615, "Y": 0.004801, "R": [1, 15]},
    6: {"y": 0.012883, "Y": 0.001074, "R": [10, 30]}
}


# ------------------------------------------------------------
# 3. VALIDAÇÃO DOS PARÂMETROS
# ------------------------------------------------------------

def validar_parametros(dados):

    obrigatorios = [
        "A0", "At", "C0", "CA", "Payback",
        "PN", "N", "H", "Classe", "validade"
    ]

    for campo in obrigatorios:
        if campo not in dados:
            raise ValueError(
                f"Parâmetro obrigatório ausente: {campo}"
            )

    if dados["A0"] < 0:
        raise ValueError("Ano de instalação inválido.")

    if dados["At"] < dados["A0"]:
        raise ValueError(
            "O ano de referência deve ser igual ou posterior "
            "ao ano de instalação."
        )

    if dados["C0"] <= 0 or dados["CA"] <= 0:
        raise ValueError(
            "Os consumos devem ser maiores que zero."
        )

    if dados["Payback"] <= 0:
        raise ValueError("O Payback deve ser maior que zero.")

    if dados["PN"] <= 0 or dados["N"] <= 0:
        raise ValueError(
            "A potência e o número de placas devem ser positivos."
        )

    if dados["H"] not in IRRADIACAO_REGIONAL:
        raise ValueError("Região de instalação inválida.")

    if dados["Classe"] not in CLASSES:
        raise ValueError("Classe do sistema inválida.")

    if dados["validade"] <= 0:
        raise ValueError(
            "A validade dos créditos deve ser maior que zero."
        )


# ------------------------------------------------------------
# 4. MOTOR MATEMÁTICO
# ------------------------------------------------------------

def realizar_calculos(dados):

    # Validar parâmetros recebidos
    validar_parametros(dados)

    # Extrair os parâmetros
    A0 = dados["A0"]
    At = dados["At"]
    C0 = dados["C0"]
    CA = dados["CA"]
    Payback = dados["Payback"]
    PN = dados["PN"]
    N = dados["N"]
    H = dados["H"]
    Classe = dados["Classe"]
    validade = dados["validade"]

    # --------------------------------------------------------
    # 4.1. Características regionais
    # --------------------------------------------------------

    h = IRRADIACAO_REGIONAL[H]

    # Produção anual inicial (kWh)
    P0 = N * h * 365 * PN / 1000

    # Produção mensal inicial (kWh)
    Po = N * h * 30 * PN / 1000

    # --------------------------------------------------------
    # 4.2. Características da classe do sistema
    # --------------------------------------------------------

    y = CLASSES[Classe]["y"]
    Y = CLASSES[Classe]["Y"]

    R = gmean(CLASSES[Classe]["R"])

    # Vida útil estimada em meses
    r = 12 * R

    # --------------------------------------------------------
    # 4.3. Período de análise
    # --------------------------------------------------------

    Af = A0 + 36

    Ano = np.arange(A0, Af)

    t = Ano - A0

    # --------------------------------------------------------
    # 4.4. Taxa de crescimento do consumo
    # --------------------------------------------------------

    if At == A0:

        if CA != C0:
            raise ValueError(
                "Para calcular o crescimento do consumo, "
                "o ano de referência deve ser posterior "
                "ao ano de instalação quando os consumos "
                "forem diferentes."
            )

        i = 1.0

    else:

        i = (CA / C0) ** (1 / (At - A0))

    # --------------------------------------------------------
    # 4.5. Produção anual com degradação
    # --------------------------------------------------------

    P = P0 * np.exp(-y * t)

    # --------------------------------------------------------
    # 4.6. Consumo anual crescente
    # --------------------------------------------------------

    C = C0 * (i ** t)

    # --------------------------------------------------------
    # 4.7. Construção do DataFrame
    # --------------------------------------------------------

    DF = pd.DataFrame({

        "Ano": Ano,
        "Produção": P,
        "Consumo": C

    })

    # --------------------------------------------------------
    # 4.8. Satisfação e utilidade
    # --------------------------------------------------------

    DF["Satisfação"] = (
        DF["Produção"] - DF["Consumo"]
    )

    DF["Utilidade"] = (
        DF["Satisfação"].cumsum()
    )

    # --------------------------------------------------------
    # 4.9. Análise dos créditos de geração
    # --------------------------------------------------------

    DF['Créditos Válidos'] = (
        DF['Satisfação']
        .rolling(window=validade, min_periods=1).
        sum().clip(lower=0)
    )

    creditos_gerados_acum = (
        DF['Satisfação'].
        clip(lower=0).cumsum()
    )

    credito_consumido_acum = (
        -DF['Satisfação'].
        clip(upper=0)).cumsum()
    )

    DF['Crédito perdido'] = (
        (creditos_gerados_acum - DF['Créditos Válidos'] - credito_consumido_acum)
        .clip(lower=0).cummax()
    )

    # --------------------------------------------------------
    # 4.10. Indicadores do ano de referência
    # --------------------------------------------------------

    referencia = DF.loc[DF["Ano"] == At].iloc[0]

    indicadores = {

        "producao_inicial": P0,

        "producao_mensal_inicial": Po,

        "producao_referencia": referencia["Produção"],

        "consumo_referencia": referencia["Consumo"],

        "satisfacao_referencia": referencia["Satisfação"],

        "utilidade_referencia": referencia["Utilidade"],

        "creditos_validos": referencia["Créditos Válidos"],

        "credito_perdido": referencia["Crédito perdido"],

        "crescimento_consumo": i,

        "degradacao_anual": y,

        "degradacao_mensal": Y,

        "vida_util_anos": R,

        "vida_util_meses": r,

        "payback_meses": Payback * 12

    }

    # --------------------------------------------------------
    # 4.11. Retorno dos resultados
    # --------------------------------------------------------

    return {

        "tabela": DF,

        "indicadores": indicadores,

        "parametros": dados

    }
