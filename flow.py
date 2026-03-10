import streamlit.components.v1 as components

def render_flow():
    # โค้ด HTML สำหรับหน้า Flow 
    # อัปเดตล่าสุด: รองรับ Dark Mode สมบูรณ์แบบ (ปรับสีกล่องข้อความทุุกกล่อง) และปรับ Layout ให้ยืดหยุ่นในมือถือ
    html_code = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            // เปิดใช้งาน Dark Mode ตามระบบของผู้ใช้งาน
            tailwind.config = {
                darkMode: 'media',
            }
        </script>
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
                    --line-color: #94a3b8; /* ปรับสีเส้นให้สว่างขึ้นใน Dark Mode */
                    --bg-card-shadow: rgba(255,255,255,0.05);
                    --bg-knockout: #0e1117;
                }
            }

            body { 
                font-family: 'Sarabun', sans-serif; 
                background-color: transparent;
                margin: 0; 
                padding: 1rem 0.5rem; 
                color: var(--text-desc);
            }
            
            /* คลาสสำหรับวาดเส้น */
            .line-v { width: 3px; background-color: var(--line-color); margin: 0 auto; transition: background-color 0.3s; }
            .line-h { height: 3px; background-color: var(--line-color); margin: 0 auto; width: 100%; transition: background-color 0.3s; }
            .border-line { border-color: var(--line-color) !important; transition: border-color 0.3s; }
            .border-t-line { border-top-color: var(--line-color) !important; border-top-width: 3px; transition: border-color 0.3s; }
            .border-r-line { border-right-color: var(--line-color) !important; border-right-width: 3px; transition: border-color 0.3s; }
            
            .arrow-down { 
                width: 0; height: 0; 
                border-left: 6px solid transparent; 
                border-right: 6px solid transparent; 
                border-top: 8px solid var(--line-color); 
                margin: 0 auto; 
                transition: border-top-color 0.3s;
            }
            
            .card-text { word-wrap: break-word; hyphens: auto; }

            /* =======================================
               คำสั่งบังคับสำหรับการปริ้น (PRINT STYLES)
               ======================================= */
            @media print {
                body, *, .line-v, .line-h, .arrow-down, svg, path {
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                #flow-svg {
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
    <body>
        
        <!-- ปรับ px ให้มือถือเว้นขอบนิดเดียวพอ แต่จอคอมเว้นเยอะๆ ได้ -->
        <div id="capture-area" class="w-full bg-white dark:bg-[#0e1117] transition-colors duration-300 pb-10 pt-4 px-2 sm:px-6 md:px-20 lg:px-24 rounded-lg">
            <!-- Header -->
            <div class="text-center mb-8 sm:mb-12 relative">
                <h2 class="text-2xl sm:text-3xl md:text-4xl font-extrabold mb-2 tracking-wide" style="color: var(--text-main);">Flow การให้บริการ รพ.สันทราย</h2>
                <p class="text-sm sm:text-base md:text-[1.15rem] font-bold" style="color: var(--text-main);">กรณีผู้ป่วยสงสัยตนเอง/ญาติได้รับผลกระทบจาก PM 2.5 จังหวัดเชียงใหม่</p>
                
                <!-- ปุ่มสำหรับดาวน์โหลดรูปภาพ -->
                <button onclick="downloadImage()" class="mt-5 inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600 text-white font-bold py-2.5 px-6 rounded-full shadow-lg transition-all print:hidden" data-html2canvas-ignore="true">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    ดาวน์โหลดรูปภาพ Flow
                </button>
            </div>

            <!-- Main Flow Container -->
            <div class="w-full max-w-6xl mx-auto flex flex-col md:flex-row gap-6 md:gap-10 relative z-10" id="main-flow-container">
                
                <!-- SVG Overlay -->
                <svg id="flow-svg" class="pointer-events-none z-[100] hidden md:block" style="position: absolute; top: 0; bottom: 0; left: -100px; right: -100px; width: calc(100% + 200px); height: 100%; overflow: visible;">
                    <defs>
                        <marker id="arrow-red" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 0 L 10 5 L 0 10 z" fill="#dc2626" />
                        </marker>
                        <marker id="arrow-purple" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                            <path d="M 0 0 L 10 5 L 0 10 z" class="dark:fill-[#c084fc]" fill="#9333ea" />
                        </marker>
                    </defs>
                    <path id="red-line-path" fill="none" stroke="#dc2626" stroke-width="4" stroke-linejoin="round" marker-end="url(#arrow-red)" />
                    <!-- ให้เส้นสีม่วงสว่างขึ้นใน Dark Mode -->
                    <path id="purple-line-path" fill="none" stroke="currentColor" class="text-purple-600 dark:text-purple-400" stroke-width="8" stroke-linejoin="round" marker-end="url(#arrow-purple)" stroke-dasharray="8,6" />
                </svg>

                <!-- ================= LEFT COLUMN (ONLINE) ================= -->
                <div class="w-full md:w-[40%] flex flex-col items-center">
                    
                    <!-- 1. ปรึกษาออนไลน์ -->
                    <div class="flex items-center gap-3 bg-blue-50 dark:bg-blue-900/30 border-2 border-blue-300 dark:border-blue-600 rounded-full px-4 py-2 shadow-sm relative z-10 w-fit transition-colors">
                        <div class="bg-blue-600 dark:bg-blue-500 text-white rounded-full w-8 h-8 sm:w-10 sm:h-10 shadow-inner shrink-0 relative transition-colors">
                            <span class="font-bold text-lg sm:text-xl absolute inset-0 flex items-center justify-center">1</span>
                        </div>
                        <span class="text-blue-900 dark:text-blue-100 font-bold text-lg sm:text-xl pr-2 transition-colors">ปรึกษาออนไลน์</span>
                    </div>
                    <div class="line-v h-6"></div><div class="arrow-down"></div>

                    <!-- หมอพร้อม -->
                    <div class="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-2xl sm:rounded-full px-6 py-3 shadow-sm text-center w-fit max-w-[95%] z-10 transition-colors">
                        <p class="text-blue-900 dark:text-blue-100 font-bold text-[14px] sm:text-[15px] md:text-[16px] leading-snug card-text transition-colors">ผ่านระบบหมอพร้อม/<br class="hidden sm:block">telemedicine ของโรงพยาบาล</p>
                    </div>
                    <div class="line-v h-6"></div><div class="arrow-down"></div>
                    
                    <!-- คัดกรอง -->
                    <div class="bg-blue-200 dark:bg-blue-800/40 border border-blue-300 dark:border-blue-600 rounded-full px-8 py-2 shadow-sm text-center w-fit z-10 transition-colors">
                        <p class="text-blue-900 dark:text-blue-100 font-bold text-[14px] sm:text-[15px] md:text-[16px] transition-colors">ทำการคัดกรอง</p>
                    </div>
                    <div class="line-v h-6"></div>
                    
                    <!-- 2-way Split -->
                    <div class="w-full flex flex-col items-center">
                        <div class="w-[70%] sm:w-[80%] border-t-line flex justify-between">
                            <div class="line-v h-6 mx-0"></div>
                            <div class="line-v h-6 mx-0"></div>
                        </div>
                        
                        <div class="w-full flex gap-2 sm:gap-4 items-stretch px-1 sm:px-2">
                            <!-- Left: ไม่เข้าข่าย -->
                            <div class="flex-1 flex flex-col items-center h-full">
                                <div class="bg-green-50 dark:bg-green-900/30 border-[3px] border-green-600 dark:border-green-500 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10 transition-colors">
                                    <p class="text-green-800 dark:text-green-100 font-bold text-[11px] sm:text-[13px] md:text-[14px] leading-tight card-text">ไม่เข้าข่าย/<br>อาการเล็กน้อย</p>
                                </div>
                                <div class="line-v h-4 my-1"></div>
                                <div class="bg-white dark:bg-slate-800 border-2 border-green-500 dark:border-green-600 rounded-lg p-2 shadow-sm text-center w-full flex-grow z-10 min-h-[50px] flex items-center justify-center transition-colors">
                                    <p class="text-green-700 dark:text-green-300 font-bold text-[11px] sm:text-[13px] md:text-[14px] leading-snug card-text">ให้คำแนะนำ<br>การปฏิบัติตัว<br>และส่งต่อ<br>ทีม 3 หมอ</p>
                                </div>
                            </div>
                            
                            <!-- Right: เข้าข่าย -->
                            <div class="flex-1 flex flex-col items-center h-full">
                                <div class="bg-emerald-200 dark:bg-emerald-800/40 border border-emerald-500 dark:border-emerald-600 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10 transition-colors">
                                    <p class="text-emerald-900 dark:text-emerald-100 font-bold text-[11px] sm:text-[13px] md:text-[14px] leading-tight card-text">เข้าข่าย<br>มีอาการที่สงสัย</p>
                                </div>
                                <div class="line-v h-4 my-1"></div>
                                <div id="suspect-container" class="bg-emerald-100 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-700 rounded-lg p-2 shadow-sm text-left w-full flex-grow relative z-10 transition-colors">
                                    <p class="text-emerald-900 dark:text-emerald-100 font-bold text-[11px] sm:text-[13px] leading-snug mb-2 card-text">1. ส่งต่อเข้ารับบริการ<br>ที่รพ./รพ.สต./PCU หนองหาร</p>
                                    <div id="red-source" class="bg-red-200 dark:bg-red-900/50 text-red-900 dark:text-red-100 border border-red-400 dark:border-red-600 px-2 py-1 rounded text-[11px] sm:text-[13px] font-bold leading-snug inline-block shadow-sm relative z-[110] transition-colors">
                                        2. ถ้าอาการรุนแรง<br>ประสาน 1669
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div> <!-- ปิด LEFT COLUMN -->

                <!-- ================= RIGHT COLUMN (ONSITE + SURVEILLANCE + CLINIC) ================= -->
                <div id="right-column" class="w-full md:w-[60%] flex flex-col items-center mt-10 md:mt-0 relative">
                    
                    <!-- ROW: Entry 2 & 3 -->
                    <div class="w-[100%] sm:w-[95%] flex items-stretch gap-2 sm:gap-4 relative z-10 px-1 sm:px-0">
                        
                        <!-- ====== Col 2: Onsite ====== -->
                        <div class="flex-[0.8] flex flex-col items-center h-full">
                            <div class="flex items-center justify-center gap-1 sm:gap-2 bg-pink-50 dark:bg-pink-900/30 border-2 border-pink-200 dark:border-pink-800 rounded-full px-2 sm:px-4 py-2 shadow-sm z-10 w-full h-[55px] sm:h-[65px] transition-colors">
                                <div class="bg-pink-500 text-white rounded-full w-6 h-6 sm:w-8 sm:h-8 shadow-inner shrink-0 relative transition-colors">
                                    <span class="font-bold text-sm sm:text-lg absolute inset-0 flex items-center justify-center">2</span>
                                </div>
                                <h3 class="text-pink-900 dark:text-pink-100 font-bold text-[10px] sm:text-[13px] md:text-[15px] leading-tight text-center">เข้ารับบริการ<br>ที่รพ./รพ.สต./PCU หนองหาร</h3>
                            </div>
                            <div class="line-v flex-grow min-h-[30px] sm:min-h-[40px]"></div>
                        </div>

                        <!-- ====== Col 3: Surveillance ====== -->
                        <div class="flex-[1.2] flex flex-col items-center h-full">
                            <div class="flex items-center justify-center gap-1 sm:gap-2 bg-purple-50 dark:bg-purple-900/30 border-2 border-purple-300 dark:border-purple-800 rounded-full px-2 sm:px-4 py-2 shadow-sm z-10 w-fit h-[55px] sm:h-[65px] transition-colors">
                                <div class="bg-purple-600 dark:bg-purple-500 text-white rounded-full w-6 h-6 sm:w-8 sm:h-8 shadow-inner shrink-0 relative transition-colors">
                                    <span class="font-bold text-sm sm:text-lg absolute inset-0 flex items-center justify-center">3</span>
                                </div>
                                <h3 class="text-purple-900 dark:text-purple-100 font-bold text-[11px] sm:text-[14px] md:text-[15px] leading-tight text-center">การเฝ้าระวัง</h3>
                            </div>
                            <div class="line-v h-4 sm:h-6"></div>
                            
                            <div class="w-[85%] border-t-line flex justify-between relative z-0">
                                <div class="line-v h-4 mx-0"></div>
                                <div class="line-v h-4 mx-0"></div>
                            </div>
                            
                            <div class="w-full flex gap-1 sm:gap-2 md:gap-3 items-stretch relative z-10">
                                <div class="flex-1 flex flex-col items-center h-full">
                                    <div class="bg-purple-100 dark:bg-purple-800/40 border-2 border-purple-300 dark:border-purple-600 rounded-xl p-1 sm:p-2 shadow-sm text-center w-full h-full flex justify-center items-center transition-colors">
                                        <p class="text-purple-900 dark:text-purple-100 font-bold text-[9px] sm:text-[11px] md:text-[12px] leading-snug card-text">ดึง ICD-10 โรค<br>ที่เกี่ยวข้องกับการ<br>สัมผัส PM2.5</p>
                                    </div>
                                    <div class="line-v h-4 sm:h-6"></div>
                                </div>
                                <div class="flex-1 flex flex-col items-center h-full">
                                    <div class="bg-purple-100 dark:bg-purple-800/40 border-2 border-purple-300 dark:border-purple-600 rounded-xl p-1 sm:p-2 shadow-sm text-center w-full h-full flex justify-center items-center transition-colors">
                                        <p class="text-purple-900 dark:text-purple-100 font-bold text-[9px] sm:text-[11px] md:text-[12px] leading-snug card-text">หน่วยงานที่เกี่ยวข้อง<br>(OPD, ER และ<br>PCU หนองหาร)<br>แจ้งข้อมูลผู้ป่วย<br>ผ่าน GG sheets</p>
                                    </div>
                                    <div class="line-v h-4 sm:h-6"></div>
                                </div>
                                <div class="absolute bottom-0 left-[25%] right-[25%] h-[3px]" style="background-color: var(--line-color);"></div>
                            </div>
                            <div class="line-v flex-grow min-h-[20px] sm:min-h-[30px]"></div>
                        </div>

                        <div class="absolute bottom-0 left-[20%] right-[30%] h-[3px]" style="background-color: var(--line-color);"></div>
                    </div>
                    
                    <div class="line-v h-4 sm:h-6 relative"></div>
                    <div class="arrow-down relative"></div>
                    
                    <!-- ซักประวัติ -->
                    <div class="bg-pink-100 dark:bg-pink-900/40 border border-pink-300 dark:border-pink-700 rounded-[2rem] px-2 sm:px-5 py-3 shadow-sm text-center w-full sm:w-[85%] z-10 transition-colors">
                        <p class="text-pink-900 dark:text-pink-100 font-bold text-[11px] sm:text-[14px] md:text-[15px] leading-snug card-text">เจ้าหน้าที่ซักประวัติ/อาการเบื้องต้น<br>และลงแบบคัดกรองสอบสวนโรค<br>ที่เกิดจาก PM2.5</p>
                    </div>
                    <div class="line-v h-8 relative"></div>
                    
                    <div class="w-[90%] sm:w-[85%] border-t-line flex justify-between relative z-0">
                        <div class="line-v h-6 mx-0"></div>
                        <div class="line-v h-6 mx-0"></div>
                        <div class="line-v h-6 mx-0"></div>
                    </div>
                    
                    <!-- GRID STRUCTURE -->
                    <div class="w-full sm:w-[95%] grid grid-cols-[1fr_1.2fr_1fr] gap-x-1 sm:gap-x-2 md:gap-x-3 relative z-10 px-1">
                        
                        <!-- Left: กรณีไม่เข้าข่าย -->
                        <div class="row-span-3 flex flex-col items-center h-full">
                            <div class="bg-white dark:bg-slate-800 border-[3px] border-blue-800 dark:border-blue-500 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10 h-[50px] sm:h-[60px] flex items-center justify-center transition-colors">
                                <p class="text-blue-900 dark:text-blue-100 font-bold text-[10px] sm:text-[12px] md:text-[13px] leading-tight card-text">กรณี<br>ไม่เข้าข่าย</p>
                            </div>
                            <div class="line-v h-3 sm:h-4 my-1"></div>
                            <div class="bg-white dark:bg-slate-800 border-2 border-blue-800 dark:border-blue-500 rounded-lg p-1 sm:p-2 shadow-sm text-center w-full h-full flex flex-col items-center justify-center z-10 min-h-[50px] transition-colors">
                                <p class="text-blue-900 dark:text-blue-100 font-bold text-[10px] sm:text-[12px] md:text-[13px] leading-snug card-text">ส่งตรวจคลินิก<br>ตามอาการของโรค</p>
                            </div>
                        </div>
                        
                        <!-- Middle: เข้าข่าย อาการเล็กน้อย -->
                        <div class="flex flex-col items-center h-[50px] sm:h-[60px]">
                            <div class="bg-orange-200 dark:bg-orange-900/40 border-[3px] border-orange-400 dark:border-orange-500 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10 h-full flex items-center justify-center transition-colors">
                                <p class="text-orange-900 dark:text-orange-100 font-bold text-[10px] sm:text-[12px] md:text-[13px] leading-tight card-text">เข้าข่าย<br>อาการเล็กน้อย<br>/ปานกลาง</p>
                            </div>
                        </div>
                        
                        <!-- Right: ผู้ป่วยอาการรุนแรง -->
                        <div class="flex flex-col items-center h-[50px] sm:h-[60px] relative">
                            <div id="red-target" class="w-full relative z-[110] h-full">
                                <div class="absolute -top-3 w-full h-[1px]"></div>
                                <div class="bg-red-200 dark:bg-red-900/40 border-[3px] border-red-500 dark:border-red-600 rounded-full py-2 px-1 shadow-sm text-center w-full h-full flex items-center justify-center transition-colors">
                                    <p class="text-red-900 dark:text-red-100 font-bold text-[10px] sm:text-[12px] md:text-[13px] leading-tight card-text">ผู้ป่วย<br>อาการรุนแรง</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="flex justify-center"><div class="line-v h-3 sm:h-4 my-1"></div></div>
                        <div class="flex justify-center"><div class="line-v h-3 sm:h-4 my-1"></div></div>
                        
                        <!-- Outcomes Row -->
                        <div class="flex flex-col items-center h-full w-full">
                            <div class="line-v flex-grow min-h-[30px] sm:min-h-[40px]"></div>
                        </div>
                        
                        <!-- ฝั่งขวา ห้องฉุกเฉิน -->
                        <div class="flex flex-col items-center h-full w-full">
                            <div class="bg-red-500 dark:bg-red-600 rounded-md p-1 sm:p-2 shadow-sm text-center w-full sm:w-[90%] z-10 transition-colors">
                                <p class="text-white font-bold text-[10px] sm:text-[12px] md:text-[13px] leading-tight card-text">ส่งเข้า<br>ห้องฉุกเฉิน</p>
                            </div>
                            <div class="line-v h-3 sm:h-4 my-1"></div>
                            <div id="er-refer-box" class="bg-red-500 dark:bg-red-600 rounded-md p-1 sm:p-2 shadow-sm text-center w-full sm:w-[90%] h-full flex items-center justify-center z-10 min-h-[30px] relative transition-colors">
                                <p class="text-white font-bold text-[10px] sm:text-[12px] md:text-[13px] leading-tight">ส่ง REFER</p>
                            </div>
                        </div>
                    </div>

                    <div class="line-v h-10 sm:h-14 relative z-0" style="margin-top: -1px;"></div>

                    <!-- ================= CLINIC SECTION ================= -->
                    <div class="w-full flex flex-col items-center relative z-20">
                        <div class="bg-orange-300 dark:bg-orange-800/60 border-[3px] border-orange-500 dark:border-orange-600 rounded-3xl sm:rounded-full px-2 sm:px-8 py-3 shadow-md text-center w-full sm:w-fit max-w-[95%] z-10 transition-colors">
                            <h3 class="text-orange-900 dark:text-orange-100 font-bold text-[13px] sm:text-[16px] md:text-[18px] leading-tight mb-1">ส่งเข้าคลินิกมลพิษเฉพาะ รพ.</h3>
                            <p class="text-orange-800 dark:text-orange-200 font-bold text-[10px] sm:text-[12px] md:text-[13px]">(กรณี รพ.สต./PCU หนองหาร ให้ส่งต่อ รพ.)</p>
                        </div>
                        
                        <div class="line-v h-6"></div>
                        
                        <div class="bg-orange-50 dark:bg-orange-900/20 border-[2px] border-orange-200 dark:border-orange-800 rounded-lg px-2 sm:px-6 py-3 shadow-sm text-center w-[95%] sm:w-[85%] z-10 transition-colors">
                            <p class="text-orange-900 dark:text-orange-100 font-bold text-[11px] sm:text-[14px] md:text-[15px] leading-snug card-text">ซักประวัติ / ตรวจร่างกาย /<br>ตรวจทางห้องปฏิบัติการ<br>โดยแพทย์ / สหวิชาชีพ</p>
                        </div>
                        
                        <div class="line-v h-6"></div>
                        
                        <div class="bg-orange-200 dark:bg-orange-800/40 border-[2px] border-orange-300 dark:border-orange-700 rounded-lg px-6 sm:px-10 py-2 shadow-sm text-center w-fit z-10 transition-colors">
                            <p class="text-orange-900 dark:text-orange-100 font-bold text-[12px] sm:text-[15px] md:text-[16px]">วางแผนการรักษา</p>
                        </div>
                        
                        <div class="line-v h-6"></div>
                        
                        <!-- Clinic 3-Way Split Outcomes -->
                        <div class="w-[100%] sm:w-[90%] flex flex-col items-center relative z-10 px-1 sm:px-0">
                            
                            <div class="w-[70%] sm:w-[66.66%] border-t-[3px] flex justify-between relative z-0 mx-auto" style="border-color: var(--line-color);">
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                            </div>
                            
                            <div class="w-full flex items-stretch gap-1 sm:gap-0">
                                <div class="flex-1 flex flex-col items-center px-0 sm:px-2 h-full">
                                    <div class="bg-orange-200 dark:bg-orange-800/40 border-[2px] border-orange-300 dark:border-orange-700 rounded-md p-1 sm:p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px] transition-colors">
                                        <p class="text-orange-900 dark:text-orange-100 font-bold text-[10px] sm:text-[13px] md:text-[14px]">ให้ยากลับบ้าน</p>
                                    </div>
                                </div>
                                <div class="flex-1 flex flex-col items-center px-0 sm:px-2 h-full">
                                    <div class="bg-orange-200 dark:bg-orange-800/40 border-[2px] border-orange-300 dark:border-orange-700 rounded-md p-1 sm:p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px] transition-colors">
                                        <p class="text-orange-900 dark:text-orange-100 font-bold text-[10px] sm:text-[13px] md:text-[14px] leading-tight">Admit<br>ให้การรักษา</p>
                                    </div>
                                </div>
                                <div class="flex-1 flex flex-col items-center px-0 sm:px-2 h-full">
                                    <div class="bg-orange-200 dark:bg-orange-800/40 border-[2px] border-orange-300 dark:border-orange-700 rounded-md p-1 sm:p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px] transition-colors">
                                        <p class="text-orange-900 dark:text-orange-100 font-bold text-[10px] sm:text-[13px] md:text-[14px]">ส่ง REFER</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="w-[70%] sm:w-[66.66%] border-b-[3px] flex justify-between relative z-0 mx-auto" style="border-color: var(--line-color);">
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                            </div>
                            
                            <div class="line-v h-6 sm:h-8 relative z-0 mx-auto"></div>
                            <div class="arrow-down relative z-0 mx-auto"></div>
                            
                            <!-- Post Care Box -->
                            <div class="w-full bg-blue-100 dark:bg-blue-900/40 border-2 border-blue-300 dark:border-blue-700 rounded-xl p-3 sm:p-4 shadow-md mt-1 relative z-10 transition-colors">
                                <div class="text-left w-full pl-1 sm:pl-6">
                                    <ul class="text-blue-900 dark:text-blue-100 font-bold text-[11px] sm:text-[13px] md:text-[14px] leading-relaxed space-y-1">
                                        <li class="flex items-start"><span class="mr-1">1.</span> <span class="card-text">ให้คำปรึกษาก่อนกลับบ้าน</span></li>
                                        <li class="flex items-start"><span class="mr-1">2.</span> <span class="card-text">เยี่ยมบ้านโดยทีม 3 หมอ และ อปท.</span></li>
                                        <li class="flex items-start"><span class="mr-1">3.</span> <span class="card-text">ประเมินสภาพที่อยู่ซ้ำให้เหมาะสมกับผู้ป่วย</span></li>
                                        <li class="flex items-start"><span class="mr-1">4.</span> <span class="card-text">ผู้ป่วยอาการคงที่ติดตามและสั่งยาผ่าน telemedicine เพื่อลดความเสี่ยงสัมผัสฝุ่น</span></li>
                                    </ul>
                                </div>
                            </div>
                            
                            <!-- ส่งข้อมูลควบคุมโรค -->
                            <div class="line-v h-6 sm:h-8 relative z-0 mx-auto"></div>
                            <div class="arrow-down relative z-0 mx-auto"></div>
                            
                            <div id="disease-control-box" class="w-full bg-purple-100 dark:bg-purple-900/40 border-[2px] border-purple-400 dark:border-purple-600 rounded-xl p-3 sm:p-4 shadow-md mt-1 relative z-10 text-center transition-colors">
                                <p class="text-purple-900 dark:text-purple-100 font-bold text-[12px] sm:text-[14px] md:text-[15px] leading-snug card-text">
                                    ทีมคลินิกมลพิษ แจ้งข้อมูลแก่ ควบคุมโรค (เพื่อซักประวัติ+รายงาน สสจ. ทราบ)<br class="hidden sm:block">
                                </p>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div> <!-- ปิด capture-area -->

        <script>
            // เช็คว่าระบบอยู่ใน Dark Mode หรือไม่ เพื่อปรับสีพื้นหลังก่อนดาวน์โหลด
            function isDarkMode() {
                return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            }

            async function downloadImage() {
                drawFlowLines();
                const btn = document.querySelector('button[onclick="downloadImage()"]');
                const originalContent = btn.innerHTML;
                btn.innerHTML = 'กำลังประมวลผล...';
                
                await document.fonts.ready;
                
                setTimeout(() => {
                    const captureArea = document.getElementById('capture-area');
                    
                    html2canvas(captureArea, {
                        scale: 2.5, 
                        // เซ็ตสีให้ตรงกับ Theme ปัจจุบัน (ขาวสว่าง หรือ เทาเข้ม)
                        backgroundColor: isDarkMode() ? "#0e1117" : "#ffffff",
                        useCORS: true, 
                        logging: false
                    }).then(canvas => {
                        const link = document.createElement('a');
                        link.download = 'PM25_Flow_Sansai_Hospital.png';
                        link.href = canvas.toDataURL('image/png', 1.0);
                        link.click();
                        
                        btn.innerHTML = originalContent;
                    }).catch(err => {
                        console.error("Error generating image:", err);
                        btn.innerHTML = originalContent;
                        alert("เกิดข้อผิดพลาดในการบันทึกรูปภาพ กรุณาลองใหม่อีกครั้ง");
                    });
                }, 400);
            }

            function drawFlowLines() {
                const svg = document.getElementById('flow-svg');
                const container = document.getElementById('main-flow-container');
                
                if(svg && container && container.offsetWidth >= 768) {
                    svg.classList.remove('hidden');
                    const svgRect = svg.getBoundingClientRect();
                    
                    // 1. เส้นแดง (ประสาน 1669 -> ผู้ป่วยอาการรุนแรง)
                    const redSrc = document.getElementById('red-source');
                    const redTgt = document.getElementById('red-target');
                    const redPath = document.getElementById('red-line-path');
                    const suspectCont = document.getElementById('suspect-container'); 
                    
                    if (redSrc && redTgt && redPath && suspectCont) {
                        const rSrcRect = redSrc.getBoundingClientRect();
                        const rTgtRect = redTgt.getBoundingClientRect();
                        const suspectRect = suspectCont.getBoundingClientRect();
                        
                        const rStartX = rSrcRect.right - svgRect.left;
                        const rStartY = rSrcRect.top + (rSrcRect.height / 2) - svgRect.top;
                        const rEndX = rTgtRect.left + (rTgtRect.width / 2) - svgRect.left;
                        const rEndY = rTgtRect.top - svgRect.top - 8;
                        
                        const gutterX = (suspectRect.right - svgRect.left) + 30; 
                        const safeY = rEndY - 25;
                        
                        const dRed = `M ${rStartX} ${rStartY} L ${gutterX} ${rStartY} L ${gutterX} ${safeY} L ${rEndX} ${safeY} L ${rEndX} ${rEndY}`;
                        redPath.setAttribute('d', dRed);
                    }

                    // 2. เส้นม่วง (ส่ง REFER -> แจ้งควบคุมโรค สสจ.)
                    const referBox = document.getElementById('er-refer-box');
                    const dcBox = document.getElementById('disease-control-box');
                    const pLinePath = document.getElementById('purple-line-path');
                    const rightCol = document.getElementById('right-column');
                    
                    if (referBox && dcBox && pLinePath && rightCol) {
                        const refRect = referBox.getBoundingClientRect();
                        const dcRect = dcBox.getBoundingClientRect();
                        const rightColRect = rightCol.getBoundingClientRect(); 
                        
                        const pStartX = refRect.right - svgRect.left;
                        const pStartY = refRect.top + (refRect.height / 2) - svgRect.top;
                        const pEndX = dcRect.right - svgRect.left;
                        const pEndY = dcRect.top + (dcRect.height / 2) - svgRect.top;
                        
                        const pGutterX = (rightColRect.right - svgRect.left) + 30; 
                        
                        const dPurple = `M ${pStartX} ${pStartY} L ${pGutterX} ${pStartY} L ${pGutterX} ${pEndY} L ${pEndX + 8} ${pEndY}`;
                        pLinePath.setAttribute('d', dPurple);
                    }

                } else if (svg) {
                    svg.classList.add('hidden'); // ซ่อนเส้นไขว้ข้ามฝั่งในหน้าจอมือถือ
                }
            }
            
            window.addEventListener('resize', drawFlowLines);
            window.onload = function() {
                setTimeout(drawFlowLines, 100); 
                setTimeout(drawFlowLines, 500);
            };
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', drawFlowLines);
            window.onbeforeprint = drawFlowLines;
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=2700, scrolling=True)
