
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Contas do Casal",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilização CSS leve para deixar com cara de app profissional
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 600; }
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

# Arquivo de persistência na nuvem do Streamlit
DB_FILE = "dados_casal.json"

def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Dados iniciais baseados em Setembro de 2026
        return {
            "Setembro 2026": {
                "rendas": [
                    {"pessoa": "Thiago", "desc": "Salário", "valor": 8773.17},
                    {"pessoa": "Thiago", "desc": "Diárias", "valor": 9563.00},
                    {"pessoa": "Luciana", "desc": "Salário", "valor": 16927.99},
                    {"pessoa": "Luciana", "desc": "Diárias", "valor": 4781.50}
                ],
                "despesas": [
                    {"pessoa": "Thiago", "desc": "Cartão C6", "valor": 12650.80},
                    {"pessoa": "Thiago", "desc": "Aluguel Duetto", "valor": 3000.00},
                    {"pessoa": "Thiago", "desc": "Escola Felipe", "valor": 2500.00},
                    {"pessoa": "Luciana", "desc": "Parque das Flores", "valor": 350.00}
                ]
            }
        }

def salvar_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

db = carregar_dados()

# Sidebar para navegação de Meses
st.sidebar.title("🗓️ Controle do Casal")
meses_disponiveis = list(db.keys())

# Permite adicionar um novo mês
novo_mes_input = st.sidebar.text_input("Adicionar Novo Mês (ex: Outubro 2026)")
if st.sidebar.button("Criar Mês"):
    if novo_mes_input and novo_mes_input not in db:
        db[novo_mes_input] = {"rendas": [], "despesas": []}
        salvar_dados(db)
        st.rerun()

mes_selecionado = st.sidebar.selectbox("Selecione o Mês", options=list(db.keys()), index=0)

st.title(f"Controle Financeiro — {mes_selecionado}")
st.write("Gerencie rendas, despesas e veja o acerto proporcional em tempo real de qualquer lugar.")

# Garantir estrutura do mês
if mes_selecionado not in db:
    db[mes_selecionado] = {"rendas": [], "despesas": []}

# Abas internas do App
aba_resumo, aba_lancamentos = st.tabs(["📊 Resumo e Acerto", "✏️ Adicionar Rendas/Despesas"])

with aba_resumo:
    rendas = db[mes_selecionado]["rendas"]
    despesas = db[mes_selecionado]["despesas"]
    
    total_renda_thiago = sum(r["valor"] for r in rendas if r["pessoa"] == "Thiago")
    total_renda_luciana = sum(r["valor"] for r in rendas if r["pessoa"] == "Luciana")
    renda_total = total_renda_thiago + total_renda_luciana
    
    total_desp_thiago = sum(d["valor"] for d in despesas if d["pessoa"] == "Thiago")
    total_desp_luciana = sum(d["valor"] for d in despesas if d["pessoa"] == "Luciana")
    despesa_total = total_desp_thiago + total_desp_luciana

    # Métricas Principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Renda Total", f"R$ {renda_total:,.2f}", f"Thiago: R$ {total_renda_thiago:,.2f} | Luciana: R$ {total_renda_luciana:,.2f}")
    with col2:
        st.metric("Despesas Totais", f"R$ {despesa_total:,.2f}", f"Pago Thiago: R$ {total_desp_thiago:,.2f}")
    with col3:
        if renda_total > 0:
            perc_t = total_renda_thiago / renda_total
            perc_l = total_renda_luciana / renda_total
            devia_t = despesa_total * perc_t
            diff = total_desp_thiago - devia_t
            
            if diff > 0:
                st.metric("Acerto do Mês", "Luciana deve a Thiago", f"R$ {abs(diff):,.2f}")
            else:
                st.metric("Acerto do Mês", "Thiago deve a Luciana", f"R$ {abs(diff):,.2f}")
        else:
            st.metric("Acerto do Mês", "Sem Rendas", "Cadastre rendas")

    st.markdown("---")
    
    # Exibição de Tabelas Detalhadas
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Rendas Registradas")
        if rendas:
            df_r = pd.DataFrame(rendas)
            st.dataframe(df_r, use_container_width=True)
        else:
            st.info("Nenhuma renda cadastrada neste mês.")
            
    with col_t2:
        st.subheader("Despesas Registradas")
        if despesas:
            df_d = pd.DataFrame(despesas)
            st.dataframe(df_d, use_container_width=True)
        else:
            st.info("Nenhuma despesa cadastrada neste mês.")

with aba_lancamentos:
    st.subheader("Cadastrar Nova Movimentação")
    
    tipo_mov = st.selectbox("Tipo", ["Renda", "Despesa"])
    pessoa = st.selectbox("Pessoa", ["Thiago", "Luciana"])
    desc = st.text_input("Descrição (ex: Salário, Aluguel, Supermercado)")
    valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0)
    
    if st.button("Adicionar Lançamento"):
        if desc and valor > 0:
            if tipo_mov == "Renda":
                db[mes_selecionado]["rendas"].append({"pessoa": pessoa, "desc": desc, "valor": valor})
            else:
                db[mes_selecionado]["despesas"].append({"pessoa": pessoa, "desc": desc, "valor": valor})
            
            salvar_dados(db)
            st.success("Lançamento adicionado com sucesso!")
            st.rerun()
        else:
            st.error("Preencha a descrição e informe um valor válido.")
            
    st.markdown("---")
    st.subheader("Remover Itens")
    
    # Opção para deletar itens
    if tipo_mov == "Renda" and db[mes_selecionado]["rendas"]:
        idx_del = st.selectbox("Selecione a Renda para Excluir", options=range(len(db[mes_selecionado]["rendas"])), format_func=lambda x: f"{db[mes_selecionado]['rendas'][x]['pessoa']} - {db[mes_selecionado]['rendas'][x]['desc']} (R$ {db[mes_selecionado]['rendas'][x]['valor']})")
        if st.button("Excluir Renda Selecionada"):
            db[mes_selecionado]["rendas"].pop(idx_del)
            salvar_dados(db)
            st.rerun()
            
    elif tipo_mov == "Despesa" && db[mes_selecionado]["despesas"]:
        pass # handled in block below cleanly
    
    if db[mes_selecionado]["despesas"]:
        idx_del_d = st.selectbox("Selecione a Despesa para Excluir", options=range(len(db[mes_selecionado]["despesas"])), format_func=lambda x: f"{db[mes_selecionado]['despesas'][x]['pessoa']} - {db[mes_selecionado]['despesas'][x]['desc']} (R$ {db[mes_selecionado]['despesas'][x]['valor']})")
        if st.button("Excluir Despesa Selecionada"):
            db[mes_selecionado]["despesas"].pop(idx_del_d)
            salvar_dados(db)
            st.rerun()
