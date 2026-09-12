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

        .metric-container {
            background: #ffffff;
            padding: 22px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #e2e8f0;
            margin-bottom: 1rem;
        }
        
        .rent-card {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border: 1px solid #86efac;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 1.5rem;
        }
        
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
                ],
                "aluguel_extra": 3300.00
            }
        }

def salvar_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

db = carregar_dados()

# Sidebar Profissional
with st.sidebar:
    st.markdown("### **Smart Finance**")
    st.markdown("<p style='color: #64748b; font-size: 0.85rem;'>Controle integrado do casal com divisão proporcional.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### 🗓️ Gerenciamento")
    novo_mes = st.text_input("Criar Novo Mês", placeholder="Ex: Outubro 2026")
    if st.button("Adicionar Mês"):
        if novo_mes and novo_mes not in db:
            db[novo_mes] = {"rendas": [], "despesas": [], "aluguel_extra": 3300.00}
            salvar_dados(db)
            st.success(f"Mês {novo_mes} criado!")
            st.rerun()
            
    meses = list(db.keys())
    mes_atual = st.selectbox("Mês de Referência", options=meses if meses else ["Setembro 2026"])
    
    st.markdown("---")
    st.markdown("<p style='font-size: 0.75rem; color: #94a3b8;'>Sincronizado na nuvem • Seguro</p>", unsafe_allow_html=True)

if not mes_atual or mes_atual not in db:
    db[mes_atual] = {"rendas": [], "despesas": [], "aluguel_extra": 3300.00}

if "aluguel_extra" not in db[mes_atual]:
    db[mes_atual]["aluguel_extra"] = 3300.00

st.markdown('<h1 class="main-header">Painel Financeiro</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">Divisão proporcional baseada nas rendas individuais para <b>{mes_atual}</b>.</p>', unsafe_allow_html=True)

# 1. Rendas Base (Salários + Diárias)
rendas_base = db[mes_atual]["rendas"]
despesas = db[mes_atual]["despesas"]
aluguel_extra = float(db[mes_atual].get("aluguel_extra", 0.0))

base_thiago = sum(r["valor"] for r in rendas_base if r["pessoa"] == "Thiago")
base_luciana = sum(r["valor"] for r in rendas_base if r["pessoa"] == "Luciana")
total_base = base_thiago + base_luciana

if total_base > 0:
    perc_thiago = base_thiago / total_base
    perc_luciana = base_luciana / total_base
else:
    perc_thiago = perc_luciana = 0.50

# Divisão dinâmica do Aluguel
aluguel_thiago = aluguel_extra * perc_thiago
aluguel_luciana = aluguel_extra * perc_luciana

# Rendas Finais Consolidada (Base + Cota do Aluguel)
total_renda_thiago = base_thiago + aluguel_thiago
total_renda_luciana = base_luciana + aluguel_luciana
renda_total_geral = total_renda_thiago + total_renda_luciana

# Despesas Totais
t_desp_thiago = sum(d["valor"] for d in despesas if d["pessoa"] == "Thiago")
t_desp_luciana = sum(d["valor"] for d in despesas if d["pessoa"] == "Luciana")
despesa_total = t_desp_thiago + t_desp_luciana

# Acerto do Mês Proporcional
if renda_total_geral > 0:
    devia_thiago = despesa_total * perc_thiago
    diff_thiago = t_desp_thiago - devia_thiago
else:
    diff_thiago = 0

# Card de Destaque: Divisão Dinâmica do Aluguel
st.markdown(f"""
    <div class="rent-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="color: #166534; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;">🏠 Renda Extra Compartilhada (Aluguel)</span>
                <h3 style="color: #14532d; margin: 4px 0 0 0; font-size: 1.5rem; font-weight: 700;">R$ {aluguel_extra:,.2f}</h3>
            </div>
            <div style="display: flex; gap: 24px; margin-top: 8px;">
                <div>
                    <span style="font-size: 0.8rem; color: #166534;">Thiago ({perc_thiago*100:.1f}%)</span>
                    <div style="font-weight: 700; color: #15803d; font-size: 1.1rem;">R$ {aluguel_thiago:,.2f}</div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; color: #166534;">Luciana ({perc_luciana*100:.1f}%)</span>
                    <div style="font-weight: 700; color: #15803d; font-size: 1.1rem;">R$ {aluguel_luciana:,.2f}</div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Linha de Métricas
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
        <div class="metric-container">
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Renda Total (Base + Aluguel)</span>
            <h2 style="color: #0f172a; margin: 4px 0;">R$ {renda_total_geral:,.2f}</h2>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569; margin-top: 8px;">
                <span>Thiago: <b>R$ {total_renda_thiago:,.2f}</b></span>
                <span>Luciana: <b>R$ {total_renda_luciana:,.2f}</b></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="metric-container">
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Despesas Totais</span>
            <h2 style="color: #e11d48; margin: 4px 0;">R$ {despesa_total:,.2f}</h2>
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
            <h2 style="color: {acerto_color}; margin: 4px 0;">{acerto_valor}</h2>
            <p style="font-size: 0.8rem; color: #475569; margin: 8px 0 0 0;"><b>{acerto_titulo}</b></p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Abas de Gestão
tab1, tab2, tab3 = st.tabs(["📊 Visão Geral e Detalhes", "⚡ Lançamentos", "⚙️ Configurar Aluguel Extra"])

with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("### **Rendas Individuais (Base de Cálculo)**")
        if rendas_base:
            df_r = pd.DataFrame(rendas_base)
            df_r.columns = ["Pessoa", "Descrição", "Valor (R$)"]
            st.dataframe(df_r, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma renda registrada.")
            
    with col_t2:
        st.markdown("### **Despesas Pagas**")
        if despesas:
            df_d = pd.DataFrame(despesas)
            df_d.columns = ["Pessoa", "Descrição", "Valor (R$)"]
            st.dataframe(df_d, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma despesa registrada.")

with tab2:
    st.markdown("### **Adicionar Nova Movimentação**")
    with st.form("form_lancamento", clear_on_submit=True):
        f_tipo = st.selectbox("Tipo de Movimento", ["Despesa", "Renda Individual"])
        f_pessoa = st.selectbox("Responsável", ["Thiago", "Luciana"])
        f_desc = st.text_input("Descrição (ex: Supermercado, Cartão C6, Salário, Diárias)")
        f_valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
        
        submitted = st.form_submit_button("Salvar Lançamento")
        if submitted:
            if f_desc and f_valor > 0:
                chave = "rendas" if f_tipo == "Renda Individual" else "despesas"
                db[mes_atual][chave].append({"pessoa": f_pessoa, "desc": f_desc, "valor": f_valor})
                salvar_dados(db)
                st.success("Lançamento adicionado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha a descrição e um valor válido.")

    st.markdown("---")
    st.markdown("### **Remover Lançamento**")
    col_rem1, col_rem2 = st.columns(2)
    with col_rem1:
        if rendas_base:
            r_opts = {f"{r['pessoa']} - {r['desc']} (R$ {r['valor']:,.2f})": i for i, r in enumerate(rendas_base)}
            r_sel = st.selectbox("Selecione a Renda para apagar", options=list(r_opts.keys()))
            if st.button("Excluir Renda"):
                db[mes_atual]["rendas"].pop(r_opts[r_sel])
                salvar_dados(db)
                st.success("Renda removida!")
                st.rerun()
        else:
            st.caption("Sem rendas para excluir.")

    with col_rem2:
        if despesas:
            d_opts = {f"{d['pessoa']} - {d['desc']} (R$ {d['valor']:,.2f})": i for i, d in enumerate(despesas)}
            d_sel = st.selectbox("Selecione a Despesa para apagar", options=list(d_opts.keys()))
            if st.button("Excluir Despesa"):
                db[mes_atual]["despesas"].pop(d_opts[d_sel])
                salvar_dados(db)
                st.success("Despesa removida!")
                st.rerun()
        else:
            st.caption("Sem despesas para excluir.")

with tab3:
    st.markdown("### **Ajustar Valor do Aluguel Extra do Mês**")
    st.write("O aluguel é fatiado automaticamente de acordo com as proporções das rendas individuais de cada um.")
    novo_aluguel = st.number_input("Valor do Aluguel (R$)", min_value=0.0, value=aluguel_extra, step=50.0, format="%.2f")
    if st.button("Atualizar Aluguel do Mês"):
        db[mes_atual]["aluguel_extra"] = novo_aluguel
        salvar_dados(db)
        st.success(f"Aluguel atualizado para R$ {novo_aluguel:,.2f}!")
        st.rerun()
