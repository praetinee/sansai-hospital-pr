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

            /* เพิ่ม z-index ให้กล่อง เพื่อบังส่วนของเส้นที่อาจทะลุเข้าไป */
            .flow-col { border-width: 3px; border-radius: 2rem; padding: 1.25rem; display: flex; flex-direction: column; gap: 1.25rem; position: relative; height: 100%; transition: all 0.3s; z-index: 10; }
            
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
                .shadow-sm, .shadow-md, .shadow-lg {
                    box-shadow: none !important;
                    border: 1px solid #e2e8f0 !important;
                }
            }
        </style>
    </head>
    <body class="bg-transparent antialiased">
        
        <!-- Wrapper สำหรับแช่แข็งหน้าจอให้กว้าง 1600px เสมอ (เลื่อนและซูมได้แบบรูปภาพ) -->
        <div style="width: 100%; overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch;">
            <div style="min-width: 1600px; width: 1600px; margin: 0 auto; background-color: #f8fafc;">
                
                <!-- พื้นที่สำหรับ Capture (ลบคลาส Responsive ออกทั้งหมด ให้เป็น Desktop ตลอดกาล) -->
                <div id="capture-area" class="w-full min-h-screen pb-10 pt-6 px-12 transition-all duration-300">
                    
                    <!-- Header & Download Button -->
                    <div class="text-center mb-12 relative">
                        <h2 class="text-4xl font-extrabold mb-2 tracking-wide" style="color: var(--text-main);">บทบาทของแต่ละหน่วยงาน</h2>
                        <p class="text-[1.15rem] font-bold text-muted">การดูแลผู้ป่วยที่ได้รับผลกระทบจาก PM 2.5 โรงพยาบาลสันทราย</p>
                        
                        <!-- ปุ่มสำหรับดาวน์โหลดรูปภาพ -->
                        <button onclick="downloadImage()" class="mt-5 inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 px-6 rounded-full shadow-lg transition-all print:hidden" data-html2canvas-ignore="true">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                            ดาวน์โหลดแผนผัง
                        </button>
                    </div>

                    <!-- ขยาย Main Container ให้กว้างพอดี -->
                    <div id="main-container" class="max-w-[1600px] w-full mx-auto relative pb-32 z-10 px-4">
                        
                        <!-- Alert Box -->
                        <div class="flex justify-end mb-6 relative z-20">
                            <div class="px-5 py-2.5 rounded-full font-bold shadow-lg text-sm flex items-center border" style="background-color: var(--alert-bg); color: var(--alert-text); border-color: var(--alert-border);">
                                <span class="mr-2" style="color: var(--alert-hl);">ย้ำ!</span> <span class="baseline-fix-inline">บันทึกรหัสโรค Z58.1 (Exposure to air pollution) ทุกจุดบริการเพื่อวิเคราะห์ข้อมูล</span>
                            </div>
                        </div>

                        <!-- 4 Columns Grid: เปลี่ยนเป็น CSS วาดเส้น 100% และแช่แข็ง 4 คอลัมน์เสมอ -->
                        <div id="main-grid" class="grid grid-cols-4 gap-8 relative z-10 items-stretch">

                            <!-- ================= เส้นเชื่อมแนวนอนด้านล่าง (Return Bridge) ================= -->
                            <div class="flex absolute -bottom-[45px] h-0 border-t-[3px] border-dashed z-0 items-center justify-center pointer-events-none" style="left: calc(12.5% - 1rem); right: calc(12.5% - 1rem); border-color: var(--line-color);">
                                <div class="bg-white px-6 py-2.5 rounded-full border-[2px] shadow-sm z-10 flex items-center justify-center pointer-events-auto" style="border-color: var(--line-color); transform: translateY(-1.5px);">
                                    <p class="font-bold text-[15px] whitespace-nowrap baseline-fix" style="color: var(--line-color);">
                                        การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                                    </p>
                                </div>
                            </div>

                            <!-- ================= Column 1: Left (Community) ================= -->
                            <div id="col-left" class="col-1 flow-col col-span-1 min-w-0">
                                
                                <!-- ลูกศรเชื่อมจาก Column 1 ไป Column 2 (HTML CSS แท้ 100%) -->
                                <div class="block absolute top-1/2 -right-[2rem] w-[2rem] -translate-y-1/2 z-20 pointer-events-none">
                                    <div class="w-full h-0 border-t-[3px] border-dashed" style="border-color: var(--line-color);"></div>
                                    <div class="absolute right-[2px] top-1/2 -translate-y-1/2 w-0 h-0 border-y-[6px] border-l-[8px] border-y-transparent" style="border-left-color: var(--line-color);"></div>
                                </div>

                                <!-- เส้นตั้งดันขึ้นจากด้านล่าง (Return Path) -->
                                <div class="block absolute -bottom-[45px] left-1/2 w-0 h-[45px] border-l-[3px] border-dashed -translate-x-1/2 z-0 pointer-events-none" style="border-color: var(--line-color);">
                                    <div class="absolute -top-[2px] left-1/2 -translate-x-1/2 w-0 h-0 border-x-[6px] border-b-[8px] border-x-transparent" style="border-bottom-color: var(--line-color);"></div>
                                </div>

                                <!-- บังคับบรรทัดเดียว ไม่ให้ตกบรรทัด -->
                                <div class="w-full flex justify-center">
                                    <h2 class="text-[17px] font-extrabold text-center c1-title py-3 px-6 rounded-full shadow-sm whitespace-nowrap w-max min-w-full flex items-center justify-center">
                                        <span class="baseline-fix-inline">ชุมชนและหน่วยบริการปฐมภูมิ (เชิงรุก)</span>
                                    </h2>
                                </div>

                                <div class="flex flex-col items-center text-center py-5 mt-3 bg-white/60 rounded-xl border border-yellow-200 shadow-sm">
                                    <div class="flex justify-center mb-2">
                                        <i data-lucide="users" class="w-12 h-12 c1-icon"></i>
                                    </div>
                                    <h3 class="font-bold text-xl c1-text baseline-fix">กลไก 3 หมอ</h3>
                                </div>
                                <div class="flex-grow space-y-5 mt-2">
                                     <div class="flex items-start gap-4">
                                        <i data-lucide="clipboard-list" class="w-7 h-7 c1-icon shrink-0 mt-1"></i>
                                        <div>
                                            <p class="font-bold text-main text-base baseline-fix">การลงพื้นที่เชิงรุก: อสม. และ รพ.สต.</p>
                                            <p class="text-sm text-muted leading-relaxed font-medium">เคาะประตูบ้านคัดกรองสุขภาพ เน้น 4 กลุ่มเปราะบาง (ติดเตียง/ผู้สูงอายุ/ตั้งครรภ์/เด็กเล็ก)</p>
                                        </div>
                                    </div>
                                    <div class="flex items-start gap-4">
                                        <i data-lucide="shield-check" class="w-7 h-7 c1-icon shrink-0 mt-1"></i>
                                        <div>
                                            <p class="font-bold text-main text-base baseline-fix">สนับสนุนพื้นที่ปลอดฝุ่น:</p>
                                            <p class="text-sm text-muted leading-relaxed font-medium">แจกหน้ากาก N95, จัดทำมุ้งสู้ฝุ่นให้ผู้ป่วยติดเตียง, ห้องปลอดฝุ่นในศูนย์เด็กเล็ก/โรงเรียน</p>
                                        </div>
                                    </div>
                                    <div class="flex items-start gap-4">
                                        <i data-lucide="pill" class="w-7 h-7 c1-icon shrink-0 mt-1"></i>
                                        <div>
                                            <p class="font-bold text-main text-base baseline-fix">สั่งจ่ายยาผ่าน Telemedicine :</p>
                                            <p class="text-sm text-muted leading-relaxed font-medium">ติดตามและสั่งจ่ายยาสำหรับผู้ป่วยอาการคงที่ เพื่อลดความเสี่ยงสัมผัสฝุ่น</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- ================= Column 2: Middle (Clinic & ER) ================= -->
                            <div id="col-mid" class="col-2 flow-col col-span-2 min-w-0">
                                
                                <!-- ลูกศรเชื่อมจาก Column 2 ไป Column 3 (HTML CSS แท้ 100%) -->
                                <div class="block absolute top-1/2 -right-[2rem] w-[2rem] -translate-y-1/2 z-20 pointer-events-none">
                                    <div class="w-full h-0 border-t-[3px] border-dashed" style="border-color: var(--line-color);"></div>
                                    <div class="absolute right-[2px] top-1/2 -translate-y-1/2 w-0 h-0 border-y-[6px] border-l-[8px] border-y-transparent" style="border-left-color: var(--line-color);"></div>
                                </div>

                                <div class="w-full flex justify-center">
                                    <h2 class="text-[17px] font-extrabold text-center c2-title py-3 px-6 rounded-full shadow-sm flex items-center justify-center whitespace-nowrap w-max min-w-[70%]">
                                        <span class="baseline-fix-inline">การรับผู้ป่วยและดูแลรักษา (รับ)</span>
                                    </h2>
                                </div>
                                
                                <!-- แก้ไขพื้นที่ด้วย min-w-0 และปรับอัตราส่วน grid-cols เพื่อไม่ให้ล้น -->
                                <div id="inner-grid" class="grid grid-cols-[1.05fr_0.95fr] gap-4 h-full mt-3 min-w-0">
                                    
                                    <!-- Left Sub-column (4 original rows) -->
                                    <div class="space-y-4 flex flex-col justify-between h-full min-w-0">
                                        
                                        <!-- Row 1: Online -->
                                        <div class="inner-box flex flex-col gap-2 relative border-orange-200 shadow-sm flex-1 p-4 min-w-0">
                                            <div class="flex items-center gap-2 w-full border-b border-orange-100 pb-2">
                                                <i data-lucide="smartphone" class="w-6 h-6 c2-icon shrink-0"></i>
                                                <h3 class="font-bold text-main text-[15px] baseline-fix whitespace-nowrap">ระบบก่อนถึง รพ. และออนไลน์</h3>
                                                
                                                <!-- ป้ายคลินิกมลพิษ -->
                                                <div class="bg-orange-500 text-white text-[12px] px-3 py-1 rounded-full font-bold ml-auto shrink-0 min-w-max shadow-sm flex items-center justify-center">
                                                    <span class="baseline-fix-inline whitespace-nowrap">คลินิกมลพิษ</span>
                                                </div>
                                            </div>
                                            <div class="grid grid-cols-[1fr_auto_1fr] w-full gap-2 items-center h-full min-h-[40px] min-w-0">
                                                <div class="flex flex-col justify-center h-full min-w-0">
                                                    <p class="text-muted font-medium leading-tight text-[12px] truncate">ผ่าน Line OA หรือ หมอพร้อม</p>
                                                </div>
                                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 shrink-0"></i>
                                                <div class="flex flex-col justify-center items-end text-right h-full min-w-0">
                                                    <p class="font-bold c2-text leading-tight baseline-fix text-[13px]">ประเมินเบื้องต้น</p>
                                                    <p class="text-muted font-medium leading-tight mt-1 text-[12px]">& Telemedicine</p>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Row 2: PCU หนองหาร / รพ.สต. -->
                                        <div class="inner-box flex flex-col gap-2 relative border-orange-200 shadow-sm flex-1 p-4 pt-7 min-w-0">
                                            <div class="tag-code"><span class="baseline-fix-inline">รหัส Z58.1</span></div>
                                            <div class="flex items-center gap-2 w-full border-b border-orange-100 pb-2">
                                                <i data-lucide="building-2" class="w-6 h-6 c2-icon shrink-0"></i>
                                                <h3 class="font-bold text-[15px] text-main leading-tight baseline-fix whitespace-nowrap">PCU หนองหาร & รพ.สต.</h3>
                                            </div>
                                            <div class="grid grid-cols-[0.8fr_auto_1.2fr_auto_1fr] w-full gap-2 h-full min-h-[50px] items-center text-[12px] min-w-0">
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                                    <p class="font-bold text-main leading-tight baseline-fix">คัดกรองอาการ</p>
                                                </div>
                                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 shrink-0"></i>
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1 min-w-0">
                                                    <p class="font-bold text-main leading-tight baseline-fix break-words">เข้าข่าย: ลง <a href="https://docs.google.com/spreadsheets/d/1fq34BEtpt6nWbxSupNacky3ZzlV7HymWNW2xv6LyIcA/edit?usp=sharing" target="_blank" class="text-blue-600 hover:text-blue-800 underline relative z-50 whitespace-nowrap" title="คลิกเพื่อกรอกข้อมูล">GG Sheets 🔗</a></p>
                                                    <p class="text-muted font-medium leading-tight mt-1">+ รักษาตามอาการ</p>
                                                </div>
                                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 shrink-0"></i>
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                                    <p class="text-muted font-medium leading-tight baseline-fix">อาการรุนแรง</p>
                                                    <p class="font-bold text-red-600 leading-tight mt-1">Refer รพ.</p>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Row 3: OPD -->
                                        <div class="inner-box flex flex-col gap-2 relative border-orange-200 shadow-sm flex-1 p-4 pt-7 min-w-0">
                                            <div class="tag-code"><span class="baseline-fix-inline">รหัส Z58.1</span></div>
                                            <div class="flex items-center gap-2 w-full border-b border-orange-100 pb-2">
                                                <i data-lucide="eye" class="w-6 h-6 c2-icon shrink-0"></i>
                                                <h3 class="font-bold text-[15px] text-main leading-tight baseline-fix whitespace-nowrap">ผู้ป่วยนอก (OPD)</h3>
                                            </div>
                                            <div class="grid grid-cols-[0.8fr_auto_1.2fr_auto_1fr] w-full gap-2 h-full min-h-[50px] items-center text-[12px] min-w-0">
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                                    <p class="font-bold text-main leading-tight baseline-fix">คัดกรองอาการ</p>
                                                </div>
                                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 shrink-0"></i>
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1 min-w-0">
                                                    <p class="font-bold text-main leading-tight baseline-fix break-words">เข้าข่าย: ลง <a href="https://docs.google.com/spreadsheets/d/1j5xpdB-LNhucSVNhQuqShKUDv-xyWCGB5xhC295J3M4/edit?usp=sharing" target="_blank" class="text-blue-600 hover:text-blue-800 underline relative z-50 whitespace-nowrap" title="คลิกเพื่อกรอกข้อมูล">GG Sheets 🔗</a></p>
                                                    <p class="text-muted font-medium leading-tight mt-1">+ รักษาตามอาการ</p>
                                                </div>
                                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 shrink-0"></i>
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                                    <p class="text-muted font-medium leading-tight baseline-fix">นัดติดตาม ไม่ทุเลา</p>
                                                    <p class="font-bold c2-text leading-tight mt-1 whitespace-nowrap">ส่งคลินิกมลพิษ</p>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Row 4: ER -->
                                        <div class="inner-box flex flex-col gap-2 relative border-orange-200 shadow-sm flex-1 p-4 pt-7 min-w-0">
                                            <div class="tag-code"><span class="baseline-fix-inline">รหัส Z58.1</span></div>
                                            <div class="flex items-center gap-2 w-full border-b border-orange-100 pb-2">
                                                <i data-lucide="ambulance" class="w-6 h-6 text-red-500 shrink-0"></i>
                                                <h3 class="font-bold text-[15px] text-main leading-tight baseline-fix whitespace-nowrap">ผู้ป่วยฉุกเฉิน (ER) & 1669</h3>
                                            </div>
                                            <div class="grid grid-cols-[1fr_auto_0.8fr_auto_1.4fr] w-full gap-2 h-full min-h-[50px] items-center text-[12px] min-w-0">
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1 min-w-0">
                                                    <p class="font-bold text-main leading-tight baseline-fix break-words">อาการรุนแรง</p>
                                                    <p class="text-muted font-medium leading-tight mt-1 truncate">(หอบหืด, COPD..)</p>
                                                </div>
                                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 shrink-0"></i>
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1">
                                                    <p class="font-bold text-main leading-tight baseline-fix">1669 / EMS</p>
                                                    <p class="text-muted font-medium leading-tight mt-1">รับเข้า ER</p>
                                                </div>
                                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 shrink-0"></i>
                                                <div class="flex flex-col justify-center items-center text-center h-full px-1 min-w-0">
                                                    <p class="font-bold text-main leading-tight baseline-fix break-words">เข้าข่าย: ลง <a href="https://docs.google.com/spreadsheets/d/1Ba-5IzHXOzEQziXY7vfdvDXzK0dOZv0VmoINAd-sNxU/edit?usp=drivesdk" target="_blank" class="text-blue-600 hover:text-blue-800 underline relative z-50 whitespace-nowrap" title="คลิกเพื่อกรอกข้อมูล">GG Sheets 🔗</a></p>
                                                    <p class="text-muted font-medium leading-tight mt-1">+ ประเมิน Admit/กลับบ้าน</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Right Sub-column (Pollution Clinic Box) -->
                                    <div class="inner-box border-orange-400 bg-[#fff2e5] p-4 flex flex-col h-full relative shadow-md min-w-0">
                                        
                                        <!-- หัวข้อ "คลินิกมลพิษ" จัดเรียงแบบ Flex ธรรมดา ป้องกันปัญหาตัดคำ 100% -->
                                        <div class="flex items-center justify-center gap-3 border-b-2 border-orange-200 pb-3 mb-5 w-full">
                                            <i data-lucide="stethoscope" class="w-6 h-6 text-orange-600 shrink-0"></i>
                                            <h3 class="font-extrabold text-orange-900 text-lg whitespace-nowrap baseline-fix">
                                                คลินิกมลพิษ
                                            </h3>
                                        </div>

                                        <div class="space-y-5 flex-grow text-[14px] text-main min-w-0">
                                            
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
                                                <ul class="list-disc pl-12 space-y-2 text-muted font-medium break-words">
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
                                                <div class="pl-8 space-y-3 min-w-0">
                                                    
                                                    <!-- กรณีไม่เข้าข่าย -->
                                                    <div class="bg-white p-3 rounded-lg border border-orange-100 shadow-sm flex flex-col justify-center min-h-[60px]">
                                                        <p class="font-bold text-emerald-700 mb-1.5 flex items-center gap-2 baseline-fix">
                                                            <i data-lucide="check-circle-2" class="w-5 h-5 text-emerald-500 shrink-0"></i> กรณีไม่เข้าข่าย / อาการเล็กน้อย
                                                        </p>
                                                        <p class="text-muted font-medium pl-7 border-l-2 border-emerald-300 ml-2.5 leading-tight break-words">
                                                            ให้คำแนะนำ และส่งต่อ <span class="font-bold text-main">ทีม 3 หมอ</span>
                                                        </p>
                                                    </div>
                                                    
                                                    <!-- กรณีเข้าข่าย -->
                                                    <div class="bg-white p-3 rounded-lg border border-orange-100 shadow-sm flex flex-col justify-center min-w-0">
                                                        <p class="font-bold text-red-700 mb-2 flex items-center gap-2 baseline-fix">
                                                            <i data-lucide="alert-circle" class="w-5 h-5 text-red-500 shrink-0"></i> กรณีเข้าข่าย
                                                        </p>
                                                        <ul class="list-disc pl-10 space-y-2 text-muted font-medium ml-1 break-words">
                                                            <li class="baseline-fix">ส่งพบแพทย์ ตรวจ Lab</li>
                                                            <li class="baseline-fix"><span class="text-red-600 font-bold">ส่งห้องฉุกเฉิน (ER)</span> หากอาการรุนแรง</li>
                                                            <li class="leading-snug baseline-fix mt-1">แจ้งข้อมูลผู้ป่วยที่เข้าข่ายแก่งาน<span style="color: #7e22ce; font-weight: 800;">ควบคุมโรค</span> <br/><span class="text-[12px] opacity-80 font-normal">(เพื่อให้ดำเนินการลงพื้นที่ + รายงาน สสจ.)</span></li>
                                                        </ul>
                                                    </div>

                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- ================= Column 3: Right (Control & Discharge) ================= -->
                            <div id="col-right" class="col-3 flow-col col-span-1 min-w-0">

                                <!-- เส้นตั้งทิ้งตัวลงมาด้านล่าง (Return Path) -->
                                <div class="block absolute -bottom-[45px] left-1/2 w-0 h-[45px] border-l-[3px] border-dashed -translate-x-1/2 z-0 pointer-events-none" style="border-color: var(--line-color);"></div>

                                <div class="w-full flex justify-center">
                                    <!-- บังคับบรรทัดเดียว ไม่ให้ตกบรรทัด -->
                                    <h2 class="text-[17px] font-extrabold text-center c3-title py-3 px-6 rounded-full shadow-sm whitespace-nowrap w-max min-w-full flex items-center justify-center">
                                        <span class="baseline-fix-inline">ควบคุมโรคและจำหน่ายผู้ป่วย</span>
                                    </h2>
                                </div>
                                
                                <div class="flex flex-col gap-5 h-full mt-3">
                                    <!-- 1. Disease Control -->
                                    <div class="rounded-2xl p-5 box-dc shadow-sm flex-1 flex flex-col justify-center items-center relative transition-transform hover:-translate-y-1 bg-white">
                                        <h3 class="font-bold text-center mb-5 text-lg box-dc-title py-2 px-6 rounded-full leading-tight baseline-fix w-full">
                                            งานควบคุมโรค<br><span class="text-sm font-normal">(Disease Control)</span>
                                        </h3>
                                        <div class="grid grid-cols-[1fr_auto_1fr] w-full items-center text-center gap-2 h-full">
                                            <div class="flex flex-col items-center justify-center h-full">
                                                <i data-lucide="shield-alert" class="w-10 h-10 mb-2 box-dc-icon"></i>
                                                <p class="font-bold text-[14px] text-main leading-tight baseline-fix">รับแจ้งข้อมูล</p>
                                                <p class="text-[12px] text-muted font-medium leading-tight mt-1 opacity-90">ผู้ป่วยเข้าข่าย<br/>และอาการรุนแรง</p>
                                            </div>
                                            <div class="flex items-center h-full">
                                                <i data-lucide="arrow-right" class="w-7 h-7 box-dc-icon opacity-70"></i>
                                            </div>
                                            <div class="flex flex-col items-center justify-center h-full">
                                                <i data-lucide="megaphone" class="w-10 h-10 mb-2 box-dc-icon"></i>
                                                <p class="font-bold text-[14px] text-main leading-tight baseline-fix">สอบสวน & รายงาน</p>
                                                <p class="text-[12px] text-muted font-medium mt-1 opacity-90">ลงพื้นที่สอบสวนโรค<br/>และรายงาน สสจ.</p>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- 2. Discharge -->
                                    <div class="rounded-2xl p-5 box-discharge shadow-sm flex-1 flex flex-col justify-center relative transition-transform hover:-translate-y-1 bg-white">
                                        <h3 class="font-bold text-center mb-5 text-lg box-discharge-title py-2 px-6 rounded-full leading-tight baseline-fix w-full">
                                            การจำหน่ายผู้ป่วย<br><span class="text-sm font-normal">(Discharge)</span>
                                        </h3>
                                        <div class="text-center space-y-3 flex flex-col justify-center items-center h-full">
                                            <div class="w-16 h-1 bg-current opacity-30 mx-auto rounded-full mb-2" style="color: var(--dis-title-text);"></div>
                                            <p class="text-[13px] font-bold text-muted leading-relaxed opacity-90 baseline-fix">ประสานทีมเยี่ยมบ้าน<br/>ประเมินสภาพที่อยู่อาศัยไม่ให้กำเริบซ้ำ</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                lucide.createIcons();
            });

            // ปล่อยให้ CSS จัดการวาดเส้นทั้งหมด 100% ไม่ต้องใช้ JS คำนวณแกน X Y อีกต่อไป!
            
            async function downloadImage() {
                const btn = document.querySelector('button[onclick="downloadImage()"]');
                const originalContent = btn.innerHTML;
                btn.innerHTML = 'กำลังประมวลผล...';
                
                await document.fonts.ready;
                
                // ใส่ Loading บังตาไว้กันหน้าจอกระตุกตอนกางเป็น 1600px
                const overlay = document.createElement('div');
                overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:#f8fafc;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;';
                overlay.innerHTML = `
                    <div style="font-family: 'Sarabun', sans-serif; text-align: center;">
                        <svg class="animate-spin mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                        <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b;">กำลังสร้างรูปภาพ...</h2>
                        <p style="color: #64748b; margin-top: 0.5rem;">จัดเตรียมแผนผังให้สมบูรณ์</p>
                    </div>
                `;
                document.body.appendChild(overlay);

                const captureArea = document.getElementById('capture-area');
                const origWidth = captureArea.style.width;
                const origMinWidth = captureArea.style.minWidth;
                const originalScrollY = window.scrollY;
                
                // บังคับกางเป็น 1600px
                captureArea.style.width = '1600px';
                captureArea.style.minWidth = '1600px';
                
                // ฉีด CSS บังคับโครงสร้าง Grid + บังคับเปิดเส้นลูกศรทั้งหมดของ CSS
                const forceStyle = document.createElement('style');
                forceStyle.id = 'force-desktop-style';
                forceStyle.innerHTML = `
                    #main-grid { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; }
                    #col-left { grid-column: span 1 / span 1 !important; }
                    #col-mid { grid-column: span 2 / span 2 !important; }
                    #col-right { grid-column: span 1 / span 1 !important; }
                    
                    /* บังคับโชว์ลูกศร CSS ทันทีเมื่อถูกสั่งพิมพ์ แม้หน้าจอจริงจะย่ออยู่ก็ตาม */
                    .lg\\:block { display: block !important; }
                    .lg\\:flex { display: flex !important; }
                    .lg\\:hidden { display: none !important; }
                `;
                document.head.appendChild(forceStyle);
                
                window.scrollTo(0, 0);

                // รอให้ CSS โหลดเสร็จ แล้วกดถ่ายรูปได้เลย!
                setTimeout(() => {
                    html2canvas(captureArea, {
                        scale: 2, 
                        backgroundColor: "#f8fafc", 
                        useCORS: true, 
                        scrollY: 0, 
                        windowWidth: 1600,
                        logging: false
                    }).then(canvas => {
                        cleanUpAndRestore();
                        const link = document.createElement('a');
                        link.download = 'PM25_Roles_Sansai_Hospital.png';
                        link.href = canvas.toDataURL('image/png', 1.0);
                        link.click();
                    }).catch(err => {
                        console.error("Error generating image:", err);
                        cleanUpAndRestore();
                        alert("เกิดข้อผิดพลาดในการบันทึกรูปภาพ กรุณาลองใหม่อีกครั้ง");
                    });
                }, 300);
                
                function cleanUpAndRestore() {
                    document.head.removeChild(forceStyle);
                    captureArea.style.width = origWidth;
                    captureArea.style.minWidth = origMinWidth;
                    document.body.removeChild(overlay);
                    window.scrollTo(0, originalScrollY);
                    btn.innerHTML = originalContent;
                }
            }
        </script>
    </body>
    </html>
    """
    
    # ปรับความสูงของ Iframe ให้พอดี ไม่เหลือขอบขาวด้านล่างมากเกินไป
    components.html(html_code, height=1350, scrolling=True)
