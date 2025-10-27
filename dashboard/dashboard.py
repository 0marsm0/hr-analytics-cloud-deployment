# import streamlit as st
# from components.top_employers import show_top_employers
# from components.top_occupations import occupation_chart
# from components.exp_license import show_pie_chart
# from components.karta import create_map

# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("styles.css")

# chooser = ["Alla områden", "Installation, drift, underhåll", "Kropps- och skönhetsvård", "Kultur, media, design"]
# mart_schema = {
#     "Alla områden": "mart_main",
#     "Installation, drift, underhåll": "mart_idu",
#     "Kropps- och skönhetsvård": "mart_ks",
#     "Kultur, media, design": "mart_kmd"
# }

# def dashboard_page():
#     st.set_page_config(page_title="Jobtech_Analysis",layout="wide")

#     # Sidebar
#     with st.sidebar:
#         st.markdown('<div class="logo-container">', unsafe_allow_html=True)
#         st.markdown("""
#         <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                     border-radius: 10px; color: white; margin-bottom: 20px;'>
#             <h2>📊 Analytics</h2>
#             <p style='margin: 0; opacity: 0.8;'>Dashboard</p>
#         </div>
#         """, unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#         st.markdown("---")

#         st.markdown('<div class="logo-container">', unsafe_allow_html=True)
#         option = st.selectbox(
#                 "Occupation Field",
#                 chooser
#             )
#         st.markdown('</div>', unsafe_allow_html=True)

#     # Main content
#     st.markdown('<h1 class="dashboard-title">📊 Employment Analytics Dashboard</h1>', unsafe_allow_html=True)
#     st.write("---")

#     col1, col2 = st.columns(2, gap="large")
#     with col1:

#             st.markdown('<div class="card-title">💼 Top 10 Occupations</div>', unsafe_allow_html=True)
#             st.pyplot(occupation_chart(mart_schema[option]))
#     with col2:

#             st.markdown('<div class="card-title">🚗 Driver License & Experience</div>', unsafe_allow_html=True)
#             show_pie_chart(mart_schema[option])
#     col3, col4 = st.columns(2, gap="large")
#     with col3:

#             st.markdown('<div class="card-title">🗺️ Geographic Distribution</div>', unsafe_allow_html=True)
#             st.plotly_chart(create_map(mart_schema[option]))
#     with col4:

#             st.markdown('<div class="card-title">🏢 Top 10 Employers</div>', unsafe_allow_html=True)
#             show_top_employers(mart_schema[option])

# if __name__ == "__main__":
#     dashboard_page()


import streamlit as st
from pathlib import Path
from components.top_employers import show_top_employers
from components.top_occupations import occupation_chart
from components.exp_license import show_pie_chart
from components.karta import create_map
from conn_warehouse import get_job_list


style_path = Path(__file__).parent / "styles.css"


def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css(style_path)

chooser = [
    "Alla områden",
    "Data IT",
    "Transport, distribution, lager",
    "Hälso- och sjukvård",
]
mart_schema = {
    "Alla områden": "marts.mart_main",
    "Data IT": "marts.mart_it",
    "Transport, distribution, lager": "marts.mart_log",
    "Hälso- och sjukvård": "marts.mart_med",
}


def dashboard_page():
    st.set_page_config(page_title="Jobtech_Analysis", layout="wide")

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown(
            """
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%); 
                    border-radius: 10px; color: white; margin-bottom: 20px;'>
            <h2>📊 Analytics</h2>
            <p style='margin: 0; opacity: 0.8;'>Dashboard</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        option = st.selectbox("Occupation Field", chooser)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<h1 class="dashboard-title">📊 Employment Analytics Dashboard</h1>',
        unsafe_allow_html=True,
    )

    # KPI Cards
    df = get_job_list(query=f"SELECT * FROM {mart_schema[option]}")
    total_vacancies = len(df)
    # today_vacancies = df[df['publication_date'] == df['publication_date'].max()].shape[0] if "publication_date" in df else 0
    exp_required = df[df["experience_required"].isin([True, 1])].shape[0]
    license_required = df[df["driving_license_required"].isin([True, 1])].shape[0]

    kpi1, kpi3, kpi4 = st.columns(3)
    kpi1.metric("Total Vacancies", f"{total_vacancies:,}")
    # kpi2.metric("Today’s Vacancies", f"{today_vacancies:,}")
    kpi3.metric("With Experience", f"{exp_required:,}")
    kpi4.metric("With License", f"{license_required:,}")

    st.write("---")

    # Charts
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            '<div class="card-title">💼 Top 10 Occupations</div>',
            unsafe_allow_html=True,
        )
        st.pyplot(occupation_chart(mart_schema[option]))
    with col2:
        st.markdown(
            '<div class="card-title">🚗 Driver License & Experience</div>',
            unsafe_allow_html=True,
        )
        show_pie_chart(mart_schema[option])

    col3, col4 = st.columns(2, gap="large")
    with col3:
        st.markdown(
            '<div class="card-title">🗺️ Geographic Distribution</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(create_map(mart_schema[option]), use_container_width=True)
    with col4:
        st.markdown(
            '<div class="card-title">🏢 Top 10 Employers</div>', unsafe_allow_html=True
        )
        show_top_employers(mart_schema[option])


if __name__ == "__main__":
    dashboard_page()
