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
               THEME VARIABLES (Light Mode & Dark Mode)
               ========================================= */
            :root {
                --text-main: #334155;
                --text-muted: #64748b;
                --bg-card: #ffffff;
                --border-card: #e2e8f0;

                /* Column 1 (Yellow/Community) */
                --c1-bg: #fefce8; --c1-border: #fde047; --c1-title-bg: #fef9c3; --c1-text-main: #854d0e; --c1-text-sub: #a16207; --c1-box-bg: rgba(254, 240, 138, 0.4);

                /* Column 2 (Orange/Clinic) */
                --c2-bg: #fff7ed; --c2-border: #fb923c; --c2-title-bg: #ffedd5; --c2-text-main: #9a3412; --c2-text-sub: #c2410c;

                /* Column 3 (Green/Refer) */
                --c3-bg: #f0fdf4; --c3-border: #86efac; --c3-title-bg: #dcfce7; --c3-text-main: #166534;

                /* Alert & Tags */
                --alert-bg: #1e4b3e; --alert-border: #123329; --alert-text: #ffffff; --alert-hl: #fde047;
                
                /* Connecting Lines */
                --svg-line: #94a3b8; --svg-return: #475569;
                
                /* Specfic Boxes in Col 3 */
                --bg-red: #fee2e2; --border-red: #fca5a5; --title-red: #fecaca; --text-red: #991b1b; --icon-red: #b91c1c;
                --bg-green: #bbf7d0; --border-green: #4ade80; --title-green: #86efac; --text-green: #166534;
            }

            @media (prefers-color-scheme: dark) {
                :root {
                    --text-main: #e2e8f0;
                    --text-muted: #94a3b8;
                    --bg-card: #1e293b;
                    --border-card: #334155;

                    /* Column 1 (Yellow/Community) -> Deep Olive */
                    --c1-bg: rgba(133, 77, 14, 0.15); --c1-border: rgba(253, 224, 71, 0.3); --c1-title-bg: rgba(133, 77, 14, 0.4); --c1-text-main: #fde047; --c1-text-sub: #fef08a; --c1-box-bg: rgba(133, 77, 14, 0.3);

                    /* Column 2 (Orange/Clinic) -> Deep Rust */
                    --c2-bg: rgba(154, 52, 18, 0.15); --c2-border: rgba(251, 146, 60, 0.3); --c2-title-bg: rgba(154, 52, 18, 0.4); --c2-text-main: #fdba74; --c2-text-sub: #fed7aa;

                    /* Column 3 (Green/Refer) -> Deep Forest */
                    --c3-bg: rgba(22, 101, 52, 0.15); --c3-border: rgba(134, 239, 172, 0.3); --c3-title-bg: rgba(22, 101, 52, 0.4); --c3-text-main: #86efac;

                    /* Alert & Tags */
                    --alert-bg: rgba(15, 23, 42, 0.9); --alert-border: #334155; --alert-text: #e2e8f0; --alert-hl: #fde047;
                    
                    /* Connecting Lines */
                    --svg-line: #64748b; --svg-return: #cbd5e1;
                    
                    /* Specfic Boxes in Col 3 */
                    --bg-red: rgba(153, 27, 27, 0.2); --border-red: rgba(248, 113, 113, 0.3); --title-red: rgba(153, 27, 27, 0.4); --text-red: #fca5a5; --icon-red: #fca5a5;
                    --bg-green: rgba(22, 101, 52, 0.2); --border-green: rgba(74, 222, 128, 0.3); --title-green: rgba(22, 101, 52, 0.4); --text-green: #86efac;
                }
            }

            /* =========================================
               BASE STYLES & UTILITIES
               ========================================= */
            body { font-family: 'Sarabun', sans-serif; background-color: transparent; padding: 1rem; color: var(--text-main); }
            
            .flow-col { border-width: 3px; border-radius: 2rem; padding: 1.25rem; display: flex; flex-direction: column; gap: 1.25rem; position: relative; height: 100%; transition: all 0.3s; }
            .inner-box { background-color: var(--bg-card); border: 1px solid var(--border-card); border-radius: 0.75rem; padding: 1rem; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); transition: all 0.3s; }
            
            .tag-code { position: absolute; top: 0.5rem; right: 0.5rem; background-color: var(--alert-bg); color: var(--alert-text); font-size: 0.65rem; padding: 0.15rem 0.6rem; border-radius: 9999px; font-weight: 700; z-index: 10; border: 1px solid var(--alert-border); letter-spacing: 0.025em; }
            .arrow-icon { color: var(--svg-line); flex-shrink: 0; }

            /* Semantic Theme Mappings */
            .col-1 { background-color: var(--c1-bg); border-color: var(--c1-border); }
            .col-1-title { background-color: var(--c1-title-bg); color: var(--c1-text-main); }
            .col-1-icon { color: var(--c1-text-sub); }
            .col-1-text { color: var(--c1-text-main); }
            .col-1-sub { color: var(--c1-text-sub); }
            .col-1-box { background-color: var(--c1-box-bg); border-color: var(--c1-border); }

            .col-2 { background-color: var(--c2-bg); border-color: var(--c2-border); }
            .col-2-title { background-color: var(--c2-title-bg); color: var(--c2-text-main); }
            .col-2-icon { color: var(--c2-text-sub); }
            .col-2-text { color: var(--c2-text-main); }
            .col-2-sub { color: var(--c2-text-sub); }

            .col-3 { background-color: var(--c3-bg); border-color: var(--c3-border); }
            .col-3-title { background-color: var(--c3-title-bg); color: var(--c3-text-main); }
            
            .box-refer { background-color: var(--bg-red); border-color: var(--border-red); color: var(--text-red); border-width: 3px; }
            .box-refer-title { background-color: var(--title-red); }
            .box-refer-icon { color: var(--icon-red); }

            .box-discharge { background-color: var(--bg-green); border-color: var(--border-green); color: var(--text-green); border-width: 3px; }
            .box-discharge-title { background-color: var(--title-green); }
        </style>
    </head>
    <body>
        <!-- Main Container -->
        <div id="main-container" class="max-w-[1280px] mx-auto relative pb-20 sm:pb-28 lg:pb-32">
            
            <!-- Alert Box -->
            <div class="flex justify-end mb-6 relative z-20">
                <div class="px-4 py-2.5 rounded-full font-bold shadow-md text-xs sm:text-sm flex items-center border" style="background-color: var(--alert-bg); color: var(--alert-text); border-color: var(--alert-border);">
                    <span class="mr-2" style="color: var(--alert-hl);">ย้ำ!</span> บันทึกรหัสโรค Z58.1 (Exposure to air pollution) ทุกจุดบริการเพื่อวิเคราะห์ข้อมูล
                </div>
            </div>

            <!-- SVG Overlay for Dynamic Line Drawing (Desktop Only) -->
            <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden lg:block z-0" style="overflow: visible;">
                <defs>
                    <!-- Marker Connectors -->
                    <marker id="arrow-main" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--svg-line)" />
                    </marker>
                    <!-- Marker Return Line -->
                    <marker id="arrow-return" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--svg-return)" />
                    </marker>
                </defs>
                
                <!-- Path Left -> Middle -->
                <path id="path-lm" fill="none" stroke="var(--svg-line)" stroke-width="5" marker-end="url(#arrow-main)" />
                <!-- Path Middle -> Right -->
                <path id="path-mr" fill="none" stroke="var(--svg-line)" stroke-width="5" marker-end="url(#arrow-main)" />
                <!-- Bottom Return Dashed Path -->
                <path id="path-return" fill="none" stroke="var(--svg-return)" stroke-width="4" stroke-dasharray="10, 8" stroke-linejoin="round" marker-end="url(#arrow-return)" />
            </svg>

            <!-- Return Label (Desktop Dynamic) -->
            <div id="return-label" class="absolute hidden lg:flex items-center justify-center inner-box px-8 py-2.5 rounded-full z-10 font-bold text-base whitespace-nowrap border-2" style="border-color: var(--svg-return); color: var(--text-main);">
                การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
            </div>

            <!-- 3 Columns Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 relative z-10 items-stretch">

                <!-- ================= Column 1: Left (Community) ================= -->
                <div id="col-left" class="col-1 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center col-1-title py-2 rounded-full mx-2 sm:mx-4">ชุมชนและหน่วยบริการปฐมภูมิ (รุก)</h2>
                    <div class="flex flex-col items-center text-center py-5 col-1-box border rounded-xl shadow-sm">
                        <div class="flex justify-center mb-3">
                            <i data-lucide="users" class="w-10 h-10 sm:w-12 sm:h-12 col-1-icon"></i>
                        </div>
                        <h3 class="font-bold text-lg sm:text-xl col-1-text">กลไก 3 หมอ</h3>
                    </div>
                    <div class="flex-grow space-y-4 sm:space-y-5 mt-2">
                         <div class="flex items-start gap-3 sm:gap-4">
                            <i data-lucide="clipboard-list" class="w-6 h-6 sm:w-7 sm:h-7 col-1-icon shrink-0 mt-1"></i>
                            <div>
                                <p class="font-bold col-1-text text-sm sm:text-base">การลงพื้นที่เชิงรุก: อสม. และ รพ.สต.</p>
                                <p class="text-xs sm:text-sm col-1-sub leading-relaxed mt-0.5">เคาะประตูบ้านคัดกรองสุขภาพ (SCPM-66/QAP-F4) เน้น 4 กลุ่มเปราะบาง (ติดเตียง/ผู้สูงอายุ/ตั้งครรภ์/เด็กเล็ก)</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3 sm:gap-4">
                            <i data-lucide="shield-check" class="w-6 h-6 sm:w-7 sm:h-7 col-1-icon shrink-0 mt-1"></i>
                            <div>
                                <p class="font-bold col-1-text text-sm sm:text-base">สนับสนุนพื้นที่ปลอดฝุ่น:</p>
                                <p class="text-xs sm:text-sm col-1-sub leading-relaxed mt-0.5">แจกหน้ากาก N95, จัดทำมุ้งสู้ฝุ่นให้ผู้ป่วยติดเตียง, ห้องปลอดฝุ่นในศูนย์เด็กเล็ก/โรงเรียน</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3 sm:gap-4">
                            <i data-lucide="truck" class="w-6 h-6 sm:w-7 sm:h-7 col-1-icon shrink-0 mt-1"></i>
                            <div>
                                <p class="font-bold col-1-text text-sm sm:text-base">จัดส่งยาถึงบ้าน:</p>
                                <p class="text-xs sm:text-sm col-1-sub leading-relaxed mt-0.5">สำหรับผู้ป่วยโรคเรื้อรังที่อาการคงที่ ลดความเสี่ยงสัมผัสฝุ่น</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ================= Column 2: Middle (Clinic & ER) ================= -->
                <div id="col-mid" class="col-2 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center col-2-title py-2 rounded-full mx-2 sm:mx-4">การรับผู้ป่วยและดูแลรักษา (รับ)</h2>
                    
                    <div class="space-y-4 h-full flex flex-col justify-between mt-2">
                        <!-- Row 1: Online -->
                        <div class="inner-box flex flex-wrap sm:flex-nowrap items-center justify-between gap-3 relative">
                            <div class="flex items-center gap-3 flex-grow min-w-0">
                                <i data-lucide="smartphone" class="w-8 h-8 sm:w-9 sm:h-9 col-2-icon shrink-0"></i>
                                <div class="min-w-0">
                                    <h3 class="font-bold col-2-text text-sm sm:text-base">ระบบก่อนถึง รพ. และออนไลน์</h3>
                                    <p class="text-[11px] sm:text-xs col-2-sub leading-tight mt-0.5 truncate sm:whitespace-normal">คลินิกมลพิษออนไลน์ ผ่าน Line OA หรือ หมอพร้อม</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-2 shrink-0 sm:w-auto w-full justify-end sm:justify-center mt-2 sm:mt-0">
                                <i data-lucide="arrow-right" class="arrow-icon w-5 h-5 hidden sm:block"></i>
                                <div class="text-right sm:text-center">
                                    <p class="font-bold text-[13px] sm:text-sm col-2-text">ประเมินเบื้องต้น</p>
                                    <p class="text-[11px] sm:text-xs col-2-sub">& Telemedicine</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 2: OPD -->
                        <div class="inner-box pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                <div class="flex shrink-0 col-2-icon">
                                    <i data-lucide="eye" class="w-6 h-6 sm:w-7 sm:h-7"></i>
                                    <i data-lucide="lungs" class="w-6 h-6 sm:w-7 sm:h-7 -ml-2"></i>
                                </div>
                                <div>
                                    <h3 class="font-bold text-[13px] sm:text-sm col-2-text leading-tight">ผู้ป่วยนอก (OPD) <br/>& คลินิกมลพิษ</h3>
                                </div>
                            </div>
                            <div class="flex-grow flex items-center justify-between sm:justify-around gap-1 text-[11px] sm:text-xs">
                                <div class="text-center shrink-0">
                                    <p class="font-bold col-2-text">คัดกรองอาการ</p>
                                    <p class="text-[9px] sm:text-[10px] col-2-sub">(PM2.5 > 37.5)</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center shrink-0">
                                    <p class="col-2-text">ส่งเข้า</p>
                                    <p class="font-bold col-2-icon">Pollution Clinic</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center shrink-0 w-16 sm:w-20">
                                    <p class="font-bold col-2-text">จ่ายยา/แนะนำ</p>
                                    <p class="text-[9px] sm:text-[10px] col-2-sub">นัดติดตาม 7 วัน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 3: ER -->
                        <div class="inner-box pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                <i data-lucide="ambulance" class="w-6 h-6 sm:w-7 sm:h-7 text-red-500 shrink-0"></i>
                                <div>
                                    <h3 class="font-bold text-[13px] sm:text-sm col-2-text leading-tight">ผู้ป่วยฉุกเฉิน (ER) <br/>และระบบ 1669</h3>
                                </div>
                            </div>
                            <div class="flex-grow flex items-center justify-between sm:justify-around gap-1 text-[11px] sm:text-xs">
                                <div class="text-center shrink-0">
                                    <p class="font-bold col-2-text">อาการรุนแรง</p>
                                    <p class="text-[9px] sm:text-[10px] col-2-sub">(หอบหืด, COPD..)</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center shrink-0">
                                    <p class="font-bold col-2-text">1669 ติดต่อ EMS</p>
                                    <p class="col-2-sub">รับเข้า ER</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center shrink-0 w-16 sm:w-20">
                                    <p class="font-bold col-2-text">ประเมิน Admit</p>
                                    <p class="col-2-sub">หรือ กลับบ้าน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 4: IPD -->
                        <div class="inner-box pt-8 sm:pt-6 flex items-center justify-between gap-2 sm:gap-4 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 shrink-0">
                                <i data-lucide="bed" class="w-6 h-6 sm:w-8 sm:h-8 text-blue-500"></i>
                                <h3 class="font-bold col-2-text text-[13px] sm:text-sm">ผู้ป่วยใน (IPD)</h3>
                            </div>
                            <div class="flex items-center gap-2 sm:gap-4 flex-grow justify-end">
                                <div class="text-right sm:text-center text-[11px] sm:text-sm">
                                     <p class="font-bold col-2-text">รับ Admit</p>
                                     <p class="text-[10px] sm:text-xs col-2-sub">เข้าหอผู้ป่วย</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center text-[11px] sm:text-sm shrink-0">
                                     <p class="font-bold col-2-text leading-tight">พยาบาล<br/>ซักประวัติเพิ่มเติม</p>
                                </div>
                            </div>
                         </div>
                    </div>
                </div>

                <!-- ================= Column 3: Right (Refer & Discharge) ================= -->
                <div id="col-right" class="col-3 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center col-3-title py-2 rounded-full mx-2 sm:mx-4">ระบบส่งต่อและจำหน่ายผู้ป่วย</h2>
                    
                    <div class="flex flex-col gap-5 h-full mt-2">
                        <!-- Referral System -->
                        <div class="rounded-2xl p-4 sm:p-5 box-refer shadow-sm h-1/2 flex flex-col justify-center relative">
                            <h3 class="font-bold text-center mb-4 sm:mb-5 text-sm sm:text-lg box-refer-title py-1 rounded-full mx-2 sm:mx-6 leading-tight">ระบบส่งต่อผู้ป่วย (Referral)</h3>
                            <div class="flex justify-between items-center text-center">
                                <div class="flex-1 flex flex-col items-center">
                                    <i data-lucide="hospital" class="w-8 h-8 sm:w-10 sm:h-10 mb-2 box-refer-icon"></i>
                                    <p class="font-bold text-[13px] sm:text-base leading-tight">รพ.ประเมินการ</p>
                                    <p class="text-[11px] sm:text-sm leading-tight mt-1 opacity-90">สำรองเตียงพร้อมรับ<br/>และ Ventilator พร้อมใช้</p>
                                </div>
                                <div class="flex items-center px-1 sm:px-2">
                                    <i data-lucide="arrow-right" class="w-6 h-6 sm:w-8 sm:h-8 box-refer-icon"></i>
                                </div>
                                <div class="flex-1 flex flex-col items-center">
                                    <i data-lucide="building-2" class="w-8 h-8 sm:w-10 sm:h-10 mb-2 box-refer-icon"></i>
                                    <p class="font-bold text-[13px] sm:text-base leading-tight">หาก Overcapacity</p>
                                    <p class="text-[11px] sm:text-sm mt-1 opacity-90">ส่งต่อโรงพยาบาล</p>
                                    <p class="font-extrabold text-base sm:text-lg mt-0.5">ลำพูน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Discharge -->
                        <div class="rounded-2xl p-4 sm:p-5 box-discharge shadow-sm h-1/2 flex flex-col justify-center relative">
                            <h3 class="font-bold text-center mb-4 sm:mb-5 text-sm sm:text-lg box-discharge-title py-1 rounded-full mx-2 sm:mx-6 leading-tight">การจำหน่ายผู้ป่วย (Discharge)</h3>
                            <div class="text-center space-y-2 sm:space-y-3">
                                <p class="font-bold text-base sm:text-xl">วางแผนตามหลัก D-METHOD</p>
                                <div class="w-12 sm:w-16 h-1 bg-current opacity-20 mx-auto rounded-full"></div>
                                <p class="text-[12px] sm:text-sm font-medium leading-relaxed opacity-90">ประสานทีมเยี่ยมบ้านและอาชีวอนามัย<br/>ประเมินสภาพที่อยู่อาศัยไม่ให้กำเริบซ้ำ</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Mobile view for return arrow text (Shown only on small screens) -->
             <div class="lg:hidden text-center mt-8">
                <div class="inline-flex items-center justify-center inner-box px-6 py-3 rounded-full border-2" style="border-color: var(--svg-return);">
                    <p class="font-bold text-sm sm:text-base whitespace-nowrap" style="color: var(--text-main);">
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
                    
                    // 1. Line Left -> Middle
                    const lmStartY = getY(colL) + (colL.height / 2);
                    const lmStartX = getX(colL) + colL.width;
                    const lmEndX = getX(colM);
                    document.getElementById('path-lm').setAttribute('d', `M ${lmStartX} ${lmStartY} L ${lmEndX - 10} ${lmStartY}`);
                    
                    // 2. Line Middle -> Right
                    const mrStartY = getY(colM) + (colM.height / 2);
                    const mrStartX = getX(colM) + colM.width;
                    const mrEndX = getX(colR);
                    document.getElementById('path-mr').setAttribute('d', `M ${mrStartX} ${mrStartY} L ${mrEndX - 10} ${mrStartY}`);
                    
                    // 3. Return Dashed Line (Right -> Left at Bottom)
                    const retStartX = getX(colR) + (colR.width / 2);
                    const retStartY = getY(colR) + colR.height;
                    const retEndX = getX(colL) + (colL.width / 2);
                    const retEndY = getY(colL) + colL.height;
                    
                    const dropY = Math.max(retStartY, retEndY) + 40;
                    
                    // Path: Down -> Left -> Up into column 1
                    const returnPath = `M ${retStartX} ${retStartY} L ${retStartX} ${dropY} L ${retEndX} ${dropY} L ${retEndX} ${retEndY + 15}`;
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
