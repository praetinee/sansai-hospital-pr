import streamlit.components.v1 as components

def render_roles():
    # โค้ด HTML สำหรับหน้าบทบาทหน่วยงาน สร้างเป็น Flow 3 คอลัมน์ (รุก, รับ, ส่งต่อ) ตามภาพต้นฉบับ
    html_code = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body { 
                font-family: 'Sarabun', sans-serif !important; 
                background-color: transparent; 
                margin: 0; 
                padding: 1rem; 
                color: #334155;
            }
            .flow-box {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .flow-box:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            }
            .badge-z58 {
                background-color: #1f4e3d;
                color: white;
                font-size: 0.7rem;
                font-weight: bold;
                padding: 2px 8px;
                border-radius: 9999px;
                white-space: nowrap;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            /* Dark Mode Adapts */
            @media (prefers-color-scheme: dark) {
                body { color: #e2e8f0; }
                .text-dark-adapt { color: #1e293b; } /* Keep texts inside colored boxes dark for readability */
            }
        </style>
    </head>
    <body>
        
        <div class="max-w-7xl mx-auto relative pb-16" id="main-container">
            
            <!-- Top Alert Badge -->
            <div class="flex justify-center lg:justify-end mb-6 relative z-20">
                <div class="bg-[#1f4e3d] text-white px-5 py-2.5 rounded-full font-bold shadow-lg text-sm sm:text-base flex items-center gap-2 border border-[#14362a]">
                    <i data-lucide="alert-circle" class="w-5 h-5 text-yellow-300"></i>
                    ย้ำ! บันทึกรหัสโรค Z58.1 (Exposure to air pollution) ทุกจุดบริการเพื่อวิเคราะห์ข้อมูล
                </div>
            </div>

            <!-- SVG Lines Overlay (Desktop Only) -->
            <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden lg:block z-0" style="filter: drop-shadow(0px 2px 3px rgba(0,0,0,0.2));">
                <defs>
                    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#2d6a4f" />
                    </marker>
                </defs>
                <path id="path-l-m" fill="none" stroke="#2d6a4f" stroke-width="4" marker-end="url(#arrow-green)" />
                <path id="path-m-r" fill="none" stroke="#2d6a4f" stroke-width="4" marker-end="url(#arrow-green)" />
                <path id="path-return" fill="none" stroke="#2d6a4f" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-green)" />
            </svg>

            <!-- Bottom Return Arrow Text (Dynamically Positioned) -->
            <div id="text-return" class="absolute hidden lg:flex items-center justify-center font-bold text-[#1f4e3d] bg-white px-4 py-1.5 rounded-full border-2 border-[#2d6a4f] text-sm z-10 shadow-md">
                การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
            </div>

            <!-- Flow Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-10">

                <!-- ================= LEFT: ชุมชน (รุก) ================= -->
                <div class="lg:col-span-3 bg-[#eef6d8] rounded-[2rem] border-2 border-[#d5e8b5] p-4 sm:p-5 shadow-sm flow-box flex flex-col h-full" id="box-left">
                    <h3 class="text-[#3f5e1f] text-lg sm:text-xl font-extrabold text-center mb-5 pb-3 border-b-2 border-[#d5e8b5]">ชุมชนและหน่วยบริการปฐมภูมิ (รุก)</h3>
                    
                    <div class="flex-grow space-y-4">
                        <!-- 3 หมอ -->
                        <div class="bg-white/70 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
                            <div class="bg-[#d5e8b5] p-2 rounded-full mb-2"><i data-lucide="users" class="w-6 h-6 text-[#3f5e1f]"></i></div>
                            <p class="font-bold text-[#3f5e1f] text-dark-adapt">กลไก 3 หมอ</p>
                        </div>
                        
                        <!-- เชิงรุก -->
                        <div class="bg-white/70 rounded-xl p-3 shadow-sm flex items-start gap-3">
                            <i data-lucide="clipboard-check" class="w-5 h-5 text-[#4a7c59] shrink-0 mt-0.5"></i>
                            <div>
                                <p class="font-bold text-[#3f5e1f] text-sm mb-1 text-dark-adapt">การลงพื้นที่เชิงรุก: อสม. และ รพ.สต.</p>
                                <p class="text-xs text-slate-700 leading-snug">เคาะประตูบ้านคัดกรองสุขภาพ (SCPM-66/QAP-F4) เน้น 4 กลุ่มเปราะบาง (ติดเตียง/ผู้สูงอายุ/ตั้งครรภ์/เด็กเล็ก)</p>
                            </div>
                        </div>

                        <!-- พื้นที่ปลอดภัย -->
                        <div class="bg-white/70 rounded-xl p-3 shadow-sm flex items-start gap-3">
                            <i data-lucide="shield-check" class="w-5 h-5 text-[#4a7c59] shrink-0 mt-0.5"></i>
                            <div>
                                <p class="font-bold text-[#3f5e1f] text-sm mb-1 text-dark-adapt">สนับสนุนพื้นที่ปลอดภัย</p>
                                <p class="text-xs text-slate-700 leading-snug">แจกหน้ากาก N95, จัดทำมุ้งสู้ฝุ่นให้ผู้ป่วยติดเตียง, ห้องปลอดฝุ่นในศูนย์เด็กเล็ก/โรงเรียน</p>
                            </div>
                        </div>

                        <!-- จัดส่งยา -->
                        <div class="bg-white/70 rounded-xl p-3 shadow-sm flex items-start gap-3">
                            <i data-lucide="truck" class="w-5 h-5 text-[#4a7c59] shrink-0 mt-0.5"></i>
                            <div>
                                <p class="font-bold text-[#3f5e1f] text-sm mb-1 text-dark-adapt">จัดส่งยาถึงบ้าน</p>
                                <p class="text-xs text-slate-700 leading-snug">สำหรับผู้ป่วยโรคเรื้อรังที่อาการคงที่ ลดความเสี่ยงสัมผัสฝุ่น</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Mobile Arrow (Visible only on small screens) -->
                <div class="lg:hidden flex justify-center py-1">
                    <i data-lucide="arrow-down" class="text-[#2d6a4f] w-8 h-8"></i>
                </div>

                <!-- ================= MIDDLE: รับ ================= -->
                <div class="lg:col-span-6 bg-[#fdf1e1] rounded-[2rem] border-2 border-[#f6cda3] p-4 sm:p-6 shadow-sm flow-box flex flex-col h-full" id="box-mid">
                    <h3 class="text-[#8b572a] text-lg sm:text-xl font-extrabold text-center mb-5 pb-3 border-b-2 border-[#f6cda3]">การรับผู้ป่วยและดูแลรักษา (รับ)</h3>
                    
                    <div class="flex-grow space-y-4">
                        
                        <!-- Row 1: ก่อนถึง รพ. -->
                        <div class="bg-white/60 rounded-xl p-3 shadow-sm border border-orange-100">
                            <p class="font-bold text-[#8b572a] text-xs sm:text-sm mb-2 text-dark-adapt">ระบบก่อนถึง รพ.และออนไลน์</p>
                            <div class="flex flex-col sm:flex-row items-center gap-2 sm:gap-4 text-center">
                                <div class="flex-1 bg-white p-2 rounded-lg shadow-sm w-full sm:w-auto flex flex-col items-center justify-center">
                                    <i data-lucide="smartphone" class="w-5 h-5 text-orange-500 mb-1"></i>
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-medium">คลินิกมลพิษออนไลน์ ผ่าน Line OA (@PM2.5) หรือ หมอพร้อม</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 text-orange-400 hidden sm:block"></i>
                                <i data-lucide="arrow-down" class="w-4 h-4 text-orange-400 sm:hidden"></i>
                                <div class="flex-1 bg-white p-2 rounded-lg shadow-sm w-full sm:w-auto flex items-center justify-center">
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-bold">ประเมินเบื้องต้น & Telemedicine</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 2: OPD -->
                        <div class="bg-white/60 rounded-xl p-3 shadow-sm border border-orange-100 relative">
                            <div class="flex justify-between items-center mb-2">
                                <p class="font-bold text-[#8b572a] text-xs sm:text-sm text-dark-adapt">ผู้ป่วยนอก (OPD) & คลินิกมลพิษ</p>
                                <span class="badge-z58">ลงรหัส Z58.1</span>
                            </div>
                            <div class="flex flex-col sm:flex-row items-center gap-2 text-center">
                                <div class="flex-1 bg-white p-2 rounded-lg shadow-sm w-full flex flex-col items-center justify-center">
                                    <i data-lucide="eye" class="w-5 h-5 text-orange-500 mb-1"></i>
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-medium">คัดกรองอาการ<br>(พื้นที่ PM2.5 > 37.5)</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 text-orange-400 hidden sm:block shrink-0"></i>
                                <i data-lucide="arrow-down" class="w-4 h-4 text-orange-400 sm:hidden shrink-0"></i>
                                <div class="flex-[0.8] bg-white p-2 rounded-lg shadow-sm w-full flex items-center justify-center">
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-bold">ส่งเข้า Pollution Clinic</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 text-orange-400 hidden sm:block shrink-0"></i>
                                <i data-lucide="arrow-down" class="w-4 h-4 text-orange-400 sm:hidden shrink-0"></i>
                                <div class="flex-1 bg-white p-2 rounded-lg shadow-sm w-full flex items-center justify-center">
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-medium">จ่ายยา/แนะนำ นัดติดตามหลัง 7 วัน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 3: ER -->
                        <div class="bg-white/60 rounded-xl p-3 shadow-sm border border-orange-100 relative">
                            <div class="flex justify-between items-center mb-2">
                                <p class="font-bold text-[#8b572a] text-xs sm:text-sm text-dark-adapt">ผู้ป่วยฉุกเฉิน (ER) และระบบ 1669</p>
                                <span class="badge-z58">ลงรหัส Z58.1</span>
                            </div>
                            <div class="flex flex-col sm:flex-row items-center gap-2 text-center">
                                <div class="flex-1 bg-white p-2 rounded-lg shadow-sm w-full flex flex-col items-center justify-center">
                                    <i data-lucide="ambulance" class="w-5 h-5 text-orange-500 mb-1"></i>
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-medium">อาการกำเริบรุนแรง<br>(หอบหืด, COPD, MI, Stroke)</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 text-orange-400 hidden sm:block shrink-0"></i>
                                <i data-lucide="arrow-down" class="w-4 h-4 text-orange-400 sm:hidden shrink-0"></i>
                                <div class="flex-[0.8] bg-white p-2 rounded-lg shadow-sm w-full flex items-center justify-center">
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-bold">1669 จัดชุด EMS รับเข้า ER</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 text-orange-400 hidden sm:block shrink-0"></i>
                                <i data-lucide="arrow-down" class="w-4 h-4 text-orange-400 sm:hidden shrink-0"></i>
                                <div class="flex-1 bg-white p-2 rounded-lg shadow-sm w-full flex items-center justify-center">
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-medium">ประเมิน Admit หรือ กลับบ้าน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 4: IPD -->
                        <div class="bg-white/60 rounded-xl p-3 shadow-sm border border-orange-100 relative">
                            <div class="flex justify-between items-center mb-2">
                                <p class="font-bold text-[#8b572a] text-xs sm:text-sm text-dark-adapt">ผู้ป่วยใน (IPD)</p>
                                <span class="badge-z58">ลงรหัส Z58.1</span>
                            </div>
                            <div class="flex flex-col sm:flex-row items-center gap-2 text-center">
                                <div class="flex-1 bg-white p-2 rounded-lg shadow-sm w-full flex flex-col items-center justify-center">
                                    <i data-lucide="bed" class="w-5 h-5 text-orange-500 mb-1"></i>
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-medium">รับ Admit เข้าหอผู้ป่วย</p>
                                </div>
                                <i data-lucide="arrow-right" class="w-4 h-4 text-orange-400 hidden sm:block"></i>
                                <i data-lucide="arrow-down" class="w-4 h-4 text-orange-400 sm:hidden"></i>
                                <div class="flex-1 bg-white p-2 rounded-lg shadow-sm w-full flex items-center justify-center">
                                    <p class="text-[11px] sm:text-[12px] leading-tight text-slate-700 font-bold">พยาบาลซักประวัติเพิ่มเติม</p>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- Mobile Arrow -->
                <div class="lg:hidden flex justify-center py-1">
                    <i data-lucide="arrow-down" class="text-[#2d6a4f] w-8 h-8"></i>
                </div>

                <!-- ================= RIGHT: ส่งต่อ ================= -->
                <div class="lg:col-span-3 bg-[#e8f1e6] rounded-[2rem] border-2 border-[#bad4b8] p-4 sm:p-5 shadow-sm flow-box flex flex-col h-full" id="box-right">
                    <h3 class="text-[#2d562f] text-lg sm:text-xl font-extrabold text-center mb-5 pb-3 border-b-2 border-[#bad4b8]">ระบบส่งต่อและจำหน่ายผู้ป่วย (ส่งต่อ)</h3>
                    
                    <div class="flex-grow space-y-4 flex flex-col">
                        
                        <!-- Referral Box -->
                        <div class="bg-[#f9e1e1] rounded-xl border border-[#efa1a1] p-4 shadow-sm flex-1 flex flex-col items-center text-center">
                            <p class="font-bold text-[#8c2d2d] text-sm mb-3 border-b border-[#efa1a1] pb-2 w-full text-dark-adapt">ระบบส่งต่อผู้ป่วย<br>(Referral System)</p>
                            <i data-lucide="hospital" class="w-8 h-8 text-[#8c2d2d] mb-2"></i>
                            <p class="text-[12px] text-slate-800 font-medium mb-2 leading-snug">รพช.ประเมินการสำรองเตียงพร้อมรับ และ Ventilatorพร้อมใช้</p>
                            <i data-lucide="arrow-down" class="w-4 h-4 text-[#8c2d2d] mb-2"></i>
                            <p class="text-[12px] text-slate-800 font-bold leading-snug bg-white/50 px-2 py-1 rounded">หาก Overcapacity ส่งต่อโรงพยาบาลลำพูน</p>
                        </div>

                        <!-- Discharge Box -->
                        <div class="bg-[#d9ead3] rounded-xl border border-[#a8cfa0] p-4 shadow-sm flex-1 flex flex-col justify-center text-center relative z-20" id="box-discharge">
                            <p class="font-bold text-[#385d30] text-sm mb-3 border-b border-[#a8cfa0] pb-2 w-full text-dark-adapt">การจำหน่ายผู้ป่วย<br>(Discharge)</p>
                            <p class="text-[13px] text-slate-800 font-bold mb-2">วางแผนตามหลัก D-METHOD</p>
                            <div class="bg-white/50 rounded p-2 mt-auto">
                                <p class="text-[12px] text-slate-700 leading-snug">ประสานทีมเยี่ยมบ้านและอาชีวอนามัย ประเมินสภาพที่อยู่อาศัยไม่ให้กำเริบซ้ำ</p>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- Mobile Return Arrow Placeholder -->
                <div class="lg:hidden flex flex-col items-center py-4 text-center">
                    <i data-lucide="arrow-down" class="text-[#1f4e3d] w-6 h-6 mb-1"></i>
                    <p class="font-bold text-[#1f4e3d] text-sm bg-white px-3 py-1 rounded-full border border-[#1f4e3d]">การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ</p>
                    <i data-lucide="arrow-down" class="text-[#1f4e3d] w-6 h-6 mt-1"></i>
                    <p class="text-xs text-slate-500 mt-1">(วนกลับไปสู่หน่วยบริการชุมชน)</p>
                </div>

            </div>
        </div>

        <script>
            // สร้างไอคอน
            document.addEventListener('DOMContentLoaded', () => {
                lucide.createIcons();
            });

            // ฟังก์ชันวาดเส้นเชื่อมโยงแบบเจาะจงเมื่อแสดงผลบนคอมพิวเตอร์
            function drawLines() {
                const svg = document.getElementById('flow-svg');
                const pathLM = document.getElementById('path-l-m');
                const pathMR = document.getElementById('path-m-r');
                const pathReturn = document.getElementById('path-return');
                const textReturn = document.getElementById('text-return');

                const boxL = document.getElementById('box-left');
                const boxM = document.getElementById('box-mid');
                const boxR = document.getElementById('box-right');
                const boxDischarge = document.getElementById('box-discharge');
                const container = document.getElementById('main-container');

                // ทำงานเฉพาะหน้าจอใหญ่ (lg breakpoint ของ Tailwind คือ 1024px)
                if(window.innerWidth >= 1024 && boxL && boxM && boxR && svg && container) {
                    svg.classList.remove('hidden');
                    textReturn.classList.remove('hidden');

                    const contRect = container.getBoundingClientRect();
                    const lRect = boxL.getBoundingClientRect();
                    const mRect = boxM.getBoundingClientRect();
                    const rRect = boxR.getBoundingClientRect();
                    const dRect = boxDischarge.getBoundingClientRect();

                    // 1. เส้นจาก ซ้าย (รุก) -> กลาง (รับ)
                    const lmStartX = lRect.right - contRect.left;
                    const lmStartY = (lRect.top - contRect.top) + lRect.height / 2;
                    const lmEndX = mRect.left - contRect.left;
                    pathLM.setAttribute('d', `M ${lmStartX} ${lmStartY} L ${lmEndX - 10} ${lmStartY}`);

                    // 2. เส้นจาก กลาง (รับ) -> ขวา (ส่งต่อ)
                    const mrStartX = mRect.right - contRect.left;
                    const mrStartY = (mRect.top - contRect.top) + mRect.height / 2;
                    const mrEndX = rRect.left - contRect.left;
                    pathMR.setAttribute('d', `M ${mrStartX} ${mrStartY} L ${mrEndX - 10} ${mrStartY}`);

                    // 3. เส้นโค้งย้อนกลับด้านล่าง การจำหน่าย -> ชุมชน
                    const retStartX = (dRect.left - contRect.left) + dRect.width / 2;
                    const retStartY = dRect.bottom - contRect.top;
                    const retEndX = (lRect.left - contRect.left) + lRect.width / 2;
                    const retEndY = lRect.bottom - contRect.top;
                    
                    // หากรอบล่างสุดเพื่อเว้นระยะไม่ให้ทับกล่อง
                    const dropY = Math.max(retStartY, retEndY) + 40; 

                    // วาด Path: ลงล่าง -> ซ้ายยาวๆ -> ขึ้นบน -> ชี้เข้ากล่องซ้าย
                    pathReturn.setAttribute('d', `M ${retStartX} ${retStartY} L ${retStartX} ${dropY} L ${retEndX} ${dropY} L ${retEndX} ${retEndY + 12}`);

                    // 4. จัดตำแหน่งป้ายข้อความลอยทับเส้นย้อนกลับตรงกึ่งกลางจอ
                    const textCenterX = (retStartX + retEndX) / 2;
                    textReturn.style.left = `${textCenterX}px`;
                    textReturn.style.top = `${dropY}px`;
                    textReturn.style.transform = 'translate(-50%, -50%)';

                } else {
                    // ปิดการแสดงผลบนหน้าจอเล็ก ปล่อยให้มันเรียงซ้อนกันเป็นแนวตั้งตามธรรมชาติ
                    if(svg) svg.classList.add('hidden');
                    if(textReturn) textReturn.classList.add('hidden');
                }
            }

            window.addEventListener('resize', drawLines);
            window.onload = () => { 
                setTimeout(drawLines, 100); 
                setTimeout(drawLines, 500); 
            };
        </script>
    </body>
    </html>
    """
    
    # กำหนดความสูงให้เหมาะสมกับ Flow 3 คอลัมน์ที่รายละเอียดเยอะ
    components.html(html_code, height=1350, scrolling=True)
