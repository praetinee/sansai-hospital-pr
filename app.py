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

# 2. ปรับแต่ง CSS แบบขั้นสุด เพื่อลบขอบขาว กรอบ และเมนูของ Streamlit ทิ้งทั้งหมด
hide_streamlit_style = """
<style>
    /* ซ่อนแถบเมนู, Header, Footer ของ Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* ลบระยะขอบ (Padding/Margin) ของหน้า Streamlit ให้ชิดขอบจอ 100% ไม่มีช่องว่าง */
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }

    /* บังคับให้ iframe (ตัวเว็บ HTML) กว้างและสูงเต็มหน้าจอ 100vh พอดี ไม่มีขอบ */
    iframe {
        width: 100% !important;
        height: 100vh !important;
        border: none !important;
        display: block;
    }

    /* ปรับสีพื้นหลังที่อาจเป็นรอยต่อให้เป็นสีเดียวกับเว็บเรา */
    .stApp {
        background-color: #f8fafc;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. ค้นหาไฟล์ HTML
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
        
    # ให้ Streamlit นำโค้ด HTML มาโชว์ (ความกว้าง/สูงจะถูกคุมด้วย CSS ด้านบนให้เต็มจออัตโนมัติ)
    components.html(html_code)
    
except FileNotFoundError:
    st.error(f"❌ ไม่พบไฟล์ HTML: {file_name} กรุณาตรวจสอบว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
