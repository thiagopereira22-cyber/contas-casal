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
        
        /* Lista vertical limpa e clicável para os meses */
        div[data-testid="stRadio"] > div {
            gap: 4px;
        }
        div[data-testid="stRadio"] label {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 8px 12px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 2px;
            display: flex;
            align-items: center;
        }
        div[data-testid="stRadio"] label:hover {
            background-color: #f1f5f9;
            border-color: #cbd5e1;
        }
        div[data-testid="stRadio"] label[data-checked="true"] {
            background-color: #eff6ff !important;
            border-color: #3b82f6 !important;
            font-weight: 600;
            color: #1d4ed8 !important;
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

# Meses padrão disponíveis para seleção imediata
MESES_PADRAO = [
    "Janeiro 2026", "Fevereiro 2026", "Março 2026", "Abril 2026",
    "Maio 2026", "Junho 2026", "Julho 2026", "Agosto 2026",
    "Setembro 2026", "Outubro 2026", "Novembro 2026", "Dezembro 2026"
]

RENDAS_PADRAO = [
    {"pessoa": "Thiago", "desc": "Salário", "valor": 8773.17},
    {"pessoa": "Thiago", "desc": "Diárias", "valor": 9563.00},
    {"pessoa": "Luciana", "desc": "Salário", "valor": 16927.99},
    {"pessoa": "Luciana", "desc": "Diárias", "valor": 4781.50}
]

def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = {}

    # Replica as rendas e o aluguel para todos os meses caso não existam
    for m in MESES_PADRAO:
        if m not in dados:
            dados[m] = {
                "rendas": [r.copy() for r in RENDAS_PADRAO],
                "despesas": [],
                "aluguel_extra": 3300.00,
                "aluguel_recebedor": "Thiago"
            }
        else:
            if not dados[m].get("rendas"):
                dados[m]["rendas"] = [r.copy() for r in RENDAS_PADRAO]
            if "aluguel_extra" not in dados[m]:
                dados[m]["aluguel_extra"] = 3300.00
            if "aluguel_recebedor" not in dados[m]:
                dados[m]["aluguel_recebedor"] = "Thiago"
                
    return dados

def salvar_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

db = carregar_dados()

with st.sidebar:
    st.markdown("### **Smart Finance**")
    st.markdown("<p style='color: #64748b; font-size: 0.85rem;'>Gestão integrada e proporcional do casal.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### 📅 **Selecione o Mês**")
    todos_meses = list(db.keys())
    
    # Navegação rápida com 1 clique
    mes_atual = st.radio(
        label="Navegação Mensal",
        options=todos_meses,
        index=todos_meses.index("Setembro 2026") if "Setembro 2026" in todos_meses else 0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    with st.expander("➕ Adicionar outro mês/ano"):
        novo_mes = st.text_input("Nome do Mês", placeholder="Ex: Janeiro 2027")
        if st.button("Criar e Replicar Base"):
            if novo_mes and novo_mes not in db:
                db[novo_mes] = {
                    "rendas": [r.copy() for r in RENDAS_PADRAO],
                    "despesas": [],
                    "aluguel_extra": 3300.00,
                    "aluguel_recebedor": "Thiago"
                }
                salvar_dados(db)
                st.success(f"Mês {novo_mes} criado!")
                st.rerun()

    # Replicar valores atuais para toda a planilha
    if st.button("🔄 Replicar Rendas/Aluguel p/ Todos"):
        rendas_atuais = db[mes_atual]["rendas"]
        aluguel_atual = db[mes_atual].get("aluguel_extra", 3300.00)
        recebedor_atual = db[mes_atual].get("aluguel_recebedor", "Thiago")
        
        for m in db:
            db[m]["rendas"] = [r.copy() for r in rendas_atuais]
            db[m]["aluguel_extra"] = aluguel_atual
            db[m]["aluguel_recebedor"] = recebedor_atual
            
        salvar_dados(db)
        st.success(f"Configurações de {mes_atual} replicadas para todos os meses!")
        st.rerun()

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

tab1, tab2, tab3 = st.tabs(["📊 Visão Geral e Extrato", "⚡ Lançar e Editar Contas", "⚙️ Configurar Aluguel"])

with tab1:
    st.caption("💡 Dica: você pode clicar duas vezes em qualquer linha das tabelas abaixo para editar Pessoa, Descrição ou Valor diretamente na lista.")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("### **Rendas do Mês**")
        if rendas:
            df_r = pd.DataFrame(rendas)
            df_r = df_r.rename(columns={"pessoa": "Pessoa", "desc": "Descrição", "valor": "Valor"})
            edited_r = st.data_editor(
                df_r,
                key=f"edit_r_{mes_atual}",
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Pessoa": st.column_config.SelectboxColumn("Pessoa", options=["Thiago", "Luciana"], required=True),
                    "Descrição": st.column_config.TextColumn("Descrição", required=True),
                    "Valor": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f", required=True)
                }
            )
            lista_editada_r = edited_r.rename(columns={"Pessoa": "pessoa", "Descrição": "desc", "Valor": "valor"}).to_dict(orient="records")
            if lista_editada_r != rendas:
                db[mes_atual]["rendas"] = lista_editada_r
                salvar_dados(db)
                st.rerun()
        else:
            st.info("Nenhuma renda registrada.")
            
    with col_t2:
        st.markdown("### **Despesas Pagas**")
        if despesas:
            df_d = pd.DataFrame(despesas)
            df_d = df_d.rename(columns={"pessoa": "Pessoa", "desc": "Descrição", "valor": "Valor"})
            edited_d = st.data_editor(
                df_d,
                key=f"edit_d_{mes_atual}",
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Pessoa": st.column_config.SelectboxColumn("Pessoa", options=["Thiago", "Luciana"], required=True),
                    "Descrição": st.column_config.TextColumn("Descrição", required=True),
                    "Valor": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f", required=True)
                }
            )
            lista_editada_d = edited_d.rename(columns={"Pessoa": "pessoa", "Descrição": "desc", "Valor": "valor"}).to_dict(orient="records")
            if lista_editada_d != despesas:
                db[mes_atual]["despesas"] = lista_editada_d
                salvar_dados(db)
                st.rerun()
        else:
            st.info("Nenhuma despesa registrada.")

with tab2:
    st.markdown("### **Adicionar Nova Movimentação**")
    with st.form("form_lancamento", clear_on_submit=True):
        f_tipo = st.selectbox("Tipo", ["Despesa", "Renda"])
        f_pessoa = st.selectbox("Responsável", ["Thiago", "Luciana"])
        f_desc = st.text_input("Descrição (ex: Cartão, Escola, Supermercado, Salário)")
        f_valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
        
        submitted = st.form_submit_button("Salvar Novo Lançamento")
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
    st.markdown("### **Editar ou Excluir Lançamentos Específicos**")
    
    col_edit1, col_edit2 = st.columns(2)
    with col_edit1:
        st.markdown("#### ✏️ **Editar Renda**")
        if rendas:
            r_opts = {f"{r['pessoa']} - {r['desc']} (R$ {r['valor']:,.2f})": i for i, r in enumerate(rendas)}
            r_sel_key = st.selectbox("Selecione a Renda", options=list(r_opts.keys()), key="sel_edit_renda")
            idx_r = r_opts[r_sel_key]
            item_r = rendas[idx_r]
            
            with st.form(f"form_edit_renda_{idx_r}"):
                edit_r_pessoa = st.selectbox("Pessoa", ["Thiago", "Luciana"], index=0 if item_r["pessoa"] == "Thiago" else 1)
                edit_r_desc = st.text_input("Descrição", value=item_r["desc"])
                edit_r_valor = st.number_input("Valor (R$)", min_value=0.0, value=float(item_r["valor"]), step=10.0, format="%.2f")
                
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    salvar_edicao_r = st.form_submit_button("Atualizar Renda")
                with c_btn2:
                    excluir_r = st.form_submit_button("Excluir Renda")
                    
                if salvar_edicao_r:
                    db[mes_atual]["rendas"][idx_r] = {"pessoa": edit_r_pessoa, "desc": edit_r_desc, "valor": edit_r_valor}
                    salvar_dados(db)
                    st.success("Renda atualizada com sucesso!")
                    st.rerun()
                if excluir_r:
                    db[mes_atual]["rendas"].pop(idx_r)
                    salvar_dados(db)
                    st.success("Renda excluída!")
                    st.rerun()
        else:
            st.caption("Sem rendas cadastradas.")

    with col_edit2:
        st.markdown("#### ✏️ **Editar Despesa**")
        if despesas:
            d_opts = {f"{d['pessoa']} - {d['desc']} (R$ {d['valor']:,.2f})": i for i, d in enumerate(despesas)}
            d_sel_key = st.selectbox("Selecione a Despesa", options=list(d_opts.keys()), key="sel_edit_desp")
            idx_d = d_opts[d_sel_key]
            item_d = despesas[idx_d]
            
            with st.form(f"form_edit_desp_{idx_d}"):
                edit_d_pessoa = st.selectbox("Responsável", ["Thiago", "Luciana"], index=0 if item_d["pessoa"] == "Thiago" else 1)
                edit_d_desc = st.text_input("Descrição", value=item_d["desc"])
                edit_d_valor = st.number_input("Valor (R$)", min_value=0.0, value=float(item_d["valor"]), step=10.0, format="%.2f")
                
                c_btn3, c_btn4 = st.columns(2)
                with c_btn3:
                    salvar_edicao_d = st.form_submit_button("Atualizar Despesa")
                with c_btn4:
                    excluir_d = st.form_submit_button("Excluir Despesa")
                    
                if salvar_edicao_d:
                    db[mes_atual]["despesas"][idx_d] = {"pessoa": edit_d_pessoa, "desc": edit_d_desc, "valor": edit_d_valor}
                    salvar_dados(db)
                    st.success("Despesa atualizada com sucesso!")
                    st.rerun()
                if excluir_d:
                    db[mes_atual]["despesas"].pop(idx_d)
                    salvar_dados(db)
                    st.success("Despesa excluída!")
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
