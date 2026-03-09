import streamlit.components.v1 as components

def render_new_flow():
    # โค้ด HTML สำหรับหน้า Flow ที่ออกแบบใหม่ทั้งหมด
    # โครงสร้างแบบ Swimlane 2 คอลัมน์ เชื่อมโยงข้อมูลและการส่งต่อระหว่างหน่วยงาน
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
                padding: 2rem 1rem 4rem 1rem; 
            }
            .smart-card {
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            }
            .smart-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            }
            
            /* ธีมสีแบบยืดหยุ่น */
            :root {
                --text-main: #1e293b;
                --text-muted: #475569;
                --bg-canvas: #f8fafc;
                --col-front-bg: #eff6ff;
                --col-front-border: #bfdbfe;
                --col-clinic-bg: #fff7ed;
                --col-clinic-border: #fed7aa;
                --bg-knockout: #ffffff;
            }

            @media (prefers-color-scheme: dark) {
                :root {
                    --text-main: #e2e8f0;
                    --text-muted: #cbd5e1;
                    --bg-canvas: #0f172a;
                    --col-front-bg: rgba(30, 58, 138, 0.2);
                    --col-front-border: rgba(59, 130, 246, 0.3);
                    --col-clinic-bg: rgba(124, 45, 18, 0.2);
                    --col-clinic-border: rgba(249, 115, 22, 0.3);
                    --bg-knockout: #0e1117;
                }
            }

            body { color: var(--text-main); }
            .bg-canvas { background-color: var(--bg-canvas); }
            .col-front { background-color: var(--col-front-bg); border-color: var(--col-front-border); }
            .col-clinic { background-color: var(--col-clinic-bg); border-color: var(--col-clinic-border); }
            .text-main { color: var(--text-main); }
            .text-muted { color: var(--text-muted); }
        </style>
    </head>
    <body>
        
        <div class="w-full max-w-[1200px] mx-auto relative" id="main-container">
            
            <!-- Header -->
            <div class="text-center mb-10 relative z-20 px-4">
                <div class="inline-flex items-center justify-center p-3 bg-indigo-100 rounded-full mb-3 shadow-sm">
                    <i data-lucide="git-pull-request" class="w-8 h-8 text-indigo-600"></i>
                </div>
                <h2 class="text-2xl sm:text-3xl md:text-4xl font-extrabold text-main mb-2 tracking-wide">กระบวนการทำงานและส่งต่อผู้ป่วย</h2>
                <p class="text-sm sm:text-base md:text-lg text-muted max-w-2xl mx-auto">
                    Flowchart แสดงหน้าที่และการเชื่อมโยงข้อมูลระหว่างหน่วยบริการด่านหน้า และ คลินิกมลพิษ
                </p>
            </div>

            <!-- SVG Lines Overlay -->
            <svg id="flow-svg" class="absolute top-0 left-0 w-full h-full pointer-events-none hidden md:block z-[100]" style="filter: drop-shadow(0px 2px 3px rgba(0,0,0,0.15));">
                <defs>
                    <marker id="arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb" />
                    </marker>
                    <marker id="arrow-orange" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#ea580c" />
                    </marker>
                    <marker id="arrow-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#dc2626" />
                    </marker>
                </defs>
                
                <!-- Knockout / Background cuts -->
                <g stroke="var(--bg-knockout)" stroke-width="10" fill="none" stroke-linejoin="round" stroke-linecap="round">
                    <path id="bg-line-1" />
                    <path id="bg-line-2" />
                    <path id="bg-line-3" />
                </g>

                <!-- Actual Lines -->
                <!-- 1. GG Sheet Data Flow -->
                <path id="line-ggsheet" fill="none" stroke="#2563eb" stroke-width="3" stroke-dasharray="5,5" marker-end="url(#arrow-blue)" />
                <!-- 2. Patient Transfer (Moderate) -->
                <path id="line-transfer" fill="none" stroke="#ea580c" stroke-width="4" marker-end="url(#arrow-orange)" />
                <!-- 3. Notify Clinic (Severe) -->
                <path id="line-notify" fill="none" stroke="#dc2626" stroke-width="3" stroke-dasharray="5,5" marker-end="url(#arrow-red)" />
            </svg>

            <!-- Grid 2 Columns -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10 px-2 sm:px-4">

                <!-- ================= LEFT COLUMN: หน่วยบริการด่านหน้า ================= -->
                <div class="col-front border-2 rounded-[2rem] p-5 sm:p-6 flex flex-col relative" id="col-front">
                    <div class="flex items-center justify-center gap-3 mb-6 border-b-2 border-blue-200 dark:border-blue-800 pb-3">
                        <div class="bg-blue-600 text-white p-2 rounded-lg"><i data-lucide="building" class="w-6 h-6"></i></div>
                        <h3 class="font-extrabold text-blue-900 dark:text-blue-300 text-lg sm:text-xl">OPD / ER / PCU / รพ.สต.</h3>
                    </div>
                    
                    <div class="space-y-6 flex-grow flex flex-col">
                        
                        <!-- หน้าที่ 1: เฝ้าระวัง -->
                        <div class="bg-white dark:bg-slate-800 rounded-xl p-4 sm:p-5 border border-slate-200 dark:border-slate-700 smart-card relative" id="box-front-surv">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="bg-blue-100 text-blue-800 font-bold w-6 h-6 rounded-full flex items-center justify-center text-sm">1</span>
                                <h4 class="font-bold text-main text-base">หน้าที่: เฝ้าระวัง</h4>
                            </div>
                            <div class="flex items-start gap-3 bg-blue-50 dark:bg-blue-900/30 p-3 rounded-lg border border-blue-100 dark:border-blue-800">
                                <i data-lucide="file-spreadsheet" class="w-5 h-5 text-blue-600 mt-0.5 shrink-0"></i>
                                <p class="text-sm font-medium text-main leading-snug">บันทึกข้อมูลผู้ป่วยลงใน<br/>ระบบ <span class="font-bold text-blue-700 dark:text-blue-400">GG Sheets</span></p>
                            </div>
                        </div>

                        <!-- หน้าที่ 2: คัดกรอง -->
                        <div class="bg-white dark:bg-slate-800 rounded-xl p-4 sm:p-5 border border-slate-200 dark:border-slate-700 smart-card flex-grow relative" id="box-front-screen">
                            <div class="flex items-center gap-2 mb-3 border-b border-slate-100 dark:border-slate-700 pb-2">
                                <span class="bg-blue-100 text-blue-800 font-bold w-6 h-6 rounded-full flex items-center justify-center text-sm">2</span>
                                <h4 class="font-bold text-main text-base">หน้าที่: คัดกรอง ซักประวัติ</h4>
                            </div>
                            
                            <div class="space-y-3 mt-4">
                                <!-- 2.1 ไม่เข้าข่าย -->
                                <div class="bg-slate-50 dark:bg-slate-700/50 p-3 rounded-lg border border-slate-200 dark:border-slate-600 flex items-start gap-3">
                                    <div class="w-2 h-2 rounded-full bg-slate-400 mt-1.5 shrink-0"></div>
                                    <div>
                                        <p class="text-sm font-bold text-slate-700 dark:text-slate-300">กรณีไม่เข้าข่าย</p>
                                        <p class="text-[13px] text-muted leading-tight mt-1">ให้การ <span class="font-semibold">รักษาตามอาการ</span></p>
                                    </div>
                                </div>

                                <!-- 2.2 เข้าข่าย (โยงไปขวา) -->
                                <div class="bg-orange-50 dark:bg-orange-900/20 p-3 rounded-lg border border-orange-200 dark:border-orange-800 flex items-start gap-3 relative" id="box-front-mod">
                                    <div class="w-2 h-2 rounded-full bg-orange-500 mt-1.5 shrink-0"></div>
                                    <div>
                                        <p class="text-sm font-bold text-orange-800 dark:text-orange-400">กรณีเข้าข่าย (มีอาการเล็กน้อย/ปานกลาง)</p>
                                        <p class="text-[13px] text-orange-700 dark:text-orange-500 leading-tight mt-1 font-semibold flex items-center">
                                            ส่งต่อผู้ป่วยให้แก่คลินิกมลพิษ <i data-lucide="arrow-right" class="w-4 h-4 ml-1 md:hidden"></i>
                                        </p>
                                    </div>
                                </div>

                                <!-- 2.3 รุนแรง -->
                                <div class="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border border-red-200 dark:border-red-800 flex items-start gap-3 relative" id="box-front-sev">
                                    <div class="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0"></div>
                                    <div>
                                        <p class="text-sm font-bold text-red-800 dark:text-red-400">หากมีอาการรุนแรง</p>
                                        <p class="text-[13px] text-red-700 dark:text-red-400 leading-tight mt-1">
                                            <span class="font-semibold bg-red-200 dark:bg-red-800 px-1 rounded">ส่งต่อห้องฉุกเฉิน (ER)</span><br/>
                                            + แจ้งให้คลินิกมลพิษทราบ
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- ================= RIGHT COLUMN: ทีมคลินิกมลพิษ ================= -->
                <div class="col-clinic border-2 rounded-[2rem] p-5 sm:p-6 flex flex-col relative" id="col-clinic">
                    <div class="flex items-center justify-center gap-3 mb-6 border-b-2 border-orange-200 dark:border-orange-800 pb-3">
                        <div class="bg-orange-500 text-white p-2 rounded-lg"><i data-lucide="stethoscope" class="w-6 h-6"></i></div>
                        <h3 class="font-extrabold text-orange-900 dark:text-orange-300 text-lg sm:text-xl">ทีมคลินิกมลพิษ</h3>
                    </div>
                    
                    <div class="space-y-6 flex-grow flex flex-col">
                        
                        <!-- หน้าที่ 1: เฝ้าระวัง -->
                        <div class="bg-white dark:bg-slate-800 rounded-xl p-4 sm:p-5 border border-slate-200 dark:border-slate-700 smart-card relative" id="box-clinic-surv">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="bg-orange-100 text-orange-800 font-bold w-6 h-6 rounded-full flex items-center justify-center text-sm">1</span>
                                <h4 class="font-bold text-main text-base">หน้าที่: เฝ้าระวัง</h4>
                            </div>
                            <div class="space-y-2 text-sm text-main">
                                <div class="flex items-start gap-2">
                                    <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-500 mt-0.5 shrink-0"></i>
                                    <p>ติดตามผ่านระบบ <span class="font-bold">HOS (ICD-10)</span> ที่เกี่ยวข้องกับ PM2.5</p>
                                </div>
                                <div class="flex items-start gap-2 bg-blue-50 dark:bg-blue-900/20 p-2 rounded border border-blue-100 dark:border-blue-800/50">
                                    <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-500 mt-0.5 shrink-0"></i>
                                    <p>ติดตามผ่าน <span class="font-bold">GG Sheets</span> จาก OPD/ER/PCU หนองหาร</p>
                                </div>
                            </div>
                        </div>

                        <!-- หน้าที่ 2: จัดการนัดหมายและคัดกรอง -->
                        <div class="bg-white dark:bg-slate-800 rounded-xl p-4 sm:p-5 border border-slate-200 dark:border-slate-700 smart-card flex-grow relative" id="box-clinic-screen">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="bg-orange-100 text-orange-800 font-bold w-6 h-6 rounded-full flex items-center justify-center text-sm">2</span>
                                <h4 class="font-bold text-main text-[15px] leading-tight">จัดการนัดหมาย (หมอพร้อม/Telemed/Walk-in)<br/>และ <span class="text-orange-600">คัดกรอง ซักประวัติ สอบสวนโรค</span></h4>
                            </div>
                            
                            <div class="space-y-3 mt-4 border-t border-slate-100 dark:border-slate-700 pt-3">
                                <!-- 2.1.1 ไม่เข้าข่าย/อาการเล็กน้อย -->
                                <div class="bg-emerald-50 dark:bg-emerald-900/20 p-3 rounded-lg border border-emerald-200 dark:border-emerald-800 flex items-start gap-3">
                                    <div class="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 shrink-0"></div>
                                    <div>
                                        <p class="text-sm font-bold text-emerald-800 dark:text-emerald-400">กรณีไม่เข้าข่าย / อาการเล็กน้อย</p>
                                        <p class="text-[13px] text-emerald-700 dark:text-emerald-500 leading-tight mt-1 font-medium">
                                            ให้คำแนะนำ และส่งต่อ <span class="font-bold">ทีม 3 หมอ</span>
                                        </p>
                                    </div>
                                </div>

                                <!-- 2.1.2 เข้าข่าย -->
                                <div class="bg-orange-50 dark:bg-orange-900/20 p-3 rounded-lg border border-orange-200 dark:border-orange-800 flex items-start gap-3 relative" id="box-clinic-sev">
                                    <div class="w-2 h-2 rounded-full bg-orange-500 mt-1.5 shrink-0"></div>
                                    <div class="w-full">
                                        <p class="text-sm font-bold text-orange-800 dark:text-orange-400">กรณีเข้าข่าย</p>
                                        <ul class="text-[13px] text-orange-700 dark:text-orange-300 leading-tight mt-1.5 space-y-1.5 list-disc list-inside">
                                            <li><span class="font-medium">ส่งพบแพทย์ ตรวจ Lab</span></li>
                                            <li><span class="font-medium text-red-600 dark:text-red-400">ส่งห้องฉุกเฉิน (ER)</span> หากอาการรุนแรง</li>
                                        </ul>
                                        
                                        <!-- แจ้งควบคุมโรค -->
                                        <div class="mt-3 bg-purple-100 dark:bg-purple-900/40 p-2 rounded border border-purple-200 dark:border-purple-700 flex items-start gap-2">
                                            <i data-lucide="megaphone" class="w-4 h-4 text-purple-600 mt-0.5 shrink-0"></i>
                                            <p class="text-xs font-bold text-purple-800 dark:text-purple-300 leading-snug">
                                                แจ้งข้อมูลผู้ป่วยแก่ งานควบคุมโรค<br/>
                                                <span class="font-normal">(เพื่อลงพื้นที่สอบสวนโรค + รายงาน สสจ.)</span>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

            </div>
        </div>

        <!-- Script สำหรับวาดเส้นเชื่อมโยง (เฉพาะจอ Desktop) -->
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                lucide.createIcons();
            });

            function drawFlowLines() {
                const svg = document.getElementById('flow-svg');
                const container = document.getElementById('main-container');

                if(window.innerWidth >= 768 && svg && container) {
                    svg.classList.remove('hidden');

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

                    const draw = (id, pathString) => {
                        const el = document.getElementById(id);
                        if(el) el.setAttribute('d', pathString);
                        const bgEl = document.getElementById(id.replace('line-', 'bg-line-'));
                        if(bgEl) bgEl.setAttribute('d', pathString);
                    };

                    // Boxes
                    const fSurv = getR('box-front-surv');
                    const cSurv = getR('box-clinic-surv');
                    
                    const fMod = getR('box-front-mod');
                    const cScreen = getR('box-clinic-screen');
                    
                    const fSev = getR('box-front-sev');

                    // 1. เส้นจาก เฝ้าระวังด่านหน้า -> เฝ้าระวังคลินิก (ข้อมูล GG Sheets)
                    if(fSurv && cSurv) {
                        // โยงจากขอบขวากล่องซ้าย ไปขอบซ้ายกล่องขวา แบบ S-curve หรือเส้นหักศอก
                        const startX = fSurv.right;
                        const startY = fSurv.cy;
                        const endX = cSurv.left;
                        const endY = cSurv.cy;
                        const midX = startX + (endX - startX) / 2;
                        draw('line-ggsheet', `M ${startX} ${startY} L ${midX} ${startY} L ${midX} ${endY} L ${endX - 5} ${endY}`);
                    }

                    // 2. เส้นส่งต่อผู้ป่วยอาการปานกลาง -> คลินิกมลพิษ
                    if(fMod && cScreen) {
                        const startX = fMod.right;
                        const startY = fMod.cy;
                        const endX = cScreen.left;
                        // ชี้ไปที่กลางกล่องคัดกรองของคลินิก
                        const endY = cScreen.top + 40; 
                        const midX = startX + (endX - startX) / 2;
                        draw('line-transfer', `M ${startX} ${startY} L ${midX} ${startY} L ${midX} ${endY} L ${endX - 5} ${endY}`);
                    }

                    // 3. เส้นแจ้งคลินิกทราบ (อาการรุนแรง)
                    if(fSev && cScreen) {
                        const startX = fSev.right;
                        const startY = fSev.cy;
                        const endX = cScreen.left;
                        // ชี้ไปที่ส่วนจัดการของคลินิกด้านล่างๆ
                        const endY = cScreen.bottom - 40; 
                        const midX = startX + (endX - startX) * 0.3; // หักเลี้ยวก่อนเส้นอื่นเล็กน้อยเพื่อไม่ทับกัน
                        draw('line-notify', `M ${startX} ${startY} L ${midX} ${startY} L ${midX} ${endY} L ${endX - 5} ${endY}`);
                    }

                } else {
                    if(svg) svg.classList.add('hidden');
                }
            }

            window.addEventListener('resize', drawFlowLines);
            window.onload = () => { 
                setTimeout(drawFlowLines, 100); 
                setTimeout(drawFlowLines, 500); 
            };
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=950, scrolling=True)
