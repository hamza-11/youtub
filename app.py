import streamlit as st
import yt_dlp
import os
import traceback

# ================== تحميل الفيديو ==================
def download_video(link, file_type, cookies_file=None, debug=False):
    progress_text = st.empty()
    progress_bar = st.progress(0)

    def my_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').replace('%','')
            try:
                percent = float(percent)
                progress_bar.progress(int(percent))
                progress_text.text(f"⬇️ جارِ التحميل: {percent:.1f}%")
            except:
                pass
        elif d['status'] == 'finished':
            progress_text.text("✅ اكتمل التحميل، جارِ التحويل...")
            progress_bar.progress(100)

    # إعداد yt-dlp
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
    }

    if file_type == "MP3":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)

            # تحديد اسم الملف النهائي
            base_filename = ydl.prepare_filename(info)
            if file_type == "MP3":
                file_name = os.path.splitext(base_filename)[0] + ".mp3"
            else:
                file_name = base_filename

        # التحقق من وجود الملف
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                file_data = f.read()
            st.download_button(
                label=f"⬇️ تنزيل {os.path.basename(file_name)}",
                data=file_data,
                file_name=os.path.basename(file_name),
                mime="audio/mpeg" if file_type == "MP3" else "video/mp4",
            )
            return f"✅ تم إنشاء رابط تنزيل: {os.path.basename(file_name)}"
        else:
            return f"⚠️ الملف لم يتم إنشاؤه."

    except Exception as e:
        if debug:
            error_details = traceback.format_exc()
            st.error("❌ حدث خطأ أثناء التحميل (تفاصيل كاملة):")
            st.code(error_details, language="bash")
        else:
            error_msg = str(e).split("\n")[0]
            st.error(f"❌ حدث خطأ: {error_msg}")
        return f"❌ فشل تحميل الرابط: {link}"

# ================== واجهة Streamlit ==================
st.set_page_config(page_title="تحميل YouTube MP3/MP4", layout="wide")

st.title("📥 تحميل فيديوهات YouTube (MP3 / MP4)")

st.markdown("""
**ملاحظات:**
- يمكنك إدخال عدة روابط (رابط في كل سطر).
- اختر الصيغة (MP3 / MP4).
- إذا كان الفيديو خاص أو يتطلب تسجيل دخول، يمكنك رفع ملف **cookies.txt** من حسابك.
""")

# إدخال البيانات
links = st.text_area("روابط YouTube", placeholder="ضع الروابط هنا...")
file_type = st.selectbox("اختر الصيغة", ["MP3", "MP4"])
cookies_file_upload = st.file_uploader("رفع ملف cookies.txt (اختياري)", type=["txt"])
debug_mode = st.checkbox("🔎 تفعيل وضع Debug (إظهار تفاصيل الأخطاء)", value=False)

# حفظ ملف الكوكيز لو موجود
cookies_file_path = None
if cookies_file_upload:
    cookies_file_path = "cookies.txt"
    with open(cookies_file_path, "wb") as f:
        f.write(cookies_file_upload.getbuffer())

# زر التحميل
if st.button("🚀 ابدأ التحميل"):
    if links.strip():
        links_list = links.strip().split("\n")
        for link in links_list:
            st.write(f"🔗 جاري التحميل من: {link}")
            status = download_video(link.strip(), file_type, cookies_file_path, debug=debug_mode)
            st.write(status)
    else:
        st.warning("⚠️ يرجى إدخال روابط صحيحة.")
