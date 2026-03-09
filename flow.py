import streamlit.components.v1 as components

def render_flow():
    # โค้ด HTML สำหรับหน้า Flow ที่ออกแบบใหม่ด้วย Grid & Flexbox ที่รัดกุม 
    # อัปเดตล่าสุด: ย้ายกล่อง "ส่งข้อมูลให้ควบคุมโรค" ไปไว้ด้านล่างสุด 
    # และเพิ่มเส้นลูกศรสีม่วงโยงจากกล่อง REFER ลงมารวมที่ด้านล่างอย่างเป็นระบบ
    html_code = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
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
        </style>
    </head>
    <body>
        
        <!-- Header -->
        <div class="text-center mb-8 sm:mb-12">
            <h2 class="text-2xl sm:text-3xl md:text-4xl font-extrabold mb-2 tracking-wide" style="color: var(--text-main);">Flow การให้บริการ</h2>
            <p class="text-sm sm:text-base md:text-[1.15rem] font-bold" style="color: var(--text-main);">กรณีผู้ป่วยสงสัยตนเอง/ญาติได้รับผลกระทบจาก PM 2.5 จังหวัดเชียงใหม่</p>
        </div>

        <!-- Main Flow Container -->
        <div class="w-full max-w-6xl mx-auto flex flex-col md:flex-row gap-8 md:gap-12 relative z-10" id="main-flow-container">
            
            <!-- SVG Overlay สำหรับเส้นโยงข้ามคอลัมน์ -->
            <svg id="flow-svg" class="absolute inset-0 w-full h-full pointer-events-none z-[100] hidden md:block" style="filter: drop-shadow(0px 3px 5px rgba(0, 0, 0, 0.3));">
                <defs>
                    <marker id="arrow-red" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#dc2626" />
                    </marker>
                    <marker id="arrow-purple" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#9333ea" />
                    </marker>
                </defs>
                <!-- เส้นพื้นหลังตัดขอบ -->
                <path id="red-line-bg" fill="none" stroke="var(--bg-knockout)" stroke-width="10" stroke-linejoin="round" />
                <path id="purple-line-bg" fill="none" stroke="var(--bg-knockout)" stroke-width="10" stroke-linejoin="round" />
                <!-- เส้นตัวจริง -->
                <path id="red-line-path" fill="none" stroke="#dc2626" stroke-width="4" stroke-linejoin="round" marker-end="url(#arrow-red)" />
                <path id="purple-line-path" fill="none" stroke="#9333ea" stroke-width="4" stroke-linejoin="round" marker-end="url(#arrow-purple)" stroke-dasharray="6,4" />
            </svg>

            <!-- ================= LEFT COLUMN (ONLINE) ================= -->
            <div class="w-full md:w-[40%] flex flex-col items-center">
                <!-- 1. ปรึกษาออนไลน์ -->
                <div class="flex items-center gap-3 bg-blue-50 border-2 border-blue-300 rounded-full px-4 py-2 shadow-sm relative z-10">
                    <div class="bg-blue-600 text-white rounded-full w-8 h-8 sm:w-10 sm:h-10 flex items-center justify-center font-bold text-lg sm:text-xl shadow-inner">1</div>
                    <span class="text-blue-900 font-bold text-lg sm:text-xl pr-2">ปรึกษาออนไลน์</span>
                </div>
                <div class="line-v h-6"></div><div class="arrow-down"></div>
                
                <!-- หมอพร้อม -->
                <div class="bg-blue-50 border border-blue-200 rounded-2xl sm:rounded-full px-6 sm:px-8 py-3 shadow-sm text-center w-[90%] sm:w-auto z-10">
                    <p class="text-blue-900 font-bold text-[14px] sm:text-[15px] md:text-[16px] leading-snug card-text">ผ่านระบบหมอพร้อม/<br class="hidden sm:block">telemedicine ของโรงพยาบาล</p>
                </div>
                <div class="line-v h-6"></div><div class="arrow-down"></div>
                
                <!-- คัดกรอง -->
                <div class="bg-blue-200 border border-blue-300 rounded-full px-8 py-2 shadow-sm text-center z-10">
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
                        <div class="flex-1 flex flex-col items-center">
                            <div class="bg-green-50 border-[3px] border-green-600 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10">
                                <p class="text-green-800 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-tight card-text">ไม่เข้าข่าย/<br>อาการเล็กน้อย</p>
                            </div>
                            <div class="line-v h-4 my-1"></div>
                            <div class="bg-white border-2 border-green-500 rounded-lg p-2 shadow-sm text-center w-full flex-grow z-10">
                                <p class="text-green-700 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-snug card-text">ให้คำแนะนำ<br>การปฏิบัติตัว<br>และส่งต่อ<br>ทีม 3 หมอ</p>
                            </div>
                        </div>
                        
                        <!-- Right: เข้าข่าย -->
                        <div class="flex-1 flex flex-col items-center">
                            <div class="bg-emerald-200 border border-emerald-500 rounded-2xl sm:rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10">
                                <p class="text-emerald-900 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-tight card-text">เข้าข่าย<br>มีอาการที่สงสัย</p>
                            </div>
                            <div class="line-v h-4 my-1"></div>
                            <div class="bg-emerald-100 border border-emerald-200 rounded-lg p-2 shadow-sm text-left w-full flex-grow relative z-10">
                                <p class="text-emerald-900 font-bold text-[12px] sm:text-[13px] leading-snug mb-2 card-text">1. ส่งต่อเข้ารับบริการ<br>ที่รพ./รพ.สต./PCU หนองหาร</p>
                                <!-- กล่องต้นทางของเส้นสีแดง -->
                                <div id="red-source" class="bg-red-200 text-red-900 border border-red-400 px-2 py-1 rounded text-[12px] sm:text-[13px] font-bold leading-snug inline-block shadow-sm relative z-[110]">
                                    2. ถ้าอาการรุนแรง<br>ประสาน 1669
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ================= RIGHT COLUMN (ONSITE + SURVEILLANCE + CLINIC) ================= -->
            <div class="w-full md:w-[60%] flex flex-col items-center mt-10 md:mt-0 relative">
                
                <!-- ROW: Entry 2 & 3 -->
                <div class="w-[98%] sm:w-[95%] flex items-stretch gap-2 sm:gap-4 relative z-10">
                    
                    <!-- ====== Col 2: Onsite ====== -->
                    <div class="flex-[0.8] flex flex-col items-center h-full">
                        <!-- 2. เข้ารับบริการ -->
                        <div class="flex items-center justify-center gap-1 sm:gap-2 bg-pink-50 border-2 border-pink-200 rounded-full px-1 sm:px-2 py-2 shadow-sm z-10 w-[95%] sm:w-full h-[55px] sm:h-[65px]">
                            <div class="bg-pink-500 text-white rounded-full w-6 h-6 sm:w-8 sm:h-8 flex items-center justify-center font-bold text-sm sm:text-lg shadow-inner shrink-0">2</div>
                            <h3 class="text-pink-900 font-bold text-[12px] sm:text-[14px] md:text-[15px] leading-tight text-center">เข้ารับบริการ<br>ที่รพ./รพ.สต./PCU หนองหาร</h3>
                        </div>
                        <div class="line-v flex-grow min-h-[30px] sm:min-h-[40px]"></div>
                    </div>

                    <!-- ====== Col 3: Surveillance ====== -->
                    <div class="flex-[1.2] flex flex-col items-center h-full">
                        <!-- 3. การเฝ้าระวัง -->
                        <div class="flex items-center justify-center gap-1 sm:gap-2 bg-purple-50 border-2 border-purple-300 rounded-full px-2 py-2 shadow-sm z-10 w-[80%] sm:w-[75%] h-[55px] sm:h-[65px]">
                            <div class="bg-purple-600 text-white rounded-full w-6 h-6 sm:w-8 sm:h-8 flex items-center justify-center font-bold text-sm sm:text-lg shadow-inner shrink-0">3</div>
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
                    
                    <!-- ฝั่งขวา ห้องฉุกเฉิน (จะถูกโยงเข้าควบคุมโรคด้วยเส้นสีม่วง) -->
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
                    <div class="bg-orange-300 border-[3px] border-orange-500 rounded-3xl sm:rounded-full px-3 sm:px-6 py-3 shadow-md text-center w-[95%] sm:w-[90%] z-10">
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
                            <div class="flex-1 flex flex-col items-center px-1 sm:px-2">
                                <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10">
                                    <p class="text-orange-900 font-bold text-[12px] sm:text-[13px] md:text-[14px]">ให้ยากลับบ้าน</p>
                                </div>
                            </div>
                            <div class="flex-1 flex flex-col items-center px-1 sm:px-2">
                                <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10">
                                    <p class="text-orange-900 font-bold text-[12px] sm:text-[13px] md:text-[14px] leading-tight">Admit<br>ให้การรักษา</p>
                                </div>
                            </div>
                            <div class="flex-1 flex flex-col items-center px-1 sm:px-2">
                                <div class="bg-orange-200 border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full flex-grow flex items-center justify-center relative z-10">
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
                        
                        <!-- NEW PLACEMENT: ส่งข้อมูลควบคุมโรค (อยู่ล่างสุด รับข้อมูลต่อจาก Post Care และ ER) -->
                        <div class="line-v h-6 sm:h-8 relative z-0 mx-auto"></div>
                        <div class="arrow-down relative z-0 mx-auto"></div>
                        
                        <div id="disease-control-box" class="w-full bg-purple-100 border-[2px] border-purple-400 rounded-xl p-3 sm:p-4 shadow-md mt-1 relative z-10 text-center">
                            <p class="text-purple-900 font-bold text-[13px] sm:text-[14px] md:text-[15px] leading-snug card-text">
                                ทีมคลินิกมลพิษ แจ้งข้อมูลแก่ ควบคุมโรค เพื่อซักประวัติ+รายงาน สสจ. ทราบ)<br class="hidden sm:block">
                            </p>
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <!-- Script สำหรับวาดเส้นโยง SVG -->
        <script>
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
                    const redBg = document.getElementById('red-line-bg');
                    
                    if (redSrc && redTgt && redPath) {
                        const rSrcRect = redSrc.getBoundingClientRect();
                        const rTgtRect = redTgt.getBoundingClientRect();
                        
                        const rStartX = rSrcRect.right - svgRect.left;
                        const rStartY = rSrcRect.top + (rSrcRect.height / 2) - svgRect.top;
                        const rEndX = rTgtRect.left + (rTgtRect.width / 2) - svgRect.left;
                        const rEndY = rTgtRect.top - svgRect.top - 8;
                        
                        const gutterX = rStartX + 25; 
                        const safeY = rEndY - 40;
                        
                        const dRed = `M ${rStartX} ${rStartY} L ${gutterX} ${rStartY} L ${gutterX} ${safeY} L ${rEndX} ${safeY} L ${rEndX} ${rEndY}`;
                        redPath.setAttribute('d', dRed);
                        if(redBg) redBg.setAttribute('d', dRed);
                    }

                    // 2. เส้นม่วง (ส่ง REFER -> แจ้งควบคุมโรค สสจ.)
                    const referBox = document.getElementById('er-refer-box');
                    const dcBox = document.getElementById('disease-control-box');
                    const pLinePath = document.getElementById('purple-line-path');
                    const pLineBg = document.getElementById('purple-line-bg');
                    
                    if (referBox && dcBox && pLinePath) {
                        const refRect = referBox.getBoundingClientRect();
                        const dcRect = dcBox.getBoundingClientRect();
                        
                        const pStartX = refRect.right - svgRect.left;
                        const pStartY = refRect.top + (refRect.height / 2) - svgRect.top;
                        const pEndX = dcRect.right - svgRect.left;
                        const pEndY = dcRect.top + (dcRect.height / 2) - svgRect.top;
                        
                        // ลากออกทางขวาให้พ้นกรอบ แล้วดิ่งลงมาหาเป้าหมาย
                        const pGutterX = Math.max(pStartX + 30, pEndX + 30); 
                        
                        const dPurple = `M ${pStartX} ${pStartY} L ${pGutterX} ${pStartY} L ${pGutterX} ${pEndY} L ${pEndX + 8} ${pEndY}`;
                        pLinePath.setAttribute('d', dPurple);
                        if(pLineBg) pLineBg.setAttribute('d', dPurple);
                    }

                } else if (svg) {
                    svg.classList.add('hidden'); // ซ่อนในมือถือ
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
    
    components.html(html_code, height=2650, scrolling=True)
