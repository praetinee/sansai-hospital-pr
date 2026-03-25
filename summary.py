import re
import streamlit.components.v1 as components
from inventory_tab import load_and_process_inventory, parse_value

def shorten_item_name(name):
    """ฟังก์ชันย่อชื่อเวชภัณฑ์ให้สั้นลง เพื่อให้แสดงผลใน Badges ได้สวยงาม"""
    name = str(name)
    # ลบข้อความในวงเล็บ (เช่น ขนาด, หน่วย)
    name = re.sub(r'\(.*?\)', '', name)
    # ตัดคำอธิบายหลังเครื่องหมาย - หรือ ,
    name = name.split(' - ')[0].split(',')[0]
    
    # พจนานุกรมสำหรับย่อคำ
    subs = {
        "หน้ากากอนามัย": "หน้ากาก",
        "ทางการแพทย์": "",
        "Solution": "Sol.",
        "Syrup": "Syr.",
        "Inhaler": "Inh.",
        "Suspension": "Susp.",
        "Tablet": "Tab.",
        "Capsule": "Cap."
    }
    
    # แทนที่คำโดยไม่สนใจตัวพิมพ์เล็ก-ใหญ่
    for old, new in subs.items():
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        name = pattern.sub(new, name)
        
    # ลบช่องว่างส่วนเกิน
    name = ' '.join(name.split())
    
    # ถ้ายังยาวไป ให้ตัดแล้วใส่ ...
    if len(name) > 28:
        name = name[:25] + "..."
        
    return name.strip()

def get_current_inventory_status(df, item_col, date_columns):
    """ฟังก์ชันคำนวณยอดคงเหลือที่แท้จริง โดยอิงโลจิกเดียวกับ inventory_tab"""
    in_stock = []
    out_stock = []
    total_sum = 0
    latest_date = "ล่าสุด"

    if df is None or df.empty or not date_columns:
        return in_stock, out_stock, total_sum, latest_date

    # 1. หาวันที่ที่มีการกรอกข้อมูลล่าสุด
    filled_dates = []
    for col in date_columns:
        if any(parse_value(val) is not None for val in df[col]):
            filled_dates.append(col)
            
    if not filled_dates:
        return in_stock, out_stock, total_sum, latest_date

    latest_date = filled_dates[-1]

    # 2. คำนวณยอดปัจจุบันของแต่ละรายการ (ดึงยอดย้อนหลังถ้าช่องล่าสุดว่าง)
    for index, row in df.iterrows():
        item_name = str(row[item_col])
        current_val = 0
        
        for col in date_columns:
            val = parse_value(row[col])
            if val is not None:
                current_val = val
            if col == latest_date:
                break
        
        total_sum += current_val
        
        # ย่อชื่อเวชภัณฑ์ก่อนจัดกลุ่ม
        short_name = shorten_item_name(item_name)
        
        # จัดกลุ่มว่ามีของ หรือของขาด
        if current_val > 0:
            in_stock.append(short_name)
        else:
            out_stock.append(short_name)

    return in_stock, out_stock, total_sum, latest_date

def render_summary():
    # 1. ดึงข้อมูลจาก Google Sheets (ใช้ฟังก์ชันและแคชเดิมจาก inventory_tab เพื่อความรวดเร็ว)
    med_supplies_sheet = "
