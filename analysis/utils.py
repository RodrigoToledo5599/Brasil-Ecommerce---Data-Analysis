"""Funções de apoio usadas pelos notebooks de análise (estilo dos gráficos e carregamento da base)."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Cores (paleta validada para daltonismo)
AZUL = "#2a78d6"      # cor principal
LARANJA = "#eb6834"   # destaque (atraso, problema)
CINZA = "#b8b7b2"     # contexto / sem destaque
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
GRADE = "#e8e7e3"

NORDESTE = ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"]

PASTA_FIGURAS = Path("figures")


def aplicar_estilo():
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": GRADE,
        "axes.labelcolor": TEXTO_2,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlecolor": TEXTO,
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRADE,
        "grid.linewidth": 0.8,
        "xtick.color": TEXTO_2,
        "ytick.color": TEXTO_2,
        "font.size": 10,
        "legend.frameon": False,
    })


def subtitulo(ax, texto):
    """Linha de texto abaixo do título, dentro do gráfico."""
    ax.text(0, 1.02, texto, transform=ax.transAxes, color=TEXTO_2, fontsize=9.5, va="bottom")


def fonte(fig, texto="Fonte: Olist / Kaggle — Brazilian E-Commerce Public Dataset"):
    fig.text(0.01, -0.02, texto, color=TEXTO_2, fontsize=8, ha="left", va="top")


def salvar(fig, nome):
    """Salva o gráfico em analysis/figures/ para usar no site."""
    PASTA_FIGURAS.mkdir(exist_ok=True)
    fig.savefig(PASTA_FIGURAS / f"{nome}.png", dpi=200, bbox_inches="tight", facecolor="white")


def carregar_base():
    """Lê a order_reviews_all.csv (gerada em score-initial-analisys) e cria colunas auxiliares."""
    datas = [
        "review_creation_date", "review_answer_timestamp", "order_purchase_timestamp",
        "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date",
    ]
    base = pd.read_csv("created-tables/order_reviews_all.csv", parse_dates=datas)
    base["entrega_atrasada"] = base["entrega_atrasada"].astype("boolean")
    base["nota_ruim"] = base["review_score"] < 3
    for coluna in ["qtd_itens", "qtd_vendedores", "qtd_pagamentos", "payment_installments"]:
        base[coluna] = base[coluna].astype("Int64")

    base["dias_entrega"] = (base["order_delivered_customer_date"] - base["order_purchase_timestamp"]).dt.days
    base["dias_prometidos"] = (base["order_estimated_delivery_date"] - base["order_purchase_timestamp"]).dt.days
    base["dias_vendedor"] = (
        base["order_delivered_carrier_date"] - base["order_approved_at"]
    ).dt.total_seconds() / 86400
    base["dias_transportadora"] = (
        base["order_delivered_customer_date"] - base["order_delivered_carrier_date"]
    ).dt.total_seconds() / 86400
    base["regiao_cliente"] = base["customer_state"].isin(NORDESTE).map({True: "Nordeste", False: "Outras regiões"})
    return base


def apenas_entregues(base):
    entregues = base.loc[base["entrega_atrasada"].notna()].copy()
    entregues["entrega_atrasada"] = entregues["entrega_atrasada"].astype(bool)
    return entregues
