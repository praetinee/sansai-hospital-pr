import streamlit.components.v1 as components

def render_roles():
    # โค้ด HTML สำหรับหน้าบทบาทหน่วยงาน ปรับโครงสร้างเป็น Flow 3 คอลัมน์ (รุก-รับ-ส่งต่อ) 
    # รองรับ Responsive และ Theme (Light/Dark) เต็มรูปแบบ
    # แก้ไขล่าสุด: ทำให้เส้นลูกศรข้ามคอลัมน์ใหญ่และชัดเจนยิ่งขึ้น เพิ่มขอบและเงา
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
                padding: 1rem 1rem 4rem 1rem; 
            }
            .role-card {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .role-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            }
            
            /* สีสำหรับธีมสว่างและมืดแบบยืดหยุ่น */
            :root {
                --bg-main-title: #1e3a8a;
                --bg-sub-title: #475569;
                --card-bg: rgba(255, 255, 255, 0.95);
                --card-border: #e2e8f0;
                --card-forward-bg: rgba(248, 250, 252, 0.95);
                --text-normal: #334155;
                --col-bg-left: rgba(240, 253, 244, 0.6);
                --col-border-left: #bbf7d0;
                --col-bg-mid: rgba(255, 247, 237, 0.6);
                --col-border-mid: #fed7aa;
                --col-bg-right: rgba(239, 246, 255, 0.6);
                --col-border-right: #bfdbfe;
                --bg-knockout: #ffffff; /* เส้นขอบตัดสีขาวสำหรับลูกศรใน Light Mode */
            }

            @media (prefers-color-scheme: dark) {
                :root {
                    --bg-main-title: #93c5fd;
                    --bg-sub-title: #cbd5e1;
                    --card-bg: rgba(30, 41, 59, 0.95);
                    --card-border: #334155;
                    --card-forward-bg: rgba(15, 23, 42, 0.95);
                    --text-normal: #e2e8f0;
                    --col-bg-left: rgba(20, 83, 45, 0.2);
                    --col-border-left: rgba(34, 197, 94, 0.3);
                    --col-bg-mid: rgba(124, 45, 18, 0.2);
                    --col-border-mid: rgba(249, 115, 22, 0.3);
                    --col-bg-right: rgba(30, 58, 138, 0.2);
                    --col-border-right: rgba(59, 130, 246, 0.3);
                    --bg-knockout: #0e1117; /* เส้นขอบตัดสีดำสำหรับลูกศรใน Dark Mode */
                }
            }

            body { color: var(--text-normal); }
            .bg-main-title { color: var(--bg-main-title); }
            .bg-sub-title { color: var(--bg-sub-title); }
            .card-bg { background-color: var(--card-bg); border-color: var(--card-border); }
            .card-forward { background-color: var(--card-forward-bg); border-color: var(--card-border); }
            .text-normal { color: var(--text-normal); }
            .col-bg-left { background-color: var(--col-bg-left); border-color: var(--col-border-left); }
            .col-bg-mid { background-color: var(--col-bg-mid); border-color: var(--col-border-mid); }
            .col-bg-right { background-color: var(--col-bg-right); border-color: var(--col-border-right); }
        </style>
    </head>
    <body>
        
        <div class="w-full max-w-[1400px] mx-auto relative" id="main-container">
            
            <!-- Header -->
            <div class="text-center mb-8 relative z-20 px-4">
                <div class="inline-flex items-center justify-center p-3 bg-blue-100 rounded-full mb-3 shadow-sm">
                    <i data-lucide="git-merge" class="w-8 h-8 text-blue-600"></i>
                </div>
                <h2 class="text-2xl sm:text-3xl md:text-4xl font-extrabold bg-main-title mb-2 tracking-wide">บทบาทของแต่ละหน่วยงาน</h2>
                <p class="text-sm sm:text-base md:text-lg bg-sub-title max-w-3xl mx-auto">
                    สรุปหน้าที่รับผิดชอบและทิศทางการส่งต่อผู้ป่วย แบ่งตามกระบวนการ รุก-รับ-ส่งต่อ
                </p>
            </div>

            <!-- SVG Lines Overlay (วาดลูกศรเชื่อมคอลัมน์เฉพาะหน้าจอ Desktop) -->
            <!-- ปรับให้อยู่ชั้นหน้าสุด z-[100] และเพิ่มความเข้มของเงา -->
            <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden xl:block z-[100]" style="filter: drop-shadow(0px 3px 4px rgba(0,0,0,0.3));">
                <defs>
                    <!-- ขยายขนาดหัวลูกศรให้ใหญ่ขึ้น -->
                    <marker id="arrow-orange" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="8" markerHeight="8" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#ea580c" />
                    </marker>
                    <marker id="arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="8" markerHeight="8" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#15803d" />
                    </marker>
                </defs>
                <!-- เส้นพื้นหลัง (Knockout Effect) ให้เส้นหลักดูโดดเด่นตัดกับพื้น -->
                <path id="bg-m-r-1" fill="none" stroke="var(--bg-knockout)" stroke-width="11" stroke-linejoin="round" stroke-linecap="round" />
                <path id="bg-m-r-2" fill="none" stroke="var(--bg-knockout)" stroke-width="11" stroke-linejoin="round" stroke-linecap="round" />
                <path id="bg-return" fill="none" stroke="var(--bg-knockout)" stroke-width="11" stroke-linejoin="round" stroke-linecap="round" />
                
                <!-- เส้นส่งต่อ (เส้นจริง): กลาง ไป ขวา (หนา 5px สีเข้ม) -->
                <path id="path-m-r-1" fill="none" stroke="#ea580c" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" marker-end="url(#arrow-orange)" />
                <path id="path-m-r-2" fill="none" stroke="#ea580c" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" marker-end="url(#arrow-orange)" />
                <!-- เส้นส่งต่อกลับ (ดูแลต่อเนื่อง): ลากกลับไปซ้าย (หนา 5px สีเขียวเข้ม) -->
                <path id="path-return" fill="none" stroke="#15803d" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" marker-end="url(#arrow-green)" />
            </svg>

            <!-- 3 Columns Layout -->
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 relative z-10">

                <!-- ================= COLUMN 1: รุก (ชุมชนและฟื้นฟู) ================= -->
                <div class="col-bg-left border-2 rounded-[2rem] p-4 sm:p-5 flex flex-col h-full w-full relative" id="col-left">
                    <h3 class="text-center font-bold text-green-800 dark:text-green-400 text-lg mb-4 border-b-2 border-green-200 dark:border-green-800 pb-2">
                        ชุมชนและการดูแลต่อเนื่อง (รุก)
                    </h3>
                    
                    <div class="space-y-4 flex-grow flex flex-col justify-center">
                        <!-- การดูแลต่อเนื่อง -->
                        <div class="card-bg border rounded-xl overflow-hidden role-card shadow-sm w-full" id="card-postcare">
                            <div class="p-4 sm:p-5">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="bg-emerald-100 p-2 rounded-lg shrink-0">
                                        <i data-lucide="home" class="w-6 h-6 text-emerald-600"></i>
                                    </div>
                                    <div>
                                        <h4 class="text-lg font-bold bg-main-title leading-tight">ทีมดูแลต่อเนื่อง</h4>
                                        <p class="text-xs font-medium text-emerald-600">ทีม 3 หมอ / อปท.</p>
                                    </div>
                                </div>
                                <div class="pl-2 sm:pl-[3.2rem]">
                                    <p class="font-bold text-normal text-sm mb-1">หน้าที่รับผิดชอบ:</p>
                                    <ul class="list-disc list-outside ml-4 text-normal text-[13px] sm:text-[14px] space-y-1 mb-3">
                                        <li>ให้คำปรึกษาก่อนผู้ป่วยกลับบ้าน</li>
                                        <li>ลงพื้นที่เยี่ยมบ้านโดยทีม 3 หมอ และ อปท.</li>
                                        <li>ประเมินสภาพที่อยู่ซ้ำให้เหมาะสมกับผู้ป่วย</li>
                                        <li class="font-semibold text-emerald-600 dark:text-emerald-400">กรณีผู้ป่วยอาการคงที่: ติดตาม/สั่งยาผ่าน Telemedicine</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="card-forward border-t px-4 sm:px-5 py-3 pl-4 sm:pl-[4.2rem]">
                                <p class="font-bold text-normal text-sm mb-1">การส่งต่อ/สิ้นสุด:</p>
                                <p class="text-[13px] text-normal"><span class="text-emerald-500 font-bold">➔</span> <span class="font-bold">สิ้นสุดกระบวนการ:</span> เฝ้าระวังผู้ป่วยในชุมชนต่อเนื่องป้องกันกำเริบซ้ำ</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ================= COLUMN 2: รับ (คัดกรองและรักษา) ================= -->
                <div class="col-bg-mid border-2 rounded-[2rem] p-4 sm:p-5 flex flex-col h-full w-full relative" id="col-mid">
                    <h3 class="text-center font-bold text-orange-800 dark:text-orange-400 text-lg mb-4 border-b-2 border-orange-200 dark:border-orange-800 pb-2">
                        การรับผู้ป่วยและดูแลรักษา (รับ)
                    </h3>
                    
                    <div class="space-y-4 flex-grow flex flex-col justify-center">
                        <!-- บริการออนไลน์ -->
                        <div class="card-bg border rounded-xl overflow-hidden role-card shadow-sm" id="card-online">
                            <div class="p-4">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="bg-blue-100 p-2 rounded-lg shrink-0">
                                        <i data-lucide="monitor-smartphone" class="w-6 h-6 text-blue-600"></i>
                                    </div>
                                    <div>
                                        <h4 class="text-lg font-bold bg-main-title leading-tight">ทีมให้บริการออนไลน์</h4>
                                        <p class="text-xs font-medium text-blue-600">ระบบหมอพร้อม / Telemedicine</p>
                                    </div>
                                </div>
                                <div class="pl-2 sm:pl-[3.2rem]">
                                    <p class="font-bold text-normal text-sm mb-1">หน้าที่รับผิดชอบ:</p>
                                    <ul class="list-disc list-outside ml-4 text-normal text-[13px] sm:text-[14px] space-y-1 mb-2">
                                        <li>รับปรึกษาออนไลน์</li>
                                        <li>ทำการคัดกรองอาการเบื้องต้น</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="card-forward border-t px-4 py-3 pl-4 sm:pl-[4.2rem]">
                                <p class="font-bold text-normal text-sm mb-1">ส่งต่อ:</p>
                                <p class="text-[12px] sm:text-[13px] text-normal leading-tight">
                                    <span class="text-orange-500 font-bold">➔</span> <b>ทีม 3 หมอ</b> (อาการเล็กน้อย)<br>
                                    <span class="text-orange-500 font-bold">➔</span> <b>รพ./รพ.สต.</b> (เข้าข่ายสงสัย)<br>
                                    <span class="text-red-500 font-bold">➔</span> <b class="text-red-600 dark:text-red-400">1669</b> (รุนแรง)
                                </p>
                            </div>
                        </div>

                        <!-- จุดรับบริการปฐมภูมิ -->
                        <div class="card-bg border rounded-xl overflow-hidden role-card shadow-sm" id="card-onsite">
                            <div class="p-4">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="bg-pink-100 p-2 rounded-lg shrink-0">
                                        <i data-lucide="hospital" class="w-6 h-6 text-pink-600"></i>
                                    </div>
                                    <div>
                                        <h4 class="text-lg font-bold bg-main-title leading-tight">จุดรับบริการ / ปฐมภูมิ</h4>
                                        <p class="text-xs font-medium text-pink-600">รพ. / รพ.สต. / PCU หนองหาร</p>
                                    </div>
                                </div>
                                <div class="pl-2 sm:pl-[3.2rem]">
                                    <p class="font-bold text-normal text-sm mb-1">หน้าที่รับผิดชอบ:</p>
                                    <ul class="list-disc list-outside ml-4 text-normal text-[13px] sm:text-[14px] space-y-1 mb-2">
                                        <li>รับผู้ป่วย Walk-in / ส่งต่อออนไลน์</li>
                                        <li>เจ้าหน้าที่ซักประวัติ / อาการเบื้องต้น</li>
                                        <li>ลงแบบคัดกรองสอบสวนโรคจาก PM 2.5</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="card-forward border-t px-4 py-3 pl-4 sm:pl-[4.2rem]">
                                <p class="font-bold text-normal text-sm mb-1">ส่งต่อ:</p>
                                <p class="text-[12px] sm:text-[13px] text-normal leading-tight">
                                    <span class="text-orange-500 font-bold">➔</span> <b>คลินิกทั่วไป</b> (ไม่เข้าข่าย)<br>
                                    <span class="text-orange-500 font-bold">➔</span> <b>คลินิกมลพิษ</b> (เล็กน้อย/ปานกลาง)<br>
                                    <span class="text-orange-500 font-bold">➔</span> <b>ทีมควบคุมโรค</b> (แจ้งข้อมูลสอบสวน)<br>
                                    <span class="text-red-500 font-bold">➔</span> <b class="text-red-600 dark:text-red-400">ห้องฉุกเฉิน ER</b> (รุนแรง)
                                </p>
                            </div>
                        </div>

                        <!-- คลินิกมลพิษ -->
                        <div class="card-bg border rounded-xl overflow-hidden role-card shadow-sm" id="card-clinic">
                            <div class="p-4">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="bg-orange-100 p-2 rounded-lg shrink-0">
                                        <i data-lucide="stethoscope" class="w-6 h-6 text-orange-600"></i>
                                    </div>
                                    <div>
                                        <h4 class="text-lg font-bold bg-main-title leading-tight">ทีมคลินิกมลพิษ</h4>
                                        <p class="text-xs font-medium text-orange-600">คลินิกมลพิษ (เฉพาะ รพ.)</p>
                                    </div>
                                </div>
                                <div class="pl-2 sm:pl-[3.2rem]">
                                    <p class="font-bold text-normal text-sm mb-1">หน้าที่รับผิดชอบ:</p>
                                    <ul class="list-disc list-outside ml-4 text-normal text-[13px] sm:text-[14px] space-y-1 mb-2">
                                        <li>รับส่งต่อจาก รพ.สต./PCU</li>
                                        <li>แพทย์/สหวิชาชีพ ซักประวัติ ตรวจร่างกาย/Lab</li>
                                        <li>วางแผนการรักษาให้แก่ผู้ป่วย</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="card-forward border-t px-4 py-3 pl-4 sm:pl-[4.2rem]">
                                <p class="font-bold text-normal text-sm mb-1">ผลการรักษา:</p>
                                <p class="text-[12px] sm:text-[13px] text-normal leading-tight">
                                    <span class="text-orange-500 font-bold">➔</span> <b>ให้ยากลับบ้าน / Admit:</b> เข้าสู่การดูแลต่อเนื่อง<br>
                                    <span class="text-red-500 font-bold">➔</span> <b class="text-red-600 dark:text-red-400">ส่ง REFER:</b> ส่งรักษา รพ. ระดับสูง
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ================= COLUMN 3: ส่งต่อ (ฉุกเฉินและสนับสนุน) ================= -->
                <div class="col-bg-right border-2 rounded-[2rem] p-4 sm:p-5 flex flex-col h-full w-full relative" id="col-right">
                    <h3 class="text-center font-bold text-blue-800 dark:text-blue-400 text-lg mb-4 border-b-2 border-blue-200 dark:border-blue-800 pb-2">
                        ฉุกเฉินและระบบสนับสนุน (ส่งต่อ)
                    </h3>
                    
                    <div class="space-y-4 flex-grow flex flex-col justify-center">
                        <!-- ฉุกเฉิน -->
                        <div class="card-bg border rounded-xl overflow-hidden role-card shadow-sm" id="card-er">
                            <div class="p-4">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="bg-red-100 p-2 rounded-lg shrink-0">
                                        <i data-lucide="ambulance" class="w-6 h-6 text-red-600"></i>
                                    </div>
                                    <div>
                                        <h4 class="text-lg font-bold bg-main-title leading-tight">ทีมแพทย์ฉุกเฉิน</h4>
                                        <p class="text-xs font-medium text-red-600">ห้องฉุกเฉิน (ER) / สายด่วน 1669</p>
                                    </div>
                                </div>
                                <div class="pl-2 sm:pl-[3.2rem]">
                                    <p class="font-bold text-normal text-sm mb-1">หน้าที่รับผิดชอบ:</p>
                                    <ul class="list-disc list-outside ml-4 text-normal text-[13px] sm:text-[14px] space-y-1 mb-2">
                                        <li>รับแจ้งเหตุ 1669 ออกรับผู้ป่วยรุนแรง</li>
                                        <li>ประเมินและให้การรักษาเบื้องต้นในห้องฉุกเฉิน</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="card-forward border-t px-4 py-3 pl-4 sm:pl-[4.2rem]">
                                <p class="font-bold text-normal text-sm mb-1">ส่งต่อ:</p>
                                <p class="text-[12px] sm:text-[13px] text-normal leading-tight">
                                    <span class="text-red-500 font-bold">➔</span> <b class="text-red-600 dark:text-red-400">ส่ง REFER:</b> ประสานส่งต่อ รพ.ระดับสูง
                                </p>
                            </div>
                        </div>

                        <!-- ทีมควบคุมโรค -->
                        <div class="card-bg border rounded-xl overflow-hidden role-card shadow-sm" id="card-control">
                            <div class="p-4">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="bg-indigo-100 p-2 rounded-lg shrink-0">
                                        <i data-lucide="shield-alert" class="w-6 h-6 text-indigo-600"></i>
                                    </div>
                                    <div>
                                        <h4 class="text-lg font-bold bg-main-title leading-tight">ทีมควบคุมโรค</h4>
                                        <p class="text-xs font-medium text-indigo-600">หน่วยงานควบคุมโรค</p>
                                    </div>
                                </div>
                                <div class="pl-2 sm:pl-[3.2rem]">
                                    <p class="font-bold text-normal text-sm mb-1">หน้าที่รับผิดชอบ:</p>
                                    <ul class="list-disc list-outside ml-4 text-normal text-[13px] sm:text-[14px] space-y-1 mb-2">
                                        <li>รับข้อมูลผู้ป่วยเข้าข่าย/รุนแรง</li>
                                        <li>ลงพื้นที่ซักประวัติและสอบสวนโรคเพิ่มเติม</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="card-forward border-t px-4 py-3 pl-4 sm:pl-[4.2rem]">
                                <p class="font-bold text-normal text-sm mb-1">รายงานผล:</p>
                                <p class="text-[12px] sm:text-[13px] text-normal leading-tight">
                                    <span class="text-indigo-500 font-bold">➔</span> <b>สสจ.เชียงใหม่:</b> รายงานสถานการณ์โรค
                                </p>
                            </div>
                        </div>

                        <!-- ทีมเฝ้าระวัง -->
                        <div class="card-bg border rounded-xl overflow-hidden role-card shadow-sm" id="card-surv">
                            <div class="p-4">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="bg-purple-100 p-2 rounded-lg shrink-0">
                                        <i data-lucide="activity" class="w-6 h-6 text-purple-600"></i>
                                    </div>
                                    <div>
                                        <h4 class="text-lg font-bold bg-main-title leading-tight">ทีมเฝ้าระวัง</h4>
                                        <p class="text-xs font-medium text-purple-600 leading-tight">คลินิกมลพิษ / OPD / ER / PCU หนองหาร</p>
                                    </div>
                                </div>
                                <div class="pl-2 sm:pl-[3.2rem]">
                                    <p class="font-bold text-normal text-sm mb-1">หน้าที่รับผิดชอบ:</p>
                                    
                                    <div class="text-normal text-[13px] sm:text-[14px] space-y-3 mb-2 ml-1">
                                        <div>
                                            <p class="font-bold text-purple-700 dark:text-purple-400">OPD / ER / PCU หนองหาร:</p>
                                            <ul class="list-disc list-outside ml-5 mt-1 space-y-1">
                                                <li>แจ้งข้อมูลผู้ป่วยผ่านระบบ Google Sheets</li>
                                            </ul>
                                        </div>
                                        <div>
                                            <p class="font-bold text-orange-600 dark:text-orange-400">คลินิกมลพิษ:</p>
                                            <ul class="list-disc list-outside ml-5 mt-1 space-y-1">
                                                <li>ดึงข้อมูลผู้ป่วยจาก ICD-10 โรคที่เกี่ยวข้องกับ PM 2.5</li>
                                                <li>ตรวจสอบข้อมูล gg sheets ที่หน่วยงานอื่นกรอกมา</li>
                                            </ul>
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
            // สร้างไอคอน
            document.addEventListener('DOMContentLoaded', () => {
                lucide.createIcons();
            });

            // ฟังก์ชันวาดเส้นเชื่อมโยง SVG อัตโนมัติ (เฉพาะหน้าจอคอมพิวเตอร์ที่วาง 3 คอลัมน์)
            function drawLines() {
                const svg = document.getElementById('flow-svg');
                const colL = document.getElementById('col-left');
                const colM = document.getElementById('col-mid');
                const colR = document.getElementById('col-right');
                const container = document.getElementById('main-container');

                const pathMR1 = document.getElementById('path-m-r-1');
                const pathMR2 = document.getElementById('path-m-r-2');
                const pathReturn = document.getElementById('path-return');
                
                const bgMR1 = document.getElementById('bg-m-r-1');
                const bgMR2 = document.getElementById('bg-m-r-2');
                const bgReturn = document.getElementById('bg-return');

                // ทำงานเฉพาะหน้าจอขนาด xl (1280px ขึ้นไปตาม Tailwind) ที่แสดงผลแบบ 3 คอลัมน์
                if(window.innerWidth >= 1280 && colL && colM && colR && svg && container) {
                    svg.classList.remove('hidden');

                    const contRect = container.getBoundingClientRect();
                    const lRect = colL.getBoundingClientRect();
                    const mRect = colM.getBoundingClientRect();
                    const rRect = colR.getBoundingClientRect();

                    // เส้นส่งต่อ 1 (บน): กลาง ไป ขวา (หนาและเป็นเส้นทึบ)
                    const mr1StartX = mRect.right - contRect.left;
                    const mr1StartY = (mRect.top - contRect.top) + (mRect.height * 0.3);
                    const mr1EndX = rRect.left - contRect.left;
                    const dMR1 = `M ${mr1StartX} ${mr1StartY} L ${mr1EndX - 15} ${mr1StartY}`;
                    pathMR1.setAttribute('d', dMR1);
                    bgMR1.setAttribute('d', dMR1);

                    // เส้นส่งต่อ 2 (กลาง): กลาง ไป ขวา (หนาและเป็นเส้นทึบ)
                    const mr2StartX = mRect.right - contRect.left;
                    const mr2StartY = (mRect.top - contRect.top) + (mRect.height * 0.6);
                    const mr2EndX = rRect.left - contRect.left;
                    const dMR2 = `M ${mr2StartX} ${mr2StartY} L ${mr2EndX - 15} ${mr2StartY}`;
                    pathMR2.setAttribute('d', dMR2);
                    bgMR2.setAttribute('d', dMR2);

                    // เส้นย้อนกลับด้านล่าง (การดูแลต่อเนื่อง): จากใต้คอลัมน์กลาง โยงกลับไปใต้คอลัมน์ซ้าย
                    const retStartX = (mRect.left - contRect.left) + (mRect.width / 2);
                    const retStartY = mRect.bottom - contRect.top;
                    const retEndX = (lRect.left - contRect.left) + (lRect.width / 2);
                    const retEndY = lRect.bottom - contRect.top;
                    
                    // หากรอบล่างสุดเพื่อเว้นระยะไม่ให้ทับกล่อง (ลงไป 40px)
                    const dropY = Math.max(retStartY, retEndY) + 40; 

                    // วาด Path: ลากลง -> ลากซ้ายยาวๆ -> ลากขึ้น -> ชี้เข้าใต้กล่องซ้าย
                    const dReturn = `M ${retStartX} ${retStartY} L ${retStartX} ${dropY} L ${retEndX} ${dropY} L ${retEndX} ${retEndY + 18}`;
                    pathReturn.setAttribute('d', dReturn);
                    bgReturn.setAttribute('d', dReturn);

                } else {
                    // ปิดเส้นบนมือถือ/แท็บเล็ต ปล่อยให้การ์ดเรียงต่อกันเป็นแนวตั้งตามธรรมชาติ
                    if(svg) svg.classList.add('hidden');
                }
            }

            // วาดเส้นตอนโหลดเสร็จและตอนย่อขยายจอ
            window.addEventListener('resize', drawLines);
            window.onload = () => { 
                setTimeout(drawLines, 100); 
                setTimeout(drawLines, 500); 
            };
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=1950, scrolling=True)
