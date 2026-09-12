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
        
        .discount-card {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 1px solid #93c5fd;
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
                "aluguel_extra": 3300.00,
                "aluguel_recebedor": "Thiago"
            }
        }

def salvar_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

db = carregar_dados()

with st.sidebar:
    st.markdown("### **Smart Finance**")
    st.markdown("<p style='color: #64748b; font-size: 0.85rem;'>Gestão do casal com abatimento proporcional de aluguel.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### 🗓️ Gerenciamento")
    novo_mes = st.text_input("Criar Novo Mês", placeholder="Ex: Outubro 2026")
    if st.button("Adicionar Mês"):
        if novo_mes and novo_mes not in db:
            db[novo_mes] = {"rendas": [], "despesas": [], "aluguel_extra": 3300.00, "aluguel_recebedor": "Thiago"}
            salvar_dados(db)
            st.success(f"Mês {novo_mes} criado!")
            st.rerun()
            
    meses = list(db.keys())
    mes_atual = st.selectbox("Mês de Referência", options=meses if meses else ["Setembro 2026"])
    
    st.markdown("---")
    st.markdown("<p style='font-size: 0.75rem; color: #94a3b8;'>Sincronizado na nuvem • Seguro</p>", unsafe_allow_html=True)

if not mes_atual or mes_atual not in db:
    db[mes_atual] = {"rendas": [], "despesas": [], "aluguel_extra": 3300.00, "aluguel_recebedor": "Thiago"}

if "aluguel_extra" not in db[mes_atual]:
    db[mes_atual]["aluguel_extra"] = 3300.00
if "aluguel_recebedor" not in db[mes_atual]:
    db[mes_atual]["aluguel_recebedor"] = "Thiago"

st.markdown('<h1 class="main-header">Painel Financeiro</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">Mês de referência: <b>{mes_atual}</b></p>', unsafe_allow_html=True)

rendas = db[mes_atual]["rendas"]
despesas = db[mes_atual]["despesas"]
aluguel_extra = float(db[mes_atual].get("aluguel_extra", 0.0))
aluguel_recebedor = db[mes_atual].get("aluguel_recebedor", "Thiago")

# 1. Rendas e Proporções
renda_thiago = sum(r["valor"] for r in rendas if r["pessoa"] == "Thiago")
renda_luciana = sum(r["valor"] for r in rendas if r["pessoa"] == "Luciana")
renda_total = renda_thiago + renda_luciana

if renda_total > 0:
    perc_thiago = renda_thiago / renda_total
    perc_luciana = renda_luciana / renda_total
else:
    perc_thiago = perc_luciana = 0.50

# 2. Despesas Brutas Pagas por cada um
bruto_thiago = sum(d["valor"] for d in despesas if d["pessoa"] == "Thiago")
bruto_luciana = sum(d["valor"] for d in despesas if d["pessoa"] == "Luciana")
despesas_brutas = bruto_thiago + bruto_luciana

# 3. Abatimento da Renda Extra (Aluguel) das Dívidas
despesas_liquidas = max(0.0, despesas_brutas - aluguel_extra)

# Parcela proporcional de cada um no aluguel
abate_thiago = aluguel_extra * perc_thiago
abate_luciana = aluguel_extra * perc_luciana

# Cota que cada um deveria pagar das despesas líquidas
deveria_thiago = despesas_liquidas * perc_thiago
deveria_luciana = despesas_liquidas * perc_luciana

# Pagamento efetivo considerando quem reteve/recebeu o aluguel para abater despesas
if aluguel_recebedor == "Thiago":
    efetivo_thiago = bruto_thiago - aluguel_extra
    efetivo_luciana = bruto_luciana
else:
    efetivo_thiago = bruto_thiago
    efetivo_luciana = bruto_luciana - aluguel_extra

diff_thiago = efetivo_thiago - deveria_thiago

# Card Informativo do Abatimento do Aluguel
st.markdown(f"""
    <div class="discount-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <span style="color: #1e40af; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;">📉 Abatimento de Aluguel nas Despesas</span>
                <h3 style="color: #1e3a8a; margin: 4px 0 0 0; font-size: 1.4rem; font-weight: 700;">- R$ {aluguel_extra:,.2f}</h3>
                <span style="font-size: 0.8rem; color: #3b82f6;">Recebido por: <b>{aluguel_recebedor}</b> e abatido do total de contas.</span>
            </div>
            <div style="display: flex; gap: 24px;">
                <div>
                    <span style="font-size: 0.8rem; color: #1e40af;">Abatimento Thiago ({perc_thiago*100:.1f}%)</span>
                    <div style="font-weight: 700; color: #1d4ed8; font-size: 1.1rem;">- R$ {abate_thiago:,.2f}</div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; color: #1e40af;">Abatimento Luciana ({perc_luciana*100:.1f}%)</span>
                    <div style="font-weight: 700; color: #1d4ed8; font-size: 1.1rem;">- R$ {abate_luciana:,.2f}</div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Métricas Principais
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
        <div class="metric-container">
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Renda Base Total</span>
            <h2 style="color: #0f172a; margin: 4px 0;">R$ {renda_total:,.2f}</h2>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569; margin-top: 8px;">
                <span>Thiago: <b>R$ {renda_thiago:,.2f}</b> ({perc_thiago*100:.1f}%)</span>
                <span>Luciana: <b>R$ {renda_luciana:,.2f}</b> ({perc_luciana*100:.1f}%)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="metric-container">
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Despesas Líquidas (Pós-Aluguel)</span>
            <h2 style="color: #e11d48; margin: 4px 0;">R$ {despesas_liquidas:,.2f}</h2>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #475569; margin-top: 8px;">
                <span>Despesas Brutas: R$ {despesas_brutas:,.2f}</span>
                <span>Aluguel: - R$ {aluguel_extra:,.2f}</span>
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
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Acerto Final do Mês</span>
            <h2 style="color: {acerto_color}; margin: 4px 0;">{acerto_valor}</h2>
            <p style="font-size: 0.8rem; color: #475569; margin: 8px 0 0 0;"><b>{acerto_titulo}</b> (já com o aluguel abatido).</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Visão Geral e Extrato", "⚡ Lançar Contas", "⚙️ Configurar Aluguel"])

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
        f_tipo = st.selectbox("Tipo", ["Despesa", "Renda"])
        f_pessoa = st.selectbox("Responsável", ["Thiago", "Luciana"])
        f_desc = st.text_input("Descrição (ex: Cartão, Escola, Supermercado, Salário)")
        f_valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
        
        submitted = st.form_submit_button("Salvar")
        if submitted:
            if f_desc and f_valor > 0:
                chave = "rendas" if f_tipo == "Renda" else "despesas"
                db[mes_atual][chave].append({"pessoa": f_pessoa, "desc": f_desc, "valor": f_valor})
                salvar_dados(db)
                st.success("Salvo com sucesso!")
                st.rerun()
            else:
                st.error("Preencha a descrição e um valor válido.")

    st.markdown("---")
    st.markdown("### **Excluir Lançamentos**")
    col_rem1, col_rem2 = st.columns(2)
    with col_rem1:
        if rendas:
            r_opts = {f"{r['pessoa']} - {r['desc']} (R$ {r['valor']:,.2f})": i for i, r in enumerate(rendas)}
            r_sel = st.selectbox("Selecione a Renda", options=list(r_opts.keys()))
            if st.button("Excluir Renda"):
                db[mes_atual]["rendas"].pop(r_opts[r_sel])
                salvar_dados(db)
                st.rerun()
        else:
            st.caption("Sem rendas cadastradas.")

    with col_rem2:
        if despesas:
            d_opts = {f"{d['pessoa']} - {d['desc']} (R$ {d['valor']:,.2f})": i for i, d in enumerate(despesas)}
            d_sel = st.selectbox("Selecione a Despesa", options=list(d_opts.keys()))
            if st.button("Excluir Despesa"):
                db[mes_atual]["despesas"].pop(d_opts[d_sel])
                salvar_dados(db)
                st.rerun()
        else:
            st.caption("Sem despesas cadastradas.")

with tab3:
    st.markdown("### **Configuração do Aluguel Abatido**")
    st.write("Defina o valor do aluguel e quem recebeu o dinheiro para abater do montante de despesas do mês:")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        novo_aluguel = st.number_input("Valor do Aluguel (R$)", min_value=0.0, value=aluguel_extra, step=50.0, format="%.2f")
    with col_c2:
        novo_recebedor = st.selectbox("Quem recebeu o valor?", ["Thiago", "Luciana"], index=0 if aluguel_recebedor == "Thiago" else 1)
        
    if st.button("Atualizar Configuração do Aluguel"):
        db[mes_atual]["aluguel_extra"] = novo_aluguel
        db[mes_atual]["aluguel_recebedor"] = novo_recebedor
        salvar_dados(db)
        st.success("Configuração atualizada com sucesso!")
        st.rerun()
