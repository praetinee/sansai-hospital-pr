import streamlit.components.v1 as components

def render_dashboard():
    html_code = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Sarabun', sans-serif !important; background-color: #f8fafc; margin: 0; padding: 1rem 2rem; }
            ::-webkit-scrollbar { width: 8px; }
            ::-webkit-scrollbar-track { background: #f1f1f1; rounded: 8px; }
            ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 8px; }
            ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        </style>
    </head>
    <body class="text-slate-800">
        
        <!-- Image Zoom Modal -->
        <div id="zoom-modal" class="hidden fixed inset-0 z-[100] bg-black/90 backdrop-blur-sm items-center justify-center p-4 transition-opacity duration-300" onclick="closeZoom()">
            <div class="relative max-w-4xl w-full flex flex-col items-center">
                <button onclick="closeZoom()" class="absolute -top-12 right-0 text-white/80 hover:text-white transition-colors p-2 bg-white/10 rounded-full">
                    <i data-lucide="x" class="w-6 h-6"></i>
                </button>
                <img id="zoomed-img" src="" alt="Zoomed View" class="max-w-full max-h-[80vh] object-contain rounded-lg shadow-2xl bg-white p-2" onclick="event.stopPropagation()" />
                <p class="text-white/70 text-sm mt-4 font-medium bg-black/50 px-4 py-2 rounded-full backdrop-blur-md">แตะบริเวณว่างเพื่อปิด</p>
            </div>
        </div>

        <!-- Hero Section -->
        <div class="bg-gradient-to-b from-emerald-600 to-emerald-500 text-white pb-16 pt-10 px-4 rounded-[2.5rem] shadow-md mb-8">
            <div class="max-w-4xl mx-auto text-center space-y-4">
                <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tight">แผนรองรับวิกฤตฝุ่นละอองขนาดเล็ก PM2.5</h2>
                <p class="text-emerald-100 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
                    เตรียมความพร้อม เฝ้าระวัง และดูแลสุขภาพประชาชนในเขตอำเภอสันทราย 
                    ด้วยนวัตกรรมและการบริการทางการแพทย์
                </p>
            </div>
        </div>

        <main class="w-full max-w-7xl mx-auto space-y-8">
            
            <!-- 0. PHEOC Section -->
            <section class="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100 relative">
                <div class="absolute top-0 left-0 w-2 h-full bg-blue-500"></div>
                <div class="p-6 md:p-8 lg:p-10">
                    <div class="flex items-center space-x-3 mb-8">
                        <div class="bg-blue-100 p-2.5 rounded-xl">
                            <i data-lucide="shield-alert" class="text-blue-600 w-7 h-7 md:w-8 md:h-8"></i>
                        </div>
                        <h3 class="text-xl md:text-2xl font-bold text-slate-800">การเปิดศูนย์ปฏิบัติการฉุกเฉิน (PHEOC)</h3>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-gradient-to-br from-slate-50 to-blue-50/30 border border-slate-200 p-6 rounded-2xl flex items-center space-x-5 hover:shadow-md transition-shadow">
                            <div class="bg-blue-600 text-white p-4 rounded-full shadow-sm">
                                <i data-lucide="activity" class="w-6 h-6"></i>
                            </div>
                            <div>
                                <p class="text-sm md:text-base text-slate-500 font-medium mb-1">ระดับจังหวัดเชียงใหม่</p>
                                <p class="text-xl md:text-2xl font-bold text-slate-800">12 มกราคม 2569</p>
                            </div>
                        </div>
                        <div class="bg-gradient-to-br from-slate-50 to-sky-50/30 border border-slate-200 p-6 rounded-2xl flex items-center space-x-5 hover:shadow-md transition-shadow">
                            <div class="bg-sky-600 text-white p-4 rounded-full shadow-sm">
                                <i data-lucide="activity" class="w-6 h-6"></i>
                            </div>
                            <div>
                                <p class="text-sm md:text-base text-slate-500 font-medium mb-1">ระดับเขตสุขภาพที่ 1</p>
                                <p class="text-xl md:text-2xl font-bold text-slate-800">4 มีนาคม 2569</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 1. Real-time Monitoring Section -->
            <section class="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
                <div class="p-6 md:p-8 lg:p-10">
                    <div class="flex items-center space-x-3 mb-6">
                        <div class="bg-orange-100 p-2 rounded-lg">
                            <i data-lucide="wind" class="text-orange-600 w-6 h-6 md:w-8 md:h-8"></i>
                        </div>
                        <h3 class="text-xl md:text-2xl font-bold text-slate-800">การเฝ้าระวังค่าฝุ่น PM2.5 (Real-time)</h3>
                    </div>
                    
                    <div class="mb-8 border-b border-slate-100 pb-6 text-center lg:text-left">
                        <p class="text-slate-700 text-lg md:text-xl font-medium">จุดตรวจวัด: <span class="font-bold text-emerald-700">โรงพยาบาลสันทราย</span></p>
                        <p class="text-slate-500 mt-2 text-base md:text-lg">สนับสนุนเครื่อง DustBoy โดย คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเชียงใหม่</p>
                    </div>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12 items-start mb-8">
                        <div class="flex flex-col items-center w-full space-y-4 lg:col-span-2">
                            <h4 class="font-bold text-slate-700 text-lg flex items-center bg-slate-50 px-4 py-2 rounded-full">
                                <i data-lucide="smartphone" class="w-5 h-5 mr-2 text-emerald-600"></i> หน้าเว็บไซต์ (Dashboard)
                            </h4>
                            <div class="w-full h-[700px] max-w-full mx-auto rounded-xl overflow-hidden shadow-2xl border-4 border-slate-100 bg-white relative">
                                <iframe src="https://pm25-sansai-dashboard-tuc6yczy4hhl8vbmxdyxcp.streamlit.app/?embed=true&embed_options=light_theme" class="w-full h-full" style="border: none;" allowfullscreen></iframe>
                            </div>
                        </div>

                        <div class="flex flex-col items-center w-full space-y-6 lg:pt-4">
                            <h4 class="font-bold text-slate-700 text-lg flex items-center mb-4 bg-slate-50 px-4 py-2 rounded-full">
                                <i data-lucide="download" class="w-5 h-5 mr-2 text-emerald-600"></i> รูปรายงานผล (ดาวน์โหลดได้จากเวป)
                            </h4>
                            <div class="relative w-full max-w-xs mx-auto shadow-xl rounded-xl overflow-hidden border border-slate-200">
                                <img src="https://i.postimg.cc/qMTCvMHp/pm25-report-20260114-0413.png" alt="รายงาน" class="w-full h-auto object-cover" />
                            </div>
                            <p class="text-base text-slate-500 mt-3 text-center px-4">*ท่านสามารถกดรับรูปรายงานผลแบบนี้ได้ที่หน้า Dashboard</p>
                        </div>
                    </div>

                    <div class="w-full bg-slate-50/80 p-6 md:p-8 rounded-2xl border border-slate-200 flex flex-col md:flex-row items-center justify-center gap-8 backdrop-blur-sm">
                        <div class="flex flex-col md:flex-row items-center gap-6">
                            <div class="text-center md:text-right flex flex-col items-center md:items-end">
                                <p class="font-bold text-slate-800 text-lg md:text-xl mb-1">เข้าใช้งานระบบ</p>
                                <p class="text-slate-600 font-medium text-base">สแกนเพื่อดูค่าฝุ่น Real-time</p>
                                <button onclick="openZoom('https://i.postimg.cc/9fnJ6wS3/rad-b-PM2-5-rph-s-nth-ray.png')" class="text-emerald-600 text-sm mt-2 flex items-center hover:underline">
                                    <i data-lucide="maximize-2" class="w-4 h-4 mr-1"></i> (คลิกรูปเพื่อขยาย)
                                </button>
                            </div>
                            <div class="bg-white p-3 border border-slate-200 rounded-xl shadow-sm w-40 h-40 flex items-center justify-center cursor-zoom-in hover:scale-105 transition-all" onclick="openZoom('https://i.postimg.cc/9fnJ6wS3/rad-b-PM2-5-rph-s-nth-ray.png')">
                                <img src="https://i.postimg.cc/9fnJ6wS3/rad-b-PM2-5-rph-s-nth-ray.png" alt="QR Code" class="w-full h-full object-contain" />
                            </div>
                        </div>
                        <div class="hidden md:block w-px h-24 bg-slate-300"></div>
                        <div class="w-full max-w-xs text-center md:text-left">
                            <a href="https://pm25-sansai-dashboard-tuc6yczy4hhl8vbmxdyxcp.streamlit.app/" target="_blank" class="flex items-center justify-center w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-4 px-6 rounded-xl transition-all shadow-lg">
                                เปิด Dashboard <i data-lucide="external-link" class="ml-2 w-5 h-5"></i>
                            </a>
                            <p class="text-sm text-slate-400 mt-3 font-mono break-all px-2">pm25-sansai-dashboard.streamlit.app</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 2. Service Section -->
            <section class="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
                <div class="p-6 md:p-8 lg:p-10">
                    <div class="flex items-center space-x-3 mb-6">
                        <div class="bg-red-100 p-2 rounded-lg">
                            <i data-lucide="heart-pulse" class="text-red-600 w-6 h-6 md:w-8 md:h-8"></i>
                        </div>
                        <h3 class="text-xl md:text-2xl font-bold text-slate-800">คลินิกมลพิษ (บริการเชิงรับ)</h3>
                    </div>
                    <div class="flex flex-col items-center">
                        <p class="text-lg md:text-xl leading-relaxed font-medium text-slate-600 mb-8 text-center max-w-4xl mx-auto">
                            คลินิกมลพิษ ซึ่งประชาชนทั่วไปสามารถนัดหมายได้ง่ายผ่านหมอพร้อม เปิดให้บริการนัดหมาย จันทร์-ศุกร์ 8.00-14.00 น. ไม่ว่าจะเป็นทางแอพพลิเคชั่น หมอพร้อม หรือทางไลน์ หมอพร้อม ดังรูป
                        </p>
                        <div class="w-full max-w-6xl bg-slate-50 rounded-2xl p-4 md:p-6 border border-slate-100 shadow-inner flex justify-center">
                            <img src="https://i.postimg.cc/R0DP1WxQ/hmx-phr-xm.png" alt="หมอพร้อม" class="w-full h-auto object-contain rounded-lg shadow-md" />
                        </div>
                    </div>
                </div>
            </section>

            <!-- 3. Health Checks -->
            <section class="bg-white rounded-2xl shadow-lg border-t-8 border-indigo-500 p-6 md:p-8 flex flex-col hover:shadow-xl transition-shadow">
                <div class="flex items-center mb-8 border-b border-slate-100 pb-6">
                    <div class="bg-indigo-100 p-3.5 rounded-xl mr-4">
                        <i data-lucide="users" class="w-8 h-8 text-indigo-600"></i>
                    </div>
                    <h3 class="text-xl md:text-2xl font-bold text-slate-800">สรุปผลการตรวจสุขภาพอาสาสมัครดับไฟป่า</h3>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    <div class="flex items-start bg-slate-50 p-5 rounded-xl border border-slate-100">
                        <i data-lucide="calendar" class="w-6 h-6 text-indigo-400 mr-4 mt-0.5"></i>
                        <div>
                            <span class="block text-sm text-slate-500 font-bold uppercase tracking-wide mb-1">วันที่ตรวจ</span>
                            <span class="text-lg font-semibold text-slate-800">2 กุมภาพันธ์ 2569</span>
                        </div>
                    </div>
                    <div class="flex items-start bg-slate-50 p-5 rounded-xl border border-slate-100">
                        <i data-lucide="activity" class="w-6 h-6 text-indigo-400 mr-4 mt-0.5"></i>
                        <div>
                            <span class="block text-sm text-slate-500 font-bold uppercase tracking-wide mb-1">หน่วยงานและสถานที่</span>
                            <span class="text-base font-semibold text-slate-800 block">โดยทีม สสอ.สันทราย และ โรงพยาบาลสันทราย</span>
                            <span class="block text-sm text-slate-600 mt-1">ณ ที่ว่าการอำเภอสันทราย</span>
                        </div>
                    </div>
                </div>
                <div class="bg-gradient-to-r from-indigo-50 to-blue-50 p-6 md:p-8 rounded-2xl border border-indigo-100">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 items-center text-center">
                        <div class="bg-white p-6 rounded-xl shadow-sm border border-indigo-50/50 flex flex-col justify-center h-full">
                            <span class="block text-base text-slate-600 font-medium mb-3">จำนวนผู้เข้ารับการตรวจรวม</span>
                            <div class="flex items-baseline justify-center">
                                <span class="text-5xl font-extrabold text-indigo-700">128</span>
                                <span class="text-indigo-600 ml-2 font-medium text-lg">คน</span>
                            </div>
                        </div>
                        <div class="bg-white p-6 rounded-xl shadow-sm border border-emerald-50/50 flex flex-col justify-center h-full relative overflow-hidden">
                            <div class="absolute top-0 right-0 w-16 h-16 bg-emerald-100 rounded-bl-full opacity-50"></div>
                            <span class="block text-base text-slate-600 font-medium mb-3">สุขภาพเหมาะสมสำหรับการเป็น<br class="hidden md:block"/>ด่านหน้าผจญเพลิง</span>
                            <div class="flex flex-col items-center justify-center">
                                <div class="flex items-baseline">
                                    <span class="text-5xl font-extrabold text-emerald-600">68</span>
                                    <span class="text-emerald-600 ml-2 font-medium text-lg">คน</span>
                                </div>
                                <span class="text-emerald-500 bg-emerald-50 px-3 py-1 rounded-full text-sm font-bold mt-2">คิดเป็น 53.1%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
        
        <script>
            function openZoom(src) {
                document.getElementById('zoomed-img').src = src;
                const modal = document.getElementById('zoom-modal');
                modal.classList.remove('hidden');
                modal.classList.add('flex');
            }
            function closeZoom() {
                const modal = document.getElementById('zoom-modal');
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }
            document.addEventListener('DOMContentLoaded', () => { lucide.createIcons(); });
        </script>
    </body>
    </html>
    """
    
    # กำหนดความสูงให้ครอบคลุมหน้าจอ (เผื่อพื้นที่ล้นได้ ไม่เป็นไร)
    components.html(html_code, height=3600, scrolling=True)
