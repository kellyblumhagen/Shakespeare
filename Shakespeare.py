import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import glob, nltk, os, re
from nltk.corpus import stopwords 

st.markdown("""
# Analyzing Shakespeare Texts
""")

# Create a dictionary (not a list)
books = {" ": " ", "A Mid Summer Night's Dream":"Data/summer.txt", "The Merchant of Venice":"Data/merchant.txt", "Romeo and Juliet":"Data/romeo.txt"}

# Sidebar
st.sidebar.header("Word Cloud Settings")
max_word = st.sidebar.slider(
    "Max Words", min_value = 10, max_value = 200, value = 100, step = 10)
max_font = st.sidebar.slider(
    "Size of Largest Word", min_value = 50, max_value = 350, value = 60, step = 10)
img_width = st.sidebar.slider(
    "Image Width", min_value = 100, max_value = 800, value = 400, step = 10)
random = st.sidebar.slider(
    "Random State", min_value = 30, max_value = 100, value = 20)
remove_stop_words = st.sidebar.checkbox("Remove Stop Words", value = True)
st.sidebar.header("Word Count Settings")
n_words = st.sidebar.slider(
    "Minimum Count of Words", min_value = 5, max_value = 100, value = 40, step = 1)

## Select text files
image = st.selectbox("Choose a Text File", books.keys())

# Get the value
image = books.get(image)

if image != " ":
    stop_words = []
    raw_text = open(image, "r").read().lower()
    nltk_stop_words = stopwords.words("english")
    set = re.sub(r"[^\w\s]", "", raw_text)


    if remove_stop_words:
        stop_words = set(nltk_stop_words)
        stop_words.update(["us", "one", "though", "will", "said", "now", "well", "man", "may",
                           "little", "say", "must", "way", "long", "yet", "mean",
                           "put", "seem", "asked", "made", "half", "much",
                           "certainly", "might", "came", "thou"])
        # These are all lowercase

tokens = nltk.word_tokenize(raw_text)
tokens = [x for x in tokens if not x.lower() in stop_words]


tab1, tab2, tab3 = st.tabs(["Word Cloud", "Bar Chart", "View Text"])

# TAB 1 (WORD CLOUD)
with tab1:
    if image != " ":
        cloud = WordCloud(background_color="white", max_words = max_word, max_font_size = max_font, stopwords = stop_words, random_state = random)
        wc = cloud.generate(set)
        word_cloud = wc.to_file("wordcloud.png")
        st.image(wc.to_array(), width = img_width)

# TAB 2 (BAR CHART)
with tab2:
    if image != " ":
        st.markdown("""#### Bar Chart""")
frequency = nltk.FreqDist(tokens)
freq_df = pd.DataFrame(frequency.items(), columns = ["Word", "Count"])
freq_chart = alt.Chart(freq_df).transform_filter(
    alt.FieldGTEPredicate(field="Count", gte = n_words)
).mark_bar().encode(
    y = alt.Y("Word", sort = alt.EncodingSortField(
    "Count", op = "Min", order = "Descending")),
    x = "Count").properties(width = 800)
freq_text = freq_chart.mark_text(align = "Left", baselin = "Middle", dx = 3).encode(text = "Count")
chart = freq_chart + freq_text
st.altair_chart(chart)

# TAB 3 (VIEW TEXT)
with tab3:
    if image != " ":
        raw_text = open(image, "r").read().lower()
        st.write(raw_text)
