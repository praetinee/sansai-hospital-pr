import streamlit.components.v1 as components

def render_roles():
    # โค้ด HTML สำหรับหน้าบทบาทหน่วยงาน อ้างอิงข้อมูลจาก Flow การให้บริการโดยตรง
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
                padding: 1rem 1rem 3rem 1rem; 
            }
            .card-hover:hover {
                transform: translateY(-4px);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            }
            /* สีสำหรับธีมสว่างและมืดตามระบบ Streamlit */
            @media (prefers-color-scheme: dark) {
                body { color: #e2e8f0; }
                .bg-custom-card { background-color: #1e293b; border-color: #334155; }
                .bg-forward { background-color: #334155; }
                .text-custom-title { color: #93c5fd; }
                .text-custom-body { color: #cbd5e1; }
                .border-separator { border-color: #475569; }
            }
            @media (prefers-color-scheme: light) {
                body { color: #334155; }
                .bg-custom-card { background-color: #ffffff; border-color: #e2e8f0; }
                .bg-forward { background-color: #f8fafc; }
                .text-custom-title { color: #1e3a8a; }
                .text-custom-body { color: #475569; }
                .border-separator { border-color: #e2e8f0; }
            }
        </style>
    </head>
    <body>
        
        <div class="max-w-5xl mx-auto">
            <!-- Header -->
            <div class="text-center mb-10">
                <div class="inline-flex items-center justify-center p-3 bg-blue-100 rounded-full mb-4">
                    <i data-lucide="network" class="w-8 h-8 text-blue-600"></i>
                </div>
                <h2 class="text-3xl sm:text-4xl font-extrabold text-custom-title mb-3 tracking-wide">บทบาทของแต่ละหน่วยงาน</h2>
                <p class="text-lg text-custom-body max-w-2xl mx-auto">
                    สรุปหน้าที่รับผิดชอบและลำดับการส่งต่อผู้ป่วย อ้างอิงตาม Flow การให้บริการ
                </p>
            </div>

            <!-- Timeline/Grid of Roles -->
            <div class="space-y-6">

                <!-- 1. บริการออนไลน์ -->
                <div class="bg-custom-card border rounded-2xl p-0 overflow-hidden transition-all duration-300 card-hover">
                    <div class="p-6">
                        <div class="flex items-center gap-4 mb-4">
                            <div class="bg-blue-100 p-3 rounded-xl shrink-0">
                                <i data-lucide="monitor-smartphone" class="w-7 h-7 text-blue-600"></i>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-custom-title">1. ทีมให้บริการออนไลน์</h3>
                                <p class="text-sm font-medium text-blue-600 dark:text-blue-400">ระบบหมอพร้อม / Telemedicine</p>
                            </div>
                        </div>
                        <div class="pl-[4.5rem]">
                            <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="check-square" class="w-4 h-4 text-emerald-500"></i> หน้าที่รับผิดชอบ:</p>
                            <ul class="list-disc list-outside ml-5 text-custom-body text-[15px] space-y-1 mb-4">
                                <li>รับปรึกษาออนไลน์</li>
                                <li>ทำการคัดกรองอาการเบื้องต้น</li>
                            </ul>
                        </div>
                    </div>
                    <div class="bg-forward border-t border-separator px-6 py-4 pl-[6rem]">
                        <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="arrow-right-circle" class="w-4 h-4 text-orange-500"></i> การส่งต่อหน่วยงานถัดไป:</p>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-custom-body">
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">ทีม 3 หมอ:</span> กรณีไม่เข้าข่าย/อาการเล็กน้อย (เพื่อให้คำแนะนำการปฏิบัติตัว)</span></div>
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">รพ./รพ.สต./PCU:</span> กรณีเข้าข่ายมีอาการที่สงสัย</span></div>
                            <div class="flex items-start gap-2 md:col-span-2"><span class="text-red-500 font-bold">➔</span> <span><span class="font-bold text-red-600 dark:text-red-400">1669:</span> กรณีผู้ป่วยมีอาการรุนแรง</span></div>
                        </div>
                    </div>
                </div>

                <!-- 2. จุดรับบริการปฐมภูมิ -->
                <div class="bg-custom-card border rounded-2xl p-0 overflow-hidden transition-all duration-300 card-hover">
                    <div class="p-6">
                        <div class="flex items-center gap-4 mb-4">
                            <div class="bg-pink-100 p-3 rounded-xl shrink-0">
                                <i data-lucide="hospital" class="w-7 h-7 text-pink-600"></i>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-custom-title">2. จุดรับบริการ / ปฐมภูมิ</h3>
                                <p class="text-sm font-medium text-pink-600 dark:text-pink-400">รพ. / รพ.สต. / PCU หนองหาร</p>
                            </div>
                        </div>
                        <div class="pl-[4.5rem]">
                            <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="check-square" class="w-4 h-4 text-emerald-500"></i> หน้าที่รับผิดชอบ:</p>
                            <ul class="list-disc list-outside ml-5 text-custom-body text-[15px] space-y-1 mb-4">
                                <li>รับผู้ป่วย Walk-in และผู้ป่วยที่ส่งต่อมาจากระบบออนไลน์</li>
                                <li>เจ้าหน้าที่ซักประวัติ / อาการเบื้องต้น</li>
                                <li>ลงแบบคัดกรองสอบสวนโรคที่เกิดจาก PM 2.5</li>
                            </ul>
                        </div>
                    </div>
                    <div class="bg-forward border-t border-separator px-6 py-4 pl-[6rem]">
                        <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="arrow-right-circle" class="w-4 h-4 text-orange-500"></i> การส่งต่อหน่วยงานถัดไป:</p>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-custom-body">
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">คลินิกทั่วไป:</span> กรณีไม่เข้าข่าย (ส่งตรวจตามอาการโรค)</span></div>
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">ทีมควบคุมโรค:</span> แจ้งข้อมูลเมื่อพบผู้ป่วยเข้าข่าย/อาการรุนแรง</span></div>
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">คลินิกมลพิษ:</span> กรณีเข้าข่ายอาการเล็กน้อย/ปานกลาง (รพ.สต./PCU ให้ส่งต่อ รพ.)</span></div>
                            <div class="flex items-start gap-2"><span class="text-red-500 font-bold">➔</span> <span><span class="font-bold text-red-600 dark:text-red-400">ห้องฉุกเฉิน (ER):</span> กรณีผู้ป่วยอาการรุนแรง</span></div>
                        </div>
                    </div>
                </div>

                <!-- 3. ทีมเฝ้าระวัง -->
                <div class="bg-custom-card border rounded-2xl p-0 overflow-hidden transition-all duration-300 card-hover">
                    <div class="p-6">
                        <div class="flex items-center gap-4 mb-4">
                            <div class="bg-purple-100 p-3 rounded-xl shrink-0">
                                <i data-lucide="activity" class="w-7 h-7 text-purple-600"></i>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-custom-title">3. ทีมเฝ้าระวัง</h3>
                                <p class="text-sm font-medium text-purple-600 dark:text-purple-400">OPD / ER / PCU หนองหาร</p>
                            </div>
                        </div>
                        <div class="pl-[4.5rem]">
                            <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="check-square" class="w-4 h-4 text-emerald-500"></i> หน้าที่รับผิดชอบ:</p>
                            <ul class="list-disc list-outside ml-5 text-custom-body text-[15px] space-y-1 mb-4">
                                <li>ดึงข้อมูล ICD-10 โรคที่เกี่ยวข้องกับการสัมผัส PM 2.5</li>
                                <li>หน่วยงานที่เกี่ยวข้อง แจ้งข้อมูลผู้ป่วยผ่านระบบ Google Sheets</li>
                            </ul>
                        </div>
                    </div>
                    <div class="bg-forward border-t border-separator px-6 py-4 pl-[6rem]">
                        <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="arrow-right-circle" class="w-4 h-4 text-orange-500"></i> การนำข้อมูลไปใช้:</p>
                        <div class="text-sm text-custom-body">
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span>นำข้อมูลไปประกอบการซักประวัติและคัดกรองสอบสวนโรคที่เกิดจาก PM 2.5</span></div>
                        </div>
                    </div>
                </div>

                <!-- 4. ทีมควบคุมโรค -->
                <div class="bg-custom-card border rounded-2xl p-0 overflow-hidden transition-all duration-300 card-hover">
                    <div class="p-6">
                        <div class="flex items-center gap-4 mb-4">
                            <div class="bg-indigo-100 p-3 rounded-xl shrink-0">
                                <i data-lucide="shield-alert" class="w-7 h-7 text-indigo-600"></i>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-custom-title">4. ทีมควบคุมโรค</h3>
                                <p class="text-sm font-medium text-indigo-600 dark:text-indigo-400">หน่วยงานควบคุมโรค</p>
                            </div>
                        </div>
                        <div class="pl-[4.5rem]">
                            <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="check-square" class="w-4 h-4 text-emerald-500"></i> หน้าที่รับผิดชอบ:</p>
                            <ul class="list-disc list-outside ml-5 text-custom-body text-[15px] space-y-1 mb-4">
                                <li>รับข้อมูลผู้ป่วยที่เข้าข่าย / ผู้ป่วยอาการรุนแรง</li>
                                <li>ลงพื้นที่เพื่อทำการซักประวัติและสอบสวนโรคเพิ่มเติม</li>
                            </ul>
                        </div>
                    </div>
                    <div class="bg-forward border-t border-separator px-6 py-4 pl-[6rem]">
                        <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="arrow-right-circle" class="w-4 h-4 text-orange-500"></i> การส่งต่อหน่วยงานถัดไป:</p>
                        <div class="text-sm text-custom-body">
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">สสจ.เชียงใหม่:</span> แจ้งข้อมูลและรายงานสถานการณ์ให้สำนักงานสาธารณสุขจังหวัดรับทราบ</span></div>
                        </div>
                    </div>
                </div>

                <!-- 5. คลินิกมลพิษ -->
                <div class="bg-custom-card border rounded-2xl p-0 overflow-hidden transition-all duration-300 card-hover">
                    <div class="p-6">
                        <div class="flex items-center gap-4 mb-4">
                            <div class="bg-orange-100 p-3 rounded-xl shrink-0">
                                <i data-lucide="stethoscope" class="w-7 h-7 text-orange-600"></i>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-custom-title">5. ทีมคลินิกมลพิษ</h3>
                                <p class="text-sm font-medium text-orange-600 dark:text-orange-400">คลินิกมลพิษ (เฉพาะ รพ.)</p>
                            </div>
                        </div>
                        <div class="pl-[4.5rem]">
                            <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="check-square" class="w-4 h-4 text-emerald-500"></i> หน้าที่รับผิดชอบ:</p>
                            <ul class="list-disc list-outside ml-5 text-custom-body text-[15px] space-y-1 mb-4">
                                <li>รับผู้ป่วยที่ส่งต่อมาจาก รพ.สต. และ PCU หนองหาร</li>
                                <li>แพทย์/สหวิชาชีพ ทำการซักประวัติ ตรวจร่างกาย และตรวจทางห้องปฏิบัติการ</li>
                                <li>วางแผนการรักษาให้แก่ผู้ป่วย</li>
                            </ul>
                        </div>
                    </div>
                    <div class="bg-forward border-t border-separator px-6 py-4 pl-[6rem]">
                        <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="arrow-right-circle" class="w-4 h-4 text-orange-500"></i> ผลการรักษา / การส่งต่อ:</p>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-custom-body">
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">ให้ยากลับบ้าน:</span> เข้าสู่กระบวนการดูแลต่อเนื่อง</span></div>
                            <div class="flex items-start gap-2"><span class="text-orange-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">Admit ให้การรักษา:</span> เข้าสู่กระบวนการดูแลต่อเนื่องหลังจำหน่าย</span></div>
                            <div class="flex items-start gap-2"><span class="text-red-500 font-bold">➔</span> <span><span class="font-bold text-red-600 dark:text-red-400">ส่ง REFER:</span> ส่งต่อผู้ป่วยไปรักษาตัวยังสถานพยาบาลอื่น</span></div>
                        </div>
                    </div>
                </div>

                <!-- 6. ฉุกเฉิน -->
                <div class="bg-custom-card border rounded-2xl p-0 overflow-hidden transition-all duration-300 card-hover">
                    <div class="p-6">
                        <div class="flex items-center gap-4 mb-4">
                            <div class="bg-red-100 p-3 rounded-xl shrink-0">
                                <i data-lucide="ambulance" class="w-7 h-7 text-red-600"></i>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-custom-title">6. ทีมแพทย์ฉุกเฉิน</h3>
                                <p class="text-sm font-medium text-red-600 dark:text-red-400">ห้องฉุกเฉิน (ER) / สายด่วน 1669</p>
                            </div>
                        </div>
                        <div class="pl-[4.5rem]">
                            <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="check-square" class="w-4 h-4 text-emerald-500"></i> หน้าที่รับผิดชอบ:</p>
                            <ul class="list-disc list-outside ml-5 text-custom-body text-[15px] space-y-1 mb-4">
                                <li>รับแจ้งเหตุ ประสานงาน และออกรับผู้ป่วยที่มีอาการรุนแรงผ่าน 1669</li>
                                <li>รับผู้ป่วยอาการรุนแรงเข้าห้องฉุกเฉิน เพื่อประเมินและให้การรักษาเบื้องต้น</li>
                            </ul>
                        </div>
                    </div>
                    <div class="bg-forward border-t border-separator px-6 py-4 pl-[6rem]">
                        <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="arrow-right-circle" class="w-4 h-4 text-orange-500"></i> การส่งต่อหน่วยงานถัดไป:</p>
                        <div class="text-sm text-custom-body">
                            <div class="flex items-start gap-2"><span class="text-red-500 font-bold">➔</span> <span><span class="font-bold text-red-600 dark:text-red-400">ส่ง REFER:</span> ประสานงานส่งต่อผู้ป่วยอาการรุนแรงไปยังสถานพยาบาลระดับสูง</span></div>
                        </div>
                    </div>
                </div>

                <!-- 7. การดูแลต่อเนื่อง -->
                <div class="bg-custom-card border rounded-2xl p-0 overflow-hidden transition-all duration-300 card-hover">
                    <div class="p-6">
                        <div class="flex items-center gap-4 mb-4">
                            <div class="bg-emerald-100 p-3 rounded-xl shrink-0">
                                <i data-lucide="home" class="w-7 h-7 text-emerald-600"></i>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-custom-title">7. ทีมดูแลต่อเนื่อง</h3>
                                <p class="text-sm font-medium text-emerald-600 dark:text-emerald-400">ทีม 3 หมอ / อปท.</p>
                            </div>
                        </div>
                        <div class="pl-[4.5rem]">
                            <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="check-square" class="w-4 h-4 text-emerald-500"></i> หน้าที่รับผิดชอบ:</p>
                            <ul class="list-disc list-outside ml-5 text-custom-body text-[15px] space-y-1 mb-4">
                                <li>ให้คำปรึกษาก่อนผู้ป่วยกลับบ้าน</li>
                                <li>ลงพื้นที่เยี่ยมบ้านโดยทีม 3 หมอ และ อปท.</li>
                                <li>ประเมินสภาพที่อยู่ซ้ำให้เหมาะสมกับผู้ป่วย</li>
                                <li><span class="font-semibold text-emerald-600 dark:text-emerald-400">กรณีผู้ป่วยอาการคงที่:</span> ติดตามและสั่งยาผ่าน Telemedicine เพื่อลดความเสี่ยงสัมผัสฝุ่น</li>
                            </ul>
                        </div>
                    </div>
                    <div class="bg-forward border-t border-separator px-6 py-4 pl-[6rem]">
                        <p class="font-bold text-custom-body mb-2 flex items-center gap-2"><i data-lucide="arrow-right-circle" class="w-4 h-4 text-orange-500"></i> การส่งต่อ/สิ้นสุด:</p>
                        <div class="text-sm text-custom-body">
                            <div class="flex items-start gap-2"><span class="text-emerald-500 font-bold">➔</span> <span><span class="font-bold text-slate-700 dark:text-slate-300">สิ้นสุดกระบวนการ:</span> เฝ้าระวังผู้ป่วยในชุมชนอย่างต่อเนื่องเพื่อป้องกันการกำเริบซ้ำ</span></div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <script>
            // สร้างไอคอนเมื่อโหลดหน้าเสร็จ
            document.addEventListener('DOMContentLoaded', () => {
                lucide.createIcons();
            });
        </script>
    </body>
    </html>
    """
    
    # ปรับความสูงตามจำนวนเนื้อหา
    components.html(html_code, height=1900, scrolling=True)
