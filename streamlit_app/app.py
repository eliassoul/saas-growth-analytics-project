import streamlit as st

from utils.data_loader import load_executive_metrics

from pages.executive_overview import render_overview
from pages.revenue_dynamics import render_revenue_dynamics
from pages.customer_retention import render_customer_retention
from pages.growth_analysis import render_growth
from pages.strategic_diagnosis import render_diagnosis

st.set_page_config(
    page_title="SaaS Growth Analytics",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

df = load_executive_metrics()


# ---------------------------------------------------------
# Sidebar Header
# ---------------------------------------------------------

st.sidebar.markdown("# SaaS Growth Analytics")
st.sidebar.caption("Executive Intelligence Dashboard")

st.sidebar.divider()


# ---------------------------------------------------------
# Custom Style
# ---------------------------------------------------------

st.markdown("""
<style>          

/* -----------------------------------------------------
GLOBAL FONT CONFIGURATION
Applies the Poppins font across the entire Streamlit app
to create a modern and consistent UI appearance.
----------------------------------------------------- */

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', Arial, sans-serif;
}


/* -----------------------------------------------------
SIDEBAR LAYOUT ADJUSTMENTS
Removes default Streamlit padding and spacing to allow
full control over sidebar layout and navigation styling.
----------------------------------------------------- */

/* Remove top padding from the sidebar container */
section[data-testid="stSidebar"] > div {
    padding-top: 0rem !important;
}

/* Reduce vertical spacing between sidebar elements */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}

/* Remove top margin from sidebar titles */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    margin-top: 0rem !important;
}


/* -----------------------------------------------------
CUSTOM SIDEBAR NAVIGATION (RADIO BUTTONS)
Transforms Streamlit radio buttons into styled navigation
items resembling a modern dashboard sidebar menu.
----------------------------------------------------- */

/* Hide the default radio circle indicator */
div[role="radiogroup"] > label > div:first-child {
    display: none;
}

/* Style each navigation item */
div[role="radiogroup"] label {
    width: 100%;
    display: flex;

    padding: 10px 12px;
    border-radius: 8px;
    margin-bottom: 6px;

    background-color: var(--secondary-background-color);
    color: var(--text-color);
}


/* -----------------------------------------------------
ACTIVE INDICATOR BAR
Adds a vertical accent bar on hover and when the item
is selected to improve visual navigation feedback.
----------------------------------------------------- */

/* Base container for navigation text */
div[role="radiogroup"] label > div:last-child {
    position: relative;
}

/* Hidden indicator bar (default state) */
div[role="radiogroup"] label > div:last-child::before {
    content: "";
    position: absolute;
    left: -10px;
    top: 20%;
    height: 60%;
    width: 0px;

    background-color: #3B82F6;
    border-radius: 4px;

    transition: width 0.18s cubic-bezier(.4,0,.2,1);
}

/* Show indicator on hover */
div[role="radiogroup"] label:hover > div:last-child::before {
    width: 4px;
}

/* Keep indicator visible for active item */
div[role="radiogroup"] input:checked + div::before {
    width: 4px;
}


/* -----------------------------------------------------
HOVER INTERACTION
Provides visual feedback when users hover over
navigation items.
----------------------------------------------------- */

div[role="radiogroup"] label:hover > div:last-child {
    color: #3B82F6;
    transition: all 0.2s cubic-bezier(.4,0,.2,1);        
}


/* -----------------------------------------------------
ACTIVE NAVIGATION STATE
Highlights the currently selected section in the sidebar.
----------------------------------------------------- */

div[role="radiogroup"] input:checked + div,
div[role="radiogroup"] input:checked + div * {
    font-weight: 600 !important;
    color: #3B82F6 !important;
}


/* -----------------------------------------------------
SIDEBAR FOOTER
Allows positioning of fixed content (credits, links,
or metadata) at the bottom of the sidebar.
----------------------------------------------------- */

.sidebar-footer {
    position: fixed;
    bottom: 20px;
    left: 0;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Navigation
# ---------------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Revenue Dynamics",
        "Customer Retention",
        "Growth Analysis",
        "Strategic Diagnosis"
    ]
)

st.sidebar.divider()

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.sidebar.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)

st.sidebar.markdown("Built by **Elias Soul**")

col1, col2, col3 = st.sidebar.columns(3)

with col1:
    st.markdown(
        """
        <div style="text-align:center;">
        <a href="https://github.com/eliassoul" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" width="28">
        </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col2:
    st.markdown(
        """
        <div style="text-align:center;">
        <a href="https://share.streamlit.io/user/eliassoul" target="_blank">
            <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="28">
        </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style="text-align:center;">
        <a href="https://www.linkedin.com/in/eliassoul/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="28">
        </a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Page Routing
# ---------------------------------------------------------

if page == "Executive Overview":
    render_overview(df)

elif page == "Revenue Dynamics":
    render_revenue_dynamics(df)

elif page == "Customer Retention":
    render_customer_retention(df)

elif page == "Growth Analysis":
    render_growth()

elif page == "Strategic Diagnosis":
    render_diagnosis()