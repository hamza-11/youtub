import streamlit as st
import yt_dlp
import os

def download_video(link, file_type, cookies_str=None):
    ydl_opts = {
        'format': 'bestaudio/best' if file_type == "MP3" else 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    if file_type == "MP3":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    if cookies_str:
        ydl_opts['cookiefile'] = 'cookies.txt'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if cookies_str:
                with open('cookies.txt', 'w') as f:
                    f.write(cookies_str)
            ydl.download([link])

        # بعد التحميل، إنشاء رابط للتنزيل
        file_name = ydl.prepare_filename({'title': ydl.extract_info(link, download=False)['title'], 'ext': 'mp3' if file_type == 'MP3' else 'mp4'})
        with open(file_name, 'rb') as f:
            file_data = f.read()
        st.download_button(
            label=f"تنزيل {os.path.basename(file_name)}",
            data=file_data,
            file_name=os.path.basename(file_name),
            mime="audio/mpeg" if file_type == "MP3" else "video/mp4",
        )
        return f"تم إنشاء رابط تنزيل لـ: {link}"
    except Exception as e:
        return f"حدث خطأ أثناء التحميل: {str(e)}"

# واجهة المستخدم باستخدام Streamlit
st.title("برنامج تحميل فيديوهات يوتيوب")
st.markdown("""
<span style="color: orange;">**هام:**</span> لتجاوز مشكلة التحقق من أنك لست روبوتًا، يمكنك إدخال ملفات تعريف الارتباط الخاصة بك من يوتيوب أدناه.
""", unsafe_allow_html=True)
st.write("أدخل روابط الفيديوهات أدناه (رابط في كل سطر) واختر الصيغة المطلوبة.")

# إدخال الروابط
links = st.text_area("روابط YouTube", placeholder="أدخل الروابط هنا...")
file_type = st.selectbox("اختر الصيغة", ["MP3", "MP4"])

# إضافة مربع نص لإدخال ملفات تعريف الارتباط
cookies_input = st.text_area("إدخال ملفات تعريف الارتباط (اختياري)", placeholder="الصق محتوى ملف تعريف الارتباط هنا...")

download_button = st.button("تحميل الفيديوهات")

if download_button:
    if links.strip():
        st.write("جارِ تحميل الفيديوهات...")
        links_list = links.strip().split("\n")
        for link in links_list:
            status = download_video(link.strip(), file_type, cookies_input)
            st.write(status)
    else:
        st.warning("يرجى إدخال روابط صحيحة.")
