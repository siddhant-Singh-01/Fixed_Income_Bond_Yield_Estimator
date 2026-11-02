from bond_calculator import bond_calc as bc
from bond_chart import plot_graph as pg
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Bond Yield Estimator",
    layout="wide"
)
st.write("Compare bond investments against bank savings.")

# Initializing session state
if "bonds" not in st.session_state:
    st.session_state.bonds = {}
if "bond_counter" not in st.session_state:
    st.session_state.bond_counter = 0

# Creating new tab
if st.button("+ Add bond"):
    bond_id = st.session_state.bond_counter
    st.session_state.bonds[bond_id] = {
        "name": f"Default name {bond_id}",
        "price": 1000.0,
        "coupon": 50.0,
        "principal": 1000.0,
        "start_year": 2026,
        "end_year": 2030,
        "result": 3.82
    }
    st.session_state.bond_counter += 1
    st.rerun()

# Reusable bond interface
def bond_page(bond_id, bond_data):
    st.subheader(bond_data["name"])
    name = st.text_input(
                "Bond name: ",
                value=bond_data["name"],
                key=f"name_{bond_id}"
            )
    st.session_state.bonds[bond_id]["name"] = name
    with st.form(key=f"bond_form_{bond_id}"):
        price = st.number_input(
            "Purchase price (£): ",
            min_value=0.01,
            value=bond_data["price"],
            key=f"price_{bond_id}"
        )
        coupon = st.number_input(
            "Annual coupon (£): ",
            min_value=0.0,
            value=bond_data["coupon"],
            key=f"coupon_{bond_id}"
        )
        principal = st.number_input(
            "Principal (£): ",
            min_value=0.01,
            value=bond_data["principal"],
            key=f"principal_{bond_id}"
        )
        start_year = st.number_input(
            "Start year: ",
            value=bond_data["start_year"],
            step=1,
            key=f"start_{bond_id}"
        )
        end_year = st.number_input(
            "End year: ",
            value=bond_data["end_year"],
            step=1,
            key=f"end_{bond_id}"
        )
        submitted = st.form_submit_button("Calculate")

    # Calculting bond
    if submitted:
        st.session_state.bonds[bond_id].update({
            "name": name,
            "price": price,
            "coupon": coupon,
            "principal": principal,
            "start_year": start_year,
            "end_year": end_year
        })
        st.session_state.bonds[bond_id].pop("calculator", None)
        st.session_state.bonds[bond_id].pop("result", None)
        calc = bc(start_year, end_year, price, coupon, principal)
        result = calc.Yield()
        st.session_state.bonds[bond_id]["calculator"] = calc
        st.session_state.bonds[bond_id]["result"] = result

    # Displaying saved results   
    if "calculator" in st.session_state.bonds[bond_id]:
        result = st.session_state.bonds[bond_id]["result"]
        calc = st.session_state.bonds[bond_id]["calculator"]
        st.metric(
            label="Break-even bank interest rate",
            value=f"{result:.2f}%"
        )
        fig = pg(calc)
        st.plotly_chart(fig, use_container_width=True)
    
# Generating Dynamic Tabs
if st.session_state.bonds:
    tab_names = []
    for bond_id, bond_data in st.session_state.bonds.items():
        tab_names.append(bond_data["name"])
    tabs = st.tabs(tab_names)
    for tab, (bond_id, bond_data) in zip(tabs, st.session_state.bonds.items()):
        with tab:
            bond_page(bond_id, bond_data)
else:
    st.info("Click 'Add bond' to create your first bond.")
