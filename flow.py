import streamlit.components.v1 as components

def render_flow():
    # อัปเดตล่าสุด: นำกรอบแช่แข็งขนาด 1280px มาครอบเพื่อแก้ปัญหาการบิดเบี้ยวเวลาย่อหน้าต่าง 100%
    html_code = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;700;800&display=swap" rel="stylesheet">
        <style>
            /* ตั้งค่า Theme แบบยืดหยุ่นรองรับ Light/Dark Mode */
            :root {
                --text-main: #1e3a8a;
                --text-desc: #334155;
                --line-color: #1e293b;
                --bg-card-shadow: rgba(0,0,0,0.1);
                --bg-knockout: #ffffff;
            }
            
            @media (prefers-color-scheme: dark) {
                :root {
                    --text-main: #60a5fa;
                    --text-desc: #e2e8f0;
                    --line-color: #cbd5e1;
                    --bg-card-shadow: rgba(255,255,255,0.05);
                    --bg-knockout: #0e1117;
                }
            }

            body { 
                font-family: 'Sarabun', sans-serif; 
                background-color: transparent;
                margin: 0; 
                padding: 1rem; 
                color: var(--text-desc);
            }
            
            /* คลาสสำหรับวาดเส้น */
            .line-v { width: 3px; background-color: var(--line-color); margin: 0 auto; }
            .line-h { height: 3px; background-color: var(--line-color); margin: 0 auto; width: 100%; }
            .border-line { border-color: var(--line-color) !important; }
            .border-t-line { border-top-color: var(--line-color) !important; border-top-width: 3px; }
            .border-r-line { border-right-color: var(--line-color) !important; border-right-width: 3px; }
            
            .arrow-down { 
                width: 0; height: 0; 
                border-left: 6px solid transparent; 
                border-right: 6px solid transparent; 
                border-top: 8px solid var(--line-color); 
                margin: 0 auto; 
            }
            
            .card-text { word-wrap: break-word; hyphens: auto; }

            /* =======================================
               THAI FONT BASELINE FIX
               ======================================= */
            .baseline-fix {
                position: relative !important;
                top: -4px !important;
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
                body, *, .line-v, .line-h, .arrow-down, #dynamic-lines-container {
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                #dynamic-lines-container {
                    display: block !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                }
                .shadow-sm, .shadow-md {
                    box-shadow: none !important;
                    border: 1px solid #e2e8f0 !important;
                }
            }
        </style>
    </head>
    <body class="bg-transparent antialiased">
        
        <!-- Wrapper แช่แข็งหน้าจอให้กว้าง 1280px เสมอ (เลื่อนและซูมได้แบบรูปภาพ ลบ Responsive ทิ้ง) -->
        <div style="width: 100%; overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch;">
            <div style="min-width: 1280px; width: 1280px; margin: 0 auto; background-color: #ffffff;">
                
                <div id="capture-area" class="w-full pb-10 pt-8 px-16 relative">
                    <!-- Header -->
                    <div class="text-center mb-12 relative">
                        <h2 class="text-4xl font-extrabold mb-2 tracking-wide" style="color: var(--text-main);">ขั้นตอนการให้บริการ รพ.สันทราย</h2>
                        <p class="text-[1.15rem] font-bold" style="color: var(--text-main);">กรณีผู้ป่วยสงสัยตนเอง/ญาติได้รับผลกระทบจาก PM 2.5 จังหวัดเชียงใหม่</p>
                        
                        <!-- ปุ่มสำหรับดาวน์โหลดรูปภาพ -->
                        <button onclick="downloadImage()" class="mt-5 inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 px-6 rounded-full shadow-lg transition-all print:hidden" data-html2canvas-ignore="true">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                            ดาวน์โหลดรูปภาพ Flow
                        </button>
                    </div>

                    <!-- Main Flow Container (Frozen 1280px version) -->
                    <div class="w-full max-w-6xl mx-auto flex flex-row gap-12 relative z-10" id="main-flow-container">
                        
                        <!-- Dynamic Lines Container -->
                        <div id="dynamic-lines-container" class="absolute inset-0 pointer-events-none z-[100] block">
                            <!-- เส้นสีแดง -->
                            <div id="red-seg-1" class="absolute bg-red-600"></div>
                            <div id="red-seg-2" class="absolute bg-red-600"></div>
                            <div id="red-seg-3" class="absolute bg-red-600"></div>
                            <div id="red-seg-4" class="absolute bg-red-600"></div>
                            <div id="red-arrow" class="absolute w-0 h-0 border-t-[10px] border-l-[6px] border-r-[6px] border-t-red-600 border-l-transparent border-r-transparent"></div>

                            <!-- เส้นสีม่วง -->
                            <div id="purp-seg-1" class="absolute border-t-[4px] border-dashed border-purple-600 box-border"></div>
                            <div id="purp-seg-2" class="absolute border-l-[4px] border-dashed border-purple-600 box-border"></div>
                            <div id="purp-seg-3" class="absolute border-t-[4px] border-dashed border-purple-600 box-border"></div>
                            <div id="purp-arrow" class="absolute w-0 h-0 border-r-[10px] border-t-[6px] border-b-[6px] border-r-purple-600 border-t-transparent border-b-transparent"></div>
                        </div>

                        <!-- ================= LEFT COLUMN (ONLINE) ================= -->
                        <div class="w-[40%] flex flex-col items-center">
                            
                            <!-- 1. ปรึกษาออนไลน์ -->
                            <div class="flex items-center gap-3 bg-blue-50 border-2 border-blue-300 rounded-full px-4 py-2 shadow-sm relative z-10 w-fit">
                                <div class="bg-blue-600 rounded-full shrink-0 shadow-inner relative overflow-hidden" style="width: 40px; height: 40px; min-width: 40px;">
                                    <svg width="100%" height="100%" viewBox="0 0 40 40" class="absolute inset-0 pointer-events-none">
                                        <text x="50%" y="50%" text-anchor="middle" dy=".35em" font-family="Arial, sans-serif" font-weight="bold" font-size="20" fill="#ffffff">1</text>
                                    </svg>
                                </div>
                                <span class="text-blue-900 font-bold text-xl pr-2 baseline-fix-inline">ปรึกษาออนไลน์</span>
                            </div>
                            <div class="line-v h-6"></div><div class="arrow-down"></div>

                            <!-- หมอพร้อม -->
                            <div class="bg-blue-50 border border-blue-200 rounded-full px-6 py-3 shadow-sm text-center w-fit max-w-[90%] z-10">
                                <p class="text-blue-900 font-bold text-[16px] leading-snug card-text baseline-fix">ผ่านระบบหมอพร้อม/<br>telemedicine ของโรงพยาบาล</p>
                            </div>
                            <div class="line-v h-6"></div><div class="arrow-down"></div>
                            
                            <!-- คัดกรอง -->
                            <div class="bg-blue-200 border border-blue-300 rounded-full px-8 py-2 shadow-sm text-center w-fit z-10">
                                <p class="text-blue-900 font-bold text-[16px] baseline-fix">ทำการคัดกรอง</p>
                            </div>
                            <div class="line-v h-6"></div>
                            
                            <!-- 2-way Split -->
                            <div class="w-full flex flex-col items-center">
                                <div class="w-[70%] border-t-line flex justify-between">
                                    <div class="line-v h-6 mx-0"></div>
                                    <div class="line-v h-6 mx-0"></div>
                                </div>
                                
                                <div class="w-[90%] flex gap-4 items-stretch">
                                    <!-- Left: ไม่เข้าข่าย -->
                                    <div class="flex-1 flex flex-col items-center h-full">
                                        <div class="bg-green-50 border-[3px] border-green-600 rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10">
                                            <p class="text-green-800 font-bold text-[14px] leading-tight card-text baseline-fix">ไม่เข้าข่าย/<br>อาการเล็กน้อย</p>
                                        </div>
                                        <div class="line-v h-4 my-1"></div>
                                        <div class="bg-white border-2 border-green-500 rounded-lg p-2 shadow-sm text-center w-full flex-grow z-10 min-h-[50px] flex items-center justify-center">
                                            <p class="text-green-700 font-bold text-[14px] leading-snug card-text baseline-fix">ให้คำแนะนำ<br>การปฏิบัติตัว<br>และส่งต่อ<br>ทีม 3 หมอ</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Right: เข้าข่าย -->
                                    <div class="flex-1 flex flex-col items-center h-full">
                                        <div class="bg-emerald-200 border border-emerald-500 rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10">
                                            <p class="text-emerald-900 font-bold text-[14px] leading-tight card-text baseline-fix">เข้าข่าย<br>มีอาการที่สงสัย</p>
                                        </div>
                                        <div class="line-v h-4 my-1"></div>
                                        <div id="suspect-container" class="bg-emerald-100 border border-emerald-200 rounded-lg p-2 shadow-sm text-left w-full flex-grow relative z-10">
                                            <p class="text-emerald-900 font-bold text-[13px] leading-snug mb-2 card-text baseline-fix">1. ส่งต่อเข้ารับบริการ<br>ที่รพ./รพ.สต./PCU หนองหาร</p>
                                            <div id="red-source" class="bg-red-200 text-red-900 border border-red-400 px-2 py-1 rounded text-[13px] font-bold leading-snug inline-block shadow-sm relative z-[110]">
                                                <span class="baseline-fix block">2. ถ้าอาการรุนแรง<br>ประสาน 1669</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div> <!-- ปิด LEFT COLUMN -->

                        <!-- ================= RIGHT COLUMN (ONSITE + SURVEILLANCE + CLINIC) ================= -->
                        <div id="right-column" class="w-[60%] flex flex-col items-center mt-0 relative">
                            
                            <!-- ROW: Entry 2 & 3 -->
                            <div class="w-[95%] flex items-stretch gap-4 relative z-10">
                                
                                <!-- ====== Col 2: Onsite ====== -->
                                <div class="flex-[0.8] flex flex-col items-center h-full">
                                    <div class="flex items-center justify-center gap-2 bg-pink-50 border-2 border-pink-200 rounded-full px-4 py-2 shadow-sm z-10 w-fit h-[65px]">
                                        <div class="bg-pink-500 rounded-full shrink-0 shadow-inner relative overflow-hidden" style="width: 32px; height: 32px; min-width: 32px;">
                                            <svg width="100%" height="100%" viewBox="0 0 32 32" class="absolute inset-0 pointer-events-none">
                                                <text x="50%" y="50%" text-anchor="middle" dy=".35em" font-family="Arial, sans-serif" font-weight="bold" font-size="18" fill="#ffffff">2</text>
                                            </svg>
                                        </div>
                                        <h3 class="text-pink-900 font-bold text-[15px] leading-tight text-center baseline-fix">เข้ารับบริการ<br>ที่รพ./รพ.สต./PCU หนองหาร</h3>
                                    </div>
                                    <div class="line-v flex-grow min-h-[40px]"></div>
                                </div>

                                <!-- ====== Col 3: Surveillance ====== -->
                                <div class="flex-[1.2] flex flex-col items-center h-full">
                                    <div class="flex items-center justify-center gap-2 bg-purple-50 border-2 border-purple-300 rounded-full px-4 py-2 shadow-sm z-10 w-fit h-[65px]">
                                        <div class="bg-purple-600 rounded-full shrink-0 shadow-inner relative overflow-hidden" style="width: 32px; height: 32px; min-width: 32px;">
                                            <svg width="100%" height="100%" viewBox="0 0 32 32" class="absolute inset-0 pointer-events-none">
                                                <text x="50%" y="50%" text-anchor="middle" dy=".35em" font-family="Arial, sans-serif" font-weight="bold" font-size="18" fill="#ffffff">3</text>
                                            </svg>
                                        </div>
                                        <h3 class="text-purple-900 font-bold text-[15px] leading-tight text-center baseline-fix">การเฝ้าระวัง</h3>
                                    </div>
                                    <div class="line-v h-6"></div>
                                    
                                    <div class="w-[85%] border-t-line flex justify-between relative z-0">
                                        <div class="line-v h-4 mx-0"></div>
                                        <div class="line-v h-4 mx-0"></div>
                                    </div>
                                    
                                    <!-- ICD-10 & GG Sheets -->
                                    <div class="w-full flex gap-3 items-stretch relative z-10">
                                        <div class="flex-1 flex flex-col items-center h-full">
                                            <div class="bg-purple-100 border-2 border-purple-300 rounded-xl p-2 shadow-sm text-center w-full h-full flex justify-center items-center">
                                                <p class="text-purple-900 font-bold text-[12px] leading-snug card-text baseline-fix">ดึง ICD-10 โรค<br>ที่เกี่ยวข้องกับการ<br>สัมผัส PM2.5</p>
                                            </div>
                                            <div class="line-v h-6"></div>
                                        </div>
                                        <div class="flex-1 flex flex-col items-center h-full">
                                            <div class="bg-purple-100 border-2 border-purple-300 rounded-xl p-2 shadow-sm text-center w-full h-full flex justify-center items-center">
                                                <p class="text-purple-900 font-bold text-[12px] leading-snug card-text baseline-fix">หน่วยงานที่เกี่ยวข้อง<br>(OPD, ER และ<br>PCU หนองหาร)<br>แจ้งข้อมูลผู้ป่วย<br>ผ่าน GG sheets</p>
                                            </div>
                                            <div class="line-v h-6"></div>
                                        </div>
                                        <div class="absolute bottom-0 left-[25%] right-[25%] h-[3px]" style="background-color: var(--line-color);"></div>
                                    </div>
                                    <div class="line-v flex-grow min-h-[30px]"></div>
                                </div>

                                <div class="absolute bottom-0 left-[20%] right-[30%] h-[3px]" style="background-color: var(--line-color);"></div>
                            </div>
                            
                            <!-- Drop down to ซักประวัติ -->
                            <div class="line-v h-6 relative"></div>
                            <div class="arrow-down relative"></div>
                            
                            <!-- ซักประวัติ -->
                            <div class="bg-pink-100 border border-pink-300 rounded-[2rem] px-5 py-3 shadow-sm text-center w-[85%] z-10">
                                <p class="text-pink-900 font-bold text-[15px] leading-snug card-text baseline-fix">เจ้าหน้าที่ซักประวัติ/อาการเบื้องต้น<br>และลงแบบคัดกรองสอบสวนโรค<br>ที่เกิดจาก PM2.5</p>
                            </div>
                            <div class="line-v h-8 relative"></div>
                            
                            <!-- 3-way Split Header line -->
                            <div class="w-[85%] border-t-line flex justify-between relative z-0">
                                <div class="line-v h-6 mx-0"></div>
                                <div class="line-v h-6 mx-0"></div>
                                <div class="line-v h-6 mx-0"></div>
                            </div>
                            
                            <!-- GRID STRUCTURE (3 คอลัมน์ ไม่เข้าข่าย / เล็กน้อย / รุนแรง) -->
                            <div class="w-[95%] grid grid-cols-[1fr_1.2fr_1fr] gap-x-3 relative z-10">
                                
                                <!-- Left: กรณีไม่เข้าข่าย -->
                                <div class="row-span-3 flex flex-col items-center h-full">
                                    <div class="bg-white border-[3px] border-blue-800 rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10 h-[60px] flex items-center justify-center">
                                        <p class="text-blue-900 font-bold text-[13px] leading-tight card-text baseline-fix">กรณี<br>ไม่เข้าข่าย</p>
                                    </div>
                                    <div class="line-v h-4 my-1"></div>
                                    <div class="bg-white border-2 border-blue-800 rounded-lg p-2 shadow-sm text-center w-full h-full flex flex-col items-center justify-center z-10 min-h-[50px]">
                                        <p class="text-blue-900 font-bold text-[13px] leading-snug card-text baseline-fix">ส่งตรวจคลินิก<br>ตามอาการของโรค</p>
                                    </div>
                                </div>
                                
                                <!-- Middle: เข้าข่าย อาการเล็กน้อย -->
                                <div class="flex flex-col items-center h-[60px]">
                                    <div class="bg-orange-200 border-[3px] border-orange-400 rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10 h-full flex items-center justify-center">
                                        <p class="text-orange-900 font-bold text-[13px] leading-tight card-text baseline-fix">เข้าข่าย<br>อาการเล็กน้อย<br>/ปานกลาง</p>
                                    </div>
                                </div>
                                
                                <!-- Right: ผู้ป่วยอาการรุนแรง -->
                                <div class="flex flex-col items-center h-[60px] relative">
                                    <div id="red-target" class="w-full relative z-[110] h-full">
                                        <div class="absolute -top-3 w-full h-[1px]"></div>
                                        <div class="bg-red-200 border-[3px] border-red-500 rounded-full py-2 px-1 shadow-sm text-center w-full h-full flex items-center justify-center">
                                            <p class="text-red-900 font-bold text-[13px] leading-tight card-text baseline-fix">ผู้ป่วย<br>อาการรุนแรง</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Connectors down from Headers -->
                                <div class="flex justify-center"><div class="line-v h-4 my-1"></div></div>
                                <div class="flex justify-center"><div class="line-v h-4 my-1"></div></div>
                                
                                <!-- Outcomes Row -->
                                <div class="flex flex-col items-center h-full w-full">
                                    <div class="line-v flex-grow min-h-[40px]"></div>
                                </div>
                                
                                <div class="flex flex-col items-center h-full w-full">
                                    <div class="bg-red-500 rounded-md p-2 shadow-sm text-center w-[90%] z-10 flex flex-col justify-center">
                                        <p class="text-white font-bold text-[13px] leading-tight card-text baseline-fix">ส่งเข้า<br>ห้องฉุกเฉิน</p>
                                    </div>
                                    <div class="line-v h-4 my-1"></div>
                                    <div id="er-refer-box" class="bg-red-500 rounded-md p-2 shadow-sm text-center w-[90%] h-full flex items-center justify-center z-10 min-h-[30px] relative">
                                        <p class="text-white font-bold text-[13px] leading-tight baseline-fix">Admit หรือ Refer</p>
                                    </div>
                                </div>
                            </div>

                            <!-- เส้นที่เชื่อมตรงเข้าสู่กล่องคลินิกมลพิษ -->
                            <div class="line-v h-14 relative z-0" style="margin-top: -1px;"></div>

                            <!-- ================= CLINIC SECTION ================= -->
                            <div class="w-full flex flex-col items-center relative z-20">
                                <div class="bg-orange-300 border-[3px] border-orange-500 rounded-full px-8 py-3 shadow-md text-center w-fit max-w-[95%] z-10">
                                    <h3 class="text-orange-900 font-bold text-[18px] leading-tight mb-1 baseline-fix">ส่งเข้าคลินิกมลพิษเฉพาะ รพ.</h3>
                                    <p class="text-orange-800 font-bold text-[13px] baseline-fix">(กรณี รพ.สต./PCU หนองหาร ให้ส่งต่อ รพ.)</p>
                                </div>
                                
                                <div class="line-v h-6"></div>
                                
                                <div class="bg-orange-50 border-[2px] border-orange-200 rounded-lg px-6 py-3 shadow-sm text-center w-[85%] z-10">
                                    <p class="text-orange-900 font-bold text-[15px] leading-snug card-text baseline-fix">ซักประวัติ / ตรวจร่างกาย /<br>ตรวจทางห้องปฏิบัติการ<br>โดยแพทย์ / สหวิชาชีพ</p>
                                </div>
                                
                                <div class="line-v h-6"></div>
                                
                                <div class="bg-orange-200 border-[2px] border-orange-300 rounded-lg px-10 py-2 shadow-sm text-center w-fit z-10">
                                    <p class="text-orange-900 font-bold text-[16px] baseline-fix">วางแผนการรักษา</p>
                                </div>
                                
                                <div class="line-v h-6"></div>
                                
                                <!-- Clinic 3-Way Split Outcomes -->
                                <div class="w-[90%] flex flex-col items-center relative z-10">
                                    
                                    <div class="w-[66.66%] border-t-[3px] flex justify-between relative z-0 mx-auto" style="border-color: var(--line-color);">
                                        <div class="w-[3px] h-8 mx-0" style="background-color: var(--line-color);"></div>
                                        <div class="w-[3px] h-8 mx-0" style="background-color: var(--line-color);"></div>
                                        <div class="w-[3px] h-8 mx-0" style="background-color: var(--line-color);"></div>
                                    </div>
                                    
                                    <div class="w-full flex items-stretch">
                                        <div class="flex-1 flex flex-col items-center px-2 h-full">
                                            <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px]">
                                                <p class="text-orange-900 font-bold text-[14px] baseline-fix">ให้ยากลับบ้าน</p>
                                            </div>
                                        </div>
                                        <div class="flex-1 flex flex-col items-center px-2 h-full">
                                            <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px]">
                                                <p class="text-orange-900 font-bold text-[14px] leading-tight baseline-fix">Admit<br>ให้การรักษา</p>
                                            </div>
                                        </div>
                                        <div class="flex-1 flex flex-col items-center px-2 h-full">
                                            <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px]">
                                                <p class="text-orange-900 font-bold text-[14px] baseline-fix">ส่ง REFER</p>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="w-[66.66%] border-b-[3px] flex justify-between relative z-0 mx-auto" style="border-color: var(--line-color);">
                                        <div class="w-[3px] h-8 mx-0" style="background-color: var(--line-color);"></div>
                                        <div class="w-[3px] h-8 mx-0" style="background-color: var(--line-color);"></div>
                                        <div class="w-[3px] h-8 mx-0" style="background-color: var(--line-color);"></div>
                                    </div>
                                    
                                    <div class="line-v h-8 relative z-0 mx-auto"></div>
                                    <div class="arrow-down relative z-0 mx-auto"></div>
                                    
                                    <!-- Post Care Box -->
                                    <div class="w-full bg-blue-100 border-2 border-blue-300 rounded-xl p-4 shadow-md mt-1 relative z-10">
                                        <div class="text-left w-full pl-6">
                                            <ul class="text-blue-900 font-bold text-[14px] leading-relaxed space-y-1">
                                                <li class="flex items-start baseline-fix"><span class="mr-1">1.</span> <span class="card-text">ให้คำปรึกษาก่อนกลับบ้าน</span></li>
                                                <li class="flex items-start baseline-fix"><span class="mr-1">2.</span> <span class="card-text">เยี่ยมบ้านโดยทีม 3 หมอ และ อปท.</span></li>
                                                <li class="flex items-start baseline-fix"><span class="mr-1">3.</span> <span class="card-text">ประเมินสภาพที่อยู่ซ้ำให้เหมาะสมกับผู้ป่วย</span></li>
                                                <li class="flex items-start baseline-fix"><span class="mr-1">4.</span> <span class="card-text">ผู้ป่วยอาการคงที่ติดตามและสั่งยาผ่าน telemedicine เพื่อลดความเสี่ยงสัมผัสฝุ่น</span></li>
                                            </ul>
                                        </div>
                                    </div>
                                    
                                    <div class="line-v h-8 relative z-0 mx-auto"></div>
                                    <div class="arrow-down relative z-0 mx-auto"></div>
                                    
                                    <div id="disease-control-box" class="w-full bg-purple-100 border-[2px] border-purple-400 rounded-xl p-4 shadow-md mt-1 relative z-10 text-center flex flex-col justify-center">
                                        <p class="text-purple-900 font-bold text-[15px] leading-snug card-text baseline-fix">
                                            ทีมคลินิกมลพิษ แจ้งข้อมูลแก่ ควบคุมโรค (เพื่อซักประวัติ+รายงาน สสจ. ทราบ)<br>
                                        </p>
                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                </div> <!-- ปิด capture-area -->
            </div>
        </div> <!-- ปิด wrapper แช่แข็ง -->

        <script>
            // โค้ดดาวน์โหลดฉบับปรับปรุง (ไม่ต้องทำหน้าจอจำลอง เพราะหน้าหลักถูกแช่แข็ง 1280px แล้ว)
            async function downloadImage() {
                const btn = document.querySelector('button[onclick="downloadImage()"]');
                const originalContent = btn.innerHTML;
                btn.innerHTML = 'กำลังประมวลผล...';
                
                await document.fonts.ready;
                
                // แสดง Loading overlay ไว้สวยๆ 
                const overlay = document.createElement('div');
                overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:#ffffff;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;';
                overlay.innerHTML = `
                    <div style="font-family: 'Sarabun', sans-serif; text-align: center;">
                        <svg class="animate-spin mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                        <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b;">กำลังสร้างรูปภาพ...</h2>
                    </div>
                `;
                document.body.appendChild(overlay);
                
                window.scrollTo(0, 0);
                drawFlowLines();
                
                setTimeout(() => {
                    const captureArea = document.getElementById('capture-area');
                    html2canvas(captureArea, {
                        scale: 3, // ความคมชัดระดับ 3x
                        backgroundColor: "#ffffff",
                        useCORS: true, 
                        scrollY: 0, 
                        windowWidth: 1280, 
                        logging: false
                    }).then(canvas => {
                        document.body.removeChild(overlay);
                        const link = document.createElement('a');
                        link.download = 'PM25_Flow_Sansai_Hospital.png';
                        link.href = canvas.toDataURL('image/png', 1.0);
                        link.click();
                        btn.innerHTML = originalContent;
                    }).catch(err => {
                        console.error("Error generating image:", err);
                        document.body.removeChild(overlay);
                        btn.innerHTML = originalContent;
                        alert("เกิดข้อผิดพลาดในการบันทึกรูปภาพ กรุณาลองใหม่อีกครั้ง");
                    });
                }, 300); 
            }

            function drawFlowLines() {
                const linesContainer = document.getElementById('dynamic-lines-container');
                const container = document.getElementById('main-flow-container');
                
                if(linesContainer && container) {
                    const contRect = container.getBoundingClientRect();
                    
                    const getRelRect = (el) => {
                        const rect = el.getBoundingClientRect();
                        return {
                            top: rect.top - contRect.top,
                            bottom: rect.bottom - contRect.top,
                            left: rect.left - contRect.left,
                            right: rect.right - contRect.left,
                            width: rect.width,
                            height: rect.height
                        };
                    };

                    // 1. เส้นแดง (ประสาน 1669 -> ผู้ป่วยอาการรุนแรง)
                    const redSrc = document.getElementById('red-source');
                    const redTgt = document.getElementById('red-target');
                    const suspectCont = document.getElementById('suspect-container'); 
                    
                    if (redSrc && redTgt && suspectCont) {
                        const rSrcRect = getRelRect(redSrc);
                        const rTgtRect = getRelRect(redTgt);
                        const suspectRect = getRelRect(suspectCont);
                        
                        const rStartX = rSrcRect.right;
                        const rStartY = rSrcRect.top + (rSrcRect.height / 2);
                        const rEndX = rTgtRect.left + (rTgtRect.width / 2);
                        const rEndY = rTgtRect.top - 4; 
                        
                        // ลากอ้อมให้พ้นขอบกล่องเขียวไปทางขวา 30px
                        const gutterX = suspectRect.right + 30; 
                        const safeY = rEndY - 25;
                        
                        document.getElementById('red-seg-1').style.cssText = `left: ${rStartX}px; top: ${rStartY - 2}px; width: ${gutterX - rStartX}px; height: 4px;`;
                        document.getElementById('red-seg-2').style.cssText = `left: ${gutterX - 2}px; top: ${Math.min(rStartY, safeY) - 2}px; width: 4px; height: ${Math.abs(safeY - rStartY) + 4}px;`;
                        document.getElementById('red-seg-3').style.cssText = `left: ${Math.min(gutterX, rEndX) - 2}px; top: ${safeY - 2}px; width: ${Math.abs(rEndX - gutterX) + 4}px; height: 4px;`;
                        
                        const rs4Height = Math.max(0, (rEndY - 10) - (safeY - 2));
                        document.getElementById('red-seg-4').style.cssText = `left: ${rEndX - 2}px; top: ${safeY - 2}px; width: 4px; height: ${rs4Height}px;`;
                        
                        document.getElementById('red-arrow').style.cssText = `left: ${rEndX - 6}px; top: ${rEndY - 10}px;`;
                    }

                    // 2. เส้นม่วง (ส่ง REFER -> แจ้งควบคุมโรค สสจ.)
                    const referBox = document.getElementById('er-refer-box');
                    const dcBox = document.getElementById('disease-control-box');
                    const rightCol = document.getElementById('right-column'); 
                    
                    if (referBox && dcBox && rightCol) {
                        const refRect = getRelRect(referBox);
                        const dcRect = getRelRect(dcBox);
                        const rightColRect = getRelRect(rightCol);
                        
                        const pStartX = refRect.right;
                        const pStartY = refRect.top + (refRect.height / 2);
                        const pEndX = dcRect.right;
                        const pEndY = dcRect.top + (dcRect.height / 2);
                        
                        // ลากอ้อมให้พ้นขอบขวาสุดของฝั่งขวาไป 30px
                        const pGutterX = rightColRect.right + 30; 
                        
                        document.getElementById('purp-seg-1').style.cssText = `left: ${pStartX}px; top: ${pStartY - 2}px; width: ${pGutterX - pStartX}px; height: 0px;`;
                        document.getElementById('purp-seg-2').style.cssText = `left: ${pGutterX - 2}px; top: ${pStartY - 2}px; width: 0px; height: ${pEndY - pStartY + 4}px;`;
                        
                        document.getElementById('purp-seg-3').style.cssText = `left: ${pEndX + 12}px; top: ${pEndY - 2}px; width: ${pGutterX - pEndX - 12}px; height: 0px;`;
                        
                        document.getElementById('purp-arrow').style.cssText = `left: ${pEndX + 2}px; top: ${pEndY - 6}px;`;
                    }
                }
            }
            
            window.addEventListener('resize', drawFlowLines);
            window.onload = function() {
                setTimeout(drawFlowLines, 100); 
                setTimeout(drawFlowLines, 500);
            };
            
        </script>
    </body>
    </html>
    """
    
    # ปรับความสูงให้รองรับกล่อง 1280px ได้เต็มที่
    components.html(html_code, height=2700, scrolling=True)
