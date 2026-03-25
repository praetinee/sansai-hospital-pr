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
    med_supplies_sheet = "https://docs.google.com/spreadsheets/d/1-WhGMaME7Gbe7o6V4_rtbrqxCZSX4Bfnsz-siOV9T4Q/edit?gid=38922931#gid=38922931"
    medicines_sheet = "https://docs.google.com/spreadsheets/d/1-WhGMaME7Gbe7o6V4_rtbrqxCZSX4Bfnsz-siOV9T4Q/edit?gid=50246944#gid=50246944"

    df_sup, cols_sup = load_and_process_inventory(med_supplies_sheet, "รายการพัสดุการแพทย์")
    df_med, cols_med = load_and_process_inventory(medicines_sheet, "รายการยา")

    # 2. คำนวณภาพรวม (Smart Summary) โดยใช้โลจิกที่ถูกต้อง
    sup_in, sup_out, sup_sum, sup_date = get_current_inventory_status(df_sup, "รายการพัสดุการแพทย์", cols_sup)
    med_in, med_out, med_sum, med_date = get_current_inventory_status(df_med, "รายการยา", cols_med)

    # 3. สร้าง Badges สำหรับแสดงผลรายชื่อแบบคลุมโทน
    def get_badges(items, is_success=True):
        if not items:
            return '<span class="text-[10px] text-slate-400 font-medium">- ไม่มี -</span>'
        
        if is_success:
            # ใช้สีเทาอ่อนสำหรับของที่มี เพื่อความคลีน (สะอาดตา)
            classes = "bg-slate-50 text-slate-600 border-slate-200"
            display_items = items[:10] # แสดงแค่ 10 อันแรกให้หน้าเว็บไม่ล้น
            remainder = len(items) - 10
        else:
            # ใช้สีแดงอ่อนสำหรับของขาดเพื่อเป็นการแจ้งเตือน (Alert)
            classes = "bg-red-50 text-red-600 border-red-200"
            display_items = items # ของขาดให้แสดงทั้งหมด
            remainder = 0
            
        badges = [f'<span class="inline-block px-1.5 py-0.5 text-[10px] font-bold rounded border {classes} mb-1 mr-1">{item}</span>' for item in display_items]
        
        if remainder > 0:
            badges.append(f'<span class="inline-block px-1.5 py-0.5 text-[10px] font-bold rounded border bg-slate-50 text-slate-500 border-slate-200 mb-1 mr-1">+{remainder} อื่นๆ</span>')
        
        return "".join(badges)

    sup_in_badges = get_badges(sup_in, True)
    sup_out_badges = get_badges(sup_out, False)
    med_in_badges = get_badges(med_in, True)
    med_out_badges = get_badges(med_out, False)
    
    # กำหนดสถานะภาพรวมแบบแยกกันระหว่างพัสดุและยา (คลุมโทนฟ้า/แดง)
    sup_status_html = '<span class="bg-red-50 text-red-600 px-2 py-0.5 rounded text-[10px] font-bold border border-red-200">สถานะ: มีรายการขาด</span>' if len(sup_out) > 0 else '<span class="bg-blue-50 text-blue-600 px-2 py-0.5 rounded text-[10px] font-bold border border-blue-200">สถานะ: เพียงพอ</span>'
    med_status_html = '<span class="bg-red-50 text-red-600 px-2 py-0.5 rounded text-[10px] font-bold border border-red-200">สถานะ: มีรายการขาด</span>' if len(med_out) > 0 else '<span class="bg-blue-50 text-blue-600 px-2 py-0.5 rounded text-[10px] font-bold border border-blue-200">สถานะ: เพียงพอ</span>'

    # URL ของรูปภาพคลินิกมลพิษ
    CLINIC_IMAGE_URL = "https://i.postimg.cc/R0DP1WxQ/หมอพร_อม.png"

    # 4. โค้ด HTML สำหรับแสดงผล
    html_code = f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        
        <script>
            tailwind.config = {{
                theme: {{
                    extend: {{
                        fontFamily: {{ sans: ['Sarabun', 'sans-serif'], }},
                        colors: {{
                            theme: {{
                                bg: '#F8FAFC', card: '#FFFFFF', border: '#E2E8F0',
                                primary: '#1E40AF', secondary: '#1E3A8A', accent: '#3B82F6', text: '#334155',
                            }}
                        }},
                        boxShadow: {{ 'paper': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)', }}
                    }}
                }}
            }}
        </script>
        <style>
            body {{ font-family: 'Sarabun', sans-serif; background-color: transparent; margin: 0; padding: 0.5rem; }}
            .section-title {{ position: relative; padding-left: 1rem; margin-bottom: 0.75rem; color: #1E3A8A; font-weight: 800; font-size: 1.15rem; }}
            .section-title::before {{ content: ''; position: absolute; left: 0; top: 0.25rem; bottom: 0.25rem; width: 4px; background-color: #3B82F6; border-radius: 2px; }}
            .info-box {{ background-color: white; border: 1px solid #E2E8F0; border-radius: 0.75rem; padding: 1.25rem; height: 100%; display: flex; flex-direction: column; transition: all 0.3s; }}
            .info-box:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-color: #BFDBFE; }}
            .bullet-list li {{ position: relative; padding-left: 1.25rem; margin-bottom: 0.35rem; line-height: 1.5; color: #475569; }}
            .bullet-list li::before {{ content: '•'; color: #3B82F6; font-weight: bold; position: absolute; left: 0; }}
            
            /* Responsive fixes for text */
            @media (min-width: 1024px) {{ .section-title {{ font-size: 1.25rem; }} }}
            
            /* Hide scrollbar when modal is open */
            body.modal-open {{ overflow: hidden; }}
        </style>
    </head>
    <body class="text-slate-700">

        <div class="w-full max-w-[1200px] mx-auto bg-white shadow-xl rounded-3xl overflow-hidden border border-slate-200 relative">
            <!-- Background Pattern -->
            <div class="absolute top-0 right-0 w-32 h-32 md:w-64 md:h-64 bg-slate-50 rounded-bl-full z-0 opacity-50"></div>

            <!-- Header -->
            <header class="bg-gradient-to-r from-theme-primary to-theme-secondary text-white p-6 md:p-8 relative z-10">
                <div class="flex flex-col md:flex-row items-center md:items-start gap-4 md:gap-6 text-center md:text-left">
                    <div class="bg-white/10 p-3 md:p-4 rounded-2xl backdrop-blur-sm border border-white/20 shrink-0 mt-2">
                        <span class="text-4xl md:text-5xl lg:text-6xl">🏥</span>
                    </div>
                    <div>
                        <h2 class="text-lg md:text-xl text-blue-200 font-medium mb-1">สรุปผลการดำเนินงาน ปี 2569</h2>
                        <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold leading-tight">การบริหารจัดการปัญหาฝุ่นละอองขนาดเล็ก (PM2.5)</h1>
                        <p class="text-blue-100 mt-2 text-base md:text-lg opacity-90">โรงพยาบาลสันทรายและเครือข่ายสุขภาพ อำเภอสันทราย</p>
                        
                        <!-- PHEOC Information (ปรับรูปแบบใหม่ ไร้กรอบ) -->
                        <div class="mt-3 text-left">
                            <div class="flex items-center justify-center md:justify-start gap-1.5 mb-1 text-white">
                                <span class="text-red-400 animate-pulse text-sm">🚨</span> 
                                <strong class="text-sm font-semibold tracking-wide">การเปิดศูนย์ปฏิบัติการฉุกเฉิน (PHEOC)</strong>
                            </div>
                            <div class="flex flex-col sm:flex-row justify-center md:justify-start sm:gap-6 gap-1 text-[13px] text-blue-100 md:pl-6 opacity-90">
                                <div class="flex items-center justify-center md:justify-start gap-1.5">
                                    <span class="w-1.5 h-1.5 bg-blue-300 rounded-full"></span> 
                                    <strong>จังหวัดเชียงใหม่:</strong> 12 มกราคม 2569
                                </div>
                                <div class="flex items-center justify-center md:justify-start gap-1.5">
                                    <span class="w-1.5 h-1.5 bg-blue-300 rounded-full"></span> 
                                    <strong>เขตสุขภาพที่ 1:</strong> 4 มีนาคม 2569
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <!-- Content Body (4 Columns Grid) -->
            <div class="p-4 md:p-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 relative z-10 bg-slate-50/50 items-stretch">

                <!-- 1. Surveillance -->
                <div class="info-box shadow-paper">
                    <h3 class="section-title">1. ระบบเฝ้าระวังอัจฉริยะ<br><span class="text-sm font-normal text-slate-400">(Smart Surveillance System)</span></h3>
                    <div class="flex items-center gap-3 mb-4 bg-blue-50 p-3 rounded-lg border border-blue-100 mt-2">
                        <span class="text-2xl md:text-3xl">📊</span>
                        <div class="text-[13px] font-semibold text-theme-primary">Real-time Monitoring Dashboard</div>
                    </div>
                    <ul class="bullet-list text-[13px]">
                        <li><a href="https://sshos-pm25-surveillance-gkw9z3865puvrk29g3qep2.streamlit.app/" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline transition-colors"><strong>สำหรับผู้บริหาร:</strong></a> ติดตามสถานการณ์ฝุ่นเทียบกับจำนวนผู้ป่วยโรคที่เกี่ยวข้อง</li>
                        <li><a href="https://pm25-sansai-dashboard-tuc6yczy4hhl8vbmxdyxcp.streamlit.app/" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline transition-colors"><strong>สำหรับประชาชน:</strong></a> ติดตามสถานการณ์ฝุ่นละอองในพื้นที่</li>
                        <li><strong>แหล่งข้อมูลแม่นยำ:</strong> เชื่อมโยงข้อมูลจากเครื่อง DustBoy และ Smog-epinorth</li>
                    </ul>
                </div>

                <!-- 2. Risk Comm -->
                <div class="info-box shadow-paper">
                    <h3 class="section-title">2. การสื่อสารความเสี่ยง<br><span class="text-sm font-normal text-slate-400">(Risk Communication)</span></h3>
                    <div class="space-y-3 mt-2 flex-grow">
                        <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <strong class="text-theme-primary block text-sm mb-1">เชิงรุกถึงหน้าบ้าน (Offline)</strong>
                            <p class="text-[12px] text-slate-600">อสม. เคาะประตูบ้าน ให้ความรู้กลุ่มเปราะบางรายครัวเรือน</p>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <strong class="text-theme-primary block text-sm mb-1">ช่องทางดิจิทัล (Online)</strong>
                            <p class="text-[12px] text-slate-600">แจ้งรายงานค่าฝุ่นและแนวทางปฏิบัติผ่าน LINE OA และ Webpage สาธารณะ</p>
                        </div>
                    </div>
                </div>

                <!-- 3. Environment -->
                <div class="info-box shadow-paper">
                    <h3 class="section-title">3. การจัดการสิ่งแวดล้อม<br><span class="text-sm font-normal text-slate-400">(Environmental Health)</span></h3>
                    <ul class="bullet-list text-[13px] mt-2">
                        <li><strong>ในหน่วยงาน (รพ.สันทราย):</strong> ตรวจวัดระดับ PM2.5 อย่างต่อเนื่อง</li>
                        <li><strong>ภาคประชาชน:</strong> ดำเนินการคัดกรองสุขภาพ พร้อมสนับสนุน <strong>"มุ้งสู้ฝุ่น"</strong> และหน้ากากอนามัยสำหรับกลุ่มเสี่ยง</li>
                    </ul>
                </div>

                <!-- 4. Facility Management -->
                <div class="info-box shadow-paper">
                    <h3 class="section-title">4. พื้นที่ปลอดภัย<br><span class="text-sm font-normal text-slate-400">(Clean Room & Safety Zone)</span></h3>
                    
                    <!-- Stats -->
                    <div class="mb-3 mt-2">
                        <div class="bg-blue-50 p-2.5 rounded-lg text-center border border-blue-100">
                            <div class="text-2xl font-bold text-theme-primary leading-none mb-1">30</div>
                            <div class="text-[11px] text-blue-800 font-bold">ห้องปลอดฝุ่น (มาตรฐานกรมอนามัย)</div>
                        </div>
                    </div>

                    <!-- Detailed Coverage (3 Zones) -->
                    <div class="space-y-2 flex-grow">
                        <!-- Zone 1: OPD & Public -->
                        <div class="bg-slate-50 rounded-lg p-2 border border-slate-100">
                            <h4 class="text-[11px] font-bold text-slate-700 mb-1 flex items-center gap-1">
                                <span class="text-blue-500">🏥</span> พื้นที่บริการและส่วนกลาง
                            </h4>
                            <ul class="grid grid-cols-2 gap-x-1 gap-y-1 text-[10px] text-slate-600">
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>OPD (ทั้ง 3 ชั้น)</li>
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>ห้องฟัน (6 ห้อง)</li>
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>ห้องฝากครรภ์</li>
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>คลินิกมลพิษ</li>
                                <li class="flex items-start gap-1 col-span-2"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>ห้องประชุม</li>
                            </ul>
                        </div>

                        <!-- Zone 2: IPD -->
                        <div class="bg-slate-50 rounded-lg p-2 border border-slate-100">
                            <h4 class="text-[11px] font-bold text-slate-700 mb-1 flex items-center gap-1">
                                <span class="text-blue-500">🛌</span> หอผู้ป่วยใน (IPD)
                            </h4>
                            <ul class="grid grid-cols-1 gap-x-1 gap-y-1 text-[10px] text-slate-600">
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>กุมารเวชกรรม (4 ห้อง)</li>
                            </ul>
                        </div>

                        <!-- Zone 3: Critical & Specialized -->
                        <div class="bg-slate-50 rounded-lg p-2 border border-slate-100">
                            <h4 class="text-[11px] font-bold text-slate-700 mb-1 flex items-center gap-1">
                                <span class="text-blue-500">🚨</span> เฉพาะทางและวิกฤต
                            </h4>
                            <ul class="grid grid-cols-2 gap-x-1 gap-y-1 text-[10px] text-slate-600">
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>ห้องฉุกเฉิน (ER)</li>
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>ห้อง ICU</li>
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>NICU (3 ห้อง)</li>
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>ห้องคลอด</li>
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>ห้องฟอกไต</li>
                                <li class="flex items-start gap-1"><span class="w-1 h-1 rounded-full bg-slate-400 mt-1.5 shrink-0"></span>ห้องส่องกล้อง</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- 5. Medical Service -->
                <div class="info-box shadow-paper">
                    <h3 class="section-title">5. การบริการทางการแพทย์<br><span class="text-sm font-normal text-slate-400">(Pollution Clinic)</span></h3>
                    <div class="flex items-start gap-3 mb-3 mt-2">
                        <div class="bg-blue-50 text-theme-primary p-2.5 rounded-lg text-xl border border-blue-100">🏥</div>
                        <div>
                            <h4 class="font-bold text-[13px] text-theme-primary">คลินิกมลพิษ</h4>
                            <p class="text-[11px] text-slate-500">เปิดทุกวันในเวลาราชการ</p>
                        </div>
                    </div>
                    
                    <!-- Thumbnail Image -->
                    <div class="mb-3 rounded-lg overflow-hidden border border-slate-200 cursor-pointer group relative bg-slate-50 flex justify-center p-1" onclick="openModal('clinicModal')">
                        <img src="{CLINIC_IMAGE_URL}" alt="คลินิกมลพิษ" class="h-20 w-auto max-w-full object-contain group-hover:scale-105 transition-transform duration-300">
                        <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <span class="text-white text-xs font-bold flex items-center gap-1">🔍 คลิกขยายรูปภาพ</span>
                        </div>
                    </div>
                    
                    <ul class="bullet-list text-[12px] mb-4 text-slate-600 space-y-2">
                        <li class="flex justify-between items-start pr-1">
                            <div class="flex flex-col">
                                <span>นัดหมายผ่าน <strong>"หมอพร้อม"</strong></span>
                                <span class="text-[10px] text-blue-600 font-medium mt-0.5">จันทร์-ศุกร์ 8.00-14.00 น.</span>
                            </div>
                            <span class="text-[10px] font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded border border-slate-200 mt-0.5 shrink-0">0 ราย</span>
                        </li>
                        <li class="flex justify-between items-center pr-1 mt-2">
                            <span>ผู้ป่วย <strong>Walk-in</strong></span>
                            <span class="text-[10px] font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded border border-slate-200 shrink-0">0 ราย</span>
                        </li>
                    </ul>
                    
                    <hr class="border-dashed border-slate-200 my-3">
                    
                    <!-- Hero Care Update -->
                    <h3 class="section-title !text-[13px] !mb-2">การตรวจสุขภาพอาสาดับไฟป่า <br><span class="font-normal text-slate-500 text-[11px]">(ก่อนเริ่มภารกิจ)</span></h3>
                    
                    <div class="space-y-2 flex-grow">
                        <!-- Location 1 -->
                        <div class="bg-slate-50 border border-slate-100 p-2 rounded-lg">
                            <div class="text-[10px] text-slate-700 font-bold mb-1.5 border-b border-slate-200 pb-1 leading-snug">📍 ที่ว่าการอำเภอสันทราย</div>
                            <div class="flex justify-between items-center px-1">
                                <div class="text-center">
                                    <div class="text-[9px] text-slate-400 mb-0.5">ตรวจทั้งหมด</div>
                                    <div class="text-base font-extrabold text-slate-700 leading-none">128 <span class="font-medium text-[9px] text-slate-400">คน</span></div>
                                </div>
                                <div class="h-6 w-px bg-slate-200"></div>
                                <div class="text-center">
                                    <div class="text-[9px] text-slate-400 mb-0.5">ด่านหน้า</div>
                                    <div class="text-base font-extrabold text-blue-600 leading-none">68 <span class="font-medium text-[9px] text-blue-500">คน</span></div>
                                </div>
                            </div>
                        </div>

                        <!-- Location 2 -->
                        <div class="bg-slate-50 border border-slate-100 p-2 rounded-lg">
                            <div class="text-[10px] text-slate-700 font-bold mb-1.5 border-b border-slate-200 pb-1 leading-snug">📍 รพ.สต. ในเขตอำเภอ</div>
                            <div class="flex justify-between items-center px-1">
                                <div class="text-center">
                                    <div class="text-[9px] text-slate-400 mb-0.5">ตรวจทั้งหมด</div>
                                    <div class="text-base font-extrabold text-slate-700 leading-none">25 <span class="font-medium text-[9px] text-slate-400">คน</span></div>
                                </div>
                                <div class="h-6 w-px bg-slate-200"></div>
                                <div class="text-center">
                                    <div class="text-[9px] text-slate-400 mb-0.5">ด่านหน้า</div>
                                    <div class="text-base font-extrabold text-blue-600 leading-none">16 <span class="font-medium text-[9px] text-blue-500">คน</span></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 6. Epi Investigation -->
                <div class="info-box shadow-paper">
                    <h3 class="section-title">6. เฝ้าระวังทางระบาดวิทยา<br><span class="text-sm font-normal text-slate-400">(Epidemiological Surveillance)</span></h3>
                    
                    <div class="mb-4 mt-2">
                        <p class="text-[12px] text-slate-600 mb-2 leading-relaxed"><strong>มาตรการ:</strong> ประสาน 
                            <a href="https://docs.google.com/spreadsheets/d/1Ba-5IzHXOzEQziXY7vfdvDXzK0dOZv0VmoINAd-sNxU/edit?usp=drivesdk" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline font-semibold transition-colors">ER</a>, 
                            <a href="https://docs.google.com/spreadsheets/d/1j5xpdB-LNhucSVNhQuqShKUDv-xyWCGB5xhC295J3M4/edit?usp=sharing" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline font-semibold transition-colors">OPD</a> และ 
                            <a href="https://docs.google.com/spreadsheets/d/1fq34BEtpt6nWbxSupNacky3ZzlV7HymWNW2xv6LyIcA/edit?usp=sharing" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline font-semibold transition-colors">PCU หนองหาร</a> 
                            เพื่อเฝ้าระวัง สอบสวนโรค
                        </p>
                        <div class="flex flex-wrap gap-1.5">
                            <span class="px-2 py-0.5 bg-slate-100 text-slate-600 text-[10px] rounded font-bold border border-slate-200">COPD</span>
                            <span class="px-2 py-0.5 bg-slate-100 text-slate-600 text-[10px] rounded font-bold border border-slate-200">Asthma</span>
                            <span class="px-2 py-0.5 bg-slate-100 text-slate-600 text-[10px] rounded font-bold border border-slate-200">Z58.1</span>
                        </div>
                    </div>

                    <div class="relative py-2 flex-grow">
                        <div class="absolute left-4 top-2 bottom-2 w-0.5 bg-slate-200"></div>
                        
                        <!-- Stat 1 -->
                        <div class="relative pl-10 mb-4">
                            <div class="absolute left-2 top-1.5 w-4 h-4 bg-slate-400 rounded-full border-4 border-white shadow-sm"></div>
                            <div class="text-[12px] text-slate-500 font-medium">ผู้ป่วยเฝ้าระวังสะสม</div>
                            <div class="text-2xl font-extrabold text-slate-400 mt-0.5">- <span class="text-xs font-normal text-slate-400">ราย</span></div>
                        </div>

                        <!-- Stat 2 -->
                        <div class="relative pl-10 mb-4">
                            <div class="absolute left-2 top-1.5 w-4 h-4 bg-orange-400 rounded-full border-4 border-white shadow-sm"></div>
                            <div class="text-[12px] text-slate-500 font-medium">ผลการวินิจฉัยเบื้องต้น</div>
                            <div class="bg-slate-50 p-2 rounded shadow-sm border border-slate-100 text-[11px] text-slate-600 mt-1 leading-snug">
                                ไม่พบความสัมพันธ์ที่มีนัยสำคัญ
                            </div>
                        </div>

                        <!-- Stat 3 -->
                        <div class="relative pl-10">
                            <div class="absolute left-2 top-1.5 w-4 h-4 bg-theme-primary rounded-full border-4 border-white shadow-sm"></div>
                            <div class="text-[12px] text-slate-500 font-medium">ยืนยันผลกระทบจากฝุ่น</div>
                            <div class="text-2xl font-extrabold text-theme-primary">0 <span class="text-xs font-normal text-slate-400">ราย</span></div>
                        </div>
                    </div>
                </div>

                <!-- 7. Medical Supplies -->
                <div class="info-box shadow-paper">
                    <h3 class="section-title">7. คลังพัสดุการแพทย์<br><span class="text-sm font-normal text-slate-400">(Medical Supplies)</span></h3>
                    
                    <div class="flex flex-col mt-2 flex-grow justify-start">
                        <div class="flex items-center gap-3 mb-3 bg-blue-50 p-3 rounded-lg border border-blue-100">
                            <span class="text-2xl md:text-3xl">📦</span>
                            <div>
                                <div class="text-[13px] font-semibold text-theme-primary">พัสดุการแพทย์</div>
                                <a href="#" onclick="window.parent.document.querySelectorAll('[data-baseweb=\\'tab\\']')[4].click(); return false;" class="text-[11px] font-bold text-blue-600 hover:text-blue-800 underline transition-colors">
                                    คลิกดูจำนวนคงเหลือ ➔
                                </a>
                            </div>
                        </div>
                        
                        <div class="flex-grow">
                            <div class="mb-2">
                                <span class="text-[10px] font-bold text-slate-600 flex items-center gap-1 mb-1.5">🚨 รายการที่ขาดแคลน/หมด:</span>
                                <div class="pl-1">{sup_out_badges}</div>
                            </div>
                            <div>
                                <span class="text-[10px] font-bold text-slate-600 flex items-center gap-1 mb-1.5">✅ รายการที่มีพร้อมใช้:</span>
                                <div class="pl-1">{sup_in_badges}</div>
                            </div>
                        </div>
                        
                        <div class="mt-3 pt-2 border-t border-slate-100 flex flex-wrap justify-between items-center text-[10px] font-medium text-slate-500 gap-1.5">
                            <span class="flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full bg-slate-400"></span> 
                                อัปเดต: {sup_date}
                            </span>
                            {sup_status_html}
                        </div>
                    </div>
                </div>

                <!-- 8. Medicines -->
                <div class="info-box shadow-paper">
                    <h3 class="section-title">8. คลังเวชภัณฑ์ยา<br><span class="text-sm font-normal text-slate-400">(Medicines)</span></h3>
                    
                    <div class="flex flex-col mt-2 flex-grow justify-start">
                        <div class="flex items-center gap-3 mb-3 bg-blue-50 p-3 rounded-lg border border-blue-100">
                            <span class="text-2xl md:text-3xl">💊</span>
                            <div>
                                <div class="text-[13px] font-semibold text-theme-primary">เวชภัณฑ์ยา</div>
                                <a href="#" onclick="window.parent.document.querySelectorAll('[data-baseweb=\\'tab\\']')[4].click(); return false;" class="text-[11px] font-bold text-blue-600 hover:text-blue-800 underline transition-colors">
                                    คลิกดูจำนวนคงเหลือ ➔
                                </a>
                            </div>
                        </div>
                        
                        <div class="flex-grow">
                            <div class="mb-2">
                                <span class="text-[10px] font-bold text-slate-600 flex items-center gap-1 mb-1.5">🚨 รายการที่ขาดแคลน/หมด:</span>
                                <div class="pl-1">{med_out_badges}</div>
                            </div>
                            <div>
                                <span class="text-[10px] font-bold text-slate-600 flex items-center gap-1 mb-1.5">✅ รายการที่มีพร้อมใช้:</span>
                                <div class="pl-1">{med_in_badges}</div>
                            </div>
                        </div>
                        
                        <div class="mt-3 pt-2 border-t border-slate-100 flex flex-wrap justify-between items-center text-[10px] font-medium text-slate-500 gap-1.5">
                            <span class="flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full bg-slate-400"></span> 
                                อัปเดต: {med_date}
                            </span>
                            {med_status_html}
                        </div>
                    </div>
                </div>

            </div>

            <!-- Footer -->
            <footer class="bg-theme-primary text-white/80 p-4 text-center text-sm md:text-base">
                <p>กลุ่มงานอาชีวเวชกรรม โรงพยาบาลสันทราย</p>
            </footer>
            
            <!-- Lightbox Modal สำหรับแสดงรูปใหญ่ -->
            <div id="clinicModal" class="fixed inset-0 z-50 hidden flex items-center justify-center bg-black/80 backdrop-blur-sm transition-opacity" onclick="closeModal('clinicModal')">
                <div class="relative w-full max-w-3xl max-h-[90vh] p-4 flex justify-center items-center flex-col">
                    <button class="absolute top-2 right-6 text-white hover:text-red-400 text-5xl font-bold cursor-pointer drop-shadow-md z-50" onclick="closeModal('clinicModal')">&times;</button>
                    <img src="{CLINIC_IMAGE_URL}" class="max-w-full max-h-[85vh] object-contain rounded-xl shadow-2xl border-2 border-white/20" onclick="event.stopPropagation()">
                    <p class="text-white mt-3 text-sm">คลิกพื้นที่สีดำ หรือปุ่ม X เพื่อปิด</p>
                </div>
            </div>
            
            <script>
                function openModal(id) {{
                    document.getElementById(id).classList.remove('hidden');
                    document.body.classList.add('modal-open');
                }}
                function closeModal(id) {{
                    document.getElementById(id).classList.add('hidden');
                    document.body.classList.remove('modal-open');
                }}
            </script>
        </div>
    </body>
    </html>
    """
    
    # ขยายความสูงให้เหมาะสมกับหน้าจอแบบ 4 คอลัมน์และรองรับองค์ประกอบที่เพิ่มขึ้น
    components.html(html_code, height=1550, scrolling=True)
