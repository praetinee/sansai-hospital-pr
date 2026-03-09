import streamlit.components.v1 as components

def render_pm25_flow():
    html_code = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style type="text/tailwindcss">
            /* =========================================
               THEME VARIABLES (FIXED PALETTE)
               ล็อคโทนสีตาม Mockup ให้เป็น "กล่องเข้มบนพื้นพาสเทล" 
               เพื่อการอ่านที่ชัดเจนและไม่หม่นหมองในทุกธีม
               ========================================= */
            :root {
                /* Dark Cards (ใช้กับกล่องหลักใน Col 1 & 2) */
                --card-bg: #1e293b; /* Slate 800 */
                --card-border: #334155; /* Slate 700 */
                --card-text: #f8fafc; /* Slate 50 */
                --card-muted: #cbd5e1; /* Slate 300 */

                /* Column 1 (Community - Pastel Yellow) */
                --c1-bg: #fef3c7; /* Amber 100 */
                --c1-border: #fcd34d; /* Amber 300 */
                --c1-text: #92400e; /* Amber 800 */
                --c1-icon: #d97706; /* Amber 600 */

                /* Column 2 (Clinic - Pastel Orange) */
                --c2-bg: #ffedd5; /* Orange 100 */
                --c2-border: #fdba74; /* Orange 300 */
                --c2-text: #9a3412; /* Orange 800 */

                /* Column 3 (Refer - Pastel Green) */
                --c3-bg: #d1fae5; /* Emerald 100 */
                --c3-border: #6ee7b7; /* Emerald 300 */
                --c3-text: #065f46; /* Emerald 800 */

                /* Col 3 Inner Boxes */
                --ref-bg: #fee2e2; --ref-border: #fca5a5; --ref-text: #991b1b;
                --dis-bg: #dcfce7; --dis-border: #86efac; --dis-text: #166534;

                /* Connecting Lines */
                --line-color: #475569; /* Slate 600 */
            }

            /* =========================================
               BASE STYLES & UTILITIES
               ========================================= */
            body { font-family: 'Sarabun', sans-serif; background-color: transparent; padding: 1rem; }
            
            .flow-col { border-width: 3px; border-radius: 2rem; padding: 1.25rem; display: flex; flex-direction: column; gap: 1.25rem; position: relative; height: 100%; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5); }
            
            .dark-card { background-color: var(--card-bg); border: 2px solid var(--card-border); color: var(--card-text); border-radius: 1rem; padding: 1rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); transition: transform 0.2s; }
            .dark-card:hover { transform: translateY(-2px); }
            
            .tag-code { position: absolute; top: 0.5rem; right: 0.5rem; background-color: #334155; color: #f8fafc; font-size: 0.65rem; padding: 0.2rem 0.6rem; border-radius: 9999px; font-weight: 700; z-index: 10; border: 1px solid #475569; letter-spacing: 0.025em; }
            
            /* Semantic Colors */
            .col-1 { background-color: var(--c1-bg); border-color: var(--c1-border); }
            .col-2 { background-color: var(--c2-bg); border-color: var(--c2-border); }
            .col-3 { background-color: var(--c3-bg); border-color: var(--c3-border); }
            
            .box-refer { background-color: var(--ref-bg); border-color: var(--ref-border); color: var(--ref-text); border-width: 3px; }
            .box-discharge { background-color: var(--dis-bg); border-color: var(--dis-border); color: var(--dis-text); border-width: 3px; }
        </style>
    </head>
    <body>
        <div id="main-container" class="max-w-[1280px] mx-auto relative pb-20 sm:pb-28 lg:pb-32">
            
            <!-- Alert Box -->
            <div class="flex justify-end mb-6 relative z-20">
                <div class="px-5 py-2.5 rounded-full font-bold shadow-md text-xs sm:text-sm flex items-center border border-slate-700 bg-slate-800 text-white">
                    <span class="text-yellow-400 mr-2">ย้ำ!</span> บันทึกรหัสโรค Z58.1 (Exposure to air pollution) ทุกจุดบริการเพื่อวิเคราะห์ข้อมูล
                </div>
            </div>

            <!-- SVG Overlay for Dynamic Line Drawing (Desktop Only) -->
            <!-- ใช้ overflow:visible เพื่อป้องกันหัวลูกศรโดนตัด -->
            <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden lg:block z-0" style="overflow: visible;">
                <defs>
                    <!-- Marker สำหรับเส้นประทั้งหมด -->
                    <marker id="arrow-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line-color)" />
                    </marker>
                </defs>
                
                <!-- Path Left -> Middle (เส้นประ) -->
                <path id="path-lm" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" marker-end="url(#arrow-head)" />
                <!-- Path Middle -> Right (เส้นประ) -->
                <path id="path-mr" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" marker-end="url(#arrow-head)" />
                <!-- Bottom Return Dashed Path (เส้นประ) -->
                <path id="path-return" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" stroke-linejoin="round" marker-end="url(#arrow-head)" />
            </svg>

            <!-- Return Label (Desktop Dynamic) -->
            <div id="return-label" class="absolute hidden lg:flex items-center justify-center bg-white px-8 py-2 rounded-full z-10 border-2" style="border-color: var(--line-color); color: var(--line-color);">
                <p class="font-bold text-base whitespace-nowrap">
                    การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                </p>
            </div>

            <!-- 3 Columns Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 relative z-10 items-stretch">

                <!-- ================= Column 1: Left (Community) ================= -->
                <div id="col-left" class="col-1 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm" style="background-color: var(--c1-border); color: var(--c1-text);">
                        ชุมชนและหน่วยบริการปฐมภูมิ (รุก)
                    </h2>
                    
                    <!-- Dark Card (กลไก 3 หมอ) -->
                    <div class="dark-card flex flex-col items-center text-center mt-2">
                        <div class="flex justify-center mb-2">
                            <i data-lucide="users" class="w-10 h-10 sm:w-12 sm:h-12 text-yellow-400"></i>
                        </div>
                        <h3 class="font-bold text-lg sm:text-xl text-white">กลไก 3 หมอ</h3>
                    </div>
                    
                    <!-- Text Items on Pastel Background -->
                    <div class="flex-grow space-y-5 sm:space-y-6 mt-4 px-2" style="color: var(--c1-text);">
                         <div class="flex items-start gap-3 sm:gap-4">
                            <i data-lucide="clipboard-list" class="w-6 h-6 sm:w-7 sm:h-7 shrink-0 mt-0.5" style="color: var(--c1-icon);"></i>
                            <div>
                                <p class="font-bold text-sm sm:text-base leading-tight">การลงพื้นที่เชิงรุก: อสม. และ รพ.สต.</p>
                                <p class="text-[13px] sm:text-sm leading-relaxed mt-1 font-medium opacity-90">เคาะประตูบ้านคัดกรองสุขภาพ เน้น 4 กลุ่มเปราะบาง (ติดเตียง/ผู้สูงอายุ/ตั้งครรภ์/เด็กเล็ก)</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3 sm:gap-4">
                            <i data-lucide="shield-check" class="w-6 h-6 sm:w-7 sm:h-7 shrink-0 mt-0.5" style="color: var(--c1-icon);"></i>
                            <div>
                                <p class="font-bold text-sm sm:text-base leading-tight">สนับสนุนพื้นที่ปลอดฝุ่น:</p>
                                <p class="text-[13px] sm:text-sm leading-relaxed mt-1 font-medium opacity-90">แจกหน้ากาก N95, จัดทำมุ้งสู้ฝุ่นให้ผู้ป่วยติดเตียง, ห้องปลอดฝุ่นในศูนย์เด็กเล็ก/โรงเรียน</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3 sm:gap-4">
                            <i data-lucide="pill" class="w-6 h-6 sm:w-7 sm:h-7 shrink-0 mt-0.5" style="color: var(--c1-icon);"></i>
                            <div>
                                <p class="font-bold text-sm sm:text-base leading-tight">สั่งจ่ายยาผ่าน Telemedicine :</p>
                                <p class="text-[13px] sm:text-sm leading-relaxed mt-1 font-medium opacity-90">ติดตามและสั่งจ่ายยาสำหรับผู้ป่วยอาการคงที่ เพื่อลดความเสี่ยงสัมผัสฝุ่น</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ================= Column 2: Middle (Clinic & ER) ================= -->
                <div id="col-mid" class="col-2 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm" style="background-color: var(--c2-border); color: var(--c2-text);">
                        การรับผู้ป่วยและดูแลรักษา (รับ)
                    </h2>
                    
                    <div class="space-y-4 h-full flex flex-col justify-between mt-2">
                        <!-- Row 1: Online -->
                        <div class="dark-card flex flex-wrap sm:flex-nowrap items-center justify-between gap-3 relative">
                            <div class="flex items-center gap-3 flex-grow min-w-0">
                                <i data-lucide="smartphone" class="w-8 h-8 sm:w-9 sm:h-9 text-orange-400 shrink-0"></i>
                                <div class="min-w-0">
                                    <h3 class="font-bold text-sm sm:text-base">ระบบก่อนถึง รพ. และออนไลน์</h3>
                                    <p class="text-[11px] sm:text-[13px] leading-tight mt-0.5 truncate sm:whitespace-normal font-medium" style="color: var(--card-muted);">คลินิกมลพิษออนไลน์ ผ่าน Line OA หรือ หมอพร้อม</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-2 shrink-0 sm:w-auto w-full justify-end sm:justify-center mt-2 sm:mt-0">
                                <i data-lucide="arrow-right" class="w-5 h-5 hidden sm:block text-slate-400"></i>
                                <div class="text-right sm:text-center">
                                    <p class="font-bold text-[13px] sm:text-sm text-orange-300">ประเมินเบื้องต้น</p>
                                    <p class="text-[11px] sm:text-xs" style="color: var(--card-muted);">& Telemedicine</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 2: OPD -->
                        <div class="dark-card pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                <div class="flex shrink-0 text-orange-400">
                                    <i data-lucide="eye" class="w-6 h-6 sm:w-7 sm:h-7"></i>
                                    <i data-lucide="lungs" class="w-6 h-6 sm:w-7 sm:h-7 -ml-2"></i>
                                </div>
                                <div>
                                    <h3 class="font-bold text-[13px] sm:text-sm leading-tight">ผู้ป่วยนอก (OPD) <br/>& คลินิกมลพิษ</h3>
                                </div>
                            </div>
                            <div class="flex-grow flex items-center justify-between sm:justify-around gap-1 text-[11px] sm:text-xs">
                                <div class="text-center shrink-0">
                                    <p class="font-bold text-orange-300">คัดกรองอาการ</p>
                                    <p class="text-[9px] sm:text-[10px]" style="color: var(--card-muted);">(PM2.5 > 37.5)</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 sm:w-5 sm:h-5 text-slate-400"></i>
                                <div class="text-center shrink-0">
                                    <p style="color: var(--card-muted);">ส่งเข้า</p>
                                    <p class="font-bold text-orange-400">Pollution Clinic</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 sm:w-5 sm:h-5 text-slate-400"></i>
                                <div class="text-center shrink-0 w-16 sm:w-20">
                                    <p class="font-bold text-orange-300">จ่ายยา/แนะนำ</p>
                                    <p class="text-[9px] sm:text-[10px]" style="color: var(--card-muted);">นัดติดตาม 7 วัน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 3: ER -->
                        <div class="dark-card pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                <i data-lucide="ambulance" class="w-6 h-6 sm:w-7 sm:h-7 text-red-400 shrink-0"></i>
                                <div>
                                    <h3 class="font-bold text-[13px] sm:text-sm leading-tight">ผู้ป่วยฉุกเฉิน (ER) <br/>และระบบ 1669</h3>
                                </div>
                            </div>
                            <div class="flex-grow flex items-center justify-between sm:justify-around gap-1 text-[11px] sm:text-xs">
                                <div class="text-center shrink-0">
                                    <p class="font-bold text-red-300">อาการรุนแรง</p>
                                    <p class="text-[9px] sm:text-[10px]" style="color: var(--card-muted);">(หอบหืด, COPD..)</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 sm:w-5 sm:h-5 text-slate-400"></i>
                                <div class="text-center shrink-0">
                                    <p class="font-bold text-red-300">1669 ติดต่อ EMS</p>
                                    <p style="color: var(--card-muted);">รับเข้า ER</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 sm:w-5 sm:h-5 text-slate-400"></i>
                                <div class="text-center shrink-0 w-16 sm:w-20">
                                    <p class="font-bold text-orange-300">ประเมิน Admit</p>
                                    <p style="color: var(--card-muted);">หรือ กลับบ้าน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 4: IPD -->
                        <div class="dark-card pt-8 sm:pt-6 flex items-center justify-between gap-2 sm:gap-4 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 shrink-0">
                                <i data-lucide="bed" class="w-6 h-6 sm:w-8 sm:h-8 text-blue-400"></i>
                                <h3 class="font-bold text-[13px] sm:text-sm">ผู้ป่วยใน (IPD)</h3>
                            </div>
                            <div class="flex items-center gap-2 sm:gap-4 flex-grow justify-end">
                                <div class="text-right sm:text-center text-[11px] sm:text-sm">
                                     <p class="font-bold text-blue-300">รับ Admit</p>
                                     <p class="text-[10px] sm:text-xs" style="color: var(--card-muted);">เข้าหอผู้ป่วย</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 sm:w-5 sm:h-5 text-slate-400"></i>
                                <div class="text-center text-[11px] sm:text-sm shrink-0">
                                     <p class="font-bold text-blue-300 leading-tight">พยาบาล<br/>ซักประวัติเพิ่มเติม</p>
                                </div>
                            </div>
                         </div>
                    </div>
                </div>

                <!-- ================= Column 3: Right (Refer & Discharge) ================= -->
                <div id="col-right" class="col-3 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm" style="background-color: var(--c3-border); color: var(--c3-text);">
                        ระบบส่งต่อและจำหน่ายผู้ป่วย
                    </h2>
                    
                    <div class="flex flex-col gap-5 h-full mt-2">
                        <!-- Referral System -->
                        <div class="rounded-2xl p-4 sm:p-5 box-refer shadow-md h-1/2 flex flex-col justify-center relative transition-all hover:-translate-y-1">
                            <h3 class="font-bold text-center mb-4 sm:mb-5 text-sm sm:text-lg py-1.5 rounded-full mx-2 sm:mx-6 leading-tight shadow-sm" style="background-color: var(--ref-border); color: #fff;">
                                ระบบส่งต่อผู้ป่วย (Referral)
                            </h3>
                            <div class="flex justify-between items-center text-center">
                                <div class="flex-1 flex flex-col items-center">
                                    <i data-lucide="hospital" class="w-8 h-8 sm:w-10 sm:h-10 mb-2"></i>
                                    <p class="font-bold text-[13px] sm:text-base leading-tight">รพ.ประเมินการ</p>
                                    <p class="text-[11px] sm:text-sm font-medium leading-tight mt-1 opacity-90">สำรองเตียงพร้อมรับ<br/>และ Ventilator พร้อมใช้</p>
                                </div>
                                <div class="flex items-center px-1 sm:px-2">
                                    <i data-lucide="arrow-right" class="w-6 h-6 sm:w-8 sm:h-8 opacity-70"></i>
                                </div>
                                <div class="flex-1 flex flex-col items-center">
                                    <i data-lucide="building-2" class="w-8 h-8 sm:w-10 sm:h-10 mb-2"></i>
                                    <p class="font-bold text-[13px] sm:text-base leading-tight">หาก Overcapacity</p>
                                    <p class="text-[11px] sm:text-sm font-medium mt-1 opacity-90">ส่งต่อโรงพยาบาล</p>
                                    <p class="font-extrabold text-base sm:text-lg mt-0.5">ลำพูน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Discharge -->
                        <div class="rounded-2xl p-4 sm:p-5 box-discharge shadow-md h-1/2 flex flex-col justify-center relative transition-all hover:-translate-y-1">
                            <h3 class="font-bold text-center mb-4 sm:mb-5 text-sm sm:text-lg py-1.5 rounded-full mx-2 sm:mx-6 leading-tight shadow-sm" style="background-color: var(--dis-border); color: #fff;">
                                การจำหน่ายผู้ป่วย (Discharge)
                            </h3>
                            <div class="text-center space-y-2 sm:space-y-3">
                                <p class="font-bold text-base sm:text-xl">วางแผนตามหลัก D-METHOD</p>
                                <div class="w-12 sm:w-16 h-1 bg-current opacity-30 mx-auto rounded-full"></div>
                                <p class="text-[12px] sm:text-sm font-bold leading-relaxed opacity-90">ประสานทีมเยี่ยมบ้านและอาชีวอนามัย<br/>ประเมินสภาพที่อยู่อาศัยไม่ให้กำเริบซ้ำ</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Mobile view for return arrow text (Shown only on small screens) -->
             <div class="lg:hidden text-center mt-8">
                <div class="inline-flex items-center justify-center bg-white px-6 py-3 rounded-full border-2" style="border-color: var(--line-color); color: var(--line-color);">
                    <p class="font-bold text-sm sm:text-base whitespace-nowrap">
                        การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                    </p>
                </div>
            </div>

        </div>
        
        <script>
            // Initialize Icons
            document.addEventListener('DOMContentLoaded', () => {
                lucide.createIcons();
            });

            // Dynamic Line Drawing Function (Desktop Only)
            function drawLines() {
                const svg = document.getElementById('flow-svg');
                const container = document.getElementById('main-container');
                const label = document.getElementById('return-label');
                
                if (window.innerWidth >= 1024 && svg && container) { // lg breakpoint
                    svg.classList.remove('hidden');
                    if (label) {
                        label.classList.remove('hidden');
                        label.classList.add('flex');
                    }
                    
                    const contRect = container.getBoundingClientRect();
                    const colL = document.getElementById('col-left').getBoundingClientRect();
                    const colM = document.getElementById('col-mid').getBoundingClientRect();
                    const colR = document.getElementById('col-right').getBoundingClientRect();
                    
                    // Helpers relative to container
                    const getX = (rect) => rect.left - contRect.left;
                    const getY = (rect) => rect.top - contRect.top;
                    
                    // 1. Line Left -> Middle (หยุดก่อนขอบเพื่อไม่ให้หัวลูกศรแหว่ง)
                    const lmStartY = getY(colL) + (colL.height / 2);
                    const lmStartX = getX(colL) + colL.width;
                    const lmEndX = getX(colM) - 8;
                    document.getElementById('path-lm').setAttribute('d', `M ${lmStartX} ${lmStartY} L ${lmEndX} ${lmStartY}`);
                    
                    // 2. Line Middle -> Right (หยุดก่อนขอบ)
                    const mrStartY = getY(colM) + (colM.height / 2);
                    const mrStartX = getX(colM) + colM.width;
                    const mrEndX = getX(colR) - 8;
                    document.getElementById('path-mr').setAttribute('d', `M ${mrStartX} ${mrStartY} L ${mrEndX} ${mrStartY}`);
                    
                    // 3. Return Dashed Line (Right -> Left at Bottom)
                    const retStartX = getX(colR) + (colR.width / 2);
                    const retStartY = getY(colR) + colR.height;
                    const retEndX = getX(colL) + (colL.width / 2);
                    const retEndY = getY(colL) + colL.height;
                    
                    // คำนวณระยะลงล่างให้ปลอดภัย
                    const dropY = Math.max(retStartY, retEndY) + 50;
                    
                    // Path: ลากลง -> ลากไปซ้าย -> ลากขึ้น (ชี้เข้าไปที่ก้นคอลัมน์ซ้าย)
                    // (retEndY + 12) เพื่อให้เหลือพื้นที่สำหรับวาดหัวลูกศรตอนแทงขึ้นพอดี
                    const returnPath = `M ${retStartX} ${retStartY} L ${retStartX} ${dropY} L ${retEndX} ${dropY} L ${retEndX} ${retEndY + 12}`;
                    document.getElementById('path-return').setAttribute('d', returnPath);
                    
                    // Center the label on the bottom line
                    if (label) {
                        label.style.top = `${dropY}px`;
                        label.style.left = `${getX(colM) + (colM.width / 2)}px`;
                        label.style.transform = 'translate(-50%, -50%)';
                    }
                    
                } else {
                    // Hide SVG/Label on smaller screens (CSS Grid handles vertical stacking natively)
                    if (svg) svg.classList.add('hidden');
                    if (label) {
                        label.classList.add('hidden');
                        label.classList.remove('flex');
                    }
                }
            }

            window.addEventListener('resize', drawLines);
            window.addEventListener('load', () => { 
                setTimeout(drawLines, 100); 
                setTimeout(drawLines, 500); 
            });
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=980, scrolling=True)
