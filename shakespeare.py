import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import nltk
nltk.download('punkt')
import glob, nltk, os, re
from nltk.corpus import stopwords 
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
# import string
st.set_option('deprecation.showPyplotGlobalUse', False)


st.markdown('''
# Analyzing Shakespeare Texts
''')

# Create a dictionary (not a list)
books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}

# Sidebar
st.sidebar.header('Word Cloud Settings')
max_word = st.sidebar.slider("Max Words",min_value=10, max_value=200, value=100, step=10)
size_of_largest_word = st.sidebar.slider("Size of largest Word",min_value=50, max_value=350, value=60, step=10)
image_width = st.sidebar.slider("Image Width",min_value=100, max_value=800, value=400, step=10)
random_state = st.sidebar.slider("Random State",min_value=20, max_value=100, value=20, step=10)
remove_stop_words = st.sidebar.checkbox("Remove Stop Words?",value=True)
st.sidebar.header('Word Count Settings')
min_cnt_of_words = st.sidebar.slider("Minimum count of words",min_value=5, max_value=100, value=40, step=5)

## Select text files
image = st.selectbox("Choose a text file", books.keys())

## Get the value
image = books.get(image)

tab1,tab2,tab3 = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

with tab1:

    if image != " ":
        stop_words = []
        #stop_words_list = []
        raw_text = open(image,"r").read().lower()
        nltk_stop_words = stopwords.words('english')

        if remove_stop_words:
            stop_words = set(nltk_stop_words)
            stop_words.update(['and', 'us', 'one', 'though','will', 'said', 'now', 'well', 'man', 'may',
            'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
            'put', 'seem', 'asked', 'made', 'half', 'much', 
            'certainly', 'might', 'came','thou','thy'])
            #stop_words_list = [i for i in stop_words if i.lower() not in nltk_stop_words]
            # These are all lowercase
        tokens = nltk.word_tokenize(raw_text)

        #wordcloud = WordCloud(stopwords=stop_words, background_color="white").generate(raw_text)
        wordcloud = WordCloud(stopwords=stop_words, max_words=max_word,width=image_width,random_state=random_state, max_font_size=size_of_largest_word, background_color="white").generate(raw_text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()


with tab2:
    if image != " ":
        st.write('Bar Chart')

        raw_text = open(image,"r").read().lower()

        def word_frequency(sentence):
            sentence = "".join(sentence)
            new_tokens = nltk.word_tokenize(sentence)
            new_tokens = [t.lower() for t in new_tokens]
            new_tokens =[t for t in new_tokens if t not in stop_words]
            new_tokens = [t for t in new_tokens if t.isalpha()]
            counted = Counter(new_tokens)
            # counted
            word_freq = pd.DataFrame(counted.items(),columns=["word","frequency"]).sort_values(by="frequency",ascending=False)
            return word_freq
        
        tab2_word_freq = word_frequency(raw_text)

        df_1 = tab2_word_freq[tab2_word_freq["frequency"]>=min_cnt_of_words]

        bars = alt.Chart(df_1).mark_bar().encode(
            alt.X('frequency'),
            alt.Y('word', sort='-x')
            # tooltip=['frequency:Q', 'word:Q']
        ).properties(height=600, width=600).interactive()
        
        bars

with tab3:
    if image != " ":
        raw_text = open(image,"r").read().lower()
        st.write(raw_text)