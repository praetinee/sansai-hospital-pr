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

# 2. เพิ่มข้อความเช็คสถานะ (ถ้าเห็นข้อความนี้ แสดงว่า Streamlit ทำงานปกติ)
st.markdown("### ⏳ กำลังโหลดระบบ PM2.5 Action Plan...")

# 3. ค้นหาไฟล์ HTML (รองรับทั้งการรันบน Local และ Cloud)
file_name = "PM25ActionPlan2026.html"
if os.path.exists(file_name):
    html_file_path = file_name
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, file_name)

# 4. อ่านและโหลดไฟล์ HTML
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
        
    # แสดงผล HTML
    components.html(html_code, height=2800, scrolling=True)
    
except FileNotFoundError:
    st.error(f"❌ ไม่พบไฟล์ HTML ที่ตำแหน่ง: {html_file_path}")
    st.info("💡 คำแนะนำ: โปรดตรวจสอบว่าไฟล์ชื่อ PM25ActionPlan2026.html อยู่ในโฟลเดอร์เดียวกัน และสะกดตัวพิมพ์เล็ก-ใหญ่ถูกต้อง")
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการโหลด: {e}")
