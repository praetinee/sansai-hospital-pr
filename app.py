import streamlit as st
import streamlit.components.v1 as components
import os

# 1. ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="PM2.5 Action Plan - โรงพยาบาลสันทราย",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS (ลดการซ่อนแบบรุนแรงลง เพื่อให้เห็นว่า Streamlit ทำงานอยู่)
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* ปรับให้ชิดขอบจอมากขึ้น แต่ไม่ไปซ่อน header จนมองไม่เห็นสถานะโหลด */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. ค้นหาไฟล์ HTML โดยใช้ Path แบบสัมบูรณ์ (ป้องกันปัญหาหาไฟล์ไม่เจอเมื่อรันจากที่อื่น)
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "PM25ActionPlan2026.html")

# 4. อ่านและโหลดไฟล์ HTML
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
        
    # แสดงผล HTML (ใส่ความสูงให้ครอบคลุม และ width ให้เต็มจอ)
    components.html(html_code, height=3000, width=None, scrolling=True)
    
except FileNotFoundError:
    st.error(f"❌ ไม่พบไฟล์ HTML ที่ตำแหน่ง: {html_file_path}")
    st.info("💡 คำแนะนำ: โปรดตรวจสอบให้แน่ใจว่าไฟล์ PM25ActionPlan2026.html อยู่ในโฟลเดอร์เดียวกับไฟล์ app.py และสะกดชื่อไฟล์ถูกต้อง")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลด: {e}")
