import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title(':red[Fuel Economy]')

image = Image.open('fuel-economy.jpg')

df = pd.read_csv('data/VehicleMPG-1984to2023.csv')

YearRnge = sorted(df['ModelYear'].unique())
MinYear = df['ModelYear'].min()
MaxYear = df['ModelYear'].max()

#Sidebar - Year selector
YearSlider = st.sidebar.select_slider("Model Year:", options=YearRnge, value=(MinYear, MaxYear))
LwrRnge, UpprRnge = list(YearSlider)[0], list(YearSlider)[1]

#Multiselect - Make selector
df_make = df[(df['ModelYear']>=LwrRnge) & (df['ModelYear']<=UpprRnge)].sort_values('Make')
sb_make = st.sidebar.multiselect("Make:", options=df_make['Make'].unique(), max_selections=3)

#Multiselect - Model selector
df_model = df_make[df_make['Make'].isin(sb_make) ].sort_values('Model') 
# & (df_make['Fuel Type 1'].str.contains("Electricity") == False & df_make['Fuel Type 1'].str.contains("Natural Gas")) == False 
sb_model = st.sidebar.multiselect("Model:", options=df_model['Model'].unique(), max_selections=3)

#Dataframe - Final selection
df_final = df_model[df_model['Model'].isin(sb_model) ].sort_values('Model') 


tab1,tab2,tab3,tab4 = st.tabs(['What is Fuel Economy?', 'Fuel Economy MPG by Model', 'Fuel Economy MPG by Vehicle Class', 'Electric Vehicle'])

with tab1:
    st.markdown(""" <style> .font {font-size:18px ; font-family: 'Arial'; color: red;} </style> """, unsafe_allow_html=True)
    st.markdown(""" <p class="font">Car fuel economy is directly related to miles per gallon, or MPG or miles per gallon electric (MPGe). The higher its mpg, the better your car's fuel economy.</p>""", unsafe_allow_html=True)

    st.markdown(""" <style> .font {font-size:14px ; font-family: 'Arial'; color: red;} </style> """, unsafe_allow_html=True)
    st.markdown(""" <p class="font">Your car's fuel economy - how far your vehicle can go using a specific amount of fuel - can have a real impact on your expenses. Choosing a vehicle with good fuel economy or taking steps to boost the fuel economy of your current vehicle, just might save you money at the gas pump.</p>""", unsafe_allow_html=True)

    st.image(image, width=900)

with tab2:
    df_final

    CityMPG=alt.Chart(df_final).mark_bar().encode(
        x='Model',
        y='mean(CityMPG)'
    ).properties(height=500,width=200)

    HighwayMPG=alt.Chart(df_final).mark_bar().encode(
        x='Model',
        y='mean(HighwayMPG)'
    ).properties(height=500,width=200)

    CombinedMPG=alt.Chart(df_final).mark_bar().encode(
        x='Model',
        y='mean(CombinedMPG)'
    ).properties(height=500,width=200)
    # .transform_fold(
    # as_=['type', 'Model'],
    # fold=['mean(CityMPG)','mean(HighwayMPG)', 'mean(CombinedMPG)'])

    CityMPG | HighwayMPG | CombinedMPG
    # base = alt.Chart(df).properties(height=500)
    # CityMPG = alt.Chart(df_final).mark_bar().encode(
    #         x=alt.X('Model:N'),
    #         y=alt.Y('MPG:Q'),
    #         color=alt.Color('MPG:Q')
    #         ).transform_fold(
    #         ['CityMPG:Q', 'HighwayMPG:Q', 'CombinedMPG:Q'],
    #         as_=['MPG:Q', 'MPG:Q']
    #         )
    
    # .transform_fold(
    #         ['CityMPG:Q', 'HighwayMPG:Q', 'CombinedMPG:Q'],
    #         as_=['MPG:Q', 'Model:N']
    #         )
    # CityMPG
    # st.altair_chart(CityMPG, theme="streamlit", use_container_width=True)
        # transform_fold(
        #     ['CityMPG', 'HighwayMPG', 'CombinedMPG'],
        #     as_=['MPG', 'price']
        # )
    # alt.Chart(source).mark_bar().encode(
    # x='year:O',
    # y='sum(yield):Q',
    # color='year:N',
    # column='site:N'
    # )
# #sb_make_1 = alt.selection(type="multi")
# base = alt.Chart(Model)
# MPG = base.mark_bar().encode(
#     x=alt.X('Model:Q'),
#     y=alt.Y('average(CombinedMPG):N')
#     ).properties(
#         width=20
#     # ).add_selection(
#     #     sb_make_1
#     # ).add_selection(
#     #     sb_year_1
#     # ).add_selection(
#     #     sb_model_1
#     # ).transform_filter(
#     #     sb_make_1)
#     # ).transform_filter(
#     #     sb_year_1
#     # ).transform_filter(
#     #     sb_model_1
#      )


# MPG
