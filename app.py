import streamlit as st
from dashboard import render_dashboard
from flow import render_flow
from pm25_flow import render_pm25_flow

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
    /* อนุญาตให้แสดง Header ของ Streamlit เพื่อใช้เมนู Tool ได้ */
    /* header {visibility: hidden !important;} */
    footer {visibility: hidden !important;}

    /* ปรับระยะขอบของ Streamlit Container เพิ่ม padding-top เพื่อไม่ให้ถูก Header บัง */
    .block-container {
        padding-top: 4rem !important; 
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* ตกแต่ง Tabs ของ Streamlit ให้ดูทันสมัยและไม่โดนตัด */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        padding: 0 1rem;
        background-color: transparent;
        flex-wrap: wrap; /* รองรับหน้าจอมือถือให้ Tab ปัดบรรทัดได้ */
    }
    .stTabs [data-baseweb="tab"] {
        /* เปลี่ยนจากการล็อกความสูง (height) เป็นใช้ padding แทน เพื่อป้องกันหน้าจอตัดขอบ */
        padding: 0.75rem 1.5rem;
        border-radius: 10px 10px 0 0;
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
    
    /* ลบขอบ iframe */
    iframe {
        border: none !important;
        width: 100% !important;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. จัดการแสดงผล Tabs และเรียกใช้โมดูล (อัปเดต: ลบแท็บกระบวนการทำงานออก)
tab1, tab2, tab3 = st.tabs([
    "📊 แผนการดำเนินงาน", 
    "🔄 Flow การให้บริการ", 
    "🗺️ แผนผัง PM2.5"
])

with tab1:
    # เรียกใช้ฟังก์ชันจากไฟล์ dashboard.py
    render_dashboard()
    
with tab2:
    # เรียกใช้ฟังก์ชันจากไฟล์ flow.py
    render_flow()

with tab3:
    # เรียกใช้ฟังก์ชันจากไฟล์ pm25_flow.py 
    render_pm25_flow()
