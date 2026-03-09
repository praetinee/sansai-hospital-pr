import streamlit.components.v1 as components

def render_flow():
    # โค้ด HTML สำหรับหน้า Flow ที่ออกแบบใหม่ด้วย Flexbox ที่รัดกุม 
    # แก้ปัญหาเส้นขาด/ทับซ้อน และใช้ SVG ในการวาดเส้นโยงข้ามคอลัมน์
    html_code = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;700;800&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Sarabun', sans-serif; background-color: #fdfbf5; margin: 0; padding: 2rem 1rem; }
        </style>
    </head>
    <body>
        
        <!-- Header -->
        <div class="text-center mb-8">
            <h2 class="text-3xl font-extrabold text-[#1e3a8a] mb-2 tracking-wide">Flow การให้บริการ</h2>
            <p class="text-[1.15rem] font-bold text-[#1e3a8a]">กรณีผู้ป่วยสงสัยตนเอง/ญาติได้รับผลกระทบจาก PM 2.5 จังหวัดเชียงใหม่</p>
        </div>

        <!-- Main Flow Container -->
        <div class="w-full max-w-6xl mx-auto flex flex-col md:flex-row gap-8 relative z-10" id="main-flow-container">
            
            <!-- SVG Red Line Overlay (วาดเส้นเชื่อมสีแดงอัตโนมัติ) -->
            <svg id="flow-svg" class="absolute inset-0 w-full h-full pointer-events-none z-0 hidden md:block">
                <defs>
                    <marker id="arrow-red" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#dc2626" />
                    </marker>
                </defs>
                <path id="red-line-path" fill="none" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow-red)" />
            </svg>

            <!-- ================= LEFT COLUMN (ONLINE) ================= -->
            <div class="w-full md:w-[45%] flex flex-col items-center">
                <!-- 1. ปรึกษาออนไลน์ -->
                <div class="flex items-center gap-3 bg-[#e0e7ff] border-2 border-blue-300 rounded-full px-4 py-2 shadow-sm">
                    <div class="bg-[#2563eb] text-white rounded-full w-9 h-9 flex items-center justify-center font-bold text-xl shadow-inner">1</div>
                    <span class="text-[#1e3a8a] font-bold text-xl pr-2">ปรึกษาออนไลน์</span>
                </div>
                <div class="w-[3px] h-6 bg-slate-800"></div><div class="w-0 h-0 border-l-[6px] border-r-[6px] border-t-[8px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                
                <!-- หมอพร้อม -->
                <div class="bg-[#e0e7ff] border border-blue-200 rounded-full px-8 py-3 shadow-sm text-center">
                    <p class="text-[#1e40af] font-bold text-[15px] sm:text-[16px] leading-snug">ผ่านระบบหมอพร้อม/<br>telemedicine ของโรงพยาบาล</p>
                </div>
                <div class="w-[3px] h-6 bg-slate-800"></div><div class="w-0 h-0 border-l-[6px] border-r-[6px] border-t-[8px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                
                <!-- คัดกรอง -->
                <div class="bg-[#93c5fd] border border-blue-300 rounded-full px-8 py-2 shadow-sm text-center">
                    <p class="text-[#1e3a8a] font-bold text-[15px] sm:text-[16px]">ทำการคัดกรอง</p>
                </div>
                <div class="w-[3px] h-6 bg-slate-800"></div>
                
                <!-- 2-way Split -->
                <div class="w-full flex flex-col items-center">
                    <div class="w-[60%] border-t-[3px] border-slate-800 flex justify-between">
                        <div class="w-[3px] h-6 bg-slate-800"></div>
                        <div class="w-[3px] h-6 bg-slate-800"></div>
                    </div>
                    
                    <div class="w-[95%] sm:w-[85%] flex gap-3 sm:gap-6 items-stretch">
                        <!-- Left: ไม่เข้าข่าย -->
                        <div class="flex-1 flex flex-col items-center">
                            <div class="bg-white border-[3px] border-[#16a34a] rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full">
                                <p class="text-[#166534] font-bold text-[13px] sm:text-[14px] leading-tight">ไม่เข้าข่าย/<br>อาการเล็กน้อย</p>
                            </div>
                            <div class="w-[3px] h-4 bg-slate-800 my-1"></div>
                            <div class="bg-white border-2 border-[#22c55e] rounded-lg p-2 shadow-sm text-center w-full flex-grow">
                                <p class="text-[#15803d] font-bold text-[13px] sm:text-[14px] leading-snug">ให้คำแนะนำ<br>การปฏิบัติตัว<br>และส่งต่อ<br>ทีม 3 หมอ</p>
                            </div>
                        </div>
                        
                        <!-- Right: เข้าข่าย -->
                        <div class="flex-1 flex flex-col items-center">
                            <div class="bg-[#86efac] border border-green-400 rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full">
                                <p class="text-[#14532d] font-bold text-[13px] sm:text-[14px] leading-tight">เข้าข่าย<br>มีอาการที่สงสัย</p>
                            </div>
                            <div class="w-[3px] h-4 bg-slate-800 my-1"></div>
                            <div class="bg-[#86efac] rounded-lg p-2 shadow-sm text-left w-full flex-grow relative">
                                <p class="text-[#064e3b] font-bold text-[13px] leading-snug mb-2">1. ส่งต่อเข้ารับบริการ<br>ที่รพ./รพ.สต.</p>
                                <!-- กล่องต้นทางของเส้นสีแดง -->
                                <div id="red-source" class="bg-[#fca5a5] text-[#7f1d1d] px-2 py-1 rounded text-[13px] font-bold leading-snug inline-block shadow-sm">
                                    2. ถ้าอาการรุนแรง<br>ประสาน 1669
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ================= RIGHT COLUMN (ONSITE + CLINIC) ================= -->
            <div class="w-full md:w-[55%] flex flex-col items-center mt-12 md:mt-0 relative">
                <!-- 2. เข้ารับบริการ -->
                <div class="flex items-center gap-3 bg-[#fce7f3] border-2 border-pink-200 rounded-full px-4 py-2 shadow-sm">
                    <div class="bg-[#d946ef] text-white rounded-full w-9 h-9 flex items-center justify-center font-bold text-xl shadow-inner">2</div>
                    <h3 class="text-[#831843] font-bold text-xl pr-2 leading-tight text-center">เข้ารับบริการ<br><span class="text-lg">ที่รพ./รพ.สต.</span></h3>
                </div>
                <div class="w-[3px] h-6 bg-slate-800"></div><div class="w-0 h-0 border-l-[6px] border-r-[6px] border-t-[8px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                
                <!-- ซักประวัติ -->
                <div class="bg-[#fbcfe8] border border-pink-300 rounded-[2rem] px-5 py-3 shadow-sm text-center w-[90%] sm:w-[80%]">
                    <p class="text-[#831843] font-bold text-[14px] sm:text-[15px] leading-snug">เจ้าหน้าที่ซักประวัติ/อาการเบื้องต้น<br>และลงแบบคัดกรองสอบสวนโรค<br>ที่เกิดจาก PM2.5</p>
                </div>
                <div class="w-[3px] h-8 bg-slate-800"></div>
                
                <!-- 3-way Split -->
                <div class="w-[85%] border-t-[3px] border-slate-800 flex justify-between">
                    <div class="w-[3px] h-6 bg-slate-800"></div>
                    <div class="w-[3px] h-6 bg-slate-800"></div>
                    <div class="w-[3px] h-6 bg-slate-800"></div>
                </div>
                
                <div class="w-[95%] flex gap-2 sm:gap-3 items-stretch relative z-10">
                    <!-- Left: กรณีไม่เข้าข่าย -->
                    <div class="flex-1 flex flex-col items-center h-full">
                        <div class="bg-white border-[3px] border-[#1e3a8a] rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full">
                            <p class="text-[#1e3a8a] font-bold text-[12px] sm:text-[13px] leading-tight">กรณี<br>ไม่เข้าข่าย</p>
                        </div>
                        <div class="w-[3px] h-4 bg-slate-800 my-1"></div>
                        <div class="bg-white border-2 border-[#1e3a8a] rounded-lg p-2 shadow-sm text-center w-full h-full">
                            <p class="text-[#1e3a8a] font-bold text-[12px] sm:text-[13px] leading-snug">ส่งตรวจคลินิก<br>ตามอาการของโรค</p>
                        </div>
                    </div>
                    
                    <!-- Middle: เข้าข่าย อาการเล็กน้อย -->
                    <div class="flex-[1.2] flex flex-col items-center h-full">
                        <div class="bg-[#fed7aa] border-[3px] border-orange-400 rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full z-10">
                            <p class="text-[#9a3412] font-bold text-[12px] sm:text-[13px] leading-tight">เข้าข่าย<br>อาการเล็กน้อย<br>/ปานกลาง</p>
                        </div>
                        <!-- Flex-grow จะทำให้เส้นยาวยืดลงไปชนกับกล่องคลินิกมลพิษด้านล่างพอดีเป๊ะ! -->
                        <div class="w-[3px] flex-grow bg-slate-800 min-h-[20px]"></div>
                    </div>
                    
                    <!-- Right: ผู้ป่วยอาการรุนแรง -->
                    <div class="flex-1 flex flex-col items-center h-full relative">
                        <!-- เป้าหมายรับเส้นสีแดง -->
                        <div id="red-target" class="w-full relative">
                            <!-- เพิ่มที่ว่างด้านบนเล็กน้อยให้ลูกศรสีแดงชี้ลงมาได้ -->
                            <div class="absolute -top-3 w-full h-[1px]"></div>
                            <div class="bg-[#fca5a5] border-[3px] border-red-500 rounded-full py-2 px-1 shadow-sm text-center w-full">
                                <p class="text-[#7f1d1d] font-bold text-[12px] sm:text-[13px] leading-tight">ผู้ป่วย<br>อาการรุนแรง</p>
                            </div>
                        </div>
                        <div class="w-[3px] h-4 bg-slate-800 my-1"></div>
                        <div class="bg-[#ef4444] rounded-sm p-2 shadow-sm text-center w-[90%]">
                            <p class="text-white font-bold text-[12px] sm:text-[13px] leading-tight">ส่งเข้า<br>ห้องฉุกเฉิน</p>
                        </div>
                        <div class="w-[3px] h-4 bg-slate-800 my-1"></div>
                        <div class="bg-[#ef4444] rounded-sm p-2 shadow-sm text-center w-[90%] h-full">
                            <p class="text-white font-bold text-[12px] sm:text-[13px] leading-tight">ส่ง REFER</p>
                        </div>
                    </div>
                </div>

                <!-- ================= CLINIC SECTION (อยู่ในคอลัมน์ขวาเพื่อให้จัดกึ่งกลางเส้นพอดี) ================= -->
                <div class="w-full flex flex-col items-center relative z-20 mt-[-1px]">
                    <div class="bg-[#fdba74] border-[3px] border-orange-400 rounded-full px-4 sm:px-8 py-3 shadow-md text-center w-[95%] z-10">
                        <h3 class="text-[#7c2d12] font-bold text-[16px] sm:text-[18px] leading-tight mb-1">ส่งเข้าคลินิกมลพิษ เฉพาะรพ.</h3>
                        <p class="text-[#9a3412] font-bold text-[13px] sm:text-[14px]">(กรณีรพ.สต.ให้ส่งต่อรพ.)</p>
                    </div>
                    
                    <div class="w-[3px] h-6 bg-slate-800"></div>
                    
                    <div class="bg-[#ffedd5] border-[2px] border-orange-200 rounded-lg px-6 py-3 shadow-sm text-center w-[90%] sm:w-[85%]">
                        <p class="text-[#7c2d12] font-bold text-[14px] sm:text-[15px] leading-snug">ซักประวัติ/ตรวจร่างกาย/<br>ตรวจทางห้องปฏิบัติการ<br>โดยแพทย์/สหวิชาชีพ</p>
                    </div>
                    
                    <div class="w-[3px] h-6 bg-slate-800"></div>
                    
                    <div class="bg-[#fed7aa] border-[2px] border-orange-300 rounded-lg px-10 py-2 shadow-sm text-center w-fit">
                        <p class="text-[#7c2d12] font-bold text-[15px] sm:text-[16px]">วางแผนการรักษา</p>
                    </div>
                    
                    <div class="w-[3px] h-6 bg-slate-800"></div>
                    
                    <!-- Clinic 3-Way Split Outcomes -->
                    <div class="w-[90%] sm:w-[85%] relative flex flex-col items-center">
                        <!-- สะพานแยก 3 ทาง -->
                        <div class="w-[70%] sm:w-[66.66%] border-t-[3px] border-slate-800 flex justify-between">
                            <div class="w-[3px] h-6 bg-slate-800"></div>
                            <div class="w-[3px] h-6 bg-slate-800"></div>
                            <div class="w-[3px] h-6 bg-slate-800"></div>
                        </div>
                        
                        <div class="w-full flex gap-2 sm:gap-4 items-stretch">
                            <!-- Home -->
                            <div class="flex-1 flex flex-col items-center">
                                <div class="bg-[#fed7aa] border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full h-full flex items-center justify-center">
                                    <p class="text-[#7c2d12] font-bold text-[13px] sm:text-[14px]">ให้ยากลับบ้าน</p>
                                </div>
                                <div class="w-[3px] h-8 bg-slate-800"></div>
                            </div>
                            <!-- Admit -->
                            <div class="flex-1 flex flex-col items-center">
                                <div class="bg-[#fed7aa] border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full h-full flex items-center justify-center">
                                    <p class="text-[#7c2d12] font-bold text-[13px] sm:text-[14px] leading-tight">Admit<br>ให้การรักษา</p>
                                </div>
                                <div class="w-[3px] h-8 bg-slate-800"></div>
                            </div>
                            <!-- Refer -->
                            <div class="flex-1 flex flex-col items-center">
                                <div class="bg-[#fed7aa] border-[2px] border-orange-300 rounded-md p-2 shadow-sm text-center w-full h-[80%] flex items-center justify-center">
                                    <p class="text-[#7c2d12] font-bold text-[13px] sm:text-[14px]">ส่ง REFER</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Post Care Bridge (รวม Home และ Admit เข้าด้วยกัน) -->
                        <div class="w-full relative mt-[-1px]">
                             <!-- คานรับตรงกลางระหว่างกล่อง 1 และ 2 เป๊ะๆ ด้วยความกว้าง 33.33% -->
                             <div class="w-[33.33%] ml-[16.66%] border-t-[3px] border-slate-800 flex justify-center relative">
                                 <div class="w-[3px] h-6 bg-slate-800"></div>
                                 <div class="absolute bottom-[-24px] w-0 h-0 border-l-[6px] border-r-[6px] border-t-[8px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                             </div>
                        </div>
                        
                        <!-- Post Care Box -->
                        <div class="w-[95%] sm:w-[90%] bg-[#dbeafe] border-2 border-blue-300 rounded-lg p-4 shadow-md mt-2 flex self-start sm:ml-[5%]">
                            <div class="text-left">
                                <p class="text-[#1e3a8a] font-bold text-[13px] sm:text-[14px] leading-relaxed">
                                    1. ให้คำปรึกษาก่อนกลับบ้าน<br>
                                    2. เยี่ยมบ้านโดยทีม 3 หมอ และ อปท.<br>
                                    3. ประเมินสภาพที่อยู่ซ้ำให้เหมาะสมกับผู้ป่วย
                                </p>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- Script สำหรับวาดเส้นโยงสีแดง -->
        <script>
            function drawRedLine() {
                const source = document.getElementById('red-source');
                const target = document.getElementById('red-target');
                const line = document.getElementById('red-line-path');
                const svg = document.getElementById('flow-svg');
                
                // ถือว่าหน้าจอใหญ่พอ (Desktop/Tablet) ถึงจะวาดเส้นข้าม
                if(source && target && line && svg && window.innerWidth >= 768) {
                    svg.classList.remove('hidden');
                    const svgRect = svg.getBoundingClientRect();
                    const srcRect = source.getBoundingClientRect();
                    const tgtRect = target.getBoundingClientRect();
                    
                    // คำนวณจุดเริ่มต้น (ขวาของกล่อง 1669)
                    const startX = srcRect.right - svgRect.left;
                    const startY = srcRect.top + (srcRect.height / 2) - svgRect.top;
                    
                    // คำนวณจุดเป้าหมาย (บนของกล่องอาการรุนแรง)
                    const endX = tgtRect.left + (tgtRect.width / 2) - svgRect.left;
                    const endY = tgtRect.top - svgRect.top - 8;
                    
                    // วาดเส้น: ลากไปทางขวาให้พ้นกล่อง -> หักลง -> หักขวาหาเป้าหมาย
                    const gutterX = startX + Math.max(20, (tgtRect.left - srcRect.right)/2); 
                    const d = `M ${startX} ${startY} L ${gutterX} ${startY} L ${gutterX} ${endY - 20} L ${endX} ${endY - 20} L ${endX} ${endY}`;
                    
                    line.setAttribute('d', d);
                } else if (svg) {
                    svg.classList.add('hidden'); // ซ่อนถ้าจอเล็กเกินไป
                }
            }
            
            // ให้วาดเส้นใหม่ทุกครั้งที่มีการ Resize
            window.addEventListener('resize', drawRedLine);
            // หน่วงเวลาวาดครั้งแรก เพื่อรอให้ฟอนต์และกล่องโหลดเสร็จสมบูรณ์
            setTimeout(drawRedLine, 500);
            setTimeout(drawRedLine, 1000);
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=1900, scrolling=True)
