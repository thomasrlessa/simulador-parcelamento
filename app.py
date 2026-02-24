import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador Estratégico de Parcelamento", layout="wide")

st.title("💳 Simulador Estratégico: Pagar à Vista ou Parcelar?")
st.markdown("Descubra matematicamente qual decisão é mais inteligente.")

st.divider()

# =========================
# INPUTS
# =========================

col1, col2 = st.columns(2)

with col1:
    valor_produto = st.number_input("Valor do produto (R$)", min_value=0.0, value=1000.0)
    parcelas = st.number_input("Número de parcelas", min_value=1, value=10)
    tem_juros = st.selectbox("Tem juros?", ["Não", "Sim"])

with col2:
    taxa_juros = 0.0
    if tem_juros == "Sim":
        taxa_juros = st.number_input("Taxa de juros mensal (%)", min_value=0.0, value=2.0) / 100
    
    rendimento = st.number_input("Rendimento mensal do investimento (%)", min_value=0.0, value=1.0) / 100

calcular = st.button("Calcular")

st.divider()

# =========================
# CÁLCULOS
# =========================

if calcular:

    # Valor total parcelado
    if tem_juros == "Sim":
        valor_parcela = valor_produto * (taxa_juros * (1 + taxa_juros) ** parcelas) / ((1 + taxa_juros) ** parcelas - 1)
        total_pago = valor_parcela * parcelas
    else:
        valor_parcela = valor_produto / parcelas
        total_pago = valor_produto

    # Simulação investimento
    saldo = valor_produto
    historico = []

    for i in range(parcelas):
        saldo = saldo * (1 + rendimento) - valor_parcela
        historico.append(saldo)

    saldo_final = saldo

    # =========================
    # RESULTADOS
    # =========================

    st.subheader("📊 Resultados")

    colA, colB, colC = st.columns(3)

    colA.metric("💰 Total Pago Parcelado", f"R$ {total_pago:,.2f}")
    colB.metric("📈 Saldo Final Investindo", f"R$ {saldo_final:,.2f}")
    colC.metric("💳 Valor da Parcela", f"R$ {valor_parcela:,.2f}")

    st.divider()

    # =========================
    # DECISÃO
    # =========================

    if saldo_final > 0:
        st.success("🏆 Melhor estratégia: Parcelar e investir o dinheiro.")
        st.write(f"Você terminaria com **R$ {saldo_final:,.2f} a mais**.")
    else:
        st.error("⚠️ Melhor estratégia: Pagar à vista.")
        st.write(f"Parcelar geraria prejuízo de **R$ {abs(saldo_final):,.2f}**.")

    st.divider()

    # =========================
    # GRÁFICO EVOLUÇÃO
    # =========================

    st.subheader("📈 Evolução do Investimento")

    fig = plt.figure()
    plt.plot(range(1, parcelas + 1), historico)
    plt.xlabel("Parcelas")
    plt.ylabel("Saldo (R$)")
    plt.title("Evolução do saldo investido")
    st.pyplot(fig)

    st.divider()

    # =========================
    # RESUMO INTELIGENTE
    # =========================

    st.subheader("🧠 Análise Estratégica")

    if tem_juros == "Não" and rendimento > 0:
        st.write("""
        Se realmente não houver juros e você investir com disciplina,
        parcelar tende a ser matematicamente vantajoso.
        """)

    if tem_juros == "Sim" and taxa_juros > rendimento:
        st.write("""
        A taxa de juros do parcelamento é maior que o rendimento do investimento.
        Isso geralmente torna o parcelamento desvantajoso.
        """)

    st.info("⚠️ Simulação matemática. Não é recomendação de investimento.")