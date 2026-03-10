import streamlit.components.v1 as components

def render_roles():
    html_code = """
    <!DOCTYPE html>
    <html lang="th" style="background: transparent;">
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
            
            .tag-code { position: absolute; top: 0.5rem; right: 0.5rem; background-color: var(--alert-bg); color: var(--alert-text); font-size: 0.7rem; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 700; z-index: 10; border: 1px solid var(--alert-border); box-shadow: 0 2px 4px rgba(0,0,0,0.15); letter-spacing: 0.025em; white-space: nowrap; }
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
               THAI FONT BASELINE FIX
               ======================================= */
            .baseline-fix {
                position: relative !important;
                top: -2px !important;
                display: block;
            }
            .baseline-fix-inline {
                position: relative !important;
                top: -2px !important;
                display: inline-block;
            }

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
    <body class="bg-transparent antialiased">
        
        <!-- พื้นที่สำหรับ Capture (เติม min-h-screen เพื่อความยืดหยุ่นหน้าจอ) -->
        <div id="capture-area" class="w-full min-h-screen bg-slate-50 pb-10 pt-6 px-4 sm:px-8 lg:px-12 transition-all duration-300">
            
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

            <!-- ขยาย Main Container ให้เป็น 1600px เพื่อไม่ให้กรอบบีบตัวหนังสือ -->
            <div id="main-container" class="max-w-[1600px] w-full mx-auto relative pb-40 sm:pb-48 lg:pb-56 z-10 px-2 sm:px-4">
                
                <!-- Alert Box -->
                <div class="flex justify-end mb-6 relative z-20">
                    <div class="px-5 py-2.5 rounded-full font-bold shadow-lg text-xs sm:text-sm flex items-center border" style="background-color: var(--alert-bg); color: var(--alert-text); border-color: var(--alert-border);">
                        <span class="mr-2" style="color: var(--alert-hl);">ย้ำ!</span> <span class="baseline-fix-inline">บันทึกรหัสโรค Z58.1 (Exposure to air pollution) ทุกจุดบริการเพื่อวิเคราะห์ข้อมูล</span>
                    </div>
                </div>

                <!-- SVG Overlay for Dynamic Line Drawing -->
                <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden z-0" style="overflow: visible;">
                    <path id="path-lm" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" stroke-linecap="round" stroke-linejoin="round" />
                    <path id="path-mr" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" stroke-linecap="round" stroke-linejoin="round" />
                    <path id="path-return" fill="none" stroke="var(--line-color)" stroke-width="3" stroke-dasharray="6,5" stroke-linecap="round" stroke-linejoin="round" />
                </svg>

                <!-- Return Label -->
                <div id="return-label" class="absolute hidden items-center justify-center bg-white px-8 py-2.5 rounded-full z-10 border-[2px] shadow-sm" style="border-color: var(--line-color);">
                    <p class="font-bold text-base whitespace-nowrap text-main baseline-fix" style="color: var(--line-color);">
                        การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                    </p>
                </div>

                <!-- 4 Columns Grid (ขยายสัดส่วนอัตโนมัติตามเนื้อหา) -->
                <div id="main-grid" class="grid grid-cols-1 lg:grid-cols-4 gap-6 sm:gap-8 relative z-10 items-stretch">

                    <!-- ================= Column 1: Left (Community) ================= -->
                    <div id="col-left" class="col-1 flow-col lg:col-span-1">
                        <!-- บังคับบรรทัดเดียว ไม่ให้ตกบรรทัด -->
                        <div class="w-full flex justify-center">
                            <h2 class="text-[15px] sm:text-base lg:text-[17px] font-extrabold text-center c1-title py-3 px-6 rounded-full shadow-sm whitespace-nowrap w-max min-w-full flex items-center justify-center">
                                <span class="baseline-fix-inline">ชุมชนและหน่วยบริการปฐมภูมิ (เชิงรุก)</span>
                            </h2>
                        </div>

                        <div class="flex flex-col items-center text-center py-5 mt-3 bg-white/60 rounded-xl border border-yellow-200 shadow-sm">
                            <div class="flex justify-center mb-2">
                                <i data-lucide="users" class="w-10 h-10 sm:w-12 sm:h-12 c1-icon"></i>
                            </div>
                            <h3 class="font-bold text-lg sm:text-xl c1-text baseline-fix">กลไก 3 หมอ</h3>
                        </div>
                        <div class="flex-grow space-y-4 sm:space-y-5 mt-2">
                             <div class="flex items-start gap-3 sm:gap-4">
                                <i data-lucide="clipboard-list" class="w-6 h-6 sm:w-7 sm:h-7 c1-icon shrink-0 mt-1"></i>
                                <div>
                                    <p class="font-bold text-main text-sm sm:text-base baseline-fix">การลงพื้นที่เชิงรุก: อสม. และ รพ.สต.</p>
                                    <p class="text-xs sm:text-sm text-muted leading-relaxed font-medium">เคาะประตูบ้านคัดกรองสุขภาพ เน้น 4 กลุ่มเปราะบาง (ติดเตียง/ผู้สูงอายุ/ตั้งครรภ์/เด็กเล็ก)</p>
                                </div>
                            </div>
                            <div class="flex items-start gap-3 sm:gap-4">
                                <i data-lucide="shield-check" class="w-6 h-6 sm:w-7 sm:h-7 c1-icon shrink-0 mt-1"></i>
                                <div>
                                    <p class="font-bold text-main text-sm sm:text-base baseline-fix">สนับสนุนพื้นที่ปลอดฝุ่น:</p>
                                    <p class="text-xs sm:text-sm text-muted leading-relaxed font-medium">แจกหน้ากาก N95, จัดทำมุ้งสู้ฝุ่นให้ผู้ป่วยติดเตียง, ห้องปลอดฝุ่นในศูนย์เด็กเล็ก/โรงเรียน</p>
                                </div>
                            </div>
                            <div class="flex items-start gap-3 sm:gap-4">
                                <i data-lucide="pill" class="w-6 h-6 sm:w-7 sm:h-7 c1-icon shrink-0 mt-1"></i>
                                <div>
                                    <p class="font-bold text-main text-sm sm:text-base baseline-fix">สั่งจ่ายยาผ่าน Telemedicine :</p>
                                    <p class="text-xs sm:text-sm text-muted leading-relaxed font-medium">ติดตามและสั่งจ่ายยาสำหรับผู้ป่วยอาการคงที่ เพื่อลดความเสี่ยงสัมผัสฝุ่น</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- ================= Column 2: Middle (Clinic & ER) ================= -->
                    <div id="col-mid" class="col-2 flow-col lg:col-span-2">
                        <div class="w-full flex justify-center">
                            <h2 class="text-[15px] sm:text-base lg:text-[17px] font-extrabold text-center c2-title py-3 px-6 rounded-full shadow-sm flex items-center justify-center whitespace-nowrap w-max min-w-[70%]">
                                <span class="baseline-fix-inline">การรับผู้ป่วยและดูแลรักษา (รับ)</span>
                            </h2>
                        </div>
                        
                        <div id="inner-grid" class="grid grid-cols-1 xl:grid-cols-2 gap-5 h-full mt-3">
                            
                            <!-- Left Sub-column (4 original rows) -->
                            <div class="space-y-4 flex flex-col justify-between h-full">
                                
                                <!-- Row 1: Online -->
                                <div class="inner-box flex flex-col gap-2 relative border-orange-200 shadow-sm flex-1 p-3 sm:p-4">
                                    <div class="flex items-center gap-2 w-full border-b border-orange-100 pb-2">
                                        <i data-lucide="smartphone" class="w-5 h-5 sm:w-6 sm:h-6 c2-icon shrink-0"></i>
                                        <h3 class="font-bold text-main text-[14px] sm:text-[15px] baseline-fix whitespace-nowrap">ระบบก่อนถึง รพ. และออนไลน์</h3>
                                        
                                        <!-- ป้ายคลินิกมลพิษ: ล็อกขนาด ห้ามหด ห้ามตัดคำ -->
                                        <div class="bg-orange-500 text-white text-[11px] px-3 py-1 rounded-full font-bold ml-auto shrink-0 min-w-max shadow-sm flex items-center justify-center">
                                            <span class="baseline-fix-inline whitespace-nowrap">คลินิกมลพิษ</span>
                                        </div>
                                    </div>
                                    <div class="grid grid-cols-[1fr_auto_1fr] w-full gap-2 items-center h-full min-h-[40px]">
                                        <div class="flex flex-col justify-center h-full">
                                            <p class="text-muted font-medium leading-tight text-[11px] sm:text-[12px]">ผ่าน Line OA หรือ หมอพร้อม</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 shrink-0"></i>
                                        <div class="flex flex-col justify-center items-end text-right h-full">
                                            <p class="font-bold c2-text leading-tight baseline-fix text-[12px] sm:text-[13px]">ประเมินเบื้องต้น</p>
                                            <p class="text-muted font-medium leading-tight mt-1 text-[11px] sm:text-[12px]">& Telemedicine</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Row 2: PCU หนองหาร / รพ.สต. -->
                                <div class="inner-box flex flex-col gap-2 relative border-orange-200 shadow-sm flex-1 p-3 sm:p-4 pt-7">
                                    <div class="tag-code"><span class="baseline-fix-inline">รหัส Z58.1</span></div>
                                    <div class="flex items-center gap-2 w-full border-b border-orange-100 pb-2">
                                        <i data-lucide="building-2" class="w-5 h-5 sm:w-6 sm:h-6 c2-icon shrink-0"></i>
                                        <h3 class="font-bold text-[14px] sm:text-[15px] text-main leading-tight baseline-fix whitespace-nowrap">PCU หนองหาร & รพ.สต.</h3>
                                    </div>
                                    <!-- ใช้ CSS Grid แบบแข็งแรง แบ่งสัดส่วนคอลัมน์ชัดเจน -->
                                    <div class="grid grid-cols-[1fr_auto_1.4fr_auto_0.8fr] w-full gap-1 sm:gap-2 h-full min-h-[50px] items-center text-[11px] sm:text-[12px]">
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="font-bold text-main leading-tight baseline-fix">คัดกรองอาการ</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-3 h-3 sm:w-4 sm:h-4 shrink-0"></i>
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="font-bold text-main leading-tight baseline-fix">เข้าข่าย: ลง GG Sheets</p>
                                            <p class="text-muted font-medium leading-tight mt-1">+ รักษาตามอาการ</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-3 h-3 sm:w-4 sm:h-4 shrink-0"></i>
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="text-muted font-medium leading-tight baseline-fix">อาการรุนแรง</p>
                                            <p class="font-bold text-red-600 leading-tight mt-1">Refer รพ.</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Row 3: OPD -->
                                <div class="inner-box flex flex-col gap-2 relative border-orange-200 shadow-sm flex-1 p-3 sm:p-4 pt-7">
                                    <div class="tag-code"><span class="baseline-fix-inline">รหัส Z58.1</span></div>
                                    <div class="flex items-center gap-2 w-full border-b border-orange-100 pb-2">
                                        <i data-lucide="eye" class="w-5 h-5 sm:w-6 sm:h-6 c2-icon shrink-0"></i>
                                        <h3 class="font-bold text-[14px] sm:text-[15px] text-main leading-tight baseline-fix whitespace-nowrap">ผู้ป่วยนอก (OPD)</h3>
                                    </div>
                                    <div class="grid grid-cols-[0.8fr_auto_1.4fr_auto_1fr] w-full gap-1 sm:gap-2 h-full min-h-[50px] items-center text-[11px] sm:text-[12px]">
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="font-bold text-main leading-tight baseline-fix">คัดกรองอาการ</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-3 h-3 sm:w-4 sm:h-4 shrink-0"></i>
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="font-bold text-main leading-tight baseline-fix">เข้าข่าย: ลง GG Sheets</p>
                                            <p class="text-muted font-medium leading-tight mt-1">+ รักษาตามอาการ</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-3 h-3 sm:w-4 sm:h-4 shrink-0"></i>
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="text-muted font-medium leading-tight baseline-fix">นัดติดตาม ไม่ทุเลา</p>
                                            <p class="font-bold c2-text leading-tight mt-1 whitespace-nowrap">ส่งคลินิกมลพิษ</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Row 4: ER -->
                                <div class="inner-box flex flex-col gap-2 relative border-orange-200 shadow-sm flex-1 p-3 sm:p-4 pt-7">
                                    <div class="tag-code"><span class="baseline-fix-inline">รหัส Z58.1</span></div>
                                    <div class="flex items-center gap-2 w-full border-b border-orange-100 pb-2">
                                        <i data-lucide="ambulance" class="w-5 h-5 sm:w-6 sm:h-6 text-red-500 shrink-0"></i>
                                        <h3 class="font-bold text-[14px] sm:text-[15px] text-main leading-tight baseline-fix whitespace-nowrap">ผู้ป่วยฉุกเฉิน (ER) & 1669</h3>
                                    </div>
                                    <div class="grid grid-cols-[1fr_auto_0.8fr_auto_1.4fr] w-full gap-1 sm:gap-2 h-full min-h-[50px] items-center text-[11px] sm:text-[12px]">
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="font-bold text-main leading-tight baseline-fix">อาการรุนแรง</p>
                                            <p class="text-muted font-medium leading-tight mt-1 whitespace-nowrap">(หอบหืด, COPD..)</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-3 h-3 sm:w-4 sm:h-4 shrink-0"></i>
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="font-bold text-main leading-tight baseline-fix">1669 / EMS</p>
                                            <p class="text-muted font-medium leading-tight mt-1">รับเข้า ER</p>
                                        </div>
                                        <i data-lucide="arrow-right" class="arrow-icon w-3 h-3 sm:w-4 sm:h-4 shrink-0"></i>
                                        <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                            <p class="font-bold text-main leading-tight baseline-fix">เข้าข่าย: ลง GG Sheets</p>
                                            <p class="text-muted font-medium leading-tight mt-1">+ ประเมิน Admit/กลับบ้าน</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Right Sub-column (Pollution Clinic Box) -->
                            <div class="inner-box border-orange-400 bg-[#fff2e5] p-5 flex flex-col h-full relative shadow-md">
                                
                                <!-- หัวข้อ "คลินิกมลพิษ" จัดเรียงแบบ Flex ธรรมดา ป้องกันปัญหาตัดคำ 100% -->
                                <div class="flex items-center justify-center gap-3 border-b-2 border-orange-200 pb-3 mb-5 w-full">
                                    <i data-lucide="stethoscope" class="w-6 h-6 text-orange-600 shrink-0"></i>
                                    <h3 class="font-extrabold text-orange-900 text-base sm:text-lg whitespace-nowrap baseline-fix">
                                        คลินิกมลพิษ
                                    </h3>
                                </div>

                                <div class="space-y-5 flex-grow text-[13px] sm:text-[14px] text-main">
                                    
                                    <!-- 1. จัดการนัดหมาย -->
                                    <div>
                                        <div class="font-bold text-orange-800 flex items-start gap-2 mb-2">
                                            <div class="bg-orange-200 rounded-full shrink-0 shadow-inner flex items-center justify-center" style="width: 22px; height: 22px; min-width: 22px;">
                                                <span class="text-[12px] text-[#9a3412] leading-none baseline-fix-inline font-black">1</span>
                                            </div>
                                            <span class="baseline-fix-inline mt-[2px]">จัดการนัดหมาย</span>
                                        </div>
                                        <p class="pl-8 text-muted font-medium">(หมอพร้อม/Telemedicine/Walk-in)</p>
                                    </div>

                                    <!-- 2. เฝ้าระวัง -->
                                    <div>
                                        <div class="font-bold text-orange-800 flex items-start gap-2 mb-2">
                                            <div class="bg-orange-200 rounded-full shrink-0 shadow-inner flex items-center justify-center" style="width: 22px; height: 22px; min-width: 22px;">
                                                <span class="text-[12px] text-[#9a3412] leading-none baseline-fix-inline font-black">2</span>
                                            </div>
                                            <span class="baseline-fix-inline mt-[2px]">เฝ้าระวัง (การเข้ารับการรักษาของผู้ป่วย)</span>
                                        </div>
                                        <ul class="list-disc pl-12 space-y-2 text-muted font-medium">
                                            <li>ตรวจสอบรหัส ICD-10 ที่เกี่ยวข้องกับการสัมผัส PM2.5 ในระบบ HosOS</li>
                                            <li>ตรวจสอบผู้ป่วยที่เข้ารับการรักษาในวันที่ฝุ่นสูง (> 37.5) GG sheets ของ OPD/ER/PCU หนองหาร</li>
                                        </ul>
                                    </div>

                                    <!-- 3. คัดกรอง ซักประวัติ -->
                                    <div>
                                        <div class="font-bold text-orange-800 flex items-start gap-2 mb-3">
                                            <div class="bg-orange-200 rounded-full shrink-0 shadow-inner flex items-center justify-center" style="width: 22px; height: 22px; min-width: 22px;">
                                                <span class="text-[12px] text-[#9a3412] leading-none baseline-fix-inline font-black">3</span>
                                            </div>
                                            <span class="baseline-fix-inline mt-[2px]">คัดกรอง ซักประวัติ สอบสวนโรค</span>
                                        </div>
                                        <div class="pl-8 space-y-3">
                                            
                                            <!-- กรณีไม่เข้าข่าย -->
                                            <div class="bg-white p-3 rounded-lg border border-orange-100 shadow-sm flex flex-col justify-center min-h-[60px]">
                                                <p class="font-bold text-emerald-700 mb-1.5 flex items-center gap-2 baseline-fix">
                                                    <i data-lucide="check-circle-2" class="w-5 h-5 text-emerald-500 shrink-0"></i> กรณีไม่เข้าข่าย / อาการเล็กน้อย
                                                </p>
                                                <p class="text-muted font-medium pl-7 border-l-2 border-emerald-300 ml-2.5 leading-tight">
                                                    ให้คำแนะนำ และส่งต่อ <span class="font-bold text-main">ทีม 3 หมอ</span>
                                                </p>
                                            </div>
                                            
                                            <!-- กรณีเข้าข่าย -->
                                            <div class="bg-white p-3 rounded-lg border border-orange-100 shadow-sm flex flex-col justify-center">
                                                <p class="font-bold text-red-700 mb-2 flex items-center gap-2 baseline-fix">
                                                    <i data-lucide="alert-circle" class="w-5 h-5 text-red-500 shrink-0"></i> กรณีเข้าข่าย
                                                </p>
                                                <ul class="list-disc pl-10 space-y-2 text-muted font-medium ml-1">
                                                    <li class="baseline-fix">ส่งพบแพทย์ ตรวจ Lab</li>
                                                    <li class="baseline-fix"><span class="text-red-600 font-bold">ส่งห้องฉุกเฉิน (ER)</span> หากอาการรุนแรง</li>
                                                    <li class="leading-snug baseline-fix mt-1">แจ้งข้อมูลผู้ป่วยที่เข้าข่ายแก่งาน<span style="color: #7e22ce; font-weight: 800;">ควบคุมโรค</span> <br/><span class="text-[11px] sm:text-[12px] opacity-80 font-normal">(เพื่อให้ดำเนินการลงพื้นที่ + รายงาน สสจ.)</span></li>
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
                        <div class="w-full flex justify-center">
                            <!-- บังคับบรรทัดเดียว ไม่ให้ตกบรรทัด -->
                            <h2 class="text-[15px] sm:text-base lg:text-[17px] font-extrabold text-center c3-title py-3 px-6 rounded-full shadow-sm whitespace-nowrap w-max min-w-full flex items-center justify-center">
                                <span class="baseline-fix-inline">ควบคุมโรคและจำหน่ายผู้ป่วย</span>
                            </h2>
                        </div>
                        
                        <div class="flex flex-col gap-5 h-full mt-3">
                            <!-- 1. Disease Control -->
                            <div class="rounded-2xl p-5 box-dc shadow-sm flex-1 flex flex-col justify-center items-center relative transition-transform hover:-translate-y-1 bg-white">
                                <h3 class="font-bold text-center mb-5 text-[15px] sm:text-lg box-dc-title py-2 px-6 rounded-full leading-tight baseline-fix w-full">
                                    งานควบคุมโรค<br><span class="text-xs sm:text-sm font-normal">(Disease Control)</span>
                                </h3>
                                <div class="grid grid-cols-[1fr_auto_1fr] w-full items-center text-center gap-2 h-full">
                                    <div class="flex flex-col items-center justify-center h-full">
                                        <i data-lucide="shield-alert" class="w-8 h-8 sm:w-10 sm:h-10 mb-2 box-dc-icon"></i>
                                        <p class="font-bold text-[13px] sm:text-[14px] text-main leading-tight baseline-fix">รับแจ้งข้อมูล</p>
                                        <p class="text-[11px] sm:text-[12px] text-muted font-medium leading-tight mt-1 opacity-90">ผู้ป่วยเข้าข่าย<br/>และอาการรุนแรง</p>
                                    </div>
                                    <div class="flex items-center h-full">
                                        <i data-lucide="arrow-right" class="w-5 h-5 sm:w-7 sm:h-7 box-dc-icon opacity-70"></i>
                                    </div>
                                    <div class="flex flex-col items-center justify-center h-full">
                                        <i data-lucide="megaphone" class="w-8 h-8 sm:w-10 sm:h-10 mb-2 box-dc-icon"></i>
                                        <p class="font-bold text-[13px] sm:text-[14px] text-main leading-tight baseline-fix">สอบสวน & รายงาน</p>
                                        <p class="text-[11px] sm:text-[12px] text-muted font-medium mt-1 opacity-90">ลงพื้นที่สอบสวนโรค<br/>และรายงาน สสจ.</p>
                                    </div>
                                </div>
                            </div>

                            <!-- 2. Discharge -->
                            <div class="rounded-2xl p-5 box-discharge shadow-sm flex-1 flex flex-col justify-center relative transition-transform hover:-translate-y-1 bg-white">
                                <h3 class="font-bold text-center mb-5 text-[15px] sm:text-lg box-discharge-title py-2 px-6 rounded-full leading-tight baseline-fix w-full">
                                    การจำหน่ายผู้ป่วย<br><span class="text-xs sm:text-sm font-normal">(Discharge)</span>
                                </h3>
                                <div class="text-center space-y-3 flex flex-col justify-center items-center h-full">
                                    <div class="w-16 h-1 bg-current opacity-30 mx-auto rounded-full mb-2" style="color: var(--dis-title-text);"></div>
                                    <p class="text-[12px] sm:text-[13px] font-bold text-muted leading-relaxed opacity-90 baseline-fix">ประสานทีมเยี่ยมบ้าน<br/>ประเมินสภาพที่อยู่อาศัยไม่ให้กำเริบซ้ำ</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Mobile view for return arrow text -->
                <div id="mobile-return-label" class="lg:hidden text-center mt-10">
                    <div class="inline-flex items-center justify-center bg-white px-6 py-3 rounded-full border-[2px]" style="border-color: var(--line-color);">
                        <p class="font-bold text-sm sm:text-base whitespace-nowrap baseline-fix" style="color: var(--line-color);">
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
                    const pathLM = `M ${lmStartX} ${lmStartY} L ${lmEndX} ${lmStartY} L ${lmEndX-8} ${lmStartY-6} M ${lmEndX} ${lmStartY} L ${lmEndX-8} ${lmStartY+6}`;
                    document.getElementById('path-lm').setAttribute('d', pathLM);
                    
                    // 2. Line Middle -> Right
                    const mrStartY = getY(colM) + (colM.height / 2);
                    const mrStartX = getX(colM) + colM.width;
                    const mrEndX = getX(colR) - 8;
                    const pathMR = `M ${mrStartX} ${mrStartY} L ${mrEndX} ${mrStartY} L ${mrEndX-8} ${mrStartY-6} M ${mrEndX} ${mrStartY} L ${mrEndX-8} ${mrStartY+6}`;
                    document.getElementById('path-mr').setAttribute('d', pathMR);
                    
                    // 3. Return Dashed Line
                    const retStartX = getX(colR) + (colR.width / 2);
                    const retStartY = getY(colR) + colR.height;
                    const retEndX = getX(colL) + (colL.width / 2);
                    const retEndY = getY(colL) + colL.height;
                    
                    const maxBottom = Math.max(
                        getY(colL) + colL.height,
                        getY(colM) + colM.height,
                        getY(colR) + colR.height
                    );
                    
                    const dropY = maxBottom + 140; 
                    const rTipY = retEndY + 15;
                    const pathReturn = `M ${retStartX} ${retStartY} L ${retStartX} ${dropY} L ${retEndX} ${dropY} L ${retEndX} ${rTipY} L ${retEndX-6} ${rTipY+8} M ${retEndX} ${rTipY} L ${retEndX+6} ${rTipY+8}`;
                    document.getElementById('path-return').setAttribute('d', pathReturn);
                    
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

            async function downloadImage() {
                const btn = document.querySelector('button[onclick="downloadImage()"]');
                const originalContent = btn.innerHTML;
                btn.innerHTML = 'กำลังประมวลผล...';
                
                await document.fonts.ready;
                
                const originalScrollY = window.scrollY;
                window.scrollTo(0, 0);
                
                const captureArea = document.getElementById('capture-area');
                
                const origCapWidth = captureArea.style.width;
                const origCapMinWidth = captureArea.style.minWidth;
                
                // กางพื้นที่ให้เต็มสัดส่วน Desktop กว้างสุดๆ (1800px) เพื่อไม่ให้กรอบบีบ
                const targetWidth = 1800;
                captureArea.style.width = targetWidth + 'px';
                captureArea.style.minWidth = targetWidth + 'px';
                
                void captureArea.offsetHeight;
                
                setTimeout(() => {
                    drawLines(true);
                }, 100);
                
                setTimeout(() => {
                    html2canvas(captureArea, {
                        scale: 2, // สเกล 2 + กว้าง 1800px = ภาพระดับ 4K โคตรชัด
                        backgroundColor: "#f8fafc", 
                        useCORS: true, 
                        scrollY: 0, 
                        windowWidth: targetWidth, 
                        windowHeight: captureArea.scrollHeight,
                        logging: false
                    }).then(canvas => {
                        captureArea.style.width = origCapWidth;
                        captureArea.style.minWidth = origCapMinWidth;
                        window.scrollTo(0, originalScrollY);
                        drawLines(); 
                        
                        const link = document.createElement('a');
                        link.download = 'PM25_Roles_Sansai_Hospital.png';
                        link.href = canvas.toDataURL('image/png', 1.0);
                        link.click();
                        
                        btn.innerHTML = originalContent;
                    }).catch(err => {
                        console.error("Error generating image:", err);
                        captureArea.style.width = origCapWidth;
                        captureArea.style.minWidth = origCapMinWidth;
                        window.scrollTo(0, originalScrollY);
                        drawLines(); 
                        btn.innerHTML = originalContent;
                        alert("เกิดข้อผิดพลาดในการบันทึกรูปภาพ กรุณาลองใหม่อีกครั้ง");
                    });
                }, 600); 
            }
        </script>
    </body>
    </html>
    """
    
    # เพิ่มความสูงขึ้นให้สัมพันธ์กับหน้าจอ
    components.html(html_code, height=1550, scrolling=True)
