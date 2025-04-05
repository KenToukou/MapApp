import pandas as pd  # Ensure pandas is imported
import streamlit as st
from streamlit_folium import st_folium

from service.CVRP_service import CVRPService
from widgets.map_widget import create_map

# Set up the Streamlit page
st.set_page_config(page_title="フライト管理アプリ", layout="wide")
cities = pd.read_csv("./data/cities.csv")
is_optimal = None


@st.cache_data
def load_cities():
    # Load or preprocess your cities data here if needed
    return cities.copy()


if "best_edges" not in st.session_state:
    st.session_state.best_edges = None

# Initialize session state for optimized data if not already present
if "optimized_cities" not in st.session_state:
    st.session_state.optimized_cities = pd.DataFrame()

if "objective_value" not in st.session_state:
    st.session_state.objective_value = None

# Load the initial cities data
current_cities = load_cities()

# Determine which cities to display: optimized or original
if not st.session_state.optimized_cities.empty:
    display_cities = st.session_state.optimized_cities
else:
    display_cities = current_cities

if st.session_state.best_edges:
    best_edges = st.session_state.best_edges
else:
    best_edges = None

st.title("フライト管理アプリ")

# Display the cities table
st.subheader("都市一覧")
if not st.session_state.optimized_cities.empty:
    st.table(st.session_state.optimized_cities)
else:
    st.table(current_cities)

st.subheader("旅行客を乗せる最適ルート探索")
m_value = st.number_input("車両数 (m)", value=4, min_value=1, step=1)
Q_value = st.number_input("最大積載量 (Q)", value=800, min_value=1, step=50)

# Add the Optimize button
st.subheader("最適化実行")
if st.button("Optimize"):
    if m_value * Q_value >= cities["乗客"].sum():
        with st.spinner("最適化中..."):

            # Initialize the Traveling Salesman Service with current cities
            traveling_salesman = CVRPService(base_df=cities, m=m_value, Q=Q_value)
            traveling_salesman.set_base_data()

            # Perform optimization
            best_edges, objective_values = traveling_salesman.optimize()

            # Store the optimized cities in session state
            st.session_state.best_edges = best_edges
            st.session_state.objective_value = objective_values
            st.session_state.optimized_cities = current_cities.copy()

        is_optimal = True

    else:
        print("解なし")
        is_optimal = False
if is_optimal:
    st.subheader(f"最適化が完了しました 最小総移動距離:{objective_values} km")
elif is_optimal is False:
    st.subheader("この条件では解けません")
st.write("best_objective:", st.session_state.objective_value)
st.markdown("有名都市を強調")


# Create and display the map based on the selected cities
jp_map = create_map(display_cities, best_edges)
st_data = st_folium(jp_map, use_container_width=True)
