import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="PM2.5 Action Plan - โรงพยาบาลสันทราย",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS เพื่อซ่อนแถบเมนูและขอบขาวของ Streamlit ให้เหมือนเป็นเว็บไซต์ปกติ
hide_streamlit_style = """
<style>
    /* ซ่อน Header และ Footer พื้นฐานของ Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ลบช่องว่างรอบๆ เพื่อให้ HTML ของเราเต็มจอภาพ */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* ซ่อน scrollbar ของ iframe ถ้าเป็นไปได้ */
    iframe {
        border: none;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. อ่านและโหลดไฟล์ HTML ขึ้นมาแสดงผล
try:
    with open("PM25ActionPlan2026.html", "r", encoding="utf-8") as f:
        html_code = f.read()
        
    # ใช้ components.html แสดงผล ตั้งค่าความสูงให้ครอบคลุมเนื้อหา (ปรับเพิ่มลดได้)
    # และเปิด scrolling=True ให้ผู้ใช้เลื่อนดูเนื้อหาในโทรศัพท์ได้สะดวก
    components.html(html_code, height=2800, scrolling=True)
    
except FileNotFoundError:
    st.error("❌ ไม่พบไฟล์ 'PM25ActionPlan2026.html' กรุณาตรวจสอบว่าไฟล์อยู่ในโฟลเดอร์เดียวกันกับ app.py")
