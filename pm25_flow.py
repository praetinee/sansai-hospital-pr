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
               ========================================= */
            :root {
                --text-main: #020617; 
                --text-muted: #1e293b; 
                --bg-card: #ffffff;
                --border-card: #cbd5e1;
                --shadow-box: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);

                /* Column 1 (Amber/Community) */
                --c1-bg: #fffbeb; --c1-border: #f59e0b; 
                --c1-title-bg: #fef3c7; --c1-title-text: #78350f; 
                --c1-icon: #b45309; 

                /* Column 2 (Orange/Clinic) */
                --c2-bg: #fff7ed; --c2-border: #f97316; 
                --c2-title-bg: #ffedd5; --c2-title-text: #7c2d12; 
                --c2-icon: #c2410c; 

                /* Column 3 (Emerald/Refer) */
                --c3-bg: #ecfdf5; --c3-border: #10b981; 
                --c3-title-bg: #d1fae5; --c3-title-text: #064e3b; 
                --c3-icon: #047857; 

                /* Inner Boxes in Col 3 */
                --ref-bg: #fef2f2; --ref-border: #ef4444; 
                --ref-title-bg: #fee2e2; --ref-title-text: #7f1d1d; 
                
                /* NEW: Disease Control (Purple) */
                --dc-bg: #faf5ff; --dc-border: #d8b4fe;
                --dc-title-bg: #f3e8ff; --dc-title-text: #581c87;
                --dc-icon: #7e22ce;

                --dis-bg: #ecfdf5; --dis-border: #10b981; 
                --dis-title-bg: #d1fae5; --dis-title-text: #064e3b; 

                /* Alert & Tags */
                --alert-bg: #0f766e; --alert-border: #115e59; 
                --alert-text: #ffffff; --alert-hl: #fde047;
                
                /* Connecting Lines */
                --svg-line: #3b82f6; 
                --svg-return: #0ea5e9; 
            }

            @media (prefers-color-scheme: dark) {
                :root {
                    --text-main: #ffffff; 
                    --text-muted: #f1f5f9; 
                    --bg-card: #1e293b;
                    --border-card: #475569;
                    --shadow-box: 0 4px 6px -1px rgba(0,0,0,0.3), 0 2px 4px -1px rgba(0,0,0,0.2);

                    /* Column 1 */
                    --c1-bg: rgba(217, 119, 6, 0.12); --c1-border: rgba(245, 158, 11, 0.7); 
                    --c1-title-bg: rgba(217, 119, 6, 0.3); --c1-title-text: #fef3c7; 
                    --c1-icon: #fbbf24;

                    /* Column 2 */
                    --c2-bg: rgba(234, 88, 12, 0.12); --c2-border: rgba(249, 115, 22, 0.7); 
                    --c2-title-bg: rgba(234, 88, 12, 0.3); --c2-title-text: #ffedd5; 
                    --c2-icon: #fb923c;

                    /* Column 3 */
                    --c3-bg: rgba(16, 185, 129, 0.12); --c3-border: rgba(16, 185, 129, 0.7); 
                    --c3-title-bg: rgba(16, 185, 129, 0.3); --c3-title-text: #d1fae5; 
                    --c3-icon: #34d399;

                    /* Inner Boxes in Col 3 */
                    --ref-bg: rgba(239, 68, 68, 0.15); --ref-border: rgba(239, 68, 68, 0.7); 
                    --ref-title-bg: rgba(239, 68, 68, 0.3); --ref-title-text: #fee2e2;
                    
                    /* NEW: Disease Control */
                    --dc-bg: rgba(168, 85, 247, 0.15); --dc-border: rgba(168, 85, 247, 0.7);
                    --dc-title-bg: rgba(168, 85, 247, 0.3); --dc-title-text: #f3e8ff;
                    --dc-icon: #c084fc;

                    --dis-bg: rgba(16, 185, 129, 0.15); --dis-border: rgba(16, 185, 129, 0.7); 
                    --dis-title-bg: rgba(16, 185, 129, 0.3); --dis-title-text: #d1fae5;

                    /* Alert & Tags */
                    --alert-bg: #134e4a; --alert-border: #0f766e; 
                    --alert-text: #ccfbf1; --alert-hl: #fde047;
                    
                    /* Connecting Lines */
                    --svg-line: #60a5fa; 
                    --svg-return: #38bdf8;
                }
            }

            /* =========================================
               BASE STYLES & UTILITIES
               ========================================= */
            body { font-family: 'Sarabun', sans-serif; background-color: transparent; padding: 1rem; color: var(--text-main); }
            
            .text-main { color: var(--text-main); }
            .text-muted { color: var(--text-muted); }

            .flow-col { border-width: 3px; border-radius: 2rem; padding: 1.25rem; display: flex; flex-direction: column; gap: 1.25rem; position: relative; height: 100%; transition: all 0.3s; }
            .inner-box { background-color: var(--bg-card); border: 1px solid var(--border-card); border-radius: 0.75rem; padding: 1rem; box-shadow: var(--shadow-box); transition: all 0.3s; }
            
            .tag-code { position: absolute; top: 0.5rem; right: 0.5rem; background-color: var(--alert-bg); color: var(--alert-text); font-size: 0.65rem; padding: 0.2rem 0.6rem; border-radius: 9999px; font-weight: 700; z-index: 10; border: 1px solid var(--alert-border); box-shadow: 0 2px 4px rgba(0,0,0,0.15); letter-spacing: 0.025em; }
            .arrow-icon { color: var(--svg-line); flex-shrink: 0; }

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
            
            .box-refer { background-color: var(--ref-bg); border-color: var(--ref-border); border-width: 3px; }
            .box-refer-title { background-color: var(--ref-title-bg); color: var(--ref-title-text); }
            .box-refer-icon { color: var(--ref-title-text); }

            .box-dc { background-color: var(--dc-bg); border-color: var(--dc-border); border-width: 3px; }
            .box-dc-title { background-color: var(--dc-title-bg); color: var(--dc-title-text); }
            .box-dc-icon { color: var(--dc-icon); }

            .box-discharge { background-color: var(--dis-bg); border-color: var(--dis-border); border-width: 3px; }
            .box-discharge-title { background-color: var(--dis-title-bg); color: var(--dis-title-text); }
        </style>
    </head>
    <body>
        <!-- Main Container -->
        <div id="main-container" class="max-w-[1280px] mx-auto relative pb-20 sm:pb-28 lg:pb-32">
            
            <!-- Alert Box -->
            <div class="flex justify-end mb-6 relative z-20">
                <div class="px-5 py-2.5 rounded-full font-bold shadow-lg text-xs sm:text-sm flex items-center border" style="background-color: var(--alert-bg); color: var(--alert-text); border-color: var(--alert-border);">
                    <span class="mr-2" style="color: var(--alert-hl);">ย้ำ!</span> บันทึกรหัสโรค Z58.1 (Exposure to air pollution) ทุกจุดบริการเพื่อวิเคราะห์ข้อมูล
                </div>
            </div>

            <!-- SVG Overlay for Dynamic Line Drawing (Desktop Only) -->
            <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden lg:block z-0" style="overflow: visible; filter: drop-shadow(0px 2px 3px rgba(0,0,0,0.15));">
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
            <div id="return-label" class="absolute hidden lg:flex items-center justify-center inner-box px-8 py-2.5 rounded-full z-10 border-[3px]" style="border-color: var(--svg-return);">
                <p class="font-bold text-base whitespace-nowrap text-main">
                    การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                </p>
            </div>

            <!-- 3 Columns Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 relative z-10 items-stretch">

                <!-- ================= Column 1: Left (Community) ================= -->
                <div id="col-left" class="col-1 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center c1-title py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm">ชุมชนและหน่วยบริการปฐมภูมิ (รุก)</h2>
                    <div class="flex flex-col items-center text-center py-5 inner-box border-2 shadow-sm" style="border-color: var(--c1-border);">
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
                <div id="col-mid" class="col-2 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center c2-title py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm">การรับผู้ป่วยและดูแลรักษา (รับ)</h2>
                    
                    <div class="space-y-4 h-full flex flex-col justify-between mt-2">
                        <!-- Row 1: Online -->
                        <div class="inner-box flex flex-wrap sm:flex-nowrap items-center justify-between gap-3 relative">
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
                                    <p class="font-bold text-[13px] sm:text-sm text-main">ประเมินเบื้องต้น</p>
                                    <p class="text-[11px] sm:text-xs text-muted font-medium">& Telemedicine</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 2: OPD -->
                        <div class="inner-box pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                <div class="flex shrink-0 c2-icon">
                                    <i data-lucide="eye" class="w-6 h-6 sm:w-7 sm:h-7"></i>
                                    <i data-lucide="lungs" class="w-6 h-6 sm:w-7 sm:h-7 -ml-2"></i>
                                </div>
                                <div>
                                    <h3 class="font-bold text-[13px] sm:text-sm text-main leading-tight">ผู้ป่วยนอก (OPD) <br/>& คลินิกมลพิษ</h3>
                                </div>
                            </div>
                            <div class="flex-grow flex items-center justify-between sm:justify-around gap-1 text-[11px] sm:text-xs">
                                <div class="text-center shrink-0">
                                    <p class="font-bold text-main">คัดกรองอาการ</p>
                                    <p class="text-[9px] sm:text-[10px] text-muted font-medium">(PM2.5 > 37.5)</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center shrink-0">
                                    <p class="text-muted font-medium">ส่งเข้า</p>
                                    <p class="font-bold c2-text">Pollution Clinic</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center shrink-0 w-16 sm:w-20">
                                    <p class="font-bold text-main">จ่ายยา/แนะนำ</p>
                                    <p class="text-[9px] sm:text-[10px] text-muted font-medium">นัดติดตาม 7 วัน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 3: ER -->
                        <div class="inner-box pt-8 sm:pt-6 flex flex-wrap items-center gap-2 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 w-full lg:w-auto mb-2 lg:mb-0 shrink-0">
                                <i data-lucide="ambulance" class="w-6 h-6 sm:w-7 sm:h-7 text-red-600 shrink-0"></i>
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
                                    <p class="font-bold text-main">1669 ติดต่อ EMS</p>
                                    <p class="text-muted font-medium">รับเข้า ER</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center shrink-0 w-16 sm:w-20">
                                    <p class="font-bold text-main">ประเมิน Admit</p>
                                    <p class="text-muted font-medium">หรือ กลับบ้าน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 4: IPD -->
                        <div class="inner-box pt-8 sm:pt-6 flex items-center justify-between gap-2 sm:gap-4 relative">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 shrink-0">
                                <i data-lucide="bed" class="w-6 h-6 sm:w-8 sm:h-8 text-blue-600"></i>
                                <h3 class="font-bold text-[13px] sm:text-sm text-main">ผู้ป่วยใน (IPD)</h3>
                            </div>
                            <div class="flex items-center gap-2 sm:gap-4 flex-grow justify-end">
                                <div class="text-right sm:text-center text-[11px] sm:text-sm">
                                     <p class="font-bold text-main">รับ Admit</p>
                                     <p class="text-[10px] sm:text-xs text-muted font-medium">เข้าหอผู้ป่วย</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-4 h-4 sm:w-5 sm:h-5"></i>
                                <div class="text-center text-[11px] sm:text-sm shrink-0">
                                     <p class="font-bold text-main leading-tight">พยาบาล<br/>ซักประวัติเพิ่มเติม</p>
                                </div>
                            </div>
                         </div>
                    </div>
                </div>

                <!-- ================= Column 3: Right (Refer, Control & Discharge) ================= -->
                <div id="col-right" class="col-3 flow-col">
                    <h2 class="text-lg sm:text-xl font-extrabold text-center c3-title py-2.5 rounded-full mx-2 sm:mx-4 shadow-sm">ระบบส่งต่อ จำหน่าย และควบคุมโรค</h2>
                    
                    <div class="flex flex-col gap-4 h-full mt-2">
                        <!-- 1. Referral System -->
                        <div class="rounded-2xl p-4 sm:p-5 box-refer shadow-md flex-1 flex flex-col justify-center relative transition-all hover:-translate-y-1">
                            <h3 class="font-bold text-center mb-3 sm:mb-4 text-sm sm:text-lg box-refer-title py-1.5 rounded-full mx-2 sm:mx-6 leading-tight shadow-sm" style="color: var(--ref-title-text);">
                                ระบบส่งต่อผู้ป่วย (Referral)
                            </h3>
                            <div class="flex justify-between items-center text-center">
                                <div class="flex-1 flex flex-col items-center">
                                    <i data-lucide="hospital" class="w-7 h-7 sm:w-9 sm:h-9 mb-1 box-refer-icon"></i>
                                    <p class="font-bold text-[13px] sm:text-base text-main leading-tight">รพ.ประเมินการ</p>
                                    <p class="text-[11px] sm:text-sm text-muted font-medium leading-tight mt-1 opacity-90">สำรองเตียงพร้อมรับ<br/>และ Ventilator พร้อมใช้</p>
                                </div>
                                <div class="flex items-center px-1">
                                    <i data-lucide="arrow-right" class="w-5 h-5 sm:w-7 sm:h-7 box-refer-icon opacity-70"></i>
                                </div>
                                <div class="flex-1 flex flex-col items-center">
                                    <i data-lucide="building-2" class="w-7 h-7 sm:w-9 sm:h-9 mb-1 box-refer-icon"></i>
                                    <p class="font-bold text-[13px] sm:text-base text-main leading-tight">หาก Overcapacity</p>
                                    <p class="text-[11px] sm:text-sm text-muted font-medium mt-1 opacity-90">ส่งต่อโรงพยาบาล</p>
                                    <p class="font-extrabold text-base sm:text-lg mt-0.5" style="color: var(--ref-title-text);">ลำพูน</p>
                                </div>
                            </div>
                        </div>

                        <!-- 2. Disease Control (NEW) -->
                        <div class="rounded-2xl p-4 sm:p-5 box-dc shadow-md flex-1 flex flex-col justify-center relative transition-all hover:-translate-y-1">
                            <h3 class="font-bold text-center mb-3 sm:mb-4 text-sm sm:text-lg box-dc-title py-1.5 rounded-full mx-2 sm:mx-6 leading-tight shadow-sm" style="color: var(--dc-title-text);">
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

                        <!-- 3. Discharge -->
                        <div class="rounded-2xl p-4 sm:p-5 box-discharge shadow-md flex-1 flex flex-col justify-center relative transition-all hover:-translate-y-1">
                            <h3 class="font-bold text-center mb-3 sm:mb-4 text-sm sm:text-lg box-discharge-title py-1.5 rounded-full mx-2 sm:mx-6 leading-tight shadow-sm" style="color: var(--dis-title-text);">
                                การจำหน่ายผู้ป่วย (Discharge)
                            </h3>
                            <div class="text-center space-y-2 sm:space-y-3">
                                <p class="font-bold text-sm sm:text-lg text-main">วางแผนตามหลัก D-METHOD</p>
                                <div class="w-12 sm:w-16 h-1 bg-current opacity-30 mx-auto rounded-full" style="color: var(--dis-title-text);"></div>
                                <p class="text-[11px] sm:text-sm font-bold text-muted leading-relaxed opacity-90">ประสานทีมเยี่ยมบ้านและอาชีวอนามัย<br/>ประเมินสภาพที่อยู่อาศัยไม่ให้กำเริบซ้ำ</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Mobile view for return arrow text (Shown only on small screens) -->
             <div class="lg:hidden text-center mt-8">
                <div class="inline-flex items-center justify-center inner-box px-6 py-3 rounded-full border-[3px]" style="border-color: var(--svg-return);">
                    <p class="font-bold text-sm sm:text-base whitespace-nowrap text-main">
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
                    // Hide SVG/Label on smaller screens
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
