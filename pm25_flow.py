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
        <style>
            body {
                font-family: 'Sarabun', sans-serif;
                background-color: transparent;
                padding: 1rem;
            }
            .flow-col {
                @apply rounded-[2rem] p-5 border-[3px] flex flex-col gap-5 relative h-full;
            }
            .col-yellow { @apply bg-[#fefce8] border-[#fde047]; }
            .col-orange { @apply bg-[#fff7ed] border-[#fb923c]; }
            .col-green { @apply bg-[#f0fdf4] border-[#86efac]; }
            
            .inner-box {
                @apply bg-white rounded-xl p-3 shadow-sm border border-gray-100;
            }
            .tag-code {
                @apply absolute -top-2.5 -right-2 bg-[#1e4b3e] text-white text-[10px] px-2 py-0.5 rounded-full font-bold z-10 shadow-sm;
            }
            .arrow-icon {
                @apply text-gray-400 shrink-0;
            }
        </style>
    </head>
    <body>
        <div class="max-w-[1280px] mx-auto relative pb-24">
            <!-- Alert Box -->
            <div class="flex justify-end mb-6">
                <div class="bg-[#1e4b3e] text-white px-4 py-2 rounded-full font-bold shadow-md text-sm flex items-center border-2 border-[#123329]">
                    <span class="text-yellow-300 mr-2">ย้ำ!</span> บันทึกรหัสโรค Z58.1 (Exposure to air pollution) ทุกจุดบริการเพื่อวิเคราะห์ข้อมูล
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 relative z-10 items-stretch">
                <!-- SVG Overlay for Main Column Connectors (Desktop) -->
                <svg class="absolute inset-0 w-full h-full pointer-events-none hidden lg:block z-20" style="overflow: visible;">
                    <defs>
                        <marker id="arrow-gray-lg" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
                            <path d="M 0 0 L 12 6 L 0 12 z" fill="#6b7280" />
                        </marker>
                    </defs>
                    <!-- Arrow from Left to Middle -->
                    <path d="M 33% 50% L 35% 50%" stroke="#6b7280" stroke-width="6" marker-end="url(#arrow-gray-lg)" />
                    <!-- Arrow from Middle to Right -->
                    <path d="M 66% 50% L 68% 50%" stroke="#6b7280" stroke-width="6" marker-end="url(#arrow-gray-lg)" />
                </svg>

                <!-- Column 1: Left (Yellow) -->
                <div class="flow-col col-yellow">
                    <h2 class="text-xl font-extrabold text-center text-[#854d0e] mb-2 bg-[#fef9c3] py-2 rounded-full mx-4">ชุมชนและหน่วยบริการปฐมภูมิ (รุก)</h2>
                    <div class="inner-box flex flex-col items-center text-center py-5 bg-[#fef08a]/30 border-[#fde047]">
                        <div class="flex justify-center mb-3">
                            <i data-lucide="users" class="w-12 h-12 text-[#a16207]"></i>
                        </div>
                        <h3 class="font-bold text-xl text-[#854d0e]">กลไก 3 หมอ</h3>
                    </div>
                    <div class="flex-grow space-y-5">
                         <div class="flex items-start gap-4">
                            <i data-lucide="clipboard-list" class="w-7 h-7 text-[#a16207] shrink-0 mt-1"></i>
                            <div>
                                <p class="font-bold text-[#854d0e] text-base">การลงพื้นที่เชิงรุก: อสม. และ รพ.สต.</p>
                                <p class="text-sm text-[#a16207] leading-relaxed">เคาะประตูบ้านคัดกรองสุขภาพ (SCPM-66/QAP-F4) เน้น 4 กลุ่มเปราะบาง (ติดเตียง/ผู้สูงอายุ/ตั้งครรภ์/เด็กเล็ก)</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-4">
                            <i data-lucide="shield-check" class="w-7 h-7 text-[#a16207] shrink-0 mt-1"></i>
                            <div>
                                <p class="font-bold text-[#854d0e] text-base">สนับสนุนพื้นที่ปลอดฝุ่น:</p>
                                <p class="text-sm text-[#a16207] leading-relaxed">แจกหน้ากาก N95, จัดทำมุ้งสู้ฝุ่นให้ผู้ป่วยติดเตียง, ห้องปลอดฝุ่นในศูนย์เด็กเล็ก/โรงเรียน</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-4">
                            <i data-lucide="truck" class="w-7 h-7 text-[#a16207] shrink-0 mt-1"></i>
                            <div>
                                <p class="font-bold text-[#854d0e] text-base">สั่งจ่ายยาผ่าน Telemedicine:</p>
                                <p class="text-sm text-[#a16207] leading-relaxed">ผู้ป่วยอาการคงที่ ติดตามและสั่งจ่ายยาผ่าน telemedicine เพื่อลดความเสี่ยงสัมผัสฝุ่น</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Column 2: Middle (Orange) -->
                <div class="flow-col col-orange">
                    <h2 class="text-xl font-extrabold text-center text-[#9a3412] mb-2 bg-[#ffedd5] py-2 rounded-full mx-4">การรับผู้ป่วยและดูแลรักษา (รับ)</h2>
                    
                    <div class="space-y-4 h-full flex flex-col justify-between">
                        <!-- Row 1: Online -->
                        <div class="inner-box flex items-center gap-3 relative bg-[#fff7ed] border-orange-200">
                            <i data-lucide="smartphone" class="w-9 h-9 text-orange-600 shrink-0"></i>
                            <div class="flex-grow">
                                <h3 class="font-bold text-[#9a3412] text-base">ระบบก่อนถึง รพ. และออนไลน์</h3>
                                <p class="text-xs text-orange-800 leading-tight">คลินิกมลพิษออนไลน์ ผ่าน Line OA หรือ หมอพร้อม</p>
                            </div>
                            <i data-lucide="arrow-right" class="arrow-icon w-6 h-6"></i>
                            <div class="text-center w-28 shrink-0">
                                 <p class="font-bold text-sm text-[#9a3412]">ประเมินเบื้องต้น</p>
                                 <p class="text-xs text-orange-800">& Telemedicine</p>
                            </div>
                        </div>

                        <!-- Row 2: OPD -->
                        <div class="inner-box flex flex-wrap items-center gap-2 relative bg-[#fff7ed] border-orange-200">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-2 w-full sm:w-auto mb-2 sm:mb-0 shrink-0">
                                <div class="flex shrink-0">
                                    <i data-lucide="eye" class="w-7 h-7 text-orange-600"></i>
                                    <i data-lucide="lungs" class="w-7 h-7 text-orange-600 -ml-2"></i>
                                </div>
                                <div>
                                    <h3 class="font-bold text-sm text-[#9a3412]">ผู้ป่วยนอก (OPD) <br/>& คลินิกมลพิษ</h3>
                                </div>
                            </div>
                            <div class="flex-grow flex items-center justify-between gap-1 text-xs">
                                <div class="text-center shrink-0">
                                    <p class="font-bold text-[#9a3412]">คัดกรองอาการ</p>
                                    <p class="text-[10px] text-orange-800">(พื้นที่ PM2.5 > 37.5)</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-5 h-5"></i>
                                <div class="text-center shrink-0">
                                    <p>ส่งเข้า</p>
                                    <p class="font-bold text-orange-700">Pollution Clinic</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-5 h-5"></i>
                                <div class="text-center w-24 shrink-0">
                                    <p class="font-bold text-[#9a3412]">จ่ายยา/แนะนำ</p>
                                    <p class="text-[10px] text-orange-800">นัดติดตามหลัง 7 วัน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 3: ER -->
                        <div class="inner-box flex flex-wrap items-center gap-2 relative bg-[#fff7ed] border-orange-200">
                            <div class="tag-code">รหัส Z58.1</div>
                            <div class="flex items-center gap-3 w-full sm:w-auto mb-2 sm:mb-0 shrink-0">
                                <i data-lucide="ambulance" class="w-8 h-8 text-red-600 shrink-0"></i>
                                <div>
                                    <h3 class="font-bold text-sm text-[#9a3412]">ผู้ป่วยฉุกเฉิน (ER) <br/>และระบบ 1669</h3>
                                </div>
                            </div>
                            <div class="flex-grow flex items-center justify-between gap-1 text-xs">
                                <div class="text-center shrink-0">
                                    <p class="font-bold text-[#9a3412]">อาการรุนแรง</p>
                                    <p class="text-[10px] text-orange-800">(หอบหืด, COPD, MI, Stroke)</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-5 h-5"></i>
                                <div class="text-center shrink-0">
                                    <p class="font-bold text-[#9a3412]">1669 ติดต่อ EMS</p>
                                    <p class="text-orange-800">รับเข้า ER</p>
                                </div>
                                <i data-lucide="arrow-right" class="arrow-icon w-5 h-5"></i>
                                <div class="text-center w-24 shrink-0">
                                    <p class="font-bold text-[#9a3412]">ประเมิน Admit</p>
                                    <p class="text-orange-800">หรือ กลับบ้าน</p>
                                </div>
                            </div>
                        </div>

                        <!-- Row 4: IPD -->
                        <div class="inner-box flex items-center gap-4 relative bg-[#fff7ed] border-orange-200">
                            <div class="tag-code">รหัส Z58.1</div>
                            <i data-lucide="bed" class="w-9 h-9 text-blue-600 shrink-0"></i>
                            <div class="flex-grow">
                                <h3 class="font-bold text-[#9a3412] text-base">ผู้ป่วยใน (IPD)</h3>
                            </div>
                            <div class="text-center text-sm shrink-0">
                                 <p class="font-bold text-[#9a3412]">รับ Admit</p>
                                 <p class="text-xs text-orange-800">เข้าหอผู้ป่วย</p>
                            </div>
                            <i data-lucide="arrow-right" class="arrow-icon w-6 h-6"></i>
                            <div class="text-center w-32 text-sm shrink-0">
                                 <p class="font-bold text-[#9a3412]">พยาบาล<br/>ซักประวัติเพิ่มเติม</p>
                            </div>
                         </div>
                    </div>
                </div>

                <!-- Column 3: Right (Green) -->
                <div class="flow-col col-green">
                    <h2 class="text-xl font-extrabold text-center text-[#166534] mb-2 bg-[#dcfce7] py-2 rounded-full mx-4">ระบบส่งต่อและจำหน่ายผู้ป่วย (ส่งต่อ)</h2>
                    
                    <!-- Referral System -->
                    <div class="rounded-2xl p-5 bg-[#fee2e2] border-[3px] border-[#fca5a5] shadow-sm text-[#991b1b]">
                        <h3 class="font-bold text-center mb-5 text-lg bg-[#fecaca] py-1 rounded-full mx-6">ระบบส่งต่อผู้ป่วย (Referral System)</h3>
                        <div class="flex justify-between items-start text-center text-sm">
                            <div class="flex-1 flex flex-col items-center">
                                <i data-lucide="hospital" class="w-10 h-10 mb-2 text-[#b91c1c]"></i>
                                <p class="font-bold text-base">รพ.ประเมินการ</p>
                                <p class="text-sm leading-tight">สำรองเตียงพร้อมรับ<br/>และ Ventilator พร้อมใช้</p>
                            </div>
                            <div class="flex items-center h-full pt-6 px-2">
                                <i data-lucide="arrow-right" class="w-8 h-8 text-[#f87171]"></i>
                            </div>
                            <div class="flex-1 flex flex-col items-center">
                                <i data-lucide="building-2" class="w-10 h-10 mb-2 text-[#b91c1c]"></i>
                                <p class="font-bold text-base">หาก Overcapacity</p>
                                <p class="text-sm">ส่งต่อโรงพยาบาล</p>
                                <p class="font-extrabold text-lg text-[#7f1d1d]">ลำพูน</p>
                            </div>
                        </div>
                    </div>

                    <!-- Discharge -->
                    <div class="rounded-2xl p-5 bg-[#bbf7d0] border-[3px] border-[#4ade80] shadow-sm text-[#166534] flex-grow flex flex-col justify-center">
                        <h3 class="font-bold text-center mb-5 text-lg bg-[#86efac] py-1 rounded-full mx-6">การจำหน่ายผู้ป่วย (Discharge)</h3>
                        <div class="text-center space-y-3">
                            <p class="font-bold text-xl">วางแผนตามหลัก D-METHOD</p>
                            <div class="w-16 h-1 bg-[#166534]/20 mx-auto rounded-full"></div>
                            <p class="text-base font-medium leading-relaxed">ประสานทีมเยี่ยมบ้านและอาชีวอนามัย<br/>ประเมินสภาพที่อยู่อาศัยไม่ให้กำเริบซ้ำ</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bottom Return Arrow SVG (Desktop) -->
            <div class="absolute bottom-0 left-0 w-full h-28 pointer-events-none z-0 hidden lg:block">
                <svg width="100%" height="100%" viewBox="0 0 1280 100" preserveAspectRatio="none" style="overflow: visible;">
                    <defs>
                        <marker id="arrow-return" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
                            <path d="M 0 0 L 12 6 L 0 12 z" fill="#4b5563" />
                        </marker>
                    </defs>
                    <!-- Path from bottom of right column, curving under, to bottom of left column -->
                    <path d="M 1050 -10 V 40 Q 1050 90 640 90 Q 230 90 230 40 V -10" stroke="#4b5563" stroke-width="5" fill="none" marker-end="url(#arrow-return)"/>
                </svg>
                <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white px-6 py-2 rounded-full shadow-md border-2 border-gray-300 z-10">
                    <p class="text-center text-gray-700 font-bold text-base flex items-center gap-2">
                        <i data-lucide="refresh-ccw" class="w-5 h-5 text-gray-500"></i> การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                    </p>
                </div>
            </div>
            
            <!-- Mobile view for return arrow text -->
             <div class="lg:hidden text-center mt-6">
                <div class="inline-block bg-white px-5 py-3 rounded-full shadow-md border-2 border-gray-300">
                    <p class="text-gray-700 font-bold flex items-center gap-3 text-sm">
                        <i data-lucide="refresh-ccw" class="w-5 h-5 text-gray-500"></i> การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
                    </p>
                </div>
            </div>

        </div>
        <script>
            lucide.createIcons();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=950, scrolling=True)
