import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from groq import Groq

from data.materials import MATERIALS, CATEGORIES
from data.calculator import calculate_project, get_summary, build_context_for_ai

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CarbonLens",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #0e1117; }
    .metric-card {
        background: #1a1d27;
        border: 1px solid #2d3142;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 8px;
    }
    .metric-label { color: #8b8fa8; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { color: #e8eaf6; font-size: 28px; font-weight: 700; margin-top: 4px; }
    .metric-sub   { color: #5c6079; font-size: 12px; margin-top: 2px; }
    .section-header {
        color: #e8eaf6;
        font-size: 16px;
        font-weight: 600;
        margin: 24px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #2d3142;
    }
    .chat-user { background: #1e2235; border-radius: 10px; padding: 10px 14px; margin: 6px 0; color: #c5c8e6; }
    .chat-ai   { background: #16192b; border-left: 3px solid #4caf81; border-radius: 0 10px 10px 0; padding: 10px 14px; margin: 6px 0; color: #c5c8e6; }
    .stButton > button {
        background: #4caf81;
        color: #0a1a12;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
    }
    .stButton > button:hover { background: #3d9a6e; }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stTextInput"] label { color: #8b8fa8 !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────
if "project_items" not in st.session_state:
    st.session_state.project_items = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
if "summary" not in st.session_state:
    st.session_state.summary = {}
if "last_uploaded_csv" not in st.session_state:
    st.session_state.last_uploaded_csv = None
if "show_results_preview" not in st.session_state:
    st.session_state.show_results_preview = False
if "chat_swap_preview" not in st.session_state:
    st.session_state.chat_swap_preview = None  # {before_df, after_df, new_items, applied}

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 CarbonLens")
    st.markdown("<p style='color:#5c6079;font-size:13px;margin-top:-12px;'>Carbon & cost analytics for the built environment</p>", unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "➕ Add Materials", "🤖 AI Assistant"],
        index=["📊 Dashboard", "➕ Add Materials", "🤖 AI Assistant"].index(
            st.session_state.pop("_nav", "📊 Dashboard")
            if "_nav" in st.session_state
            else "📊 Dashboard"
        ),
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("<p style='color:#3d3f52;font-size:11px;'>Carbon data: ICE Database v3.0<br>University of Bath</p>", unsafe_allow_html=True)

# ── Recalculate df whenever items change ─────────────────────────────────────
if st.session_state.project_items:
    st.session_state.df = calculate_project(st.session_state.project_items)
    st.session_state.summary = get_summary(st.session_state.df)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown("## Project Dashboard")

    df = st.session_state.df
    summary = st.session_state.summary

    if df.empty:
        st.info("No materials added yet. Go to **➕ Add Materials** to get started.", icon="💡")
    else:
        # ── KPI cards ───────────────────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Total embodied carbon</div>
                <div class='metric-value'>{summary['total_carbon']:,}</div>
                <div class='metric-sub'>kgCO₂e</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Total estimated cost</div>
                <div class='metric-value'>£{summary['total_cost']:,.0f}</div>
                <div class='metric-sub'>GBP</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Carbon intensity</div>
                <div class='metric-value'>{summary['avg_carbon_per_gbp']:.3f}</div>
                <div class='metric-sub'>kgCO₂e per £</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Elements tracked</div>
                <div class='metric-value'>{summary['num_elements']}</div>
                <div class='metric-sub'>building elements</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("")

        # ── Charts row 1 ────────────────────────────────────────────────────
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("<p class='section-header'>Carbon vs Cost by Element</p>", unsafe_allow_html=True)
            fig_scatter = px.scatter(
                df,
                x="Cost (£)",
                y="Carbon (kgCO₂e)",
                color="Category",
                size="Carbon (kgCO₂e)",
                hover_name="Element",
                hover_data={"Material": True, "Quantity": True, "Unit": True},
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template="plotly_dark",
            )
            fig_scatter.update_layout(
                paper_bgcolor="#1a1d27",
                plot_bgcolor="#1a1d27",
                font_color="#c5c8e6",
                legend=dict(bgcolor="#1a1d27"),
                margin=dict(t=20, b=20, l=20, r=20),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_right:
            st.markdown("<p class='section-header'>Carbon Breakdown by Element</p>", unsafe_allow_html=True)
            fig_bar = px.bar(
                df.sort_values("Carbon (kgCO₂e)", ascending=True),
                x="Carbon (kgCO₂e)",
                y="Element",
                orientation="h",
                color="Category",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template="plotly_dark",
            )
            fig_bar.update_layout(
                paper_bgcolor="#1a1d27",
                plot_bgcolor="#1a1d27",
                font_color="#c5c8e6",
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # ── Charts row 2 ────────────────────────────────────────────────────
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("<p class='section-header'>Carbon share by category</p>", unsafe_allow_html=True)
            cat_df = df.groupby("Category")["Carbon (kgCO₂e)"].sum().reset_index()
            fig_pie = px.pie(
                cat_df,
                values="Carbon (kgCO₂e)",
                names="Category",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template="plotly_dark",
                hole=0.45,
            )
            fig_pie.update_layout(
                paper_bgcolor="#1a1d27",
                font_color="#c5c8e6",
                margin=dict(t=20, b=20, l=20, r=20),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            st.markdown("<p class='section-header'>Carbon intensity heatmap (kgCO₂e per £)</p>", unsafe_allow_html=True)
            heat_df = df[["Element", "Material", "Carbon/£ ratio"]].copy()
            heat_df = heat_df.sort_values("Carbon/£ ratio", ascending=False)
            fig_heat = go.Figure(data=go.Bar(
                x=heat_df["Element"],
                y=heat_df["Carbon/£ ratio"],
                marker_color=heat_df["Carbon/£ ratio"],
                marker_colorscale=[[0, "#4caf81"], [0.5, "#f0c040"], [1, "#e05252"]],
                text=[f"{v:.4f}" for v in heat_df["Carbon/£ ratio"]],
                textposition="outside",
            ))
            fig_heat.update_layout(
                template="plotly_dark",
                paper_bgcolor="#1a1d27",
                plot_bgcolor="#1a1d27",
                font_color="#c5c8e6",
                margin=dict(t=20, b=40, l=20, r=20),
                yaxis_title="kgCO₂e / £",
                xaxis_tickangle=-30,
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        # ── Data table ──────────────────────────────────────────────────────
        st.markdown("<p class='section-header'>Full element breakdown</p>", unsafe_allow_html=True)
        display_df = df.drop(columns=["Carbon factor", "Carbon/£ ratio"]).copy()
        display_df["Carbon (kgCO₂e)"] = display_df["Carbon (kgCO₂e)"].map("{:,.1f}".format)
        display_df["Cost (£)"] = display_df["Cost (£)"].map("£{:,.2f}".format)
        st.dataframe(display_df, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: ADD MATERIALS
# ════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Materials":
    st.markdown("## Add Materials")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<p class='section-header'>Add an element</p>", unsafe_allow_html=True)

        element_name = st.text_input("Element name", placeholder="e.g. Ground floor slab")

        category_filter = st.selectbox("Filter by category", ["All"] + CATEGORIES)
        filtered = {
            k: v for k, v in MATERIALS.items()
            if category_filter == "All" or v["category"] == category_filter
        }

        material = st.selectbox("Material", list(filtered.keys()))

        if material:
            mat_info = MATERIALS[material]
            st.caption(f"📋 {mat_info['description']}")
            st.caption(f"💨 Carbon factor: **{mat_info['carbon_factor']} kgCO₂e/kg** · Unit: **{mat_info['unit']}**")

        quantity = st.number_input(
            f"Quantity ({MATERIALS[material]['unit'] if material else ''})",
            min_value=0.1, value=1.0, step=0.5
        )

        if st.button("Add to project ➕", use_container_width=True):
            if element_name and material and quantity > 0:
                with st.spinner("Calculating carbon & cost..."):
                    st.session_state.project_items.append({
                        "element": element_name,
                        "material": material,
                        "quantity": quantity,
                    })
                    st.session_state.df = calculate_project(st.session_state.project_items)
                    st.session_state.summary = get_summary(st.session_state.df)
                st.session_state.show_results_preview = True
                st.success(f"✅ Added **{element_name}**")
                st.rerun()
            else:
                st.warning("Please fill in all fields.")

        # CSV upload
        st.markdown("<p class='section-header'>Or upload a CSV</p>", unsafe_allow_html=True)
        st.caption("Columns: `element`, `material`, `quantity`")
        uploaded = st.file_uploader("Upload bill of materials", type="csv", label_visibility="collapsed")
        if uploaded and uploaded.name != st.session_state.last_uploaded_csv:
            try:
                with st.spinner(f"Importing {uploaded.name} and calculating..."):
                    csv_df = pd.read_csv(uploaded)
                    imported = 0
                    for _, row in csv_df.iterrows():
                        if row["material"] in MATERIALS:
                            st.session_state.project_items.append({
                                "element": str(row["element"]),
                                "material": str(row["material"]),
                                "quantity": float(row["quantity"]),
                            })
                            imported += 1
                    st.session_state.df = calculate_project(st.session_state.project_items)
                    st.session_state.summary = get_summary(st.session_state.df)
                    st.session_state.last_uploaded_csv = uploaded.name
                st.session_state.show_results_preview = True
                st.success(f"✅ Imported {imported} rows.")
                st.rerun()
            except Exception as e:
                st.error(f"Import failed: {e}")

    with col2:
        st.markdown("<p class='section-header'>Current project elements</p>", unsafe_allow_html=True)

        if not st.session_state.project_items:
            st.info("No elements added yet.")
        else:
            for i, item in enumerate(st.session_state.project_items):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{item['element']}**  \n`{item['material']}` — {item['quantity']} {MATERIALS[item['material']]['unit']}")
                with cols[1]:
                    if st.button("🗑", key=f"del_{i}"):
                        st.session_state.project_items.pop(i)
                        st.rerun()
                st.divider()

            if st.button("🗑 Clear all", use_container_width=True):
                st.session_state.project_items = []
                st.session_state.df = pd.DataFrame()
                st.rerun()

        # Sample project loader
        st.markdown("<p class='section-header'>Load a sample project</p>", unsafe_allow_html=True)
        if st.button("Load example: 3-storey office", use_container_width=True):
            with st.spinner("Loading sample project..."):
                st.session_state.project_items = [
                    {"element": "Ground floor slab",     "material": "Concrete (general)",         "quantity": 150},
                    {"element": "Structural frame",       "material": "Structural steel (virgin)",   "quantity": 45},
                    {"element": "Upper floor slabs",      "material": "Precast concrete",            "quantity": 200},
                    {"element": "External walls",         "material": "Brick (clay)",                "quantity": 80},
                    {"element": "Roof insulation",        "material": "PIR insulation board",        "quantity": 120},
                    {"element": "Curtain wall glazing",   "material": "Triple-glazed unit",          "quantity": 180},
                    {"element": "Internal partitions",    "material": "Concrete block",              "quantity": 60},
                    {"element": "Steel reinforcement",    "material": "Reinforcement bar (rebar)",   "quantity": 12},
                ]
                st.session_state.df = calculate_project(st.session_state.project_items)
                st.session_state.summary = get_summary(st.session_state.df)
            st.session_state.show_results_preview = True
            st.rerun()

    # ── Inline results preview ───────────────────────────────────────────────
    if st.session_state.show_results_preview and not st.session_state.df.empty:
        summary = st.session_state.summary
        df = st.session_state.df

        st.markdown("---")
        st.markdown("<p class='section-header'>📊 Results preview</p>", unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Total carbon", f"{summary['total_carbon']:,} kgCO₂e")
        with k2:
            st.metric("Total cost", f"£{summary['total_cost']:,.0f}")
        with k3:
            st.metric("Carbon intensity", f"{summary['avg_carbon_per_gbp']:.3f} kgCO₂e/£")
        with k4:
            st.metric("Elements", summary["num_elements"])

        display_df = df.drop(columns=["Carbon factor", "Carbon/£ ratio"]).copy()
        display_df["Carbon (kgCO₂e)"] = display_df["Carbon (kgCO₂e)"].map("{:,.1f}".format)
        display_df["Cost (£)"] = display_df["Cost (£)"].map("£{:,.2f}".format)
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        col_dismiss, col_dashboard = st.columns([1, 1])
        with col_dismiss:
            if st.button("Dismiss preview", use_container_width=True):
                st.session_state.show_results_preview = False
                st.rerun()
        with col_dashboard:
            if st.button("Go to full Dashboard →", use_container_width=True):
                st.session_state.show_results_preview = False
                st.session_state["_nav"] = "📊 Dashboard"
                st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# PAGE: AI ASSISTANT
# ════════════════════════════════════════════════════════════════════════════
elif page == "🤖 AI Assistant":
    st.markdown("## AI Assistant")

    df = st.session_state.df
    summary = st.session_state.summary

    if df.empty:
        st.warning("Add some materials first so the AI has data to analyse.", icon="⚠️")
    else:
        st.markdown(f"<p style='color:#5c6079;font-size:13px;'>Analysing {summary['num_elements']} elements · {summary['total_carbon']:,} kgCO₂e · £{summary['total_cost']:,.0f}</p>", unsafe_allow_html=True)

    # ── Suggested prompts ────────────────────────────────────────────────────
    st.markdown("<p class='section-header'>Suggested questions</p>", unsafe_allow_html=True)
    suggestions = [
        "Replace all structural steel with recycled steel and show me the impact",
        "Which element has the highest carbon and what's an alternative?",
        "How does this project compare to RIBA 2030 climate targets?",
        "Rank my materials from worst to best carbon intensity.",
    ]
    cols = st.columns(2)
    for i, s in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(s, key=f"sug_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": s})
                st.session_state.chat_swap_preview = None
                st.rerun()

    st.markdown("<p class='section-header'>Chat</p>", unsafe_allow_html=True)

    # ── Render chat history ──────────────────────────────────────────────────
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='chat-ai'>🌿 {msg['content']}</div>", unsafe_allow_html=True)

    # ── Swap preview table ───────────────────────────────────────────────────
    if st.session_state.chat_swap_preview and not st.session_state.chat_swap_preview.get("applied"):
        preview = st.session_state.chat_swap_preview
        st.markdown("<p class='section-header'>📊 Before vs After comparison</p>", unsafe_allow_html=True)

        before_df = preview["before_df"]
        after_df  = preview["after_df"]

        # Build comparison table
        compare_rows = []
        for _, b_row in before_df.iterrows():
            a_match = after_df[after_df["Element"] == b_row["Element"]]
            if not a_match.empty:
                a_row = a_match.iloc[0]
                carbon_delta = a_row["Carbon (kgCO₂e)"] - b_row["Carbon (kgCO₂e)"]
                cost_delta   = a_row["Cost (£)"]         - b_row["Cost (£)"]
                compare_rows.append({
                    "Element":         b_row["Element"],
                    "Before material": b_row["Material"],
                    "After material":  a_row["Material"],
                    "Before carbon":   f"{b_row['Carbon (kgCO₂e)']:,.1f}",
                    "After carbon":    f"{a_row['Carbon (kgCO₂e)']:,.1f}",
                    "Carbon saved":    f"{'−' if carbon_delta < 0 else '+'}{abs(carbon_delta):,.1f} kgCO₂e",
                    "Cost diff":       f"{'−£' if cost_delta < 0 else '+£'}{abs(cost_delta):,.2f}",
                    "Changed":         b_row["Material"] != a_row["Material"],
                })

        compare_df  = pd.DataFrame(compare_rows)
        changed_df  = compare_df[compare_df["Changed"]].drop(columns=["Changed"])
        if not changed_df.empty:
            st.markdown("**Swapped elements:**")
            st.dataframe(changed_df, use_container_width=True, hide_index=True)

        # Totals row
        b_total = before_df["Carbon (kgCO₂e)"].sum()
        a_total = after_df["Carbon (kgCO₂e)"].sum()
        b_cost  = before_df["Cost (£)"].sum()
        a_cost  = after_df["Cost (£)"].sum()
        totals_df = pd.DataFrame([{
            "":              "PROJECT TOTAL",
            "Before carbon": f"{b_total:,.1f} kgCO₂e",
            "After carbon":  f"{a_total:,.1f} kgCO₂e",
            "Carbon saved":  f"−{b_total - a_total:,.1f} kgCO₂e  ({(b_total - a_total)/b_total*100:.1f}% reduction)",
            "Cost diff":     f"{'−£' if a_cost < b_cost else '+£'}{abs(a_cost - b_cost):,.2f}",
        }])
        st.dataframe(totals_df, use_container_width=True, hide_index=True)

        col_apply, col_discard = st.columns([1, 1])
        with col_apply:
            if st.button("✅ Apply these changes to project", use_container_width=True):
                st.session_state.project_items = preview["new_items"]
                st.session_state.df      = after_df
                st.session_state.summary = get_summary(after_df)
                st.session_state.chat_swap_preview["applied"] = True
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Changes applied. Project total carbon is now {a_total:,.1f} kgCO₂e — a reduction of {b_total - a_total:,.1f} kgCO₂e ({(b_total - a_total)/b_total*100:.1f}%)."
                })
                st.rerun()
        with col_discard:
            if st.button("✖ Discard", use_container_width=True):
                st.session_state.chat_swap_preview = None
                st.rerun()

    # ── Chat input ───────────────────────────────────────────────────────────
    user_input = st.chat_input("Ask about your project — e.g. 'replace steel with recycled steel'")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_swap_preview = None
        st.rerun()

    # ── Process last user message ────────────────────────────────────────────
    needs_response = (
        st.session_state.chat_history
        and st.session_state.chat_history[-1]["role"] == "user"
    )

    if needs_response:
        project_context = build_context_for_ai(df, summary)
        valid_materials = list(MATERIALS.keys())

        system_prompt = f"""You are CarbonLens AI — an expert in embodied carbon and sustainable construction for the UK built environment.

You have access to the user's current project data:

{project_context}

Valid materials in the database: {json.dumps(valid_materials)}

IMPORTANT — SWAP DETECTION:
If the user asks you to replace, swap, or substitute a material (e.g. "replace steel with recycled steel", "swap concrete for CLT"), you MUST respond ONLY with a JSON object in this exact format and nothing else:

{{
  "type": "swap",
  "summary": "One sentence explaining what you are swapping and the expected impact.",
  "swaps": [
    {{"from_material": "exact current material name", "to_material": "exact new material name from the valid list"}}
  ]
}}

For ALL other questions (analysis, comparisons, rankings, explanations), respond in plain conversational text. Be concise (2-4 sentences per point), reference specific project numbers, and use kgCO₂e as the carbon unit."""

        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]

        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    max_tokens=800,
                    messages=[{"role": "system", "content": system_prompt}] + messages,
                )
                raw_reply = response.choices[0].message.content.strip()

                # Detect swap instruction
                swap_data = None
                try:
                    parsed = json.loads(raw_reply)
                    if parsed.get("type") == "swap":
                        swap_data = parsed
                except (json.JSONDecodeError, AttributeError):
                    pass

                if swap_data:
                    swap_map = {s["from_material"]: s["to_material"] for s in swap_data["swaps"]}
                    new_items = []
                    for item in st.session_state.project_items:
                        new_item = item.copy()
                        if item["material"] in swap_map and swap_map[item["material"]] in MATERIALS:
                            new_item["material"] = swap_map[item["material"]]
                        new_items.append(new_item)

                    after_df = calculate_project(new_items)
                    st.session_state.chat_swap_preview = {
                        "before_df": df.copy(),
                        "after_df":  after_df,
                        "new_items": new_items,
                        "applied":   False,
                    }
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": swap_data["summary"] + " Review the comparison table below."
                    })
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": raw_reply})

                st.rerun()
            except Exception as e:
                st.error(f"API error: {e}")

    if st.session_state.chat_history:
        if st.button("Clear chat", use_container_width=False):
            st.session_state.chat_history = []
            st.session_state.chat_swap_preview = None
            st.rerun()