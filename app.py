import streamlit as st
import pandas as pd
import time
#from utils.utils import *

# Set page configuration
st.set_page_config(
    page_title="Simulatore_Maka",
    page_icon=":deciduous_tree:",
    layout="wide",  # Set layout to wide
)

if 'step' not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def main():
    if st.session_state.step == 1:
        step1()
    elif st.session_state.step == 2:
        step2()
    elif st.session_state.step == 3:
        step3()

def step1():
    st.subheader('Benvenuti nel simulatore di Maka Consulting')
    st.write('Questo simulatore è stato concepito per...bla...bla. Nota bene che è solo un esempio bla bla bla') 
          
    # Add button to proceed to Step 2
    st.button('Inizia la simulazione del CLICK DAY', on_click=next_step)
            

def step2():
    st.session_state.start_time = time.time()
    st.session_state.q1 = 0
    st.session_state.q2 = 0

    st.write('Per procedere ad inviare la domanda è necessario compilare i seguenti campi:') 
    
    # question 1
    question_1 = "Seleziona l'anno della data odierna (2024)"
    options_1 = ["1989", "2042", "2024", "2204"]

    # Display the multiselect question
    user_answer_1 = st.selectbox(question_1, options_1, index=None, placeholder="Seleziona una risposta",)

    # Check if the correct answer is selected
    if user_answer_1 is not None:
        if "2024" in user_answer_1:
            st.success("✅ Risposta corretta")
            st.session_state.q1 = 1
        else:
            st.error("❌ Risposta sbagliata")

    # question 2
    question_2 = "Seleziona, nell'ordine corretto, le vocali contenute nelle parole 'Bando ISI' (aoii)"
    options_2 = ["aioi", "aoii", "aooi", "aoio"]

    # Display the multiselect question
    user_answer_2 = st.selectbox(question_2, options_2, index=None, placeholder="Seleziona una risposta")

    # Check if the correct answer is selected
    if user_answer_2 is not None:
        if "aoii" in user_answer_2:
            st.success("✅ Risposta corretta")
            st.session_state.q2 = 1
        else:
            st.error("❌ Risposta sbagliata")

    if st.session_state.q1 == 1 and st.session_state.q2 == 1:
        st.success('Tutte le risposte sono corrette, poi procedere ad inviare al domanda', icon="✅")
        # Add button to proceed to Step 2
        st.button('Invia', on_click=next_step)


def step3():
    finish_time = time.time()
    total_time = finish_time - st.session_state.start_time
    st.subheader('Hai terminato la simulazione!')
    st.write(f"Hai impiegato: {total_time} secondi")


if __name__ == '__main__':
    main()