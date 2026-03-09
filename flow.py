import streamlit.components.v1 as components

def render_flow():
    # โค้ด HTML สำหรับหน้า Flow ที่ถูกออกแบบใหม่ทั้งหมดด้วย Flexbox และ Grid 
    # เพื่อให้เป๊ะตามภาพ S__14147598.jpg และรองรับทุกขนาดหน้าจอ
    html_code = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;700;800&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Sarabun', sans-serif; background-color: #fdfbf5; margin: 0; padding: 2rem 1rem; }
            .line-v { width: 3px; background-color: #1e293b; margin: 0 auto; }
            .line-h { height: 3px; background-color: #1e293b; margin: 0 auto; }
            .arrow-down { width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid #1e293b; margin: 0 auto; }
            .arrow-down-red { width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid #dc2626; margin: 0 auto; }
        </style>
    </head>
    <body>
        
        <!-- Header -->
        <div class="text-center mb-10">
            <h2 class="text-3xl font-extrabold text-[#1e3a8a] mb-2 tracking-wide">Flow การให้บริการ</h2>
            <p class="text-[1.15rem] font-bold text-[#1e3a8a]">กรณีผู้ป่วยสงสัยตนเอง/ญาติได้รับผลกระทบจาก PM 2.5 จังหวัดเชียงใหม่</p>
        </div>

        <!-- Main Flow Container -->
        <div class="w-full max-w-5xl mx-auto flex flex-col md:flex-row gap-8 relative z-10">
            
            <!-- ================= LEFT COLUMN: ONLINE ================= -->
            <div class="flex-1 flex flex-col items-center">
                <!-- 1. ปรึกษาออนไลน์ -->
                <div class="flex items-center gap-3 bg-[#e0e7ff] border-2 border-blue-300 rounded-full px-4 py-2 shadow-sm">
                    <div class="bg-[#2563eb] text-white rounded-full w-9 h-9 flex items-center justify-center font-bold text-xl shadow-inner">1</div>
                    <span class="text-[#1e3a8a] font-bold text-xl pr-2">ปรึกษาออนไลน์</span>
                </div>
                <div class="line-v h-6"></div><div class="arrow-down"></div>
                
                <!-- หมอพร้อม -->
                <div class="bg-[#e0e7ff] border border-blue-200 rounded-full px-8 py-3 shadow-sm text-center">
                    <p class="text-[#1e40af] font-bold text-lg leading-snug">ผ่านระบบหมอพร้อม/<br>telemedicine ของโรงพยาบาล</p>
                </div>
                <div class="line-v h-6"></div><div class="arrow-down"></div>
                
                <!-- คัดกรอง -->
                <div class="bg-[#93c5fd] border border-blue-300 rounded-full px-8 py-2 shadow-sm text-center">
                    <p class="text-[#1e3a8a] font-bold text-lg">ทำการคัดกรอง</p>
                </div>
                <div class="line-v h-6"></div>
                
                <!-- Split 2-ways -->
                <div class="w-[85%] line-h"></div>
                <div class="w-[85%] flex justify-between">
                    <div class="line-v h-6 ml-0"></div>
                    <div class="line-v h-6 mr-0"></div>
                </div>
                
                <div class="w-[95%] flex justify-between items-start gap-3">
                    <!-- Left: ไม่เข้าข่าย -->
                    <div class="flex-1 flex flex-col items-center">
                        <div class="bg-white border-[3px] border-[#16a34a] rounded-full py-2 px-1 shadow-sm text-center w-full mb-4">
                            <p class="text-[#166534] font-bold text-[14px] leading-tight">ไม่เข้าข่าย/<br>อาการเล็กน้อย</p>
                        </div>
                        <div class="bg-white border-2 border-[#22c55e] rounded-lg p-3 shadow-sm text-center w-full">
                            <p class="text-[#15803d] font-bold text-[14px] leading-snug">ให้คำแนะนำ<br>การปฏิบัติตัว<br>และส่งต่อ<br>ทีม 3 หมอ</p>
                        </div>
                    </div>
                    
                    <!-- Right: เข้าข่าย -->
                    <div class="flex-1 flex flex-col items-center">
                        <div class="bg-[#86efac] border border-green-400 rounded-full py-2 px-1 shadow-sm text-center w-full mb-4">
                            <p class="text-[#14532d] font-bold text-[14px] leading-tight">เข้าข่าย<br>มีอาการที่สงสัย</p>
                        </div>
                        <div class="line-v h-4 absolute mt-[55px]"></div>
                        <div class="bg-[#86efac] rounded-lg p-3 shadow-sm text-left w-full mt-2 relative z-10">
                            <p class="text-[#064e3b] font-bold text-[13.5px] leading-snug mb-3">1. ส่งต่อเข้ารับบริการ<br>ที่รพ./รพ.สต.</p>
                            <p class="bg-[#fca5a5] text-[#7f1d1d] px-2 py-1 rounded text-[13.5px] font-bold leading-snug inline-block">2. ถ้าอาการรุนแรง<br>ประสาน 1669</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ================= RIGHT COLUMN: ONSITE ================= -->
            <div class="flex-1 flex flex-col items-center mt-12 md:mt-0 relative">
                <!-- 2. เข้ารับบริการ -->
                <div class="flex items-center gap-3 bg-[#fce7f3] border-2 border-pink-200 rounded-full px-4 py-2 shadow-sm">
                    <div class="bg-[#d946ef] text-white rounded-full w-9 h-9 flex items-center justify-center font-bold text-xl shadow-inner">2</div>
                    <h3 class="text-[#831843] font-bold text-xl pr-2 leading-tight text-center">เข้ารับบริการ<br><span class="text-lg">ที่รพ./รพ.สต.</span></h3>
                </div>
                <div class="line-v h-6"></div><div class="arrow-down"></div>
                
                <!-- ซักประวัติ -->
                <div class="bg-[#fbcfe8] border border-pink-300 rounded-[2rem] px-5 py-3 shadow-sm text-center w-[90%]">
                    <p class="text-[#831843] font-bold text-[15px] leading-snug">เจ้าหน้าที่ซักประวัติ/อาการเบื้องต้น<br>และลงแบบคัดกรองสอบสวนโรค<br>ที่เกิดจาก PM2.5</p>
                </div>
                <div class="line-v h-8"></div>
                
                <!-- RED LINE CONNECTOR (The Magic Trick) -->
                <!-- วางเส้นสีแดงไว้เหนือเส้นสีดำของการแยก 3 ทาง โดยให้มันยื่นออกไปทางซ้ายมือเพื่อเสมือนว่ามาจากคอลัมน์ซ้าย -->
                <div class="w-[90%] relative mt-2">
                    <!-- เส้นสีดำปกติ -->
                    <div class="w-full line-h"></div>
                    
                    <!-- เส้นสีแดง (ซ่อนในมือถือ) วิ่งจากซ้ายมาขวา แล้วหักลงมา -->
                    <div class="absolute top-0 right-0 w-[140%] h-[3px] bg-[#dc2626] hidden md:block" style="transform: translateY(-5px); z-index: 0;"></div>
                    <div class="absolute top-0 right-0 w-[3px] h-[25px] bg-[#dc2626] hidden md:block" style="transform: translateY(-5px); z-index: 0;"></div>
                    <div class="absolute arrow-down-red hidden md:block z-10" style="top: 20px; right: -1.5px;"></div>
                </div>
                
                <!-- Split 3-ways -->
                <div class="w-[90%] flex justify-between relative z-10">
                    <div class="line-v h-6 ml-0"></div>
                    <div class="line-v h-6 mx-auto"></div>
                    <div class="line-v h-6 mr-0"></div>
                </div>
                
                <div class="w-[95%] flex justify-between items-start gap-2 relative z-10">
                    <!-- Left: กรณีไม่เข้าข่าย -->
                    <div class="flex-1 flex flex-col items-center">
                        <div class="bg-white border-[3px] border-[#1e3a8a] rounded-full py-2 px-1 shadow-sm text-center w-full mb-6">
                            <p class="text-[#1e3a8a] font-bold text-[13px] leading-tight">กรณี<br>ไม่เข้าข่าย</p>
                        </div>
                        <div class="bg-white border-2 border-[#1e3a8a] rounded-lg p-2 shadow-sm text-center w-full">
                            <p class="text-[#1e3a8a] font-bold text-[13px] leading-snug">ส่งตรวจคลินิก<br>ตามอาการของโรค</p>
                        </div>
                    </div>
                    
                    <!-- Middle: เข้าข่าย (Connects straight down) -->
                    <div class="flex-1 flex flex-col items-center">
                        <div class="bg-[#fed7aa] border border-orange-300 rounded-[1.5rem] py-2 px-1 shadow-sm text-center w-full">
                            <p class="text-[#9a3412] font-bold text-[13px] leading-tight">เข้าข่าย<br>อาการเล็กน้อย<br>/ปานกลาง</p>
                        </div>
                        <!-- ลากยาวลงไปหาคลินิกมลพิษ -->
                        <div class="line-v h-[150px]"></div>
                    </div>
                    
                    <!-- Right: ผู้ป่วยอาการรุนแรง -->
                    <div class="flex-1 flex flex-col items-center pt-2"> <!-- Padding top to match the red arrow drop -->
                        <div class="bg-[#fca5a5] border border-red-400 rounded-full py-2 px-1 shadow-sm text-center w-full mb-4">
                            <p class="text-[#7f1d1d] font-bold text-[13px] leading-tight">ผู้ป่วย<br>อาการรุนแรง</p>
                        </div>
                        <div class="bg-[#f87171] rounded-sm p-2 shadow-sm text-center w-[85%] mb-4">
                            <p class="text-white font-bold text-[14px]">ส่งเข้า<br>ห้องฉุกเฉิน</p>
                        </div>
                        <div class="line-v h-4"></div>
                        <div class="bg-[#f87171] rounded-sm p-2 shadow-sm text-center w-[85%]">
                            <p class="text-white font-bold text-[14px]">ส่ง REFER</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= MERGED SECTION: CLINIC & POST CARE ================= -->
        <div class="w-full max-w-xl mx-auto flex flex-col items-center mt-[-40px] relative z-20">
            <!-- Oval Clinic Box -->
            <div class="bg-[#fdba74] border-2 border-orange-400 rounded-full px-8 py-4 shadow-md text-center w-[90%]">
                <h3 class="text-[#7c2d12] font-bold text-[18px]">ส่งเข้าคลินิกมลพิษ เฉพาะรพ.</h3>
                <p class="text-[#9a3412] font-bold text-[14px]">(กรณีรพ.สต.ให้ส่งต่อรพ.)</p>
            </div>
            
            <div class="line-v h-6"></div>
            
            <div class="bg-[#ffedd5] border border-orange-200 rounded-lg px-6 py-3 shadow-sm text-center w-[85%]">
                <p class="text-[#7c2d12] font-bold text-[15px] leading-snug">ซักประวัติ/ตรวจร่างกาย/<br>ตรวจทางห้องปฏิบัติการ<br>โดยแพทย์/สหวิชาชีพ</p>
            </div>
            
            <div class="line-v h-6"></div>
            
            <div class="bg-[#fed7aa] border border-orange-300 rounded-lg px-10 py-2 shadow-sm text-center">
                <p class="text-[#7c2d12] font-bold text-[16px]">วางแผนการรักษา</p>
            </div>
            
            <div class="line-v h-6"></div>
            
            <!-- 3-Way Split Clinic Outcomes -->
            <div class="w-[80%] line-h"></div>
            <div class="w-[80%] flex justify-between">
                <div class="line-v h-6 ml-0"></div>
                <div class="line-v h-6 mx-auto"></div>
                <div class="line-v h-6 mr-0"></div>
            </div>
            
            <div class="w-[90%] flex justify-between gap-4 items-start">
                <div class="flex-1 flex flex-col items-center">
                    <div class="bg-[#fed7aa] rounded-sm p-2 shadow-sm text-center w-full">
                        <p class="text-[#7c2d12] font-bold text-[14px]">ให้ยากลับบ้าน</p>
                    </div>
                    <div class="line-v h-8"></div>
                </div>
                <div class="flex-1 flex flex-col items-center">
                    <div class="bg-[#fed7aa] rounded-sm p-2 shadow-sm text-center w-full">
                        <p class="text-[#7c2d12] font-bold text-[14px] leading-tight">Admit<br>ให้การรักษา</p>
                    </div>
                    <div class="line-v h-8"></div>
                </div>
                <div class="flex-1 flex flex-col items-center">
                    <div class="bg-[#fed7aa] rounded-sm p-2 shadow-sm text-center w-full">
                        <p class="text-[#7c2d12] font-bold text-[14px]">ส่ง REFER</p>
                    </div>
                </div>
            </div>
            
            <!-- Post Care Bridge (Connects Home and Admit perfectly) -->
            <div class="w-full flex flex-col items-center mt-[-1px]">
                 <!-- วาดสะพานเชื่อมระหว่างซ้ายและกลาง -->
                 <div class="w-[66.66%] flex justify-start ml-[-33.33%]">
                     <div class="w-full line-h"></div>
                 </div>
                 <!-- ลากเส้นลงตรงกลางสะพาน (ซึ่งจะเบี่ยงซ้ายไป 16.66%) -->
                 <div class="line-v h-6 relative left-[-16.66%]"></div>
                 <div class="arrow-down relative left-[-16.66%]"></div>
                 
                 <!-- Post Care Box -->
                 <div class="bg-[#dbeafe] border-2 border-blue-200 rounded-lg p-4 shadow-md w-[85%] relative left-[-10%] mt-1">
                     <div class="text-left">
                         <p class="text-[#1e3a8a] font-bold text-[14px] leading-relaxed">
                             1. ให้คำปรึกษาก่อนกลับบ้าน<br>
                             2. เยี่ยมบ้านโดยทีม3 หมอ และอปท.<br>
                             3. ประเมินสภาพที่อยู่ซ้ำให้เหมาะสมกับผู้ป่วย
                         </p>
                     </div>
                 </div>
            </div>
            
        </div>
        
    </body>
    </html>
    """
    
    # กำหนดความสูงให้ครอบคลุมหน้าจอ
    components.html(html_code, height=1900, scrolling=True)
