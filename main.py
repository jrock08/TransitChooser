import streamlit as st
import numpy as np
import car_model
from PIL import Image

people_per_hour = st.slider('people per hour', min_value=100, max_value=60000, value=5000)

c1,c2 = st.beta_columns(2)

with c1:
    img_gondola = Image.open('gondola.jpeg')
    st.image(img_gondola)
    car_cap = st.slider('car capacity', min_value=1, max_value=50, value=30)
    car_headway = st.slider('time between cars (seconds)', min_value=1, max_value=60, value=30)

    per_person_dat, per_car_dat = car_model.car_model(car_cap, car_headway/60.0, people_per_hour)

    st.write('Per person median wait is: {:.0f} minutes'.format(np.median(per_person_dat['departure']-per_person_dat['arrival'])))
    st.write('Max wait was: {:.0f} minutes'.format(np.max(per_person_dat['departure']-per_person_dat['arrival'])))

    st.pyplot(car_model.plot_wait_hist(per_person_dat))
    st.pyplot(car_model.plot_wait_line_by_car(per_car_dat, people_per_hour))


with c2:
    img_link = Image.open('link.jpeg')
    st.image(img_link)
    car_cap = st.slider('car capacity', min_value=100, max_value=1000, value=800)
    car_headway = st.slider('time between cars (minutes)', min_value=4, max_value=25, value=6)

    per_person_dat, per_car_dat = car_model.car_model(car_cap, car_headway, people_per_hour)

    st.write('Per person median wait is: {:.0f} minutes'.format(np.median(per_person_dat['departure']-per_person_dat['arrival'])))
    st.write('Max wait was: {:.0f} minutes'.format(np.max(per_person_dat['departure']-per_person_dat['arrival'])))

    st.pyplot(car_model.plot_wait_hist(per_person_dat))
    st.pyplot(car_model.plot_wait_line_by_car(per_car_dat, people_per_hour))
