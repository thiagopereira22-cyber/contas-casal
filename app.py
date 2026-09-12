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

# Estilização CSS refinada
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .stApp {
            background-color: #070913 !important;
            color: #f1f5f9;
        }

        [data-testid="stSidebar"] {
            background-color: #0c0f1d !important;
            border-right: 1px solid #1a2238;
        }

        /* Botões de mês: estilo pílula vertical */
        div[data-testid="stRadio"] > div {
            gap: 7px;
        }
        div[data-testid="stRadio"] label {
            background: #11162b !important;
            border: 1px solid #1c2442 !important;
            padding: 9px 14px !important;
            border-radius: 12px !important;
            cursor: pointer;
            transition: all 0.25s ease;
            color: #94a3b8 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: #ff007a !important;
            color: #ffffff !important;
            transform: translateX(3px);
        }

        /* Mês selecionado com o rosa idêntico ao cartão principal */
        div[data-testid="stRadio"] label:has(input:checked),
        div[data-testid="stRadio"] label[data-checked="true"],
        div[data-testid="stRadio"] [aria-checked="true"] {
            background: linear-gradient(135deg, #ff007a 0%, #ec4899 50%, #d946ef 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 18px rgba(255, 0, 122, 0.45) !important;
        }
        div[data-testid="stRadio"] label:has(input:checked) p,
        div[data-testid="stRadio"] label:has(input:checked) span {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        div[data-testid="stRadio"] label:has(input:checked) div[role="radio"] {
            border-color: #ffffff !important;
            background-color: #ffffff !important;
        }

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

        /* Cartões com alturas fixas para simetria milimétrica */
        .card-magenta-hero {
            background: linear-gradient(135deg, #ff007a 0%, #ec4899 50%, #d946ef 100%);
            border-radius: 22px;
            padding: 22px;
            color: white;
            box-shadow: 0 10px 30px rgba(255, 0, 122, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
            height: 195px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
        }

        .card-dark {
            background: #11162b;
            border: 1px solid #1c2442;
            border-radius: 22px;
            padding: 22px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            transition: border-color 0.2s ease;
            height: 195px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
        }
        .card-dark:hover {
            border-color: #2e3b68;
        }

        .donut-card {
            background: linear-gradient(145deg, #ff007a 0%, #c026d3 100%);
            border-radius: 22px;
            padding: 22px;
            color: white;
            box-shadow: 0 12px 35px rgba(236, 72, 153, 0.35);
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            height: 406px;
            box-sizing: border-box;
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
            margin: 4px auto;
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

DESPESAS_CATALOGO_PADRAO = [
    "Aluguel Duetto", "Cond. Duetto", "Energia Duetto", "IPTU Duetto",
    "Cond. Aldepark", "Energia Aldepark", "Cartão C6", "Escola Felipe",
    "Escola Vinícius", "Dentista vinicius", "Hapvida", "Parque das Flores",
    "Parque das Flores IPTU", "Ultragás", "Gasolina", "Supermercado", "Jô"
]

def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = {}

    if "catalogo_despesas" not in dados:
        dados["catalogo_despesas"] = sorted(DESPESAS_CATALOGO_PADRAO)

    for m in MESES_PADRAO:
        if m not in dados:
            dados[m] = {
                "rendas": [r.copy() for r in RENDAS_PADRAO],
                "despesas": [],
                "rendas_extras": [
                    {"nome": "Aluguel Aldepark", "valor": 3300.00, "recebedor": "Thiago"}
                ]
            }
        else:
            if not dados[m].get("rendas"):
                dados[m]["rendas"] = [r.copy() for r in RENDAS_PADRAO]
            if "rendas_extras" not in dados[m]:
                nome_antigo = dados[m].get("renda_extra_nome", "Aluguel Aldepark")
                val_antigo = dados[m].get("renda_extra_valor", dados[m].get("aluguel_extra", 3300.00))
                rec_antigo = dados[m].get("renda_extra_recebedor", dados[m].get("aluguel_recebedor", "Thiago"))
                dados[m]["rendas_extras"] = [
                    {"nome": nome_antigo, "valor": float(val_antigo), "recebedor": rec_antigo}
                ]
                
    return dados

def salvar_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

db = carregar_dados()

mapa_meses = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9,
    "outubro": 10, "novembro": 11, "dezembro": 12
}

def ordenar_meses(item):
    partes = item.strip().split()
    mes_nome = partes[0].lower()
    ano = int(partes[1]) if len(partes) > 1 and partes[1].isdigit() else 2026
    return (ano, mapa_meses.get(mes_nome, 0))

# Barra Lateral
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="display: inline-flex; width: 48px; height: 48px; border-radius: 50%; background: #11162b; border: 2px solid #ff007a; align-items: center; justify-content: center; box-shadow: 0 0 15px rgba(255, 0, 122, 0.5);">
                <span style="color: #ff007a; font-weight: 800; font-size: 1.2rem;">⚡</span>
            </div>
            <div style="font-size: 0.8rem; font-weight: 800; color: #94a3b8; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 10px;">Meses</div>
        </div>
    """, unsafe_allow_html=True)
    
    chaves_meses = [k for k in db.keys() if k != "catalogo_despesas"]
    todos_meses = sorted(chaves_meses, key=ordenar_meses)
    mes_atual = st.radio(
        label="Navegação Mensal",
        options=todos_meses,
        index=todos_meses.index("Setembro 2026") if "Setembro 2026" in todos_meses else 0,
        label_visibility="collapsed"
    )

# Cálculos Proporcionais e Rendas Extras
rendas = db[mes_atual]["rendas"]
despesas = db[mes_atual]["despesas"]
rendas_extras = db[mes_atual].get("rendas_extras", [])

total_renda_extra = sum(float(rx["valor"]) for rx in rendas_extras)

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

despesas_liquidas = max(0.0, despesas_brutas - total_renda_extra)
deveria_thiago = despesas_liquidas * perc_thiago
deveria_luciana = despesas_liquidas * perc_luciana

extra_recebido_thiago = sum(float(rx["valor"]) for rx in rendas_extras if rx.get("recebedor") == "Thiago")
extra_recebido_luciana = sum(float(rx["valor"]) for rx in rendas_extras if rx.get("recebedor") == "Luciana")

efetivo_thiago = bruto_thiago - extra_recebido_thiago
efetivo_luciana = bruto_luciana - extra_recebido_luciana

diff_thiago = efetivo_thiago - deveria_thiago

# Top Bar
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

# Grid Superior Simétrico e Alinhado
col_left, col_right = st.columns([6.8, 3.2])

with col_left:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="card-magenta-hero">
                <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.9;">Renda Total Consolidada</span>
                <div>
                    <h2 style="font-size: 1.85rem; font-weight: 800; margin: 0; color: #ffffff; line-height: 1.2;">R$ {renda_total:,.2f}</h2>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.76rem; opacity: 0.95; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 8px;">
                    <span>Thiago: <b>R$ {renda_thiago:,.2f}</b></span>
                    <span>Luciana: <b>R$ {renda_luciana:,.2f}</b></span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
            <div class="card-dark">
                <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;">Despesas Líquidas (Contas)</span>
                <div>
                    <h2 style="font-size: 1.85rem; font-weight: 800; margin: 0; color: #ffffff; line-height: 1.2;">R$ {despesas_liquidas:,.2f}</h2>
                    <svg width="100%" height="20" viewBox="0 0 200 20" fill="none" style="margin-top: 4px;">
                        <path d="M0 14 Q 30 2, 60 10 T 120 14 T 180 6 T 200 12" stroke="#ff007a" stroke-width="3" fill="none"/>
                    </svg>
                </div>
                <div style="font-size: 0.76rem; color: #94a3b8; border-top: 1px solid #1c2442; padding-top: 8px;">
                    Bruto: R$ {despesas_brutas:,.2f} | Rendas Extras: -R$ {total_renda_extra:,.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
            <div class="card-dark">
                <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;">Rendas Extras (Abatimento)</span>
                <div>
                    <h2 style="font-size: 1.85rem; font-weight: 800; margin: 0; color: #38bdf8; line-height: 1.2;">- R$ {total_renda_extra:,.2f}</h2>
                    <svg width="100%" height="20" viewBox="0 0 200 20" fill="none" style="margin-top: 4px;">
                        <path d="M0 12 Q 40 2, 80 8 T 140 14 T 200 6" stroke="#38bdf8" stroke-width="2.5" fill="none"/>
                    </svg>
                </div>
                <div style="font-size: 0.76rem; color: #94a3b8; border-top: 1px solid #1c2442; padding-top: 8px;">
                    {len(rendas_extras)} item(ns) cadastrado(s) abatendo das despesas.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="card-dark">
                <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;">Cota Proporcional das Contas</span>
                <div>
                    <h2 style="font-size: 1.55rem; font-weight: 800; margin: 0; color: #10b981; line-height: 1.2;">Thiago {perc_thiago*100:.1f}% | Luciana {perc_luciana*100:.1f}%</h2>
                    <svg width="100%" height="20" viewBox="0 0 200 20" fill="none" style="margin-top: 4px;">
                        <path d="M0 12 Q 50 16, 100 6 T 160 12 T 200 4" stroke="#10b981" stroke-width="2.5" fill="none"/>
                    </svg>
                </div>
                <div style="font-size: 0.76rem; color: #94a3b8; border-top: 1px solid #1c2442; padding-top: 8px;">
                    Thiago: R$ {deveria_thiago:,.2f} | Luciana: R$ {deveria_luciana:,.2f}
                </div>
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
            <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.9;">Balanço do Acerto</span>
            <div class="donut-ring" style="--percent: {porcentagem_maior:.1f}%;">
                <div class="donut-content">{porcentagem_maior:.1f}%</div>
            </div>
            <div>
                <div style="font-size: 0.8rem; font-weight: 600; opacity: 0.9;">{acerto_nome}</div>
                <h2 style="font-size: 1.85rem; font-weight: 900; margin: 4px 0 0 0; line-height: 1.2;">{acerto_val}</h2>
            </div>
            <div style="display: flex; justify-content: space-around; width: 100%; font-size: 0.75rem; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 8px;">
                <div><span>Thiago Pagou</span><br><b>R$ {bruto_thiago:,.2f}</b></div>
                <div><span>Luciana Pagou</span><br><b>R$ {bruto_luciana:,.2f}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

catalogo_despesas = db.get("catalogo_despesas", sorted(DESPESAS_CATALOGO_PADRAO))

# Abas de Ação e Edição
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Extrato & Edição Direta", 
    "⚡ Lançamentos", 
    "⚙️ Configurar Renda Extra",
    "🏷️ Cadastrar Despesas"
])

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
                    "Descrição": st.column_config.SelectboxColumn("Descrição", options=catalogo_despesas, required=True),
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
            if f_tipo == "Despesa":
                f_desc = st.selectbox("Escolha a Despesa Cadastrada", options=catalogo_despesas)
            else:
                f_desc = st.text_input("Descrição da Renda (ex: Salário, Diárias, Bônus)")
                
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
                idx_cat = catalogo_despesas.index(item_d["desc"]) if item_d["desc"] in catalogo_despesas else 0
                ed_d = st.selectbox("Descrição", options=catalogo_despesas, index=idx_cat)
                
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
    st.markdown("<h4 style='color: #ffffff;'>⚙️ Rendas Extras Compartilhadas (Abatimento de Dívidas)</h4>", unsafe_allow_html=True)
    st.write("Adicione ou edite rendas extras (como Aluguel Aldepark, bônus ou rendimentos) que abatem proporcionalmente do total de contas do casal:")
    
    with st.form("form_add_renda_extra", clear_on_submit=True):
        st.markdown("##### ➕ Adicionar Nova Renda Extra")
        c_rx1, c_rx2, c_rx3 = st.columns(3)
        with c_rx1:
            novo_rx_nome = st.text_input("Identificação (ex: Aluguel Aldepark, Bônus, Rendimento)")
        with c_rx2:
            novo_rx_valor = st.number_input("Valor da Renda Extra (R$)", min_value=0.0, step=50.0, format="%.2f")
        with c_rx3:
            novo_rx_recebedor = st.selectbox("Quem recebeu o dinheiro?", ["Thiago", "Luciana"])
            
        if st.form_submit_button("Cadastrar Renda Extra"):
            if novo_rx_nome and novo_rx_valor > 0:
                if "rendas_extras" not in db[mes_atual]:
                    db[mes_atual]["rendas_extras"] = []
                db[mes_atual]["rendas_extras"].append({
                    "nome": novo_rx_nome.strip(),
                    "valor": novo_rx_valor,
                    "recebedor": novo_rx_recebedor
                })
                salvar_dados(db)
                st.success(f"Renda Extra '{novo_rx_nome}' adicionada com sucesso!")
                st.rerun()
            else:
                st.error("Preencha o nome e informe um valor maior que zero.")

    st.markdown("---")
    st.markdown("##### 📋 Rendas Extras Ativas no Mês:")
    if rendas_extras:
        for idx_rx, rx in enumerate(rendas_extras):
            c_r1, c_r2, c_r3, c_r4 = st.columns([4, 3, 3, 2])
            with c_r1:
                st.markdown(f"<div style='padding-top: 10px; font-weight: 700; color: #38bdf8;'>• {rx['nome']}</div>", unsafe_allow_html=True)
            with c_r2:
                st.markdown(f"<div style='padding-top: 10px; color: #ffffff;'>R$ {float(rx['valor']):,.2f}</div>", unsafe_allow_html=True)
            with c_r3:
                st.markdown(f"<div style='padding-top: 10px; color: #94a3b8;'>Recebido por: <b>{rx['recebedor']}</b></div>", unsafe_allow_html=True)
            with c_r4:
                if st.button("Excluir", key=f"del_rx_{idx_rx}"):
                    db[mes_atual]["rendas_extras"].pop(idx_rx)
                    salvar_dados(db)
                    st.success("Renda Extra removida!")
                    st.rerun()
    else:
        st.info("Nenhuma renda extra cadastrada para este mês.")

with tab4:
    st.markdown("<h4 style='color: #ffffff;'>🏷️ Cadastrar e Gerenciar Despesas Padrão</h4>", unsafe_allow_html=True)
    st.write("Adicione novos tipos de contas à sua lista para que fiquem disponíveis na seleção na hora do lançamento:")
    
    c_cat1, c_cat2 = st.columns([7, 3])
    with c_cat1:
        nova_desp_nome = st.text_input("Nome da Nova Despesa (ex: Academia, Combustível, Plano de Saúde)")
    with c_cat2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Adicionar à Lista"):
            if nova_desp_nome and nova_desp_nome.strip():
                nome_limpo = nova_desp_nome.strip()
                if nome_limpo not in db["catalogo_despesas"]:
                    db["catalogo_despesas"].append(nome_limpo)
                    db["catalogo_despesas"] = sorted(db["catalogo_despesas"])
                    salvar_dados(db)
                    st.success(f"'{nome_limpo}' adicionada ao catálogo de despesas!")
                    st.rerun()
                else:
                    st.warning("Essa despesa já existe na sua lista.")
                    
    st.markdown("---")
    st.markdown("##### Despesas Cadastradas Atualmente:")
    
    col_d_list = st.columns(4)
    for idx_cat, cat in enumerate(db["catalogo_despesas"]):
        col_d_list[idx_cat % 4].markdown(f"""
            <div style="background: #11162b; border: 1px solid #1c2442; padding: 6px 12px; border-radius: 10px; margin-bottom: 6px; font-size: 0.8rem; color: #cbd5e1;">
                • {cat}
            </div>
        """, unsafe_allow_html=True)
