import streamlit.components.v1 as components

def render_roles():
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
                .text-custom-title { color: #93c5fd; }
                .text-custom-body { color: #cbd5e1; }
            }
            @media (prefers-color-scheme: light) {
                body { color: #334155; }
                .bg-custom-card { background-color: #ffffff; border-color: #e2e8f0; }
                .text-custom-title { color: #1e3a8a; }
                .text-custom-body { color: #475569; }
            }
        </style>
    </head>
    <body>
        
        <div class="max-w-6xl mx-auto">
            <!-- Header -->
            <div class="text-center mb-10">
                <div class="inline-flex items-center justify-center p-3 bg-blue-100 rounded-full mb-4">
                    <i data-lucide="users" class="w-8 h-8 text-blue-600"></i>
                </div>
                <h2 class="text-3xl sm:text-4xl font-extrabold text-custom-title mb-3 tracking-wide">บทบาทของแต่ละหน่วยงาน</h2>
                <p class="text-lg text-custom-body max-w-2xl mx-auto">
                    สรุปบทบาทและหน้าที่รับผิดชอบของแต่ละส่วนงานตามกระบวนการดูแลผู้ป่วยที่ได้รับผลกระทบจากฝุ่น PM 2.5
                </p>
            </div>

            <!-- Roles Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                <!-- 1. บริการออนไลน์ -->
                <div class="bg-custom-card border rounded-2xl p-6 transition-all duration-300 card-hover">
                    <div class="flex items-center gap-4 mb-4 border-b pb-4 border-slate-100 dark:border-slate-700">
                        <div class="bg-blue-100 p-3 rounded-xl">
                            <i data-lucide="smartphone" class="w-6 h-6 text-blue-600"></i>
                        </div>
                        <h3 class="text-xl font-bold text-custom-title">ระบบบริการออนไลน์<br><span class="text-sm font-medium text-slate-500 dark:text-slate-400">หมอพร้อม / Telemedicine</span></h3>
                    </div>
                    <ul class="space-y-3 text-custom-body text-[15px]">
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-blue-500 mr-2 shrink-0 mt-0.5"></i> <span>ให้คำปรึกษาออนไลน์แก่ประชาชน</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-blue-500 mr-2 shrink-0 mt-0.5"></i> <span>ทำการคัดกรองอาการเบื้องต้น</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-blue-500 mr-2 shrink-0 mt-0.5"></i> <span>ให้คำแนะนำการปฏิบัติตัว (กรณีอาการเล็กน้อย)</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-blue-500 mr-2 shrink-0 mt-0.5"></i> <span>ติดตามอาการและสั่งยาผ่านระบบ Telemedicine สำหรับผู้ป่วยอาการคงที่</span></li>
                    </ul>
                </div>

                <!-- 2. จุดรับบริการปฐมภูมิ -->
                <div class="bg-custom-card border rounded-2xl p-6 transition-all duration-300 card-hover">
                    <div class="flex items-center gap-4 mb-4 border-b pb-4 border-slate-100 dark:border-slate-700">
                        <div class="bg-pink-100 p-3 rounded-xl">
                            <i data-lucide="hospital" class="w-6 h-6 text-pink-600"></i>
                        </div>
                        <h3 class="text-xl font-bold text-custom-title">จุดเข้ารับบริการ<br><span class="text-sm font-medium text-slate-500 dark:text-slate-400">รพ. / รพ.สต. / PCU หนองหาร</span></h3>
                    </div>
                    <ul class="space-y-3 text-custom-body text-[15px]">
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-pink-500 mr-2 shrink-0 mt-0.5"></i> <span>ซักประวัติและประเมินอาการเบื้องต้น</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-pink-500 mr-2 shrink-0 mt-0.5"></i> <span>ลงแบบคัดกรองสอบสวนโรคที่เกิดจาก PM 2.5</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-pink-500 mr-2 shrink-0 mt-0.5"></i> <span>ส่งตรวจคลินิกปกติตามอาการ (กรณีไม่เข้าข่าย)</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-pink-500 mr-2 shrink-0 mt-0.5"></i> <span>ประสานส่งต่อผู้ป่วยเข้าคลินิกมลพิษ (เฉพาะ รพ.)</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-pink-500 mr-2 shrink-0 mt-0.5"></i> <span>ประสาน 1669 หากพบผู้ป่วยมีอาการรุนแรง</span></li>
                    </ul>
                </div>

                <!-- 3. คลินิกมลพิษ -->
                <div class="bg-custom-card border rounded-2xl p-6 transition-all duration-300 card-hover">
                    <div class="flex items-center gap-4 mb-4 border-b pb-4 border-slate-100 dark:border-slate-700">
                        <div class="bg-orange-100 p-3 rounded-xl">
                            <i data-lucide="stethoscope" class="w-6 h-6 text-orange-600"></i>
                        </div>
                        <h3 class="text-xl font-bold text-custom-title">คลินิกมลพิษ<br><span class="text-sm font-medium text-slate-500 dark:text-slate-400">เฉพาะโรงพยาบาล</span></h3>
                    </div>
                    <ul class="space-y-3 text-custom-body text-[15px]">
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-orange-500 mr-2 shrink-0 mt-0.5"></i> <span>รับส่งต่อผู้ป่วยที่เข้าข่ายอาการเล็กน้อยถึงปานกลาง</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-orange-500 mr-2 shrink-0 mt-0.5"></i> <span>ซักประวัติ ตรวจร่างกาย และตรวจทางห้องปฏิบัติการ</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-orange-500 mr-2 shrink-0 mt-0.5"></i> <span>วินิจฉัยโดยแพทย์และสหวิชาชีพ</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-orange-500 mr-2 shrink-0 mt-0.5"></i> <span>วางแผนการรักษา (ให้ยากลับบ้าน, Admit, หรือส่ง Refer)</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-orange-500 mr-2 shrink-0 mt-0.5"></i> <span>ให้คำปรึกษาก่อนผู้ป่วยกลับบ้าน</span></li>
                    </ul>
                </div>

                <!-- 4. งานเฝ้าระวังและข้อมูล -->
                <div class="bg-custom-card border rounded-2xl p-6 transition-all duration-300 card-hover">
                    <div class="flex items-center gap-4 mb-4 border-b pb-4 border-slate-100 dark:border-slate-700">
                        <div class="bg-purple-100 p-3 rounded-xl">
                            <i data-lucide="activity" class="w-6 h-6 text-purple-600"></i>
                        </div>
                        <h3 class="text-xl font-bold text-custom-title">งานเฝ้าระวัง<br><span class="text-sm font-medium text-slate-500 dark:text-slate-400">OPD / ER / PCU หนองหาร</span></h3>
                    </div>
                    <ul class="space-y-3 text-custom-body text-[15px]">
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-purple-500 mr-2 shrink-0 mt-0.5"></i> <span>ดึงข้อมูล ICD-10 โรคที่เกี่ยวข้องกับการสัมผัส PM 2.5</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-purple-500 mr-2 shrink-0 mt-0.5"></i> <span>รวบรวมและแจ้งข้อมูลผู้ป่วยผ่าน Google Sheets</span></li>
                    </ul>
                </div>

                <!-- 5. ควบคุมโรค -->
                <div class="bg-custom-card border rounded-2xl p-6 transition-all duration-300 card-hover">
                    <div class="flex items-center gap-4 mb-4 border-b pb-4 border-slate-100 dark:border-slate-700">
                        <div class="bg-teal-100 p-3 rounded-xl">
                            <i data-lucide="shield-alert" class="w-6 h-6 text-teal-600"></i>
                        </div>
                        <h3 class="text-xl font-bold text-custom-title">งานควบคุมโรค<br><span class="text-sm font-medium text-slate-500 dark:text-slate-400">ทีมควบคุมโรค / สสจ.</span></h3>
                    </div>
                    <ul class="space-y-3 text-custom-body text-[15px]">
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-teal-500 mr-2 shrink-0 mt-0.5"></i> <span>รับข้อมูลผู้เข้าข่าย/ผู้ป่วยอาการรุนแรงเพื่อดำเนินการตรวจสอบ</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-teal-500 mr-2 shrink-0 mt-0.5"></i> <span>ลงพื้นที่ซักประวัติ สอบสวนโรคอย่างละเอียด</span></li>
                        <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-teal-500 mr-2 shrink-0 mt-0.5"></i> <span>รายงานและแจ้งข้อมูลการระบาดต่อ สสจ.เชียงใหม่</span></li>
                    </ul>
                </div>

                <!-- 6. ฉุกเฉิน 1669 / ทีม 3 หมอ -->
                <div class="space-y-6">
                    <div class="bg-custom-card border rounded-2xl p-6 transition-all duration-300 card-hover">
                        <div class="flex items-center gap-4 mb-4 border-b pb-4 border-slate-100 dark:border-slate-700">
                            <div class="bg-red-100 p-3 rounded-xl">
                                <i data-lucide="ambulance" class="w-6 h-6 text-red-600"></i>
                            </div>
                            <h3 class="text-xl font-bold text-custom-title">ฉุกเฉินและส่งต่อ<br><span class="text-sm font-medium text-slate-500 dark:text-slate-400">1669 / ห้องฉุกเฉิน</span></h3>
                        </div>
                        <ul class="space-y-3 text-custom-body text-[15px]">
                            <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-red-500 mr-2 shrink-0 mt-0.5"></i> <span>รับแจ้งเหตุและดูแลผู้ป่วยที่มีอาการรุนแรง</span></li>
                            <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-red-500 mr-2 shrink-0 mt-0.5"></i> <span>ดำเนินการส่งต่อ (Refer) ผู้ป่วยไปรักษายังจุดที่เหมาะสม</span></li>
                        </ul>
                    </div>

                    <div class="bg-custom-card border rounded-2xl p-6 transition-all duration-300 card-hover">
                        <div class="flex items-center gap-4 mb-4 border-b pb-4 border-slate-100 dark:border-slate-700">
                            <div class="bg-emerald-100 p-3 rounded-xl">
                                <i data-lucide="home" class="w-6 h-6 text-emerald-600"></i>
                            </div>
                            <h3 class="text-xl font-bold text-custom-title">การดูแลต่อเนื่อง<br><span class="text-sm font-medium text-slate-500 dark:text-slate-400">ทีม 3 หมอ / อปท.</span></h3>
                        </div>
                        <ul class="space-y-3 text-custom-body text-[15px]">
                            <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-emerald-500 mr-2 shrink-0 mt-0.5"></i> <span>รับข้อมูลและให้คำแนะนำเบื้องต้นแก่ผู้ป่วย</span></li>
                            <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-emerald-500 mr-2 shrink-0 mt-0.5"></i> <span>ลงพื้นที่เยี่ยมบ้านดูแลผู้ป่วยหลังจำหน่าย</span></li>
                            <li class="flex items-start"><i data-lucide="check-circle" class="w-5 h-5 text-emerald-500 mr-2 shrink-0 mt-0.5"></i> <span>ประเมินสภาพแวดล้อมที่อยู่อาศัยซ้ำให้เหมาะสม</span></li>
                        </ul>
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
    
    components.html(html_code, height=1300, scrolling=True)
