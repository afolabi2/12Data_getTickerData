import streamlit as st

# to run streamlit app
# streamlit run ./files.py/app.py

#Text Title
author = 'akt'
version = '0.001'
title_01 = f'Pull Stock Data App(Streamlit)'
st.title(title_01)

#Text Header/SubHeader
header_01    = f'by {author}'
subheader_01 = f'@version{version}'
st.header(header_01)
st.subheader(subheader_01)

#Text
text_01 = f'This app is designed to pull data from online data api sources to populate sql3lite db(s) to be used for analysis and recommendations'
text_02 = f'This app was designed by Adegbayo Akintunde with input and guidance from Adegbayo Afolabi'
st.text(text_01)
st.text(text_02)

#styling data
#st.write('Text with write')
#st.write('range(10))

#markdown
#markdown_01 = f'### header'
#st.markdown()

#Error/Colourful Text
#st.success()
#st.info()
#st.warning()
#st.error()
#st.exception()

#get help info about python
#st.help(range)


# Images
#from PIL import Image
#img = Image.open("example.jpeg")
#st.image(img, width=300, caption="Simple Image")

#Videos
#vidfile = open("example.mp4","rb").read()

