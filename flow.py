import streamlit.components.v1 as components

def render_flow():
    # โค้ด HTML สำหรับหน้า Flow 
    # อัปเดตล่าสุด: เปลี่ยนวิธีการ Freeze หน้าจอตอนดาวน์โหลด ให้ขยายเต็มที่ (1280px) เพื่อให้องค์ประกอบทุกส่วนกางออก 100%
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
                padding: 2rem 1rem; 
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
    <body>
        
        <!-- เพิ่ม px อย่างมาก เพื่อเว้นขอบซ้ายขวาให้เส้นลูกศรมีพื้นที่โชว์เวลาดาวน์โหลดรูป ไม่โดนตัด -->
        <div id="capture-area" class="w-full bg-white pb-10 pt-4 px-4 sm:px-10 md:px-24 transition-all duration-300">
            <!-- Header -->
            <div class="text-center mb-8 sm:mb-12 relative">
                <h2 class="text-2xl sm:text-3xl md:text-4xl font-extrabold mb-2 tracking-wide" style="color: var(--text-main);">Flow การให้บริการ รพ.สันทราย</h2>
                <p class="text-sm sm:text-base md:text-[1.15rem] font-bold" style="color: var(--text-main);">กรณีผู้ป่วยสงสัยตนเอง/ญาติได้รับผลกระทบจาก PM 2.5 จังหวัดเชียงใหม่</p>
                
                <!-- ปุ่มสำหรับดาวน์โหลดรูปภาพ -->
                <button onclick="downloadImage()" class="mt-5 inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 px-6 rounded-full shadow-lg transition-all print:hidden" data-html2canvas-ignore="true">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    ดาวน์โหลดรูปภาพ Flow
                </button>
            </div>

            <!-- Main Flow Container -->
            <div class="w-full max-w-6xl mx-auto flex flex-col md:flex-row gap-8 md:gap-12 relative z-10" id="main-flow-container">
                
                <!-- Dynamic Lines Container (ใช้ Div แทน SVG เพื่อแก้ปัญหาพิกัดเบี้ยว 100%) -->
                <div id="dynamic-lines-container" class="absolute inset-0 pointer-events-none z-[100] hidden md:block">
                    <!-- เส้นสีแดง (ผู้ป่วยอาการรุนแรง) -->
                    <div id="red-seg-1" class="absolute bg-red-600 transition-all duration-300"></div>
                    <div id="red-seg-2" class="absolute bg-red-600 transition-all duration-300"></div>
                    <div id="red-seg-3" class="absolute bg-red-600 transition-all duration-300"></div>
                    <div id="red-seg-4" class="absolute bg-red-600 transition-all duration-300"></div>
                    <div id="red-arrow" class="absolute w-0 h-0 border-t-[10px] border-l-[6px] border-r-[6px] border-t-red-600 border-l-transparent border-r-transparent transition-all duration-300"></div>

                    <!-- เส้นสีม่วง (แจ้งควบคุมโรค) -->
                    <div id="purp-seg-1" class="absolute border-t-[4px] border-dashed border-purple-600 box-border transition-all duration-300"></div>
                    <div id="purp-seg-2" class="absolute border-l-[4px] border-dashed border-purple-600 box-border transition-all duration-300"></div>
                    <div id="purp-seg-3" class="absolute border-t-[4px] border-dashed border-purple-600 box-border transition-all duration-300"></div>
                    <div id="purp-arrow" class="absolute w-0 h-0 border-r-[10px] border-t-[6px] border-b-[6px] border-r-purple-600 border-t-transparent border-b-transparent transition-all duration-300"></div>
                </div>

                <!-- ================= LEFT COLUMN (ONLINE) ================= -->
                <div class="w-full md:w-[40%] flex flex-col items-center">
                    
                    <!-- 1. ปรึกษาออนไลน์ (แก้เลข 1 ตกขอบด้วย absolute inset-0) -->
                    <div class="flex items-center gap-3 bg-blue-50 border-2 border-blue-300 rounded-full px-4 py-2 shadow-sm relative z-10 w-fit">
                        <div class="bg-blue-600 text-white rounded-full w-8 h-8 sm:w-10 sm:h-10 shadow-inner shrink-0 relative">
                            <span class="font-bold text-lg sm:text-xl absolute inset-0 flex items-center justify-center">1</span>
                        </div>
                        <span class="text-blue-900 font-bold text-lg sm:text-xl pr-2">ปรึกษาออนไลน์</span>
                    </div>
                    <div class="line-v h-6"></div><div class="arrow-down"></div>

                    <!-- หมอพร้อม -->
                    <div class="bg-blue-50 border border-blue-200 rounded-2xl sm:rounded-full px-6 py-3 shadow-sm text-center w-fit max-w-[90%] z-10">
                        <p class="text-blue-900 font-bold text-[14px] sm:text-[15px] md:text-[16px] leading-snug card-text">ผ่านระบบหมอพร้อม/<br class="hidden sm:block">telemedicine ของโรงพยาบาล</p>
                    </div>
                    <div class="line-v h-6"></div><div class="arrow-down"></div>
                    
                    <!-- คัดกรอง -->
                    <div class="bg-blue-200 border border-blue-300 rounded-full px-8 py-2 shadow-sm text-center w-fit z-10">
                        <p class="text-blue-900 font-bold text-[14px] sm:text-[15px] md:text-[16px]">ทำการคัดกรอง</p>
                    </div>
                    <div class="line-v h-6"></div>
                    
                    <!-- 2-way Split -->
                    <div class="w-full flex flex-col items-center">
                        <div class="w-[60%] sm:w-[70%] border-t-line flex justify-between">
                            <div class="line-v h-6 mx-0"></div>
                            <div class="line-v h-6 mx-0"></div>
                        </div>
                        
                        <div class="w-[95%] sm:w-[90%] flex gap-2 sm:gap-4 items-stretch">
                            <!-- Left: ไม่เข้าข่าย -->
                            <div class="flex-1 flex flex-col items-center h-full">
                                <div class="bg-green-50 border-[3px] border-green-600 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10">
                                    <p class="text-green-800 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-tight card-text">ไม่เข้าข่าย/<br>อาการเล็กน้อย</p>
                                </div>
                                <div class="line-v h-4 my-1"></div>
                                <div class="bg-white border-2 border-green-500 rounded-lg p-2 shadow-sm text-center w-full flex-grow z-10 min-h-[50px] flex items-center justify-center">
                                    <p class="text-green-700 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-snug card-text">ให้คำแนะนำ<br>การปฏิบัติตัว<br>และส่งต่อ<br>ทีม 3 หมอ</p>
                                </div>
                            </div>
                            
                            <!-- Right: เข้าข่าย -->
                            <div class="flex-1 flex flex-col items-center h-full">
                                <div class="bg-emerald-200 border border-emerald-500 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10">
                                    <p class="text-emerald-900 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-tight card-text">เข้าข่าย<br>มีอาการที่สงสัย</p>
                                </div>
                                <div class="line-v h-4 my-1"></div>
                                <!-- ใส่ ID เพื่อใช้อ้างอิงระยะตีเส้นสีแดงให้พ้นกล่องนี้แบบ 100% -->
                                <div id="suspect-container" class="bg-emerald-100 border border-emerald-200 rounded-lg p-2 shadow-sm text-left w-full flex-grow relative z-10">
                                    <p class="text-emerald-900 font-bold text-[12px] sm:text-[13px] leading-snug mb-2 card-text">1. ส่งต่อเข้ารับบริการ<br>ที่รพ./รพ.สต./PCU หนองหาร</p>
                                    <!-- กล่องต้นทางของเส้นสีแดง -->
                                    <div id="red-source" class="bg-red-200 text-red-900 border border-red-400 px-2 py-1 rounded text-[12px] sm:text-[13px] font-bold leading-snug inline-block shadow-sm relative z-[110]">
                                        2. ถ้าอาการรุนแรง<br>ประสาน 1669
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div> <!-- ปิด LEFT COLUMN -->

                <!-- ================= RIGHT COLUMN (ONSITE + SURVEILLANCE + CLINIC) ================= -->
                <!-- เพิ่ม ID ให้คอลัมน์ขวา เพื่อคำนวณระยะเส้นสีม่วงให้ลากหลบทั้งคอลัมน์แบบ Dynamic -->
                <div id="right-column" class="w-full md:w-[60%] flex flex-col items-center mt-10 md:mt-0 relative">
                    
                    <!-- ROW: Entry 2 & 3 -->
                    <div class="w-[98%] sm:w-[95%] flex items-stretch gap-2 sm:gap-4 relative z-10">
                        
                        <!-- ====== Col 2: Onsite ====== -->
                        <div class="flex-[0.8] flex flex-col items-center h-full">
                            <!-- 2. เข้ารับบริการ (แก้เลขตกขอบด้วย absolute inset-0) -->
                            <div class="flex items-center justify-center gap-1 sm:gap-2 bg-pink-50 border-2 border-pink-200 rounded-full px-4 py-2 shadow-sm z-10 w-fit h-[55px] sm:h-[65px]">
                                <div class="bg-pink-500 text-white rounded-full w-6 h-6 sm:w-8 sm:h-8 shadow-inner shrink-0 relative">
                                    <span class="font-bold text-sm sm:text-lg absolute inset-0 flex items-center justify-center">2</span>
                                </div>
                                <h3 class="text-pink-900 font-bold text-[12px] sm:text-[14px] md:text-[15px] leading-tight text-center">เข้ารับบริการ<br>ที่รพ./รพ.สต./PCU หนองหาร</h3>
                            </div>
                            <div class="line-v flex-grow min-h-[30px] sm:min-h-[40px]"></div>
                        </div>

                        <!-- ====== Col 3: Surveillance ====== -->
                        <div class="flex-[1.2] flex flex-col items-center h-full">
                            <!-- 3. การเฝ้าระวัง (แก้เลขตกขอบด้วย absolute inset-0) -->
                            <div class="flex items-center justify-center gap-1 sm:gap-2 bg-purple-50 border-2 border-purple-300 rounded-full px-4 py-2 shadow-sm z-10 w-fit h-[55px] sm:h-[65px]">
                                <div class="bg-purple-600 text-white rounded-full w-6 h-6 sm:w-8 sm:h-8 shadow-inner shrink-0 relative">
                                    <span class="font-bold text-sm sm:text-lg absolute inset-0 flex items-center justify-center">3</span>
                                </div>
                                <h3 class="text-purple-900 font-bold text-[12px] sm:text-[14px] md:text-[15px] leading-tight text-center">การเฝ้าระวัง</h3>
                            </div>
                            <div class="line-v h-4 sm:h-6"></div>
                            
                            <!-- Split 2-ways for 3 -->
                            <div class="w-[85%] border-t-line flex justify-between relative z-0">
                                <div class="line-v h-4 mx-0"></div>
                                <div class="line-v h-4 mx-0"></div>
                            </div>
                            
                            <!-- ICD-10 & GG Sheets -->
                            <div class="w-full flex gap-1 sm:gap-2 md:gap-3 items-stretch relative z-10">
                                <div class="flex-1 flex flex-col items-center h-full">
                                    <div class="bg-purple-100 border-2 border-purple-300 rounded-xl p-1 sm:p-2 shadow-sm text-center w-full h-full flex justify-center items-center">
                                        <p class="text-purple-900 font-bold text-[10px] sm:text-[11px] md:text-[12px] leading-snug card-text">ดึง ICD-10 โรค<br>ที่เกี่ยวข้องกับการ<br>สัมผัส PM2.5</p>
                                    </div>
                                    <div class="line-v h-4 sm:h-6"></div>
                                </div>
                                <div class="flex-1 flex flex-col items-center h-full">
                                    <div class="bg-purple-100 border-2 border-purple-300 rounded-xl p-1 sm:p-2 shadow-sm text-center w-full h-full flex justify-center items-center">
                                        <p class="text-purple-900 font-bold text-[10px] sm:text-[11px] md:text-[12px] leading-snug card-text">หน่วยงานที่เกี่ยวข้อง<br>(OPD, ER และ<br>PCU หนองหาร)<br>แจ้งข้อมูลผู้ป่วย<br>ผ่าน GG sheets</p>
                                    </div>
                                    <div class="line-v h-4 sm:h-6"></div>
                                </div>
                                <!-- Merge bottom horizontal line for 3 -->
                                <div class="absolute bottom-0 left-[25%] right-[25%] h-[3px]" style="background-color: var(--line-color);"></div>
                            </div>
                            <!-- Main trunk for 3 -->
                            <div class="line-v flex-grow min-h-[20px] sm:min-h-[30px]"></div>
                        </div>

                        <!-- Main Bridge connecting Col 2 and Col 3 -->
                        <div class="absolute bottom-0 left-[20%] right-[30%] h-[3px]" style="background-color: var(--line-color);"></div>
                    </div>
                    
                    <!-- Drop down to ซักประวัติ -->
                    <div class="line-v h-4 sm:h-6 relative"></div>
                    <div class="arrow-down relative"></div>
                    
                    <!-- ซักประวัติ -->
                    <div class="bg-pink-100 border border-pink-300 rounded-[2rem] px-4 sm:px-5 py-3 shadow-sm text-center w-[95%] sm:w-[85%] z-10">
                        <p class="text-pink-900 font-bold text-[13px] sm:text-[14px] md:text-[15px] leading-snug card-text">เจ้าหน้าที่ซักประวัติ/อาการเบื้องต้น<br>และลงแบบคัดกรองสอบสวนโรค<br>ที่เกิดจาก PM2.5</p>
                    </div>
                    <div class="line-v h-8 relative"></div>
                    
                    <!-- 3-way Split Header line -->
                    <div class="w-[90%] sm:w-[85%] border-t-line flex justify-between relative z-0">
                        <div class="line-v h-6 mx-0"></div>
                        <div class="line-v h-6 mx-0"></div>
                        <div class="line-v h-6 mx-0"></div>
                    </div>
                    
                    <!-- GRID STRUCTURE (3 คอลัมน์ ไม่เข้าข่าย / เล็กน้อย / รุนแรง) -->
                    <div class="w-[98%] sm:w-[95%] grid grid-cols-[1fr_1.2fr_1fr] gap-x-1 sm:gap-x-2 md:gap-x-3 relative z-10">
                        
                        <!-- Left: กรณีไม่เข้าข่าย -->
                        <div class="row-span-3 flex flex-col items-center h-full">
                            <div class="bg-white border-[3px] border-blue-800 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10 h-[50px] sm:h-[60px] flex items-center justify-center">
                                <p class="text-blue-900 font-bold text-[11px] sm:text-[12px] md:text-[13px] leading-tight card-text">กรณี<br>ไม่เข้าข่าย</p>
                            </div>
                            <div class="line-v h-3 sm:h-4 my-1"></div>
                            <div class="bg-white border-2 border-blue-800 rounded-lg p-2 shadow-sm text-center w-full h-full flex flex-col items-center justify-center z-10 min-h-[50px]">
                                <p class="text-blue-900 font-bold text-[11px] sm:text-[12px] md:text-[13px] leading-snug card-text">ส่งตรวจคลินิก<br>ตามอาการของโรค</p>
                            </div>
                        </div>
                        
                        <!-- Middle: เข้าข่าย อาการเล็กน้อย -->
                        <div class="flex flex-col items-center h-[50px] sm:h-[60px]">
                            <div class="bg-orange-200 border-[3px] border-orange-400 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10 h-full flex items-center justify-center">
                                <p class="text-orange-900 font-bold text-[11px] sm:text-[12px] md:text-[13px] leading-tight card-text">เข้าข่าย<br>อาการเล็กน้อย<br>/ปานกลาง</p>
                            </div>
                        </div>
                        
                        <!-- Right: ผู้ป่วยอาการรุนแรง -->
                        <div class="flex flex-col items-center h-[50px] sm:h-[60px] relative">
                            <div id="red-target" class="w-full relative z-[110] h-full">
                                <div class="absolute -top-3 w-full h-[1px]"></div>
                                <div class="bg-red-200 border-[3px] border-red-500 rounded-full py-2 px-1 shadow-sm text-center w-full h-full flex items-center justify-center">
                                    <p class="text-red-900 font-bold text-[11px] sm:text-[12px] md:text-[13px] leading-tight card-text">ผู้ป่วย<br>อาการรุนแรง</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Connectors down from Headers -->
                        <div class="flex justify-center"><div class="line-v h-3 sm:h-4 my-1"></div></div>
                        <div class="flex justify-center"><div class="line-v h-3 sm:h-4 my-1"></div></div>
                        
                        <!-- Outcomes Row -->
                        <!-- เส้นแกนกลางลากยาวลงไปรอเชื่อมต่อกับคลินิกมลพิษ -->
                        <div class="flex flex-col items-center h-full w-full">
                            <div class="line-v flex-grow min-h-[30px] sm:min-h-[40px]"></div>
                        </div>
                        
                        <!-- ฝั่งขวา ห้องฉุกเฉิน -->
                        <div class="flex flex-col items-center h-full w-full">
                            <div class="bg-red-500 rounded-md p-1 sm:p-2 shadow-sm text-center w-[95%] sm:w-[90%] z-10">
                                <p class="text-white font-bold text-[11px] sm:text-[12px] md:text-[13px] leading-tight card-text">ส่งเข้า<br>ห้องฉุกเฉิน</p>
                            </div>
                            <div class="line-v h-3 sm:h-4 my-1"></div>
                            <div id="er-refer-box" class="bg-red-500 rounded-md p-1 sm:p-2 shadow-sm text-center w-[95%] sm:w-[90%] h-full flex items-center justify-center z-10 min-h-[30px] relative">
                                <p class="text-white font-bold text-[11px] sm:text-[12px] md:text-[13px] leading-tight">ส่ง REFER</p>
                            </div>
                        </div>
                    </div>

                    <!-- เส้นที่เชื่อมตรงเข้าสู่กล่องคลินิกมลพิษ -->
                    <div class="line-v h-10 sm:h-14 relative z-0" style="margin-top: -1px;"></div>

                    <!-- ================= CLINIC SECTION ================= -->
                    <div class="w-full flex flex-col items-center relative z-20">
                        <div class="bg-orange-300 border-[3px] border-orange-500 rounded-3xl sm:rounded-full px-5 sm:px-8 py-3 shadow-md text-center w-fit max-w-[95%] z-10">
                            <h3 class="text-orange-900 font-bold text-[14px] sm:text-[16px] md:text-[18px] leading-tight mb-1">ส่งเข้าคลินิกมลพิษเฉพาะ รพ.</h3>
                            <p class="text-orange-800 font-bold text-[11px] sm:text-[12px] md:text-[13px]">(กรณี รพ.สต./PCU หนองหาร ให้ส่งต่อ รพ.)</p>
                        </div>
                        
                        <div class="line-v h-6"></div>
                        
                        <div class="bg-orange-50 border-[2px] border-orange-200 rounded-lg px-4 sm:px-6 py-3 shadow-sm text-center w-[95%] sm:w-[85%] z-10">
                            <p class="text-orange-900 font-bold text-[13px] sm:text-[14px] md:text-[15px] leading-snug card-text">ซักประวัติ / ตรวจร่างกาย /<br>ตรวจทางห้องปฏิบัติการ<br>โดยแพทย์ / สหวิชาชีพ</p>
                        </div>
                        
                        <div class="line-v h-6"></div>
                        
                        <div class="bg-orange-200 border-[2px] border-orange-300 rounded-lg px-6 sm:px-10 py-2 shadow-sm text-center w-fit z-10">
                            <p class="text-orange-900 font-bold text-[14px] sm:text-[15px] md:text-[16px]">วางแผนการรักษา</p>
                        </div>
                        
                        <div class="line-v h-6"></div>
                        
                        <!-- Clinic 3-Way Split Outcomes -->
                        <div class="w-[95%] sm:w-[90%] flex flex-col items-center relative z-10">
                            
                            <div class="w-[66.66%] border-t-[3px] flex justify-between relative z-0 mx-auto" style="border-color: var(--line-color);">
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                            </div>
                            
                            <div class="w-full flex items-stretch">
                                <div class="flex-1 flex flex-col items-center px-1 sm:px-2 h-full">
                                    <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px]">
                                        <p class="text-orange-900 font-bold text-[12px] sm:text-[13px] md:text-[14px]">ให้ยากลับบ้าน</p>
                                    </div>
                                </div>
                                <div class="flex-1 flex flex-col items-center px-1 sm:px-2 h-full">
                                    <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px]">
                                        <p class="text-orange-900 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-tight">Admit<br>ให้การรักษา</p>
                                    </div>
                                </div>
                                <div class="flex-1 flex flex-col items-center px-1 sm:px-2 h-full">
                                    <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10 min-h-[40px]">
                                        <p class="text-orange-900 font-bold text-[12px] sm:text-[13px] md:text-[14px]">ส่ง REFER</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="w-[66.66%] border-b-[3px] flex justify-between relative z-0 mx-auto" style="border-color: var(--line-color);">
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                                <div class="w-[3px] h-6 sm:h-8 mx-0" style="background-color: var(--line-color);"></div>
                            </div>
                            
                            <div class="line-v h-6 sm:h-8 relative z-0 mx-auto"></div>
                            <div class="arrow-down relative z-0 mx-auto"></div>
                            
                            <!-- Post Care Box -->
                            <div class="w-full bg-blue-100 border-2 border-blue-300 rounded-xl p-3 sm:p-4 shadow-md mt-1 relative z-10">
                                <div class="text-left w-full pl-2 sm:pl-6">
                                    <ul class="text-blue-900 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-relaxed space-y-1">
                                        <li class="flex items-start"><span class="mr-1">1.</span> <span class="card-text">ให้คำปรึกษาก่อนกลับบ้าน</span></li>
                                        <li class="flex items-start"><span class="mr-1">2.</span> <span class="card-text">เยี่ยมบ้านโดยทีม 3 หมอ และ อปท.</span></li>
                                        <li class="flex items-start"><span class="mr-1">3.</span> <span class="card-text">ประเมินสภาพที่อยู่ซ้ำให้เหมาะสมกับผู้ป่วย</span></li>
                                        <li class="flex items-start"><span class="mr-1">4.</span> <span class="card-text">ผู้ป่วยอาการคงที่ติดตามและสั่งยาผ่าน telemedicine เพื่อลดความเสี่ยงสัมผัสฝุ่น</span></li>
                                    </ul>
                                </div>
                            </div>
                            
                            <!-- ส่งข้อมูลควบคุมโรค (อยู่ล่างสุด รับข้อมูลต่อจาก Post Care และ ER) -->
                            <div class="line-v h-6 sm:h-8 relative z-0 mx-auto"></div>
                            <div class="arrow-down relative z-0 mx-auto"></div>
                            
                            <div id="disease-control-box" class="w-full bg-purple-100 border-[2px] border-purple-400 rounded-xl p-3 sm:p-4 shadow-md mt-1 relative z-10 text-center">
                                <p class="text-purple-900 font-bold text-[13px] sm:text-[14px] md:text-[15px] leading-snug card-text">
                                    ทีมคลินิกมลพิษ แจ้งข้อมูลแก่ ควบคุมโรค (เพื่อซักประวัติ+รายงาน สสจ. ทราบ)<br class="hidden sm:block">
                                </p>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div> <!-- ปิด capture-area -->

        <!-- Script สำหรับวาดเส้นโยงแบบ Div -->
        <script>
            async function downloadImage() {
                const btn = document.querySelector('button[onclick="downloadImage()"]');
                const originalContent = btn.innerHTML;
                btn.innerHTML = 'กำลังประมวลผล...';
                
                // รอให้ฟอนต์โหลดครบ 100% เพื่อไม่ให้ข้อความเพี้ยนตอนแคปรูป
                await document.fonts.ready;
                
                // 1. เก็บค่าย้อนกลับของ Scroll
                const originalScrollY = window.scrollY;
                
                // 2. เลื่อนขึ้นบนสุดเพื่อไม่ให้พิกัดเพี้ยนจาก Scroll offset
                window.scrollTo(0, 0);
                
                // 3. Freeze ความกว้างแบบ "ขยายเต็มที่" (1280px) คงที่ไปเลย
                // เพื่อให้องค์ประกอบทุกส่วนกางออก 100% ไม่บีบอัด ไม่ตกขอบ ไม่เบี้ยว
                const captureArea = document.getElementById('capture-area');
                
                const origCapWidth = captureArea.style.width;
                const origCapMinWidth = captureArea.style.minWidth;
                
                // กางพื้นที่ให้กว้างสุดๆ เพื่อบังคับ Layout แบบ Desktop สมบูรณ์
                captureArea.style.width = '1280px';
                captureArea.style.minWidth = '1280px';
                
                // วาดเส้นใหม่ให้ลงล็อคกับระยะของหน้าจอที่กางออก 1280px แล้ว
                drawFlowLines();
                
                // ดีเลย์เล็กน้อยให้เบราว์เซอร์จัด Layout โค้งมนให้เสร็จสมบูรณ์
                setTimeout(() => {
                    html2canvas(captureArea, {
                        scale: 3, // เพิ่มความคมชัด
                        backgroundColor: "#ffffff",
                        useCORS: true, 
                        scrollY: 0, 
                        windowWidth: 1280, // บอก html2canvas ว่าเราแคปไซส์นี้ จะได้ไม่ดึง CSS Media Query ผิด
                        windowHeight: captureArea.scrollHeight,
                        logging: false
                    }).then(canvas => {
                        // คืนค่า Layout กลับเป็น Responsive เหมือนเดิม
                        captureArea.style.width = origCapWidth;
                        captureArea.style.minWidth = origCapMinWidth;
                        window.scrollTo(0, originalScrollY);
                        
                        const link = document.createElement('a');
                        link.download = 'PM25_Flow_Sansai_Hospital.png';
                        link.href = canvas.toDataURL('image/png', 1.0);
                        link.click();
                        
                        btn.innerHTML = originalContent;
                    }).catch(err => {
                        console.error("Error generating image:", err);
                        
                        // คืนค่าเมื่อ error
                        captureArea.style.width = origCapWidth;
                        captureArea.style.minWidth = origCapMinWidth;
                        window.scrollTo(0, originalScrollY);
                        
                        btn.innerHTML = originalContent;
                        alert("เกิดข้อผิดพลาดในการบันทึกรูปภาพ กรุณาลองใหม่อีกครั้ง");
                    });
                }, 500); // ดีเลย์เพิ่มนิดนึงให้การจัดหน้าเว็บที่ 1280px นิ่งสนิท
            }

            function drawFlowLines() {
                const linesContainer = document.getElementById('dynamic-lines-container');
                const container = document.getElementById('main-flow-container');
                
                if(linesContainer && container && container.offsetWidth >= 768) {
                    linesContainer.classList.remove('hidden');
                    const contRect = container.getBoundingClientRect();
                    
                    // Helper ฟังก์ชันสำหรับดึงพิกัดสัมพัทธ์อ้างอิงกับ main-flow-container
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
                        const rEndY = rTgtRect.top - 4; // เว้นระยะ 4px ก่อนถึงกล่อง
                        
                        // ลากอ้อมให้พ้นขอบกล่องเขียวไปทางขวา 30px
                        const gutterX = suspectRect.right + 30; 
                        const safeY = rEndY - 25;
                        
                        document.getElementById('red-seg-1').style.cssText = `left: ${rStartX}px; top: ${rStartY - 2}px; width: ${gutterX - rStartX}px; height: 4px;`;
                        document.getElementById('red-seg-2').style.cssText = `left: ${gutterX - 2}px; top: ${Math.min(rStartY, safeY) - 2}px; width: 4px; height: ${Math.abs(safeY - rStartY) + 4}px;`;
                        document.getElementById('red-seg-3').style.cssText = `left: ${Math.min(gutterX, rEndX) - 2}px; top: ${safeY - 2}px; width: ${Math.abs(rEndX - gutterX) + 4}px; height: 4px;`;
                        
                        // ปรับความสูงของส่วนที่วิ่งลงหากล่องแดงให้เนียนกับลูกศร
                        const rs4Height = Math.max(0, (rEndY - 10) - (safeY - 2));
                        document.getElementById('red-seg-4').style.cssText = `left: ${rEndX - 2}px; top: ${safeY - 2}px; width: 4px; height: ${rs4Height}px;`;
                        
                        // ลูกศรชี้ลง
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
                        
                        // ปรับระยะให้เสียบเข้าฐานลูกศรซ้ายได้พอดี
                        document.getElementById('purp-seg-3').style.cssText = `left: ${pEndX + 12}px; top: ${pEndY - 2}px; width: ${pGutterX - pEndX - 12}px; height: 0px;`;
                        
                        // ลูกศรชี้ซ้าย
                        document.getElementById('purp-arrow').style.cssText = `left: ${pEndX + 2}px; top: ${pEndY - 6}px;`;
                    }

                } else if (linesContainer) {
                    linesContainer.classList.add('hidden'); 
                }
            }
            
            window.addEventListener('resize', drawFlowLines);
            window.onload = function() {
                setTimeout(drawFlowLines, 100); 
                setTimeout(drawFlowLines, 500);
            };
            
            // วาดใหม่เสมอเมื่อสั่งพิมพ์
            window.onbeforeprint = drawFlowLines;
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=2650, scrolling=True)
