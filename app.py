import streamlit as st
import pandas as pd
from summary import render_summary
from flow import render_flow  
from roles import render_roles
import inventory_tab 

# 1. ตั้งค่าหน้าเว็บ Streamlit ให้เป็นแบบกว้างสุด (Wide)
st.set_page_config(
    page_title="PM2.5 Action Plan - โรงพยาบาลสันทราย",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS แบบขั้นสุด (เพิ่มการบังคับใช้ฟอนต์ Sarabun)
hide_streamlit_style = """
<style>
    /* นำเข้าฟอนต์ Sarabun จาก Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700;800&display=swap');

    /* บังคับให้ทุกองค์ประกอบของ Streamlit ใช้ฟอนต์ Sarabun */
    html, body, [class*="css"], [class*="st-"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div, button, input, select, textarea, table {
        font-family: 'Sarabun', sans-serif !important;
    }

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

# 3. จัดการแสดงผล Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📑 สรุปผลภาพรวม",
    "🔄 ขั้นตอนการให้บริการ", 
    "🗺️ บทบาทของแต่ละหน่วยงาน",
    "📦 เวชภัณฑ์คงคลัง"
])

with tab1:
    render_summary()

with tab2:
    render_flow()

with tab3:
    render_roles()

with tab4:
    inventory_tab.render_inventory_ui()
