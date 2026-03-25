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

    # 3. สร้าง Badges สำหรับแสดงผลรายชื่อ
    def get_badges(items, is_success=True, is_med=False):
        if not items:
            return '<span class="text-[10px] text-gray-400 font-medium">- ไม่มี -</span>'
        
        if is_success:
            # ใช้สีน้ำเงินสำหรับพัสดุ, สีเขียวสำหรับยา
            if not is_med:
                classes = "bg-blue-50 text-blue-700 border-blue-200"
            else:
                classes = "bg-emerald-50 text-emerald-700 border-emerald-200"
                
            display_items = items[:10] # แสดงแค่ 10 อันแรกให้หน้าเว็บไม่ล้น
            remainder = len(items) - 10
        else:
            classes = "bg-red-50 text-red-600 border-red-200"
            display_items = items # ของขาดให้แสดงทั้งหมด
            remainder = 0
            
        badges = [f'<span class="inline-block px-1.5 py-0.5 text-[10px] font-bold rounded border {classes} mb-1 mr-1">{item}</span>' for item in display_items]
        
        if remainder > 0:
            badges.append(f'<span class="inline-block px-1.5 py-0.5 text-[10px] font-bold rounded border bg-gray-50 text-gray-500 border-gray-200 mb-1 mr-1">+{remainder} อื่นๆ</span>')
        
        return "".join(badges)

    sup_in_badges = get_badges(sup_in, True, False)
    sup_out_badges = get_badges(sup_out, False, False)
    med_in_badges = get_badges(med_in, True, True)
    med_out_badges = get_badges(med_out, False, True)
    
    # กำหนดสถานะภาพรวมแบบแยกกันระหว่างพัสดุและยา
    sup_status_html = '<span class="bg-orange-100 text-orange-700 px-2 py-0.5 rounded font-bold border border-orange-200">สถานะ: มีรายการขาด</span>' if len(sup_out) > 0 else '<span class="bg-green-100 text-green-700 px-2 py-0.5 rounded font-bold border border-green-200">สถานะ: เพียงพอ</span>'
    med_status_html = '<span class="bg-orange-100 text-orange-700 px-2 py-0.5 rounded font-bold border border-orange-200">สถานะ: มีรายการขาด</span>' if len(med_out) > 0 else '<span class="bg-green-100 text-green-700 px-2 py-0.5 rounded font-bold border border-green-200">สถานะ: เพียงพอ</span>'

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
                                bg: '#F0F7FF', card: '#FFFFFF', border: '#BFDBFE',
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
            .info-box {{ background-color: white; border: 1px solid #DBEAFE; border-radius: 0.75rem; padding: 1.25rem; height: 100%; display: flex; flex-direction: column; transition: all 0.3s; }}
            .info-box:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }}
            .bullet-list li {{ position: relative; padding-left: 1.25rem; margin-bottom: 0.35rem; line-height: 1.5; }}
            .bullet-list li::before {{ content: '•'; color: #3B82F6; font-weight: bold; position: absolute; left: 0; }}
            
            /* Responsive fixes for text */
            @media (min-width: 1024px) {{ .section-title {{ font-size: 1.25rem; }} }}
        </style>
    </head>
    <body class="text-slate-700">

        <div class="w-full max-w-[1200px] mx-auto bg-white shadow-xl rounded-3xl overflow-hidden border border-blue-100 relative">
            <!-- Background Pattern -->
            <div class="absolute top-0 right-0 w-32 h-32 md:w-64 md:h-64 bg-blue-50 rounded-bl-full z-0 opacity-50"></div>

            <!-- Header -->
            <header class="bg-gradient-to-r from-theme-primary to-theme-secondary text-white p-6 md:p-8 relative z-10">
                <div class="flex flex-col md:flex-row items-center md:items-start gap-4 md:gap-6 text-center md:text-left">
                    <div class="bg-white/10 p-3 md:p-4 rounded-2xl backdrop-blur-sm border border-white/20 shrink-0">
                        <span class="text-4xl md:text-5xl lg:text-6xl">🏥</span>
                    </div>
                    <div>
                        <h2 class="text-lg md:text-xl text-blue-200 font-medium mb-1">สรุปผลการดำเนินงาน ปี 2569</h2>
                        <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold leading-tight">การบริหารจัดการปัญหาฝุ่นละอองขนาดเล็ก (PM2.5)</h1>
                        <p class="text-blue-100 mt-2 text-base md:text-lg opacity-90">โรงพยาบาลสันทรายและเครือข่ายสุขภาพ อำเภอสันทราย</p>
                    </div>
                </div>
            </header>

            <!-- Content Body -->
            <div class="p-4 md:p-8 grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10 bg-slate-50/50">

                <!-- Col 1: Surveillance & Communication -->
                <div class="col-span-1 flex flex-col gap-6">
                    <!-- 1. Surveillance -->
                    <div class="info-box shadow-paper">
                        <h3 class="section-title">1. ระบบเฝ้าระวังอัจฉริยะ<br><span class="text-sm font-normal text-gray-500">(Smart Surveillance System)</span></h3>
                        <div class="flex items-center gap-3 mb-4 bg-blue-50 p-3 rounded-lg border border-blue-100">
                            <span class="text-2xl md:text-3xl">📊</span>
                            <div class="text-sm font-semibold text-theme-primary">Real-time Monitoring Dashboard</div>
                        </div>
                        <ul class="bullet-list text-sm">
                            <li><a href="https://sshos-pm25-surveillance-gkw9z3865puvrk29g3qep2.streamlit.app/" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline transition-colors"><strong>สำหรับผู้บริหาร:</strong></a> ติดตามสถานการณ์ฝุ่นเทียบกับจำนวนผู้ป่วยโรคที่เกี่ยวข้องกับการสัมผัสฝุ่น PM2.5</li>
                            <li><strong>แหล่งข้อมูลแม่นยำ:</strong> เชื่อมโยงข้อมูลจากเครื่อง <strong>DustBoy</strong> และ Smog-epinorth (Backup)</li>
                        </ul>
                    </div>

                    <!-- 2. Risk Comm -->
                    <div class="info-box shadow-paper">
                        <h3 class="section-title">2. การสื่อสารความเสี่ยง<br><span class="text-sm font-normal text-gray-500">(Risk Communication)</span></h3>
                        <div class="space-y-3">
                            <div class="bg-blue-50 p-3 rounded-lg border border-blue-100">
                                <strong class="text-theme-primary block text-sm mb-1">เชิงรุกถึงหน้าบ้าน (Offline)</strong>
                                <p class="text-sm text-gray-600">อสม. เคาะประตูบ้าน ให้ความรู้กลุ่มเปราะบางรายครัวเรือน</p>
                            </div>
                            <div class="bg-blue-50 p-3 rounded-lg border border-blue-100">
                                <strong class="text-theme-primary block text-sm mb-1">ช่องทางดิจิทัล (Online)</strong>
                                <p class="text-sm text-gray-600">แจ้งรายงานค่าฝุ่นและแนวทางปฏิบัติตัวผ่าน LINE Official และ Webpage สาธารณะ</p>
                            </div>
                        </div>
                    </div>

                    <!-- 3. Environment -->
                    <div class="info-box shadow-paper flex-grow">
                        <h3 class="section-title">3. การจัดการสิ่งแวดล้อม<br><span class="text-sm font-normal text-gray-500">(Environmental Health)</span></h3>
                        <ul class="bullet-list text-sm">
                            <li><strong>ในหน่วยงาน (รพ.สันทราย):</strong> ตรวจวัดระดับ PM2.5</li>
                            <li><strong>ภาคประชาชน:</strong> ดำเนินการคัดกรองสุขภาพ พร้อมสนับสนุน <strong>"มุ้งสู้ฝุ่น"</strong> และหน้ากากอนามัย</li>
                        </ul>
                    </div>
                </div>

                <!-- Col 2: Facilities & Service -->
                <div class="col-span-1 flex flex-col gap-6">
                    <!-- 4. Facility Management -->
                    <div class="info-box shadow-paper">
                        <h3 class="section-title">4. พื้นที่ปลอดภัย<br><span class="text-sm font-normal text-gray-500">(Clean Room & Safety Zone)</span></h3>
                        
                        <!-- Stats -->
                        <div class="mb-4">
                            <div class="bg-green-50 p-3 rounded-lg text-center border border-green-200">
                                <div class="text-3xl font-bold text-green-700">30</div>
                                <div class="text-sm text-green-800 font-bold mt-1">ห้องปลอดฝุ่น (มาตรฐานกรมอนามัย)</div>
                            </div>
                        </div>

                        <!-- Detailed Coverage (3 Zones) -->
                        <div class="space-y-2">
                            <!-- Zone 1: OPD & Public -->
                            <div class="bg-blue-50 rounded-lg p-2.5 border border-blue-100">
                                <h4 class="text-xs font-bold text-blue-800 mb-1.5 flex items-center gap-1">
                                    <span class="text-blue-600">🏥</span> พื้นที่บริการและส่วนกลาง
                                </h4>
                                <ul class="grid grid-cols-2 gap-x-1 gap-y-1 text-[11px] text-gray-700">
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-blue-400 mt-1 shrink-0"></span>OPD (ทั้ง 3 ชั้น)</li>
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-blue-400 mt-1 shrink-0"></span>ห้องฟัน (6 ห้อง)</li>
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-blue-400 mt-1 shrink-0"></span>ห้องฝากครรภ์</li>
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-blue-400 mt-1 shrink-0"></span>คลินิกมลพิษ</li>
                                    <li class="flex items-start gap-1 col-span-2"><span class="w-1.5 h-1.5 rounded-full bg-blue-400 mt-1 shrink-0"></span>ห้องประชุม (สุธรรมนุสิฐ, รวงผึ้ง, CR Room)</li>
                                </ul>
                            </div>

                            <!-- Zone 2: IPD -->
                            <div class="bg-green-50 rounded-lg p-2.5 border border-green-100">
                                <h4 class="text-xs font-bold text-green-800 mb-1.5 flex items-center gap-1">
                                    <span class="text-green-600">🛌</span> หอผู้ป่วยใน (IPD)
                                </h4>
                                <ul class="grid grid-cols-1 gap-x-1 gap-y-1 text-[11px] text-gray-700">
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-green-400 mt-1 shrink-0"></span>กุมารเวชกรรม (4 ห้อง)</li>
                                </ul>
                            </div>

                            <!-- Zone 3: Critical & Specialized -->
                            <div class="bg-red-50 rounded-lg p-2.5 border border-red-100">
                                <h4 class="text-xs font-bold text-red-800 mb-1.5 flex items-center gap-1">
                                    <span class="text-red-600">🚨</span> เฉพาะทางและวิกฤต (Critical)
                                </h4>
                                <ul class="grid grid-cols-2 gap-x-1 gap-y-1 text-[11px] text-gray-700">
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-red-400 mt-1 shrink-0"></span>ห้องฉุกเฉิน (ER)</li>
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-red-400 mt-1 shrink-0"></span>ห้อง ICU</li>
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-red-400 mt-1 shrink-0"></span>NICU (3 ห้อง)</li>
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-red-400 mt-1 shrink-0"></span>ห้องคลอด / รอคลอด</li>
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-red-400 mt-1 shrink-0"></span>ห้องฟอกไต (4 ห้อง)</li>
                                    <li class="flex items-start gap-1"><span class="w-1.5 h-1.5 rounded-full bg-red-400 mt-1 shrink-0"></span>ห้องส่องกล้อง</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- 5. Medical Service -->
                    <div class="info-box shadow-paper flex-grow">
                        <h3 class="section-title">5. การบริการทางการแพทย์<br><span class="text-sm font-normal text-gray-500">(Pollution Clinic)</span></h3>
                        <div class="flex items-start gap-3 mb-3">
                            <div class="bg-blue-100 text-blue-600 p-2 rounded-lg text-xl md:text-2xl">🏥</div>
                            <div>
                                <h4 class="font-bold text-theme-primary">คลินิกมลพิษ</h4>
                                <p class="text-sm text-gray-600">เปิดให้บริการทุกวันในเวลาราชการ</p>
                            </div>
                        </div>
                        <ul class="bullet-list text-sm mb-4">
                            <li>นัดหมายล่วงหน้าผ่าน <strong>"หมอพร้อม"</strong></li>
                            <li>รองรับผู้ป่วย <strong>Walk-in</strong></li>
                        </ul>
                        
                        <hr class="border-dashed border-gray-300 my-4">
                        
                        <!-- Hero Care Update -->
                        <h3 class="section-title !text-[14px] !mb-3">การตรวจสุขภาพอาสาดับไฟป่า ก่อนเริ่มภารกิจ</h3>
                        
                        <div class="space-y-3">
                            <!-- Location 1 -->
                            <div class="bg-orange-50 border border-orange-200 p-3 rounded-lg">
                                <div class="text-[11px] text-orange-800 font-bold mb-2 border-b border-orange-100 pb-1.5 leading-snug">📍 ที่ว่าการอำเภอสันทราย (โดย สสอ.สันทราย และ รพ.)</div>
                                <div class="flex justify-between items-center px-2">
                                    <div class="text-center">
                                        <div class="text-[10px] text-gray-500 mb-0.5">ตรวจทั้งหมด</div>
                                        <div class="text-lg font-extrabold text-orange-600 leading-none">128 <span class="font-medium text-[10px] text-orange-700">คน</span></div>
                                    </div>
                                    <div class="h-8 w-px bg-orange-200"></div>
                                    <div class="text-center">
                                        <div class="text-[10px] text-gray-500 mb-0.5">เหมาะเป็นด่านหน้า</div>
                                        <div class="text-lg font-extrabold text-green-600 leading-none">68 <span class="font-medium text-[10px] text-green-700">คน</span></div>
                                    </div>
                                </div>
                            </div>

                            <!-- Location 2 -->
                            <div class="bg-orange-50 border border-orange-200 p-3 rounded-lg">
                                <div class="text-[11px] text-orange-800 font-bold mb-2 border-b border-orange-100 pb-1.5 leading-snug">📍 รพ.สต. ในเขตอำเภอสันทราย</div>
                                <div class="flex justify-between items-center px-2">
                                    <div class="text-center">
                                        <div class="text-[10px] text-gray-500 mb-0.5">ตรวจทั้งหมด</div>
                                        <div class="text-lg font-extrabold text-orange-600 leading-none">25 <span class="font-medium text-[10px] text-orange-700">คน</span></div>
                                    </div>
                                    <div class="h-8 w-px bg-orange-200"></div>
                                    <div class="text-center">
                                        <div class="text-[10px] text-gray-500 mb-0.5">เหมาะเป็นด่านหน้า</div>
                                        <div class="text-lg font-extrabold text-green-600 leading-none">16 <span class="font-medium text-[10px] text-green-700">คน</span></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- Col 3: Epidemiology & Inventory -->
                <div class="col-span-1 flex flex-col gap-6">
                    
                    <!-- 6. Epi Investigation -->
                    <div class="info-box shadow-paper bg-gradient-to-b from-white to-blue-50 border-blue-200">
                        <h3 class="section-title">6. เฝ้าระวังทางระบาดวิทยา<br><span class="text-sm font-normal text-gray-500">(Epidemiological Surveillance)</span></h3>
                        
                        <div class="mb-4">
                            <p class="text-sm text-gray-700 mb-2 leading-relaxed"><strong>มาตรการ:</strong> ประสาน 
                                <a href="https://docs.google.com/spreadsheets/d/1Ba-5IzHXOzEQziXY7vfdvDXzK0dOZv0VmoINAd-sNxU/edit?usp=drivesdk" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline font-semibold transition-colors">ER</a>, 
                                <a href="https://docs.google.com/spreadsheets/d/1j5xpdB-LNhucSVNhQuqShKUDv-xyWCGB5xhC295J3M4/edit?usp=sharing" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline font-semibold transition-colors">OPD</a> และ 
                                <a href="https://docs.google.com/spreadsheets/d/1fq34BEtpt6nWbxSupNacky3ZzlV7HymWNW2xv6LyIcA/edit?usp=sharing" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline font-semibold transition-colors">PCU หนองหาร</a> 
                                เพื่อเฝ้าระวัง สอบสวนโรค และรายงาน สสจ.เชียงใหม่
                            </p>
                            <div class="flex flex-wrap gap-2">
                                <span class="px-2 py-1 bg-blue-100 text-blue-700 text-[11px] rounded font-bold">COPD</span>
                                <span class="px-2 py-1 bg-blue-100 text-blue-700 text-[11px] rounded font-bold">Asthma</span>
                                <span class="px-2 py-1 bg-blue-100 text-blue-700 text-[11px] rounded font-bold">Z58.1 (สัมผัสมลพิษ)</span>
                            </div>
                        </div>

                        <div class="relative py-2">
                            <div class="absolute left-4 top-2 bottom-2 w-0.5 bg-blue-200"></div>
                            
                            <!-- Stat 1 -->
                            <div class="relative pl-10 mb-4">
                                <div class="absolute left-2 top-1.5 w-4 h-4 bg-blue-500 rounded-full border-4 border-white shadow"></div>
                                <div class="text-sm text-gray-500 font-medium">ผู้ป่วยเฝ้าระวังสะสม</div>
                                <div class="text-3xl font-extrabold text-gray-400 mt-1">- <span class="text-sm font-normal text-gray-400">ราย</span></div>
                            </div>

                            <!-- Stat 2 -->
                            <div class="relative pl-10 mb-4">
                                <div class="absolute left-2 top-1.5 w-4 h-4 bg-orange-400 rounded-full border-4 border-white shadow"></div>
                                <div class="text-sm text-gray-500 font-medium">ผลการวินิจฉัยเบื้องต้น</div>
                                <div class="bg-white p-2 rounded shadow-sm border border-gray-100 text-xs text-gray-600 mt-1 leading-snug">
                                    ไม่พบความสัมพันธ์ที่มีนัยสำคัญทางคลินิกกับหมอกควันโดยตรง
                                </div>
                            </div>

                            <!-- Stat 3 -->
                            <div class="relative pl-10">
                                <div class="absolute left-2 top-1.5 w-4 h-4 bg-green-500 rounded-full border-4 border-white shadow"></div>
                                <div class="text-sm text-gray-500 font-medium">ยืนยันผลกระทบจากฝุ่น</div>
                                <div class="text-3xl font-extrabold text-green-600">0 <span class="text-sm font-normal text-gray-500">ราย</span></div>
                            </div>
                        </div>
                    </div>

                    <!-- 7. Medical Supplies -->
                    <div class="info-box shadow-paper bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200 flex-grow">
                        <h3 class="section-title !text-blue-800 before:bg-blue-500">7. คลังพัสดุการแพทย์<br><span class="text-sm font-normal text-blue-600">(Medical Supplies)</span></h3>
                        
                        <div class="flex flex-col mt-2 flex-grow justify-center">
                            <div class="bg-white p-3 rounded-xl shadow-sm border border-blue-100 relative overflow-hidden h-full flex flex-col">
                                <div class="absolute right-[-10px] top-[-5px] opacity-[0.03] text-5xl">📦</div>
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="bg-blue-100 p-2.5 rounded-full text-blue-600 text-lg shrink-0">📦</div>
                                    <div>
                                        <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wide">พัสดุการแพทย์</p>
                                        <a href="#" onclick="window.parent.document.querySelectorAll('[data-baseweb=\\'tab\\']')[4].click(); return false;" class="inline-flex items-center gap-1 mt-0.5 text-[12px] font-bold text-blue-600 hover:text-blue-800 underline transition-colors">
                                            คลิกดูรายละเอียดคงเหลือ ➔
                                        </a>
                                    </div>
                                </div>
                                <div class="mt-2 border-t border-gray-100 pt-2 flex-grow">
                                    <div class="mb-2">
                                        <span class="text-[10px] font-bold text-red-600 flex items-center gap-1 mb-1.5">🚨 รายการที่ขาดแคลน/หมด:</span>
                                        <div class="pl-1">{sup_out_badges}</div>
                                    </div>
                                    <div>
                                        <span class="text-[10px] font-bold text-blue-600 flex items-center gap-1 mb-1.5">✅ รายการที่มีพร้อมใช้:</span>
                                        <div class="pl-1">{sup_in_badges}</div>
                                    </div>
                                </div>
                                <div class="mt-3 pt-2 border-t border-gray-100 flex justify-between items-center text-[10px] sm:text-xs font-medium text-gray-600 gap-2">
                                    <span class="flex items-center gap-1.5">
                                        <span class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span> 
                                        อัปเดต: {sup_date}
                                    </span>
                                    {sup_status_html}
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 8. Medicines -->
                    <div class="info-box shadow-paper bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-200 flex-grow">
                        <h3 class="section-title !text-emerald-800 before:bg-emerald-500">8. คลังเวชภัณฑ์ยา<br><span class="text-sm font-normal text-emerald-600">(Medicines)</span></h3>
                        
                        <div class="flex flex-col mt-2 flex-grow justify-center">
                            <div class="bg-white p-3 rounded-xl shadow-sm border border-emerald-100 relative overflow-hidden h-full flex flex-col">
                                <div class="absolute right-[-10px] top-[-5px] opacity-[0.03] text-5xl">💊</div>
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="bg-emerald-100 p-2.5 rounded-full text-emerald-600 text-lg shrink-0">💊</div>
                                    <div>
                                        <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wide">เวชภัณฑ์ยา</p>
                                        <a href="#" onclick="window.parent.document.querySelectorAll('[data-baseweb=\\'tab\\']')[4].click(); return false;" class="inline-flex items-center gap-1 mt-0.5 text-[12px] font-bold text-emerald-600 hover:text-emerald-800 underline transition-colors">
                                            คลิกดูรายละเอียดคงเหลือ ➔
                                        </a>
                                    </div>
                                </div>
                                <div class="mt-2 border-t border-gray-100 pt-2 flex-grow">
                                    <div class="mb-2">
                                        <span class="text-[10px] font-bold text-red-600 flex items-center gap-1 mb-1.5">🚨 รายการที่ขาดแคลน/หมด:</span>
                                        <div class="pl-1">{med_out_badges}</div>
                                    </div>
                                    <div>
                                        <span class="text-[10px] font-bold text-emerald-600 flex items-center gap-1 mb-1.5">✅ รายการที่มีพร้อมใช้:</span>
                                        <div class="pl-1">{med_in_badges}</div>
                                    </div>
                                </div>
                                <div class="mt-3 pt-2 border-t border-gray-100 flex justify-between items-center text-[10px] sm:text-xs font-medium text-gray-600 gap-2">
                                    <span class="flex items-center gap-1.5">
                                        <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> 
                                        อัปเดต: {med_date}
                                    </span>
                                    {med_status_html}
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>

            <!-- Footer -->
            <footer class="bg-theme-primary text-white/80 p-4 text-center text-sm md:text-base">
                <p>กลุ่มงานอาชีวเวชกรรม โรงพยาบาลสันทราย</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    # ขยายความสูงให้รองรับ 3 กล่องข้อความในคอลัมน์สุดท้าย
    components.html(html_code, height=1850, scrolling=True)
