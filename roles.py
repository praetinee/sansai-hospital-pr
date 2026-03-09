import streamlit.components.v1 as components

def render_roles():
    # โค้ด HTML สำหรับหน้าบทบาทหน่วยงาน ปรับโครงสร้างเป็น Flow 3 คอลัมน์ (รุก-รับ-ส่งต่อ) 
    # แก้ไขล่าสุด: ยุบรวม "ทีมบริการออนไลน์" เข้าไปเป็นหน้าที่หนึ่งของ "ทีมคลินิกมลพิษ" อย่างสมบูรณ์
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
                --bg-knockout: #ffffff;
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
                    --bg-knockout: #0e1117;
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

            <!-- SVG Lines Overlay -->
            <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden xl:block z-[100]" style="filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.2));">
                <!-- ชั้นพื้นหลังสำหรับตัดขอบ -->
                <g stroke="var(--bg-knockout)" stroke-width="10" fill="none" stroke-linejoin="round" stroke-linecap="round">
                    <path id="bg-lm-1" /> <path id="bg-lm-2" />
                    <path id="bg-mr-1" /> <path id="bg-mr-2" /> <path id="bg-mr-3" /> <path id="bg-mr-bus" />
                    <path id="bg-return" />
                </g>

                <!-- Left to Middle -->
                <g stroke="#16a34a" stroke-width="4" fill="none" stroke-linejoin="round" stroke-linecap="round">
                    <path id="path-lm-1" /> <path id="path-lm-2" />
                </g>

                <!-- Middle to Right -->
                <g stroke="#ea580c" stroke-width="4" fill="none" stroke-linejoin="round" stroke-linecap="round">
                    <path id="path-mr-1" /> <path id="path-mr-2" /> <path id="path-mr-3" /> <path id="path-mr-bus" />
                </g>

                <!-- Return -->
                <path id="path-return" fill="none" stroke="#0284c7" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="6,5" />
            </svg>
            
            <div id="return-text" class="absolute hidden xl:flex items-center justify-center font-bold text-blue-700 bg-blue-50 px-5 py-2 rounded-full border-2 border-blue-400 text-[15px] z-[110] shadow-md">
                <i data-lucide="refresh-cw" class="w-5 h-5 mr-2 text-blue-600"></i> การดูแลต่อเนื่องป้องกันการกำเริบซ้ำ
            </div>

            <!-- 3 Columns Layout -->
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 xl:gap-12 relative z-10">

                <!-- ================= COLUMN 1: รุก (ชุมชนและฟื้นฟู) ================= -->
                <div class="col-bg-left border-2 rounded-[2rem] p-4 sm:p-5 flex flex-col h-full w-full relative" id="col-left">
                    <h3 class="text-center font-bold text-green-800 dark:text-green-400 text-lg mb-4 border-b-2 border-green-200 dark:border-green-800 pb-2">
                        ชุมชนและการดูแลต่อเนื่อง (รุก)
                    </h3>
                    
                    <div class="space-y-4 flex-grow flex flex-col justify-center">
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
                    
                    <div class="space-y-6 flex-grow flex flex-col justify-center">
                        
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
                                        <li>รับผู้ป่วย Walk-in / รับผู้ป่วยส่งต่อ</li>
                                        <li>เจ้าหน้าที่ซักประวัติ / อาการเบื้องต้น/บันทึกข้อมูลผู้ป่วยลง GG sheets</li>
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

                        <!-- คลินิกมลพิษ (รวมบริการออนไลน์) -->
                        <div class="card-bg border rounded-xl overflow-hidden role-card shadow-sm" id="card-clinic">
                            <div class="p-4">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="bg-orange-100 p-2 rounded-lg shrink-0">
                                        <i data-lucide="stethoscope" class="w-6 h-6 text-orange-600"></i>
                                    </div>
                                    <div>
                                        <h4 class="text-lg font-bold bg-main-title leading-tight">ทีมคลินิกมลพิษ</h4>
                                        <p class="text-xs font-medium text-orange-600">คลินิกมลพิษ / ระบบบริการออนไลน์</p>
                                    </div>
                                </div>
                                <div class="pl-2 sm:pl-[3.2rem]">
                                    <p class="font-bold text-normal text-sm mb-1">หน้าที่รับผิดชอบ:</p>
                                    <ul class="list-disc list-outside ml-4 text-normal text-[13px] sm:text-[14px] space-y-1 mb-2">
                                        <li>ให้บริการปรึกษาและคัดกรองผ่านออนไลน์ (หมอพร้อม / Telemedicine)</li>
                                        <li>รับดูแลผู้ป่วยที่ส่งต่อมาจาก รพ.สต./PCU</li>
                                        <li>แพทย์/สหวิชาชีพ ซักประวัติ ตรวจร่างกาย/Lab</li>
                                        <li>วางแผนการรักษาให้แก่ผู้ป่วย</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="card-forward border-t px-4 py-3 pl-4 sm:pl-[4.2rem]">
                                <p class="font-bold text-normal text-sm mb-1">ผลการตรวจ / รักษา:</p>
                                <p class="text-[12px] sm:text-[13px] text-normal leading-tight">
                                    <span class="text-orange-500 font-bold">➔</span> <b>ทีม 3 หมอ / รพ.สต.:</b> กรณีคัดกรองออนไลน์พบอาการเล็กน้อย<br>
                                    <span class="text-orange-500 font-bold">➔</span> <b>ให้ยากลับบ้าน / Admit:</b> เข้าสู่การดูแลต่อเนื่อง<br>
                                    <span class="text-red-500 font-bold">➔</span> <b class="text-red-600 dark:text-red-400">ส่ง REFER / 1669:</b> กรณีอาการรุนแรง
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
                    
                    <div class="space-y-6 flex-grow flex flex-col justify-center">
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
                                        <li class="font-semibold text-red-600">ส่ง REFER: ประสานส่งต่อ รพ.ระดับสูง</li>
                                    </ul>
                                </div>
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
                                        <li class="font-semibold text-indigo-600">แจ้ง สสจ.เชียงใหม่: รายงานสถานการณ์</li>
                                    </ul>
                                </div>
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

            // ฟังก์ชันวาดเส้นเชื่อมโยง SVG แบบ "วงจร (Bus Routing)"
            function drawLines() {
                const svg = document.getElementById('flow-svg');
                const container = document.getElementById('main-container');

                if(window.innerWidth >= 1280 && svg && container) {
                    svg.classList.remove('hidden');
                    const textRet = document.getElementById('return-text');
                    if(textRet) textRet.classList.remove('hidden');

                    const contRect = container.getBoundingClientRect();
                    const getR = (id) => {
                        const el = document.getElementById(id);
                        if(!el) return null;
                        const r = el.getBoundingClientRect();
                        return {
                            top: r.top - contRect.top, bottom: r.bottom - contRect.top,
                            left: r.left - contRect.left, right: r.right - contRect.left,
                            width: r.width, height: r.height,
                            cy: (r.top - contRect.top) + (r.height / 2),
                            cx: (r.left - contRect.left) + (r.width / 2)
                        };
                    };

                    const colL = getR('col-left'); const colM = getR('col-mid'); const colR = getR('col-right');
                    const cPost = getR('card-postcare');
                    const cOnsite = getR('card-onsite'); const cClinic = getR('card-clinic');
                    const cEr = getR('card-er'); const cControl = getR('card-control'); const cSurv = getR('card-surv');

                    const draw = (id, pathString) => {
                        document.getElementById(id).setAttribute('d', pathString);
                        document.getElementById(id.replace('path-', 'bg-')).setAttribute('d', pathString);
                    };

                    // 1. Left to Middle
                    const gapLM = colM.left - colL.right;
                    const midX_LM = colL.right + gapLM * 0.4;
                    const outL_Y = cPost.cy; 

                    draw('path-lm-1', `M ${colL.right} ${outL_Y} L ${midX_LM} ${outL_Y} L ${midX_LM} ${cOnsite.cy} L ${colM.left} ${cOnsite.cy}`);
                    draw('path-lm-2', `M ${midX_LM} ${outL_Y} L ${midX_LM} ${cClinic.cy} L ${colM.left} ${cClinic.cy}`);

                    // 2. Middle to Right
                    const gapMR = colR.left - colM.right;
                    const midX_MR = colM.right + gapMR * 0.5;

                    draw('path-mr-bus', `M ${midX_MR} ${cOnsite.cy} L ${midX_MR} ${cClinic.cy}`);
                    draw('path-mr-1', `M ${colM.right} ${cOnsite.cy} L ${midX_MR} ${cOnsite.cy} L ${midX_MR} ${cEr.cy} L ${colR.left} ${cEr.cy}`);
                    draw('path-mr-2', `M ${midX_MR} ${cControl.cy} L ${colR.left} ${cControl.cy}`);
                    draw('path-mr-3', `M ${colM.right} ${cClinic.cy} L ${midX_MR} ${cClinic.cy} L ${midX_MR} ${cSurv.cy} L ${colR.left} ${cSurv.cy}`);

                    // 3. Return Line (Right to Left Bottom)
                    const dropY = Math.max(colL.bottom, colM.bottom, colR.bottom) + 50;
                    const dRet = `M ${colR.cx} ${colR.bottom} L ${colR.cx} ${dropY} L ${colL.cx} ${dropY} L ${colL.cx} ${colL.bottom}`;
                    
                    document.getElementById('path-return').setAttribute('d', dRet);
                    document.getElementById('bg-return').setAttribute('d', dRet);

                    // Position Return Text Label
                    if(textRet) {
                        textRet.style.top = `${dropY}px`;
                        textRet.style.left = `${colM.cx}px`;
                        textRet.style.transform = `translate(-50%, -50%)`;
                    }

                } else {
                    if(svg) svg.classList.add('hidden');
                    const textRet = document.getElementById('return-text');
                    if(textRet) textRet.classList.add('hidden');
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
