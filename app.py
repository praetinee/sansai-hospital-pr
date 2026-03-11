import streamlit as st
import pandas as pd

# ------------------------------------------------------------------
# 1. ส่วนการนำเข้าหน้าเพจอื่นๆ (Dashboard และ Flow) 
# โค้ดส่วนนี้ห้ามแก้ เพื่อให้ระบบดึงหน้าเดิมที่คุณทำไว้มาแสดงได้ปกติ
# ------------------------------------------------------------------
try:
    import dashboard
except ImportError:
    dashboard = None

try:
    import flow
except ImportError:
    flow = None

# ------------------------------------------------------------------
# 2. ฟังก์ชันระบบจัดการเวชภัณฑ์คงคลัง (เพิ่มใหม่)
# ------------------------------------------------------------------
def load_and_process_inventory(file_path, item_column_name):
    """ฟังก์ชันอ่านและดึงข้อมูลเฉพาะวันที่ล่าสุด"""
    try:
        # อ่านไฟล์ CSV ข้าม 2 บรรทัดแรกที่เป็นคำอธิบาย
        df = pd.read_csv(file_path, skiprows=2, encoding='utf-8-sig')
        df.rename(columns={df.columns[0]: item_column_name}, inplace=True)
        df = df.dropna(subset=[item_column_name])
        
        date_columns = df.columns[1:]
        
        # หาวันที่ล่าสุดที่มีข้อมูลกรอกไว้
        latest_date = date_columns[0]
        valid_date_cols = []
        
        for col in reversed(date_columns):
            if df[col].notna().any():
                latest_date = col
                break
                
        for col in date_columns:
            valid_date_cols.append(col)
            if col == latest_date:
                break
                
        return df, latest_date, valid_date_cols
        
    except FileNotFoundError:
        st.error(f"⚠️ ไม่พบไฟล์: {file_path}")
        return None, None, None
    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาดในการอ่านข้อมูล: {e}")
        return None, None, None

def display_modern_inventory_table(df, item_col, latest_date, valid_date_cols):
    """ฟังก์ชันแสดงตารางเวชภัณฑ์แบบมีกราฟเส้น (Sparkline)"""
    if df is None or df.empty:
        return

    display_df = pd.DataFrame()
    display_df['รายการ'] = df[item_col]
    display_df['คงเหลือล่าสุด'] = df[latest_date].fillna(0).astype(int)
    
    # สร้างประวัติย้อนหลังเป็น List สำหรับแสดงเป็นกราฟ
    history_data = []
    for index, row in df.iterrows():
        hist = [float(x) if pd.notna(x) else 0.0 for x in row[valid_date_cols].values]
        history_data.append(hist)
        
    display_df['ประวัติย้อนหลัง'] = history_data

    # แสดงผลตารางด้วย UI แบบใหม่ของ Streamlit
    st.dataframe(
        display_df,
        column_config={
            "รายการ": st.column_config.TextColumn("📝 ชื่อรายการ", width="large"),
            "คงเหลือล่าสุด": st.column_config.NumberColumn(
                f"📦 จำนวนคงเหลือ ณ {latest_date}",
                help="ข้อมูลอัปเดตล่าสุด",
                format="%d",
            ),
            "ประวัติย้อนหลัง": st.column_config.LineChartColumn(
                "📈 แนวโน้มการเบิกจ่าย (ย้อนหลัง)",
                help=f"กราฟแสดงการเปลี่ยนแปลงตั้งแต่วันแรกถึง {latest_date}"
            )
        },
        hide_index=True,
        use_container_width=True
    )

# ------------------------------------------------------------------
# 3. ฟังก์ชันการทำงานหลักของแอป
# ------------------------------------------------------------------
def main():
    # ตั้งค่าหน้าเพจหลัก
    st.set_page_config(
        page_title="ระบบรายงาน PM 2.5 - รพ.สันทราย",
        page_icon="🏥",
        layout="wide"
    )

    st.title("🏥 ศูนย์ปฏิบัติการฉุกเฉิน (EOC) กรณีฝุ่นละออง PM 2.5")
    st.subheader("โรงพยาบาลสันทราย จังหวัดเชียงใหม่")
    st.divider()

    # สร้าง Tabs ด้านบน
    tab_dashboard, tab_flow, tab_inventory = st.tabs([
        "📊 แดชบอร์ด (Dashboard)", 
        "🔄 โฟลว์การทำงาน (Flow)", 
        "📦 เวชภัณฑ์และยาคงคลัง"
    ])

    # --- หน้า Dashboard (ของเดิม) ---
    with tab_dashboard:
        if dashboard and hasattr(dashboard, 'main'):
            dashboard.main()
        elif dashboard and hasattr(dashboard, 'render'):
            dashboard.render()
        else:
            st.info("📌 หน้าแดชบอร์ด (เชื่อมต่อไฟล์ dashboard.py)")

    # --- หน้า Flow (ของเดิม) ---
    with tab_flow:
        if flow and hasattr(flow, 'main'):
            flow.main()
        elif flow and hasattr(flow, 'render'):
            flow.render()
        else:
            st.info("📌 หน้าโฟลว์การทำงาน (เชื่อมต่อไฟล์ flow.py)")

    # --- หน้าเวชภัณฑ์คงคลัง (เพิ่มใหม่ตามคำขอ) ---
    with tab_inventory:
        st.markdown("## 🏥 ระบบรายงานเวชภัณฑ์และยาคงคลัง (PM 2.5)")
        st.markdown("แสดงข้อมูลจำนวนคงคลัง **เฉพาะข้อมูลล่าสุด** พร้อมกราฟแนวโน้มย้อนหลังเพื่อให้ดูง่ายและสบายตา")
        st.divider()

        # ชื่อไฟล์อ้างอิงตรงตามที่คุณใช้งาน
        med_supplies_file = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - พัสดุการแพทย์.csv"
        medicines_file = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - ยา.csv"

        # ดึงข้อมูลมาประมวลผล
        df_sup, latest_date_sup, valid_cols_sup = load_and_process_inventory(med_supplies_file, "รายการพัสดุการแพทย์")
        df_med, latest_date_med, valid_cols_med = load_and_process_inventory(medicines_file, "รายการยา")

        # แจ้งเตือนวันที่อัปเดตข้อมูลล่าสุด
        latest_update = latest_date_sup if latest_date_sup else "ไม่มีข้อมูล"
        st.info(f"🔄 **อัปเดตข้อมูลล่าสุดเมื่อ:** {latest_update}")

        # แบ่งหมวดหมู่พัสดุและยา
        tab_sup, tab_med = st.tabs(["📦 พัสดุการแพทย์", "💊 รายการยา"])

        with tab_sup:
            display_modern_inventory_table(df_sup, "รายการพัสดุการแพทย์", latest_date_sup, valid_cols_sup)

        with tab_med:
            display_modern_inventory_table(df_med, "รายการยา", latest_date_med, valid_cols_med)

if __name__ == "__main__":
    main()
