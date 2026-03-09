import streamlit as st
from dashboard import render_dashboard
from flow import render_flow

# 1. ตั้งค่าหน้าเว็บ Streamlit ให้เป็นแบบกว้างสุด (Wide)
st.set_page_config(
    page_title="PM2.5 Action Plan - โรงพยาบาลสันทราย",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS แบบขั้นสุด
hide_streamlit_style = """
<style>
    /* อนุญาตให้แสดงแถบเมนูและ Header ของ Streamlit */
    /* #MainMenu {visibility: hidden !important;} */
    /* header {visibility: hidden !important;} */
    footer {visibility: hidden !important;}

    /* ปรับระยะขอบของ Streamlit Container ให้เต็มจอ */
    .block-container {
        padding: 1rem 0rem 0rem 0rem !important;
        max-width: 100% !important;
    }

    /* ตกแต่ง Tabs ของ Streamlit ให้ดูทันสมัยและเข้ากับธีม */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        padding: 0 2rem;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        padding: 0 1.5rem;
        border-radius: 12px 12px 0 0;
        background-color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: bold;
        color: #475569;
        border: 1px solid #cbd5e1;
        border-bottom: none;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #059669 !important;
        color: white !important;
        border-color: #059669 !important;
    }
    
    /* ลบขอบ iframe ที่จะดึงโมดูลมาแสดง */
    iframe {
        border: none !important;
        width: 100% !important;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. จัดการแสดงผล Tabs และเรียกใช้โมดูลที่แยกไว้
tab1, tab2 = st.tabs(["📊 แผนการดำเนินงาน (Dashboard)", "🔄 Flow การให้บริการ"])

with tab1:
    # เรียกใช้ฟังก์ชันจากไฟล์ dashboard.py
    render_dashboard()
    
with tab2:
    # เรียกใช้ฟังก์ชันจากไฟล์ flow.py
    render_flow()
