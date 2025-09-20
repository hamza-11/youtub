import streamlit as st
import yt_dlp
import os

def download_video(link, file_type, cookies_file=None):
    progress_text = st.empty()
    progress_bar = st.progress(0)

    def my_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').replace('%','')
            try:
                percent = float(percent)
                progress_bar.progress(int(percent))
                progress_text.text(f"⬇️ جارِ تحميل: {percent:.1f}%")
            except:
                pass
        elif d['status'] == 'finished':
            progress_text.text("✅ اكتمل التحميل، جارِ التحويل...")
            progress_bar.progress(100)

    # إعدادات yt-dlp
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
            file_ext = 'mp3' if file_type == 'MP3' else info.get("ext", "mp4")
            file_name = ydl.prepare_filename({'title': info['title'], 'ext': file_ext})

        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                file_data = f.read()
            st.download_button(
                label=f"تنزيل {os.path.basename(file_name)}",
                data=file_data,
                file_name=os.path.basename(file_name),
                mime="audio/mpeg" if file_type == "MP3" else "video/mp4",
            )
            return f"✅ تم إنشاء رابط تنزيل لـ: {link}"
        else:
            return f"⚠️ لم أجد الملف بعد التحميل."

    except Exception as e:
        return f"❌ حدث خطأ أثناء التحميل: {str(e)}"


# واجهة المستخدم
st.set_page_config(page_title="برنامج تحميل فيديوهات يوتيوب", layout="wide")

st.markdown("""
    <style>
    body {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        text-align: right;
    }
    .css-ffhzg2 {
        direction: rtl;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📥 برنامج تحميل فيديوهات يوتيوب")
st.markdown("""
<span style="color: orange;">**هام:**</span> لتجاوز مشكلة الفيديوهات الخاصة أو المحمية، يمكنك رفع ملف **cookies.txt** من حسابك في يوتيوب.
""", unsafe_allow_html=True)

st.write("أدخل روابط الفيديوهات أدناه (رابط في كل سطر) واختر الصيغة المطلوبة.")

# التعليمات
st.markdown("""
### 📝 التعليمات:
1. الصق روابط الفيديوهات من يوتيوب في المربع أدناه (رابط واحد في كل سطر).
2. اختر الصيغة المطلوبة: **MP3** للصوت أو **MP4** للفيديو.
3. يمكنك رفع ملف **cookies.txt** (اختياريًا) لتجاوز مشاكل الفيديوهات الخاصة.  
4. اضغط على زر **تحميل** لبدء التحميل.
""", unsafe_allow_html=True)

# إدخال البيانات
links = st.text_area("روابط YouTube", placeholder="الصق الروابط هنا...")
file_type = st.selectbox("اختر الصيغة", ["MP3", "MP4"])

cookies_file_upload = st.file_uploader("رفع ملف cookies.txt (اختياري)", type=["txt"])
cookies_file_path = None

if cookies_file_upload:
    cookies_file_path = "cookies.txt"
    with open(cookies_file_path, "wb") as f:
        f.write(cookies_file_upload.getbuffer())

# زر التحميل
download_button = st.button("تحميل الفيديوهات")

if download_button:
    if links.strip():
        links_list = links.strip().split("\n")
        for link in links_list:
            st.write(f"🔗 جاري التحميل من: {link}")
            status = download_video(link.strip(), file_type, cookies_file_path)
            st.write(status)
    else:
        st.warning("⚠️ يرجى إدخال روابط صحيحة.")
