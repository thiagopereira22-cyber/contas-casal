import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Finanças do Casal | Dashboard Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS inspirada no design Neon Magenta / Midnight Dark
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Fundo geral Midnight Blue */
        .stApp {
            background-color: #070913 !important;
            color: #f1f5f9;
        }

        /* Barra lateral em cápsula escura */
        [data-testid="stSidebar"] {
            background-color: #0c0f1d !important;
            border-right: 1px solid #1a2238;
        }

        /* Botões de mês em estilo pílula vertical */
        div[data-testid="stRadio"] > div {
            gap: 6px;
        }
        div[data-testid="stRadio"] label {
            background: #11162b !important;
            border: 1px solid #1c2442 !important;
            padding: 8px 14px !important;
            border-radius: 12px !important;
            cursor: pointer;
            transition: all 0.25s ease;
            color: #94a3b8 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: #ec4899 !important;
            color: #ffffff !important;
            transform: translateX(3px);
        }
        div[data-testid="stRadio"] label[data-checked="true"] {
            background: linear-gradient(135deg, #ff007a 0%, #d946ef 100%) !important;
            border-color: #ff007a !important;
            color: #ffffff !important;
            box-shadow: 0 4px 15px rgba(255, 0, 122, 0.35);
        }

        /* Top Bar Widgets */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 12px;
        }
        .date-pill {
            background: #11162b;
            border: 1px solid #1f274a;
            border-radius: 14px;
            padding: 10px 18px;
            font-size: 0.85rem;
            color: #94a3b8;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .user-pill {
            background: #11162b;
            border: 1px solid #1f274a;
            border-radius: 16px;
            padding: 8px 16px;
            display: inline-flex;
            align-items: center;
            gap: 12px;
        }
        .avatar-circle {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff007a 0%, #a855f7 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            color: white;
            font-size: 0.85rem;
            box-shadow: 0 0 12px rgba(255, 0, 122, 0.5);
        }

        /* Card Neon Magenta Hero */
        .card-magenta-hero {
            background: linear-gradient(135deg, #ff007a 0%, #ec4899 50%, #d946ef 100%);
            border-radius: 24px;
            padding: 24px;
            color: white;
            box-shadow: 0 10px 30px rgba(255, 0, 122, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
        }

        /* Cards Dark Midnight */
        .card-dark {
            background: #11162b;
            border: 1px solid #1c2442;
            border-radius: 22px;
            padding: 22px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            transition: border-color 0.2s ease;
        }
        .card-dark:hover {
            border-color: #2e3b68;
        }

        /* Donut Widget Neon */
        .donut-card {
            background: linear-gradient(145deg, #ff007a 0%, #c026d3 100%);
            border-radius: 28px;
            padding: 28px;
            color: white;
            box-shadow: 0 12px 35px rgba(236, 72, 153, 0.35);
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .donut-ring {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            background: conic-gradient(#ffffff var(--percent), rgba(255, 255, 255, 0.2) 0);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            margin: 12px auto;
        }
        .donut-ring::after {
            content: "";
            width: 105px;
            height: 105px;
            border-radius: 50%;
            background: #d946ef;
            position: absolute;
        }
        .donut-content {
            position: relative;
            z-index: 2;
            font-weight: 800;
            font-size: 1.6rem;
        }

        /* Abas estilizadas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: #0c0f1d;
            padding: 6px;
            border-radius: 16px;
            border: 1px solid #1a2238;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border-radius: 12px !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            border: none !important;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #ff007a 0%, #ec4899 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 15px rgba(255, 0, 122, 0.4);
        }

        /* Botão padrão Streamlit */
        .stButton>button {
            background: linear-gradient(135deg, #ff007a 0%, #d946ef 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            font-weight: 700 !important;
            padding: 0.6rem 1.2rem !important;
            box-shadow: 0 4px 15px rgba(255, 0, 122, 0.3) !important;
            transition: transform 0.15s ease;
        }
        .stButton>button:hover {
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "dados_casal.json"

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

# Barra Lateral (Menu vertical com visual idêntico ao da imagem)
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="display: inline-flex; width: 48px; height: 48px; border-radius: 50%; background: #11162b; border: 2px solid #ff007a; align-items: center; justify-content: center; box-shadow: 0 0 15px rgba(255, 0, 122, 0.5);">
                <span style="color: #ff007a; font-weight: 800; font-size: 1.2rem;">⚡</span>
            </div>
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 10px;">Orçamento</div>
        </div>
    """, unsafe_allow_html=True)
    
    todos_meses = list(db.keys())
    mes_atual = st.radio(
        label="Orçamento Mensal",
        options=todos_meses,
        index=todos_meses.index("Setembro 2026") if "Setembro 2026" in todos_meses else 0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    if st.button("🔄 Replicar Rendas/Aluguel"):
        rendas_atuais = db[mes_atual]["rendas"]
        aluguel_atual = db[mes_atual].get("aluguel_extra", 3300.00)
        recebedor_atual = db[mes_atual].get("aluguel_recebedor", "Thiago")
        for m in db:
            db[m]["rendas"] = [r.copy() for r in rendas_atuais]
            db[m]["aluguel_extra"] = aluguel_atual
            db[m]["aluguel_recebedor"] = recebedor_atual
        salvar_dados(db)
        st.success("Replicado para todos os meses!")
        st.rerun()

# Cálculos Proporcionais e Aluguel
rendas = db[mes_atual]["rendas"]
despesas = db[mes_atual]["despesas"]
aluguel_extra = float(db[mes_atual].get("aluguel_extra", 3300.00))
aluguel_recebedor = db[mes_atual].get("aluguel_recebedor", "Thiago")

renda_thiago = sum(r["valor"] for r in rendas if r["pessoa"] == "Thiago")
renda_luciana = sum(r["valor"] for r in rendas if r["pessoa"] == "Luciana")
renda_total = renda_thiago + renda_luciana

if renda_total > 0:
    perc_thiago = renda_thiago / renda_total
    perc_luciana = renda_luciana / renda_total
else:
    perc_thiago = perc_luciana = 0.50

bruto_thiago = sum(d["valor"] for d in despesas if d["pessoa"] == "Thiago")
bruto_luciana = sum(d["valor"] for d in despesas if d["pessoa"] == "Luciana")
despesas_brutas = bruto_thiago + bruto_luciana

despesas_liquidas = max(0.0, despesas_brutas - aluguel_extra)
deveria_thiago = despesas_liquidas * perc_thiago
deveria_luciana = despesas_liquidas * perc_luciana

if aluguel_recebedor == "Thiago":
    efetivo_thiago = bruto_thiago - aluguel_extra
    efetivo_luciana = bruto_luciana
else:
    efetivo_thiago = bruto_thiago
    efetivo_luciana = bruto_luciana - aluguel_extra

diff_thiago = efetivo_thiago - deveria_thiago

# Top Bar com Data Atual e Perfil do Casal
st.markdown(f"""
    <div class="top-bar">
        <div class="date-pill">
            <span>📅</span> Referência: <b>{mes_atual}</b>
        </div>
        <div class="user-pill">
            <div style="text-align: right;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #ffffff;">Thiago & Luciana</div>
                <div style="font-size: 0.72rem; color: #ff007a;">Gestão Proporcional Ativa</div>
            </div>
            <div class="avatar-circle">TL</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Grid Superior idêntico à imagem de referência
col_left, col_right = st.columns([6.8, 3.2])

with col_left:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="card-magenta-hero">
                <span style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.9;">Renda Total Consolidada</span>
                <h2 style="font-size: 2rem; font-weight: 800; margin: 8px 0 12px 0;">R$ {renda_total:,.2f}</h2>
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem; opacity: 0.95;">
                    <span>Thiago: <b>R$ {renda_thiago:,.2f}</b></span>
                    <span>Luciana: <b>R$ {renda_luciana:,.2f}</b></span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
            <div class="card-dark">
                <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: #64748b;">Despesas Líquidas (Contas)</span>
                <h2 style="font-size: 1.8rem; font-weight: 800; margin: 8px 0; color: #ffffff;">R$ {despesas_liquidas:,.2f}</h2>
                <svg width="100%" height="28" viewBox="0 0 200 28" fill="none">
                    <path d="M0 18 Q 30 5, 60 14 T 120 18 T 180 8 T 200 16" stroke="#ff007a" stroke-width="3" fill="none"/>
                </svg>
                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Bruto: R$ {despesas_brutas:,.2f} | Aluguel: -R$ {aluguel_extra:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
            <div class="card-dark">
                <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: #64748b;">Aluguel Aldepark (Abatido)</span>
                <h3 style="font-size: 1.5rem; font-weight: 800; margin: 8px 0; color: #38bdf8;">- R$ {aluguel_extra:,.2f}</h3>
                <svg width="100%" height="24" viewBox="0 0 200 24" fill="none">
                    <path d="M0 16 Q 40 4, 80 12 T 140 18 T 200 8" stroke="#38bdf8" stroke-width="2.5" fill="none"/>
                </svg>
                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Recebido por {aluguel_recebedor} e descontado das contas.</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="card-dark">
                <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: #64748b;">Cota Proporcional das Contas</span>
                <h3 style="font-size: 1.3rem; font-weight: 800; margin: 8px 0; color: #10b981;">Thiago {perc_thiago*100:.1f}% | Lu {perc_luciana*100:.1f}%</h3>
                <svg width="100%" height="24" viewBox="0 0 200 24" fill="none">
                    <path d="M0 14 Q 50 20, 100 8 T 160 16 T 200 6" stroke="#10b981" stroke-width="2.5" fill="none"/>
                </svg>
                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Thiago: R$ {deveria_thiago:,.2f} | Luciana: R$ {deveria_luciana:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

with col_right:
    if diff_thiago > 0:
        acerto_nome = "Luciana deve Thiago"
        acerto_val = f"R$ {abs(diff_thiago):,.2f}"
    else:
        acerto_nome = "Thiago deve Luciana"
        acerto_val = f"R$ {abs(diff_thiago):,.2f}"

    porcentagem_maior = max(perc_thiago, perc_luciana) * 100

    st.markdown(f"""
        <div class="donut-card">
            <span style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.9;">Balanço do Acerto</span>
            <div class="donut-ring" style="--percent: {porcentagem_maior:.1f}%;">
                <div class="donut-content">{porcentagem_maior:.1f}%</div>
            </div>
            <div style="font-size: 0.8rem; font-weight: 600; opacity: 0.9; margin-top: -4px;">{acerto_nome}</div>
            <h2 style="font-size: 1.8rem; font-weight: 900; margin: 4px 0 12px 0;">{acerto_val}</h2>
            <div style="display: flex; justify-content: space-around; width: 100%; font-size: 0.75rem; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px;">
                <div><span>Thiago Pagou</span><br><b>R$ {bruto_thiago:,.2f}</b></div>
                <div><span>Luciana Pagou</span><br><b>R$ {bruto_luciana:,.2f}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# Abas de Ação e Edição
tab1, tab2, tab3 = st.tabs(["📊 Extrato & Edição Direta", "⚡ Adicionar & Gerenciar Lançamentos", "⚙️ Configurar Aluguel"])

with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("<h4 style='color: #ffffff; margin-bottom: 12px;'>📈 Rendas Registradas</h4>", unsafe_allow_html=True)
        if rendas:
            df_r = pd.DataFrame(rendas).rename(columns={"pessoa": "Pessoa", "desc": "Descrição", "valor": "Valor"})
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
        st.markdown("<h4 style='color: #ffffff; margin-bottom: 12px;'>📉 Despesas Pagas</h4>", unsafe_allow_html=True)
        if despesas:
            df_d = pd.DataFrame(despesas).rename(columns={"pessoa": "Pessoa", "desc": "Descrição", "valor": "Valor"})
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
    st.markdown("<h4 style='color: #ffffff;'>⚡ Novo Lançamento</h4>", unsafe_allow_html=True)
    with st.form("form_novo_lancamento", clear_on_submit=True):
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            f_tipo = st.selectbox("Tipo de Movimentação", ["Despesa", "Renda"])
            f_pessoa = st.selectbox("Responsável", ["Thiago", "Luciana"])
        with c_f2:
            f_desc = st.text_input("Descrição (ex: Supermercado, Aluguel, Salário, Diárias)")
            f_valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
            
        btn_salvar = st.form_submit_button("Salvar Lançamento")
        if btn_salvar:
            if f_desc and f_valor > 0:
                chave = "rendas" if f_tipo == "Renda" else "despesas"
                db[mes_atual][chave].append({"pessoa": f_pessoa, "desc": f_desc, "valor": f_valor})
                salvar_dados(db)
                st.success("Lançamento adicionado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha a descrição e um valor válido maior que zero.")

    st.markdown("---")
    st.markdown("<h4 style='color: #ffffff;'>✏️ Editar ou Excluir Lançamentos</h4>", unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        if rendas:
            r_opts = {f"{r['pessoa']} - {r['desc']} (R$ {r['valor']:,.2f})": i for i, r in enumerate(rendas)}
            r_sel = st.selectbox("Selecione a Renda", options=list(r_opts.keys()))
            idx_r = r_opts[r_sel]
            item_r = rendas[idx_r]
            with st.form(f"form_r_{idx_r}"):
                er_p = st.selectbox("Pessoa", ["Thiago", "Luciana"], index=0 if item_r["pessoa"] == "Thiago" else 1)
                er_d = st.text_input("Descrição", value=item_r["desc"])
                er_v = st.number_input("Valor (R$)", min_value=0.0, value=float(item_r["valor"]), step=10.0, format="%.2f")
                c_b1, c_b2 = st.columns(2)
                with c_b1:
                    if st.form_submit_button("Atualizar"):
                        db[mes_atual]["rendas"][idx_r] = {"pessoa": er_p, "desc": er_d, "valor": er_v}
                        salvar_dados(db)
                        st.rerun()
                with c_b2:
                    if st.form_submit_button("Excluir"):
                        db[mes_atual]["rendas"].pop(idx_r)
                        salvar_dados(db)
                        st.rerun()
        else:
            st.caption("Sem rendas cadastradas.")

    with col_e2:
        if despesas:
            d_opts = {f"{d['pessoa']} - {d['desc']} (R$ {d['valor']:,.2f})": i for i, d in enumerate(despesas)}
            d_sel = st.selectbox("Selecione a Despesa", options=list(d_opts.keys()))
            idx_d = d_opts[d_sel]
            item_d = despesas[idx_d]
            with st.form(f"form_d_{idx_d}"):
                ed_p = st.selectbox("Responsável", ["Thiago", "Luciana"], index=0 if item_d["pessoa"] == "Thiago" else 1)
                ed_d = st.text_input("Descrição", value=item_d["desc"])
                ed_v = st.number_input("Valor (R$)", min_value=0.0, value=float(item_d["valor"]), step=10.0, format="%.2f")
                c_b3, c_b4 = st.columns(2)
                with c_b3:
                    if st.form_submit_button("Atualizar"):
                        db[mes_atual]["despesas"][idx_d] = {"pessoa": ed_p, "desc": ed_d, "valor": ed_v}
                        salvar_dados(db)
                        st.rerun()
                with c_b4:
                    if st.form_submit_button("Excluir"):
                        db[mes_atual]["despesas"].pop(idx_d)
                        salvar_dados(db)
                        st.rerun()
        else:
            st.caption("Sem despesas cadastradas.")

with tab3:
    st.markdown("<h4 style='color: #ffffff;'>🏠 Configuração do Aluguel Extra (Aldepark)</h4>", unsafe_allow_html=True)
    st.write("Defina o valor do aluguel a ser abatido proporcionalmente das despesas totais:")
    c_a1, c_a2 = st.columns(2)
    with c_a1:
        novo_aluguel = st.number_input("Valor do Aluguel (R$)", min_value=0.0, value=aluguel_extra, step=50.0, format="%.2f")
    with c_a2:
        novo_recebedor = st.selectbox("Quem recebeu o dinheiro?", ["Thiago", "Luciana"], index=0 if aluguel_recebedor == "Thiago" else 1)
    if st.button("Atualizar Aluguel"):
        db[mes_atual]["aluguel_extra"] = novo_aluguel
        db[mes_atual]["aluguel_recebedor"] = novo_recebedor
        salvar_dados(db)
        st.success("Aluguel atualizado!")
        st.rerun()
