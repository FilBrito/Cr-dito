
# Crédito
### Sistema de Análise de Geração e Créditos Energéticos

## 1. Apresentação

O **Crédito** é uma aplicação computacional desenvolvida em Python, com interface web baseada em Flask e HTML, destinada à análise da geração de energia elétrica por sistemas fotovoltaicos, considerando a evolução do consumo energético, a degradação dos módulos e a dinâmica dos créditos de energia.

A ferramenta permite realizar simulações ao longo da vida útil estimada do sistema, proporcionando uma análise da relação entre produção e consumo de energia, satisfação energética, utilidade acumulada e expiração dos créditos de geração.

O objetivo é oferecer uma ferramenta de apoio à análise energética, permitindo visualizar diferentes cenários e compreender os impactos da evolução da produção fotovoltaica e do consumo energético ao longo do tempo.

---

## 2. Objetivos

A aplicação tem como principais objetivos:

- Estimar a produção anual de energia elétrica de sistemas fotovoltaicos.
- Projetar o crescimento do consumo energético.
- Considerar a degradação dos módulos fotovoltaicos.
- Analisar a relação entre produção e consumo.
- Calcular a satisfação energética e a utilidade acumulada.
- Estimar os créditos energéticos válidos.
- Identificar os créditos sujeitos à expiração.
- Apresentar os resultados por meio de tabelas e gráficos interativos.

---

## 3. Funcionalidades

### 3.1. Entrada de dados

O usuário pode informar os parâmetros necessários para a simulação:

- Ano de instalação do sistema.
- Ano de referência.
- Consumo inicial anual.
- Consumo atual anual.
- Payback do sistema.
- Potência nominal dos módulos fotovoltaicos.
- Número de módulos instalados.
- Região geográfica de instalação.
- Classe de degradação do sistema.
- Período de validade dos créditos energéticos.

### 3.2. Análise da geração

A aplicação estima a produção de energia elétrica considerando:

- Potência nominal instalada.
- Horas médias de sol pleno por região.
- Taxa de degradação anual.
- Período de operação do sistema.

### 3.3. Análise do consumo

O consumo energético é projetado utilizando uma taxa de crescimento composto, calculada a partir dos valores inicial e atual informados.

### 3.4. Análise energética

São calculados:

- Produção anual.
- Consumo anual.
- Satisfação energética.
- Utilidade acumulada.
- Créditos válidos.
- Créditos perdidos por expiração.

### 3.5. Visualização dos resultados

A aplicação apresenta:

- Indicadores de desempenho.
- Tabelas com os resultados da simulação.
- Gráfico de produção versus consumo.
- Gráfico de satisfação e utilidade.
- Gráfico de créditos válidos e créditos perdidos.

---

## 4. Tecnologias utilizadas

O projeto utiliza as seguintes tecnologias:

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem de programação |
| Flask | Desenvolvimento da aplicação web |
| HTML5 | Estrutura da interface |
| CSS3 | Estilização da interface |
| Bootstrap 5.3 | Layout responsivo |
| JavaScript | Interatividade da interface |
| NumPy | Operações matemáticas |
| Pandas | Manipulação de dados |
| SciPy | Operações estatísticas |
| Plotly | Visualização gráfica interativa |
| Matplotlib | Visualização gráfica complementar |
| OpenPyXL | Suporte à manipulação de arquivos Excel |

---

## 5. Estrutura do projeto

```text
Crédito/
│
├── app.py
├── requirements.txt
├── README.md
│
├── backend/
│   ├── __init__.py
│   └── calculos.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── scripts.js
│   │
│   └── img/
│       └── logo.png
│
└── .venv/
```

### Descrição dos arquivos

**app.py:** responsável pela inicialização do Flask, recebimento dos parâmetros e integração entre interface e processamento matemático.

**backend/calculos.py:** contém as funções responsáveis pelos cálculos e pela geração dos resultados da simulação.

**templates/index.html:** estrutura da interface web e apresentação dos resultados.

**static/css/style.css:** contém as configurações visuais da aplicação.

**static/js/scripts.js:** destinado às funcionalidades JavaScript da interface.

**static/img/logo.png:** arquivo de identidade visual da aplicação.

**requirements.txt:** lista as dependências necessárias para executar o projeto.

---

## 6. Requisitos de instalação

Para executar a aplicação, recomenda-se possuir:

- Python 3.10 ou superior.
- Gerenciador de pacotes pip.
- Navegador atualizado.
- Conexão com a internet para carregar as bibliotecas externas do Bootstrap e Plotly.

---

## 7. Instalação

### 7.1. Clonar ou obter o projeto

Disponibilize a pasta do projeto em seu computador.

### 7.2. Criar o ambiente virtual

No terminal, execute:

```bash
python -m venv .venv
```

### 7.3. Ativar o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

### 7.4. Instalar as dependências

Execute:

```bash
pip install -r requirements.txt
```

---

## 8. Execução da aplicação

Após a instalação das dependências, execute:

```bash
python app.py
```

Por padrão, a aplicação estará disponível no seguinte endereço:

http://127.0.0.1:5000

A interface poderá ser acessada diretamente pelo navegador.

Para encerrar a aplicação, pressione `CTRL + C` no terminal.

---

## 9. Metodologia de cálculo

A aplicação utiliza relações matemáticas para estimar a evolução temporal da geração e do consumo de energia elétrica.

### 9.1. Produção inicial

A produção anual inicial é estimada considerando a potência instalada e as horas médias de sol pleno:

\[
P_0 = N \cdot h \cdot 365 \cdot \frac{PN}{1000}
\]

Onde:

- \(P_0\): produção anual inicial (kWh).
- \(N\): número de módulos fotovoltaicos.
- \(h\): horas médias de sol pleno por dia.
- \(PN\): potência nominal de cada módulo (W).

### 9.2. Degradação da produção

A produção anual é projetada considerando uma taxa de degradação exponencial:

\[
P(t) = P_0 \cdot e^{-yt}
\]

Onde:

- \(P(t)\): produção no período analisado.
- \(y\): taxa de degradação anual.
- \(t\): tempo decorrido desde a instalação.

### 9.3. Crescimento do consumo

O crescimento composto do consumo é estimado por:

\[
i = \left(\frac{CA}{C_0}\right)^{\frac{1}{At-A_0}}
\]

O consumo projetado é calculado por:

\[
C(t) = C_0 \cdot i^t
\]

Onde:

- \(C_0\): consumo inicial.
- \(CA\): consumo atual.
- \(A_0\): ano de instalação.
- \(At\): ano de referência.
- \(i\): fator anual de crescimento.

### 9.4. Satisfação energética

A satisfação energética representa a diferença entre a produção e o consumo:

\[
S(t) = P(t) - C(t)
\]

### 9.5. Utilidade acumulada

A utilidade acumulada é obtida pela soma das satisfações energéticas ao longo do tempo:

\[
U(t) = \sum_{k=0}^{t} S(k)
\]

### 9.6. Créditos energéticos

A aplicação considera uma janela móvel correspondente ao período de validade informado pelo usuário para estimar os créditos válidos.

A diferença entre a utilidade acumulada e os créditos válidos representa o crédito perdido por expiração, conforme a metodologia implementada.

---

## 10. Considerações metodológicas

Os resultados apresentados dependem dos parâmetros fornecidos pelo usuário e das premissas matemáticas adotadas.

As estimativas de produção utilizam valores regionais médios de horas de sol pleno, não substituindo estudos de irradiação solar específicos para cada localidade.

A metodologia de créditos deve ser interpretada como um modelo de simulação, não necessariamente como uma reprodução integral das regras regulatórias vigentes para compensação de energia elétrica.

---

## 11. Melhorias futuras

Entre as possíveis evoluções do projeto, destacam-se:

- Exportação dos resultados para Excel.
- Geração de relatórios em PDF.
- Inclusão de indicadores econômicos.
- Análise de diferentes cenários de degradação.
- Simulação de diferentes configurações fotovoltaicas.
- Aprimoramento da metodologia de expiração dos créditos.
- Armazenamento histórico das simulações.
- Implementação de interface para comparação entre cenários.

---

## 12. Licença

A licença de utilização e distribuição deste projeto deverá ser definida pelo autor.

---

**Projeto: Crédito**

Sistema de Análise de Geração e Créditos Energéticos.
