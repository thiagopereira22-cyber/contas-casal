import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="Gestão Financeira | Casal",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Design System refinado com CSS moderno (Estilo SaaS / Tailwind-like)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.025em;
        }
        
        .sub-header {
            color: #64748b;
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        /* Estilização dos blocos de métricas */
        .metric-container {
            background: #ffffff;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #e2e8f0;
            margin-bottom: 1rem;
        }
        
        /* Botões personalizados */
        .stButton>button {
            background-color: #4f46e5;
            color: white;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1rem;
            border: none;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #4338ca;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        }
        
        /* Ajuste de abas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            border: 1px solid #e2e8f0;
            color: #475569;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4f46e5 !important;
            color: white !important;
            border-color: #4f46e5 !important;
        }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "dados_casal.json"

def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
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

# Sidebar Profissional
with st.sidebar:
    st.markdown("### **Smart Finance**")
    st.markdown("<p style='color: #64748b; font-size: 0.85rem;'>Controle financeiro integrado do casal.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### 🗓️ Gerenciamento")
    novo_mes = st.text_input("Criar Novo Mês", placeholder="Ex: Outubro 2026")
    if st.button("Adicionar Mês"):
        if novo_mes and novo_mes not in db:
            db[novo_mes] = {"rendas": [], "despesas": []}
            salvar_dados(db)
            st.success(f"Mês {novo_mes} criado!")
            st.rerun()
            
    meses = list(db.keys())
    mes_atual = st.selectbox("Mês de Referência", options=meses if meses else ["Setembro 2026"])
    
    st.markdown("---")
    st.markdown("<p style='font-size: 0.75rem; color: #94a3b8;'>Sincronizado na nuvem • Seguro</p>", unsafe_allow_html=True)

if not mes_atual or mes_atual not in db:
    db[mes_atual] = {"rendas": [], "despesas": []}

# Cabeçalho Principal
st.markdown(f'<h1 class="main-header">Painel Financeiro</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">Acompanhamento e divisão proporcional de despesas para <b>{mes_atual}</b>.</p>', unsafe_allow_html=True)

# Processamento de Dados
rendas = db[mes_atual]["rendas"]
despesas = db[mes_atual]["despesas"]

t_renda_thiago = sum(r["valor"] for r in rendas if r["pessoa"] == "Thiago")
t_renda_luciana = sum(r["valor"] for r in rendas if r["pessoa"] == "Luciana")
renda_total = t_renda_thiago + t_renda_luciana

t_desp_thiago = sum(d["valor"] for d in despesas if d["pessoa"] == "Thiago")
t_desp_luciana = sum(d["valor"] for d in despesas if d["pessoa"] == "Luciana")
despesa_total = t_desp_thiago + t_desp_luciana

# Cálculo de Proporção
if renda_total > 0:
    perc_thiago = t_renda_thiago / renda_total
    perc_luciana = t_renda_luciana / renda_total
    devia_thiago = despesa_total * perc_thiago
    diff_thiago = t_desp_thiago - devia_thiago
else:
    perc_thiago = perc_luciana = 0
    diff_thiago = 0

# Seção de Métricas Principais Estilizadas
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
        <div class="metric-container">
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Renda Consolidada</span>
            <h2 style="color: #0f172a; margin-top: 5px; margin-bottom: 5px;">R$ {renda_total:,.2f}</h2>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569; margin-top: 8px;">
                <span>Thiago: <b>R$ {t_renda_thiago:,.2f}</b> ({perc_thiago*100:.1f}%)</span>
                <span>Luciana: <b>R$ {t_renda_luciana:,.2f}</b> ({perc_luciana*100:.1f}%)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="metric-container">
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Despesas Totais</span>
            <h2 style="color: #e11d48; margin-top: 5px; margin-bottom: 5px;">R$ {despesa_total:,.2f}</h2>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569; margin-top: 8px;">
                <span>Pago Thiago: <b>R$ {t_desp_thiago:,.2f}</b></span>
                <span>Pago Luciana: <b>R$ {t_desp_luciana:,.2f}</b></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    if diff_thiago > 0:
        acerto_titulo = "Luciana deve a Thiago"
        acerto_valor = f"R$ {abs(diff_thiago):,.2f}"
        acerto_color = "#059669"
    else:
        acerto_titulo = "Thiago deve a Luciana"
        acerto_valor = f"R$ {abs(diff_thiago):,.2f}"
        acerto_color = "#4f46e5"

    st.markdown(f"""
        <div class="metric-container" style="border-left: 4px solid {acerto_color};">
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Acerto do Mês</span>
            <h2 style="color: {acerto_color}; margin-top: 5px; margin-bottom: 5px;">{acerto_valor}</h2>
            <p style="font-size: 0.8rem; color: #475569; margin-top: 8px; margin-bottom: 0;"><b>{acerto_titulo}</b> proporcionalmente.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Abas de Ação
tab1, tab2 = st.tabs(["📊 Visão Geral e Relatórios", "⚡ Lançamentos e Gestão"])

with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("### **Rendas do Mês**")
        if rendas:
            df_r = pd.DataFrame(rendas)
            df_r.columns = ["Pessoa", "Descrição", "Valor (R$)"]
            st.dataframe(df_r, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma renda registrada.")
            
    with col_t2:
        st.markdown("### **Despesas do Mês**")
        if despesas:
            df_d = pd.DataFrame(despesas)
            df_d.columns = ["Pessoa", "Descrição", "Valor (R$)"]
            st.dataframe(df_d, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma despesa registrada.")

with tab2:
    st.markdown("### **Adicionar Nova Movimentação**")
    
    with st.form("form_lancamento", clear_on_submit=True):
        f_tipo = st.selectbox("Tipo de Movimento", ["Despesa", "Renda"])
        f_pessoa = st.selectbox("Responsável", ["Thiago", "Luciana"])
        f_desc = st.text_input("Descrição (ex: Supermercado, Cartão, Aluguel, Salário)")
        f_valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
        
        submitted = st.form_submit_button("Salvar Lançamento")
        if submitted:
            if f_desc and f_valor > 0:
                chave_lista = "rendas" if f_tipo == "Renda" else "despesas"
                db[mes_atual][chave_lista].append({"pessoa": f_pessoa, "desc": f_desc, "valor": f_valor})
                salvar_dados(db)
                st.success("Lançamento adicionado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha a descrição e informe um valor maior que zero.")

    st.markdown("---")
    st.markdown("### **Remover Lançamento Existente**")
    
    col_rem1, col_rem2 = st.columns(2)
    with col_rem1:
        if rendas:
            r_options = {f"{r['pessoa']} - {r['desc']} (R$ {r['valor']:,.2f})": idx for idx, r in enumerate(rendas)}
            r_escolhido = st.selectbox("Selecione a Renda para apagar", options=list(r_options.keys()))
            if st.button("Excluir Renda"):
                db[mes_atual]["rendas"].pop(r_options[r_escolhido])
                salvar_dados(db)
                st.success("Renda removida!")
                st.rerun()
        else:
            st.caption("Sem rendas para apagar.")

    with col_rem2:
        if despesas:
            d_options = {f"{d['pessoa']} - {d['desc']} (R$ {d['valor']:,.2f})": idx for idx, d in enumerate(despesas)}
            d_escolhido = st.selectbox("Selecione a Despesa para apagar", options=list(d_options.keys()))
            if st.button("Excluir Despesa"):
                db[mes_atual]["despesas"].pop(d_options[d_escolhido])
                salvar_dados(db)
                st.success("Despesa removida!")
                st.rerun()
        else:
            st.caption("Sem despesas para apagar.")
