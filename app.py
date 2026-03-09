import streamlit as st
import streamlit.components.v1 as components
import os

# 1. ตั้งค่าหน้าเว็บ Streamlit ให้เป็นแบบกว้างสุด (Wide)
st.set_page_config(
    page_title="PM2.5 Action Plan - โรงพยาบาลสันทราย",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS แบบขั้นสุด เพื่อเปลี่ยน Streamlit ให้เป็นโครงสร้างรองรับ Web App ของเรา
hide_streamlit_style = """
<style>
    /* ซ่อนแถบเมนู, Header, Footer ของ Streamlit ให้หมดจด */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    /* ลบระยะขอบของ Streamlit Container ให้ชิดขอบจอ 100% */
    .block-container {
        padding: 0px !important;
        margin: 0px !important;
        max-width: 100% !important;
    }

    /* ล็อกหน้าจอหลักไม่ให้เลื่อน (ป้องกันปัญหา Scrollbar ซ้อนกัน 2 ชั้น) */
    .stApp {
        overflow: hidden !important;
        background-color: #f8fafc;
    }

    /* บังคับให้ iframe เต็มหน้าจอ 100% ทั้งความกว้างและความสูง */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        display: block;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. ค้นหาไฟล์ HTML อย่างรัดกุม (รองรับทั้งการรันบนคอมพิวเตอร์และบน Streamlit Cloud)
file_name = "PM25ActionPlan2026.html"
if os.path.exists(file_name):
    html_file_path = file_name
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, file_name)

# 4. โหลดและแสดงผลไฟล์ HTML
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
        
    # ให้ Streamlit นำโค้ด HTML มาโชว์ 
    # ข้อสำคัญ: ต้องใส่ scrolling=True เพื่อให้สามารถเลื่อนหน้าเว็บภายใน Iframe ได้
    components.html(html_code, scrolling=True)
    
except FileNotFoundError:
    st.error(f"❌ ไม่พบไฟล์ HTML: '{file_name}' กรุณาตรวจสอบว่าไฟล์ถูกอัปโหลดไว้ในโฟลเดอร์เดียวกับ app.py หรือไม่")
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการโหลดระบบ: {e}")
