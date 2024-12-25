import streamlit as st
import yt_dlp

def download_video(link, file_type):
    try:
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
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return f"تم تنزيل الملف بنجاح: {link}"
    except Exception as e:
        return f"حدث خطأ أثناء التحميل: {str(e)}"

# واجهة المستخدم باستخدام Streamlit
st.title("برنامج تحميل فيديوهات يوتيوب")
st.write("أدخل روابط الفيديوهات أدناه (رابط في كل سطر) واختر الصيغة المطلوبة.")

# إدخال الروابط
links = st.text_area("روابط YouTube", placeholder="أدخل الروابط هنا...")
file_type = st.selectbox("اختر الصيغة", ["MP3", "MP4"])
download_button = st.button("تحميل الفيديوهات")

if download_button:
    if links.strip():
        st.write("جارِ تحميل الفيديوهات...")
        links_list = links.strip().split("\n")
        for link in links_list:
            status = download_video(link.strip(), file_type)
            st.write(status)
    else:
        st.warning("يرجى إدخال روابط صحيحة.")
