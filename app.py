import streamlit as st
from dashboard import render_dashboard
from flow import render_flow
from pm25_flow import render_pm25_flow

# ==========================================
# 1. ตั้งค่าหน้าเพจหลัก (Page Config) ต้องอยู่บรรทัดแรกสุด
# ==========================================
st.set_page_config(
    page_title="ระบบเฝ้าระวังและดูแลผู้ป่วย PM 2.5",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ตกแต่ง CSS เพิ่มเติม (ซ่อนเมนูและปรับ UI)
# ==========================================
st.markdown("""
    <style>
    /* ซ่อน Hamburger Menu และ Footer ของ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ปรับระยะห่างด้านบนของหน้าจอให้แคบลง */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* ตกแต่ง Tabs ให้สวยงามและอ่านง่ายขึ้น */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        white-space: pre-wrap;
        background-color: #f8fafc;
        border-radius: 0.5rem 0.5rem 0 0;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        color: #475569;
        font-weight: 600;
        border: 1px solid #e2e8f0;
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e0f2fe !important;
        border-bottom: 3px solid #0284c7 !important;
        color: #0369a1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. แถบด้านข้าง (Sidebar) สำหรับเมนูหรือข้อมูลเบื้องต้น
# ==========================================
with st.sidebar:
    st.title("🏥 รพ.สันทราย")
    st.markdown("**ระบบเฝ้าระวังผู้ป่วย PM 2.5**")
    st.markdown("---")
    st.info("📌 **ย้ำเตือน:**\nกรุณาลงรหัส **Z58.1** (Exposure to air pollution) ทุกครั้งในผู้ป่วยที่เข้าข่าย เพื่อประโยชน์ในการจัดเก็บและวิเคราะห์ข้อมูล")
    st.markdown("---")
    st.caption("อัปเดตล่าสุด: ข้อมูล Flow การให้บริการ")

# ==========================================
# 4. ส่วนหัวของหน้าเว็บหลัก (Main Header)
# ==========================================
st.title("🏥 ระบบการให้บริการ รพ.สันทราย (กรณี PM 2.5)")
st.markdown("ระบบรายงานและแผนผังกระบวนการดำเนินงาน กรณีผู้ป่วยสงสัยตนเอง/ญาติได้รับผลกระทบจาก PM 2.5 จังหวัดเชียงใหม่")
st.markdown("---")

# ==========================================
# 5. จัดการแสดงผล Tabs (อัปเดตชื่อแท็บใหม่)
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📊 แผนการดำเนินงาน", 
    "🔄 Flow การให้บริการ", 
    "🗺️ บทบาทของแต่ละหน่วยงาน"
])

# ==========================================
# 6. ดึงเนื้อหาจากโมดูลภายนอกมาแสดงในแต่ละ Tab
# ==========================================
with tab1:
    render_dashboard()
    
with tab2:
    render_flow()
    
with tab3:
    render_pm25_flow()
