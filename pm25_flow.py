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
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style type="text/tailwindcss">
            /* =========================================
               THEME VARIABLES (FIXED PASTEL PALETTE)
               ========================================= */
            :root {
                --text-main: #1e293b; 
                --text-muted: #475569; 
                --bg-card: #ffffff; 
                --border-card: #e2e8f0;
                --shadow-box: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);

                /* Column 1 (Yellow/Community) */
                --c1-bg: #fefce8; --c1-border: #fde047; 
                --c1-title-bg: #fef9c3; --c1-title-text: #854d0e; 
                --c1-icon: #d97706; 

                /* Column 2 (Orange/Clinic) */
                --c2-bg: #fff7ed; --c2-border: #fb923c; 
                --c2-title-bg: #ffedd5; --c2-title-text: #9a3412; 
                --c2-icon: #ea580c; 

                /* Column 3 (Emerald/Refer) */
                --c3-bg: #f0fdf4; --c3-border: #86efac; 
                --c3-title-bg: #dcfce7; --c3-title-text: #166534; 
                --c3-icon: #059669; 
                
                /* Disease Control (Purple) */
                --dc-bg: #faf5ff; --dc-border: #d8b4fe;
                --dc-title-bg: #f3e8ff; --dc-title-text: #581c87;
                --dc-icon: #7e22ce;

                --dis-bg: #f0fdf4; --dis-border: #86efac; 
                --dis-title-bg: #dcfce7; --dis-title-text: #166534; 

                /* Alert & Tags */
                --alert-bg: #1e4b3e; --alert-border: #123329; 
                --alert-text: #ffffff; --alert-hl: #fde047;
                
                /* Connecting Lines */
                --line-color: #64748b; 
            }

            /* =========================================
               BASE STYLES & UTILITIES
               ========================================= */
            body { font-family: 'Sarabun', sans-serif; background-color: transparent; margin: 0; padding: 0; color: var(--text-main); }
            
            .text-main { color: var(--text-main); }
            .text-muted { color: var(--text-muted); }

            .flow-col { border-width: 3px; border-radius: 2rem; padding: 1.25rem; display: flex; flex-direction: column; gap: 1.25rem; position: relative; height: 100%; transition: all 0.3s; }
            
            .inner-box { background-color: var(--bg-card); border: 1px solid var(--border-card); border-radius: 0.75rem; padding: 1rem; box-shadow: var(--shadow-box); transition: all 0.3s; }
            .inner-box:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); }
            
            .tag-code { position: absolute; top: 0.5rem; right: 0.5rem; background-color: var(--alert-bg); color: var(--alert-text); font-size: 0.65rem; padding: 0.2rem 0.6rem; border-radius: 9999px; font-weight: 700; z-index: 10; border: 1px solid var(--alert-border); box-shadow: 0 2px 4px rgba(0,0,0,0.15); letter-spacing: 0.025em; }
            .arrow-icon { color: var(--line-color); flex-shrink: 0; }

            /* Semantic Theme Classes */
            .col-1 { background-color: var(--c1-bg); border-color: var(--c1-border); }
            .c1-title { background-color: var(--c1-title-bg); color: var(--c1-title-text); }
            .c1-text { color: var(--c1-title-text); }
            .c1-icon { color: var(--c1-icon); }

            .col-2 { background-color: var(--c2-bg); border-color: var(--c2-border); }
            .c2-title { background-color: var(--c2-title-bg); color: var(--c2-title-text); }
            .c2-text { color: var(--c2-title-text); }
            .c2-icon { color: var(--c2-icon); }

            .col-3 { background-color: var(--c3-bg); border-color: var(--c3-border); }
            .c3-title { background-color: var(--c3-title-bg); color: var(--c3-title-text); }

            .box-dc { background-color: var(--dc-bg); border-color: var(--dc-border); border-width: 3px; }
            .box-dc-title { background-color: var(--dc-title-bg); color: var(--dc-title-text); }
            .box-dc-icon { color: var(--dc-icon); }

            .box-discharge { background-color: var(--dis-bg); border-color: var(--dis-border); border-width: 3px; }
            .box-discharge-title { background-color: var(--dis-title-bg); color: var(--dis-title-text); }
            
            /* =======================================
               คำสั่งบังคับสำหรับการปริ้น (PRINT STYLES)
               ======================================= */
            @media print {
                body, *, svg, path {
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                #flow-svg {
                    display: block !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                }
                .shadow-sm, .shadow-md, .shadow-lg {
                    box-shadow: none !important;
                    border: 1px solid #e2e8f0 !important;
                }
            }
        </style>
    </head>
    <body class="bg-slate-50">
        
        <!-- พื้นที่สำหรับ Capture (เพิ่ม padding เพื่อไม่ให้เนื้อหาชิดขอบจอเกินไปตอนโหลดรูป) -->
        <div id="capture-area" class="w-full bg-slate-50 pb-10 pt-6 px-4 sm:px-8 lg:px-12 transition-all duration-300">
            
            <!-- Header & Download Button -->
            <div class="text-center mb-8 sm:mb-12 relative">
                <h2 class="text-2xl sm:text-3xl md:text-4xl font-extrabold mb-2 tracking-wide" style="color: var(--text-main);">บทบาทของแต่ละหน่วยงาน</h2>
                <p class="text-sm sm:text-base md:text-[1.15rem] font-bold text-muted">การดูแลผู้ป่วยที่ได้รับผลกระทบจาก PM 2.5 โรงพยาบาลสันทราย</p>
                
                <!-- ปุ่มสำหรับดาวน์โหลดรูปภาพ -->
                <button onclick="downloadImage()" class="mt-5 inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 px-6 rounded-full shadow-lg transition-all print:hidden" data-html2canvas-ignore="true">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    ดาวน์โหลดแผนผัง
                </button>
            </div>

            <!-- Main Container -->
            <div id="main-container" class="max-w-[1400px] mx-auto relative pb-20 sm:pb-28 lg:pb-32 z-10">
                
                <!-- Alert Box -->
                <div class="flex justify-end mb-6 relative z-20">
                    <div class="px-5 py-2.5 rounded-full font-bold shadow-lg text-xs sm:text-sm flex items-center border" style="background-color: var(--alert-bg); color: var(--alert-text); border-color: var(--alert-border);">
                        <span class="mr-2" style="color: var(--alert-hl);">ย้ำ!</span> บันทึกรหัสโรค Z58.1 (Exposure to air pollution) ทุกจุดบริการเพื่อวิเคราะห์ข้อมูล
                    </div>
                </div>

                <!-- SVG Overlay for Dynamic Line Drawing -->
                <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden z-0" style="overflow: visible;">
                    <defs>
                        <!-- Marker สำหรับหัวลูกศรเส้นประ -->
                        <marker id="arrow-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line-color)" />
                        </marker>
                    </defs>
                    
                    <!-- Path Left -> Middle -->
                    <path id="path-lm" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" marker-end="url(#arrow-head)" />
                    <!-- Path Middle -> Right -->
                    <path id="path-mr" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" marker-end="url(#arrow-head)" />
                    <!-- Bottom Return Dashed Path -->
                    <path id="path-return" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" stroke-linejoin="round" marker-end="url(#arrow-head)" />
                </svg>

                <!-- Return Label -->
                <div id="return-label" class="absolute hidden items-center justify-center bg-white px-8 py-2.5 rounded-full z-10 border-[2px] shadow-sm" style="border-color: var(--line-color);">
                    <p class="font-bold text-base whitespace-nowrap text-main" style="color: var(--line-color);">
                        การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                    </p>
                </div>

                <!-- 4 Columns Grid (1:2:1 Ratio to give more space to the middle section) -->
                <div id="main-grid" class="grid grid-cols-1 lg:grid-cols-4 gap-6 sm:gap-8 relative z-10 items-stretch">

                    <!-- ================= Column 1: Left (Community) ================= -->
                    <div id="col-left" class="col-1 flow-col lg:col-span-1">
                        <h2 class="text-lg sm:text-xl font-extrabold text-center c1-title py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm">ชุมชนและหน่วยบริการปฐมภูมิ (รุก)</h2>
                        <div class="flex flex-col items-center text-center py-5 bg-white/60 rounded-xl border border-yellow-200 shadow-sm">
                            <div class="flex justify-center mb-3">
                                <i data-lucide="users" class="w-10 h-10 sm:w-12 sm:h-12 c1-icon"></i>
                            </div>
                            <h3 class="font-bold text-lg sm:text-xl c1-text">กลไก 3 หมอ</h3>
                        </div>
                        <div class="flex-grow space-y-4 sm:space-y-5 mt-2">
                             <div class="flex items-start gap-3 sm:gap-4">
                                <i data-lucide="clipboard-list" class="w-6 h-6 sm:w-7 sm:h-7 c1-icon shrink-0 mt-1"></i>
                                <div>
                                    <p class="font-bold text-main text-sm sm:text-base">การลงพื้นที่เชิงรุก: อสม. และ รพ.สต.</p>
                                    <p class="text-xs sm:text-sm text-muted leading-relaxed mt-0.5 font-medium">เคาะประตูบ้านคัดกรองสุขภาพ เน้น 4 กลุ่มเปราะบาง (ติดเตียง/ผู้สูงอายุ/ตั้งครรภ์/เด็กเล็ก)</p>
                                </div>
                            </div>
                            <div class="flex items-start gap-3 sm:gap-4">
                                <i data-lucide="shield-check" class="w-6 h-6 sm:w-7 sm:h-7 c1-icon shrink-0 mt-1"></i>
                                <div>
                                    <p class="font-bold text-main text-sm sm:text-base">สนับสนุนพื้นที่ปลอดฝุ่น:</p>
                                    <p class="text-xs sm:text-sm text-muted leading-relaxed mt-0.5 font-medium">แจกหน้ากาก N95, จัดทำมุ้งสู้ฝุ่นให้ผู้ป่วยติดเตียง, ห้องปลอดฝุ่นในศูนย์เด็กเล็ก/โรงเรียน</p>
                                </div>
                            </div>
                            <div class="flex items-start gap-3 sm:gap-4">
                                <i data-lucide="pill" class="w-6 h-6 sm:w-7 sm:h-7 c1-icon shrink-0 mt-1"></i>
                                <div>
                                    <p class="font-bold text-main text-sm sm:text-base">สั่งจ่ายยาผ่าน Telemedicine :</p>
                                    <p class="text-xs sm:text-sm text-muted leading-relaxed mt-0.5 font-medium">ติดตามและสั่งจ่ายยาสำหรับผู้ป่วยอาการคงที่ เพื่อลดความเสี่ยงสัมผัสฝุ่น</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- ================= Column 2: Middle (Clinic & ER) ================= -->
                    <div id="col-mid" class="col-2 flow-col lg:col-span-2">
                        <h2 class="text-lg sm:text-xl font-extrabold text-center c2-title py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm">การรับผู้ป่วยและดูแลรักษา (รับ)</h2>
                        
                        <div id="inner-grid" class="grid grid-cols-1 xl:grid-cols-2 gap-4 h-full mt-2">
                            
                            <!-- Left Sub-column (4 original rows) -->
                            <div class="space-y-4 flex flex-col justify-between h-full">
                                <!-- Row 1: Online -->
                                <div class="inner-box flex flex-wrap sm:flex-nowrap items-center justify-between gap-3 relative border-orange-200 shadow-sm flex-1">
                                    <div class="flex items-center gap-3 flex-grow min-w-0">
                                        <i data-lucide="smartphone" class="w-8 h-8 sm:w-9 sm:h-9 c2-icon shrink-0"></i>
                                        <div class="min-w-0">
                                            <h3 class="font-bold text-main text-sm sm:text-base">ระบบก่อนถึง รพ. และออนไลน์</h3>
                                            <p class="text-[11px] sm:text-xs text-muted leading-tight mt-0.5 truncate sm:whitespace-normal font-medium">คลินิกมลพิษออนไลน์ ผ่าน Line OA หรือ หมอพร้อม</p>
                                        </div>
                                    </div>
                                    <div class="flex items-center gap-2 shrink-0 sm:w-auto w-full justify-end sm:justify-center mt-2 sm:mt-0">
                                        <i data-lucide="arrow-right" class="arrow-icon w-5 h-5 hidden sm:block"></i>
                                        <div class="text-right sm:text-center">
                                            <p class="font-bold text-[13px] sm:text-sm c2-text">ประเมินเบื้องต้น</p>
                                            <p class="text-[11px] sm:text-xs text-muted font-medium">& Telemedicine</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Row 2: PCU หนองหาร / รพ.สต. -->
                                <div class="inner-box pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative border-orange-200 shadow-sm flex-1">
                                    <div class="tag-code">รหัส Z58.1</div>
                                    <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                        <div class="flex shrink-0 c2-icon">
                                            <i data-lucide="building-2" class="w-6 h-6 sm:w-7 sm:h-7"></i>
                                        </div>
                                        <div>
                                            <h3 class="font-bold text-[13px] sm:text-sm text-main leading-tight">PCU หนองหาร<br/>& รพ.สต.</h3>
                                        </div>
                                    </div>
                                    <div class="flex-grow flex items-center justify-between sm:justify-around gap-1 text-[11px] sm:text-xs">
                                        <div class="text-center shrink-0">
                                            <p class="font-bold text-main">คัดกรองอาการ</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                        <div class="text-center shrink-0 w-20 sm:w-24">
                                            <p class="font-bold text-main leading-tight">เข้าข่าย: ลง GG Sheets</p>
                                            <p class="text-[9px] sm:text-[10px] text-muted font-medium">+ รักษาตามอาการ</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                        <div class="text-center shrink-0">
                                            <p class="text-[10px] text-muted font-medium">อาการรุนแรง</p>
                                            <p class="font-bold text-red-600">Refer รพ.</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Row 3: OPD -->
                                <div class="inner-box pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative border-orange-200 shadow-sm flex-1">
                                    <div class="tag-code">รหัส Z58.1</div>
                                    <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                        <div class="flex shrink-0 c2-icon">
                                            <i data-lucide="eye" class="w-6 h-6 sm:w-7 sm:h-7"></i>
                                        </div>
                                        <div>
                                            <h3 class="font-bold text-[13px] sm:text-sm text-main leading-tight">ผู้ป่วยนอก (OPD)</h3>
                                        </div>
                                    </div>
                                    <div class="flex-grow flex items-center justify-between sm:justify-around gap-1 text-[11px] sm:text-xs">
                                        <div class="text-center shrink-0">
                                            <p class="font-bold text-main">คัดกรองอาการ</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                        <div class="text-center shrink-0 w-20 sm:w-24">
                                            <p class="font-bold text-main leading-tight">เข้าข่าย: ลง GG Sheets</p>
                                            <p class="text-[9px] sm:text-[10px] text-muted font-medium">+ รักษาตามอาการ</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                        <div class="text-center shrink-0 w-16 sm:w-20">
                                            <p class="text-[9px] sm:text-[10px] text-muted font-medium leading-tight">นัดติดตาม ไม่ทุเลา</p>
                                            <p class="font-bold c2-text">ส่งคลินิกมลพิษ</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Row 4: ER -->
                                <div class="inner-box pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative border-orange-200 shadow-sm flex-1">
                                    <div class="tag-code">รหัส Z58.1</div>
                                    <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                        <i data-lucide="ambulance" class="w-6 h-6 sm:w-7 sm:h-7 text-red-500 shrink-0"></i>
                                        <div>
                                            <h3 class="font-bold text-[13px] sm:text-sm text-main leading-tight">ผู้ป่วยฉุกเฉิน (ER) <br/>และระบบ 1669</h3>
                                        </div>
                                    </div>
                                    <div class="flex-grow flex items-center justify-between sm:justify-around gap-1 text-[11px] sm:text-xs">
                                        <div class="text-center shrink-0">
                                            <p class="font-bold text-main">อาการรุนแรง</p>
                                            <p class="text-[9px] sm:text-[10px] text-muted font-medium">(หอบหืด, COPD..)</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                        <div class="text-center shrink-0">
                                            <p class="font-bold text-main">1669 / EMS</p>
                                            <p class="text-muted font-medium">รับเข้า ER</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                        <div class="text-center shrink-0 w-24 sm:w-28">
                                            <p class="font-bold text-main leading-tight">เข้าข่าย: ลง GG Sheets</p>
                                            <p class="text-[9px] sm:text-[10px] text-muted font-medium">+ ประเมิน Admit/กลับบ้าน</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Right Sub-column (Pollution Clinic Box) -->
                            <div class="inner-box border-orange-400 bg-[#fff2e5] p-4 sm:p-5 flex flex-col h-full relative shadow-md">
                                <h3 class="font-extrabold text-orange-900 text-sm sm:text-base mb-4 flex items-center gap-2 border-b border-orange-200 pb-2.5">
                                    <i data-lucide="stethoscope" class="w-5 h-5 text-orange-600"></i>
                                    คลินิกมลพิษ
                                </h3>

                                <div class="space-y-4 flex-grow text-[12px] sm:text-[13px] text-main overflow-y-auto pr-1">
                                    
                                    <!-- 1. จัดการนัดหมาย -->
                                    <div>
                                        <p class="font-bold text-orange-800 flex items-start gap-2 mb-1.5">
                                            <span class="bg-orange-200 text-orange-800 w-5 h-5 rounded-full flex items-center justify-center text-[11px] shrink-0 mt-0.5">1</span>
                                            จัดการนัดหมาย
                                        </p>
                                        <p class="pl-8 text-muted font-medium">(หมอพร้อม/Telemedicine/Walk-in)</p>
                                    </div>

                                    <!-- 2. เฝ้าระวัง -->
                                    <div>
                                        <p class="font-bold text-orange-800 flex items-start gap-2 mb-1.5">
                                            <span class="bg-orange-200 text-orange-800 w-5 h-5 rounded-full flex items-center justify-center text-[11px] shrink-0 mt-0.5">2</span>
                                            เฝ้าระวัง (การเข้ารับการรักษาของผู้ป่วย)
                                        </p>
                                        <ul class="list-disc pl-8 space-y-1.5 text-muted font-medium">
                                            <li>ตรวจสอบรหัส ICD-10 ที่เกี่ยวข้องกับการสัมผัส PM2.5 ในระบบ HosOS</li>
                                            <li>ตรวจสอบผู้ป่วยที่เข้ารับการรักษาในวันที่ฝุ่นสูง (> 37.5) GG sheets ของ OPD/ER/PCU หนองหาร</li>
                                        </ul>
                                    </div>

                                    <!-- 3. คัดกรอง ซักประวัติ -->
                                    <div>
                                        <p class="font-bold text-orange-800 flex items-start gap-2 mb-2">
                                            <span class="bg-orange-200 text-orange-800 w-5 h-5 rounded-full flex items-center justify-center text-[11px] shrink-0 mt-0.5">3</span>
                                            คัดกรอง ซักประวัติ สอบสวนโรค
                                        </p>
                                        <div class="pl-7 space-y-2.5">
                                            
                                            <!-- กรณีไม่เข้าข่าย -->
                                            <div class="bg-white p-2.5 rounded-lg border border-orange-100 shadow-sm">
                                                <p class="font-bold text-emerald-700 mb-1 flex items-center gap-1.5">
                                                    <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-500"></i> กรณีไม่เข้าข่าย / อาการเล็กน้อย
                                                </p>
                                                <p class="text-muted font-medium pl-5 border-l-2 border-emerald-300 ml-1.5 leading-tight">
                                                    ให้คำแนะนำ และส่งต่อ <span class="font-bold text-main">ทีม 3 หมอ</span>
                                                </p>
                                            </div>
                                            
                                            <!-- กรณีเข้าข่าย -->
                                            <div class="bg-white p-2.5 rounded-lg border border-orange-100 shadow-sm">
                                                <p class="font-bold text-red-700 mb-1.5 flex items-center gap-1.5">
                                                    <i data-lucide="alert-circle" class="w-4 h-4 text-red-500"></i> กรณีเข้าข่าย
                                                </p>
                                                <ul class="list-disc pl-8 space-y-1.5 text-muted font-medium ml-1">
                                                    <li>ส่งพบแพทย์ ตรวจ Lab</li>
                                                    <li><span class="text-red-600 font-bold">ส่งห้องฉุกเฉิน (ER)</span> หากอาการรุนแรง</li>
                                                    <li class="leading-snug">แจ้งข้อมูลผู้ป่วยที่เข้าข่ายแก่งาน<span style="color: #7e22ce; font-weight: 800;">ควบคุมโรค</span> <br/><span class="text-[11px] opacity-80">(เพื่อให้ดำเนินการลงพื้นที่ + รายงาน สสจ.)</span></li>
                                                </ul>
                                            </div>

                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- ================= Column 3: Right (Control & Discharge) ================= -->
                    <div id="col-right" class="col-3 flow-col lg:col-span-1">
                        <h2 class="text-lg sm:text-xl font-extrabold text-center c3-title py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm">ควบคุมโรค และจำหน่ายผู้ป่วย</h2>
                        
                        <div class="flex flex-col gap-4 h-full mt-2">
                            <!-- 1. Disease Control -->
                            <div class="rounded-2xl p-4 sm:p-5 box-dc shadow-sm flex-1 flex flex-col justify-center relative transition-transform hover:-translate-y-1 bg-white">
                                <h3 class="font-bold text-center mb-3 sm:mb-4 text-sm sm:text-lg box-dc-title py-1.5 rounded-full mx-2 sm:mx-6 leading-tight">
                                    งานควบคุมโรค (Disease Control)
                                </h3>
                                <div class="flex justify-between items-center text-center">
                                    <div class="flex-1 flex flex-col items-center">
                                        <i data-lucide="shield-alert" class="w-7 h-7 sm:w-9 sm:h-9 mb-1 box-dc-icon"></i>
                                        <p class="font-bold text-[13px] sm:text-base text-main leading-tight">รับแจ้งข้อมูล</p>
                                        <p class="text-[11px] sm:text-sm text-muted font-medium leading-tight mt-1 opacity-90">ผู้ป่วยเข้าข่าย<br/>และอาการรุนแรง</p>
                                    </div>
                                    <div class="flex items-center px-1">
                                        <i data-lucide="arrow-right" class="w-5 h-5 sm:w-7 sm:h-7 box-dc-icon opacity-70"></i>
                                    </div>
                                    <div class="flex-1 flex flex-col items-center">
                                        <i data-lucide="megaphone" class="w-7 h-7 sm:w-9 sm:h-9 mb-1 box-dc-icon"></i>
                                        <p class="font-bold text-[13px] sm:text-base text-main leading-tight">สอบสวน & รายงาน</p>
                                        <p class="text-[11px] sm:text-sm text-muted font-medium mt-1 opacity-90">ลงพื้นที่สอบสวนโรค<br/>และรายงาน สสจ.</p>
                                    </div>
                                </div>
                            </div>

                            <!-- 2. Discharge -->
                            <div class="rounded-2xl p-4 sm:p-5 box-discharge shadow-sm flex-1 flex flex-col justify-center relative transition-transform hover:-translate-y-1 bg-white">
                                <h3 class="font-bold text-center mb-3 sm:mb-4 text-sm sm:text-lg box-discharge-title py-1.5 rounded-full mx-2 sm:mx-6 leading-tight">
                                    การจำหน่ายผู้ป่วย (Discharge)
                                </h3>
                                <div class="text-center space-y-2 sm:space-y-3">
                                    <div class="w-12 sm:w-16 h-1 bg-current opacity-30 mx-auto rounded-full" style="color: var(--dis-title-text);"></div>
                                    <p class="text-[11px] sm:text-sm font-bold text-muted leading-relaxed opacity-90">ประสานทีมเยี่ยมบ้าน<br/>ประเมินสภาพที่อยู่อาศัยไม่ให้กำเริบซ้ำ</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Mobile view for return arrow text (Shown only on small screens) -->
                <div id="mobile-return-label" class="lg:hidden text-center mt-8">
                    <div class="inline-flex items-center justify-center bg-white px-6 py-3 rounded-full border-[2px]" style="border-color: var(--line-color);">
                        <p class="font-bold text-sm sm:text-base whitespace-nowrap" style="color: var(--line-color);">
                            การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                        </p>
                    </div>
                </div>

            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                lucide.createIcons();
            });

            // ฟังก์ชันวาดเส้น SVG ข้ามคอลัมน์
            function drawLines(forceDesktop = false) {
                const svg = document.getElementById('flow-svg');
                const container = document.getElementById('main-container');
                const label = document.getElementById('return-label');
                const mobileLabel = document.getElementById('mobile-return-label');
                
                const isDesktop = forceDesktop || window.innerWidth >= 1024;
                
                if (isDesktop && svg && container) { 
                    svg.classList.remove('hidden');
                    if (label) {
                        label.classList.remove('hidden');
                        label.classList.add('flex');
                    }
                    if (mobileLabel) mobileLabel.classList.add('hidden');
                    
                    const contRect = container.getBoundingClientRect();
                    const colL = document.getElementById('col-left').getBoundingClientRect();
                    const colM = document.getElementById('col-mid').getBoundingClientRect();
                    const colR = document.getElementById('col-right').getBoundingClientRect();
                    
                    const getX = (rect) => rect.left - contRect.left;
                    const getY = (rect) => rect.top - contRect.top;
                    
                    // 1. Line Left -> Middle
                    const lmStartY = getY(colL) + (colL.height / 2);
                    const lmStartX = getX(colL) + colL.width;
                    const lmEndX = getX(colM) - 8;
                    document.getElementById('path-lm').setAttribute('d', `M ${lmStartX} ${lmStartY} L ${lmEndX} ${lmStartY}`);
                    
                    // 2. Line Middle -> Right
                    const mrStartY = getY(colM) + (colM.height / 2);
                    const mrStartX = getX(colM) + colM.width;
                    const mrEndX = getX(colR) - 8;
                    document.getElementById('path-mr').setAttribute('d', `M ${mrStartX} ${mrStartY} L ${mrEndX} ${mrStartY}`);
                    
                    // 3. Return Dashed Line (Right -> Left at Bottom)
                    const retStartX = getX(colR) + (colR.width / 2);
                    const retStartY = getY(colR) + colR.height;
                    const retEndX = getX(colL) + (colL.width / 2);
                    const retEndY = getY(colL) + colL.height;
                    
                    const dropY = Math.max(retStartY, retEndY) + 40;
                    
                    const returnPath = `M ${retStartX} ${retStartY} L ${retStartX} ${dropY} L ${retEndX} ${dropY} L ${retEndX} ${retEndY + 15}`;
                    document.getElementById('path-return').setAttribute('d', returnPath);
                    
                    if (label) {
                        label.style.top = `${dropY}px`;
                        label.style.left = `${getX(colM) + (colM.width / 2)}px`;
                        label.style.transform = 'translate(-50%, -50%)';
                    }
                    
                } else {
                    if (svg) svg.classList.add('hidden');
                    if (label) {
                        label.classList.add('hidden');
                        label.classList.remove('flex');
                    }
                    if (mobileLabel) mobileLabel.classList.remove('hidden');
                }
            }

            window.addEventListener('resize', () => drawLines());
            window.addEventListener('load', () => { 
                setTimeout(() => drawLines(), 100); 
                setTimeout(() => drawLines(), 500); 
            });

            // ฟังก์ชันดาวน์โหลดรูป (อัปเกรดความเสถียรเต็มรูปแบบ 100%)
            async function downloadImage() {
                const btn = document.querySelector('button[onclick="downloadImage()"]');
                const originalContent = btn.innerHTML;
                btn.innerHTML = 'กำลังประมวลผล...';
                
                await document.fonts.ready;
                
                const originalScrollY = window.scrollY;
                window.scrollTo(0, 0);
                
                const captureArea = document.getElementById('capture-area');
                const mainContainer = document.getElementById('main-container');
                const mainGrid = document.getElementById('main-grid');
                const innerGrid = document.getElementById('inner-grid');
                const colLeft = document.getElementById('col-left');
                const colMid = document.getElementById('col-mid');
                const colRight = document.getElementById('col-right');
                
                // Backup styles เดิม
                const origCapWidth = captureArea.style.width;
                const origCapMinWidth = captureArea.style.minWidth;
                const origMainMaxWidth = mainContainer.style.maxWidth;
                const origMainWidth = mainContainer.style.width;
                
                // กางพื้นที่แบบ 1920px (Full HD) เพื่อให้มีพื้นที่เหลือเฟือ ไม่ให้ข้อความโดนบีบย่น
                const targetWidth = 1920;
                captureArea.style.width = targetWidth + 'px';
                captureArea.style.minWidth = targetWidth + 'px';
                
                // ปลดล็อคความกว้างสูงสุดของคอนเทนเนอร์หลักชั่วคราว
                mainContainer.style.maxWidth = targetWidth + 'px';
                mainContainer.style.width = targetWidth + 'px';
                
                // ปิดการเรียงตัวแบบมือถือ บังคับคลาสแบบ Desktop เพื่อความชัวร์ (Grid 4 คอลัมน์)
                if (mainGrid) {
                    mainGrid.classList.remove('grid-cols-1', 'lg:grid-cols-4');
                    mainGrid.classList.add('grid-cols-4');
                }
                if (innerGrid) {
                    innerGrid.classList.remove('grid-cols-1', 'xl:grid-cols-2');
                    innerGrid.classList.add('grid-cols-2');
                }
                if (colLeft) { colLeft.classList.remove('lg:col-span-1'); colLeft.classList.add('col-span-1'); }
                if (colMid) { colMid.classList.remove('lg:col-span-2'); colMid.classList.add('col-span-2'); }
                if (colRight) { colRight.classList.remove('lg:col-span-1'); colRight.classList.add('col-span-1'); }
                
                // ปิดการตัดคำ flex wrap เพื่อไม่ให้กล่องย่น
                const flexWraps = document.querySelectorAll('.flex-wrap');
                flexWraps.forEach(el => el.classList.remove('flex-wrap'));
                
                // โชว์ลูกศรทั้งหมดที่ซ่อนอยู่บนมือถือ
                const hiddenArrows = document.querySelectorAll('.hidden.sm\\:block');
                hiddenArrows.forEach(el => {
                    el.classList.remove('hidden', 'sm:block');
                    el.classList.add('block', 'temp-arrow-show');
                });
                
                void captureArea.offsetHeight;
                drawLines(true);
                
                setTimeout(() => {
                    html2canvas(captureArea, {
                        scale: 2, // Scale 2.0 บน 1920px ได้ภาพ 4K คมชัดสุดๆ
                        backgroundColor: "#f8fafc", 
                        useCORS: true, 
                        scrollY: 0, 
                        windowWidth: targetWidth, 
                        windowHeight: captureArea.scrollHeight,
                        logging: false
                    }).then(canvas => {
                        // คืนค่ารูปแบบกลับ
                        captureArea.style.width = origCapWidth;
                        captureArea.style.minWidth = origCapMinWidth;
                        mainContainer.style.maxWidth = origMainMaxWidth;
                        mainContainer.style.width = origMainWidth;
                        
                        if (mainGrid) { mainGrid.classList.remove('grid-cols-4'); mainGrid.classList.add('grid-cols-1', 'lg:grid-cols-4'); }
                        if (innerGrid) { innerGrid.classList.remove('grid-cols-2'); innerGrid.classList.add('grid-cols-1', 'xl:grid-cols-2'); }
                        if (colLeft) { colLeft.classList.remove('col-span-1'); colLeft.classList.add('lg:col-span-1'); }
                        if (colMid) { colMid.classList.remove('col-span-2'); colMid.classList.add('lg:col-span-2'); }
                        if (colRight) { colRight.classList.remove('col-span-1'); colRight.classList.add('lg:col-span-1'); }
                        
                        flexWraps.forEach(el => el.classList.add('flex-wrap'));
                        
                        const tempArrows = document.querySelectorAll('.temp-arrow-show');
                        tempArrows.forEach(el => {
                            el.classList.remove('block', 'temp-arrow-show');
                            el.classList.add('hidden', 'sm:block');
                        });
                        
                        window.scrollTo(0, originalScrollY);
                        drawLines(); 
                        
                        const link = document.createElement('a');
                        link.download = 'PM25_Roles_Sansai_Hospital.png';
                        link.href = canvas.toDataURL('image/png', 1.0);
                        link.click();
                        
                        btn.innerHTML = originalContent;
                    }).catch(err => {
                        console.error("Error generating image:", err);
                        
                        // คืนค่ากลับถ้าพัง
                        captureArea.style.width = origCapWidth;
                        captureArea.style.minWidth = origCapMinWidth;
                        mainContainer.style.maxWidth = origMainMaxWidth;
                        mainContainer.style.width = origMainWidth;
                        
                        if (mainGrid) { mainGrid.classList.remove('grid-cols-4'); mainGrid.classList.add('grid-cols-1', 'lg:grid-cols-4'); }
                        if (innerGrid) { innerGrid.classList.remove('grid-cols-2'); innerGrid.classList.add('grid-cols-1', 'xl:grid-cols-2'); }
                        if (colLeft) { colLeft.classList.remove('col-span-1'); colLeft.classList.add('lg:col-span-1'); }
                        if (colMid) { colMid.classList.remove('col-span-2'); colMid.classList.add('lg:col-span-2'); }
                        if (colRight) { colRight.classList.remove('col-span-1'); colRight.classList.add('lg:col-span-1'); }
                        
                        flexWraps.forEach(el => el.classList.add('flex-wrap'));
                        
                        const tempArrows = document.querySelectorAll('.temp-arrow-show');
                        tempArrows.forEach(el => {
                            el.classList.remove('block', 'temp-arrow-show');
                            el.classList.add('hidden', 'sm:block');
                        });
                        
                        window.scrollTo(0, originalScrollY);
                        drawLines(); 
                        
                        btn.innerHTML = originalContent;
                        alert("เกิดข้อผิดพลาดในการบันทึกรูปภาพ กรุณาลองใหม่อีกครั้ง");
                    });
                }, 300); 
            }
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=1300, scrolling=True)
