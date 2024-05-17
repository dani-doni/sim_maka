#-------- IMPORT LYBRARIES ------
import streamlit as st
import pandas as pd
import time
from datetime import datetime
from datetime import date
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
                                                          UpdateError) 

#-------- CONFIGURATION PAGE ------
st.set_page_config ( page_title="maka_simulator", page_icon="🔢", layout="centered")

# Loading config file
with open('./config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.sim = 0

def go_to_first_page():
    st.session_state.step = 1

def go_to_second_page_1():
    st.session_state.step = 2.1
    st.session_state.sim = 1
    st.session_state.start_time = time.time()

def go_to_second_page_2():
    st.session_state.step = 2.2
    st.session_state.sim = 2
    st.session_state.start_time = time.time()
    
def go_to_second_page_3():
    st.session_state.step = 2.3
    st.session_state.sim = 3
    st.session_state.start_time = time.time()

def go_to_third_page():
    st.session_state.step = 3
    st.session_state.finish_time = time.time()
    total_time = st.session_state.finish_time - st.session_state.start_time
    d = datetime.now()
    data = d.strftime('%Y-%m-%d %H:%M:%S')
    db_risultati = './risultati.csv'
    df = pd.read_csv(db_risultati, encoding='latin-1')
    new_row = pd.DataFrame({
        'name': [st.session_state.name],
        'username': [st.session_state.username],
        'performance': [total_time],
        'data': [data],
        'simulation': [st.session_state.sim]
    })
    df = pd.concat([df, new_row], ignore_index=True)

    # Save the updated DataFrame to the CSV file
    df.to_csv(db_risultati, index=False)

def check_results(not_equal_to_1):
    #Check if there some wrong answer
    if not_equal_to_1:    
        st.session_state.warning = 1
    else:
        st.session_state.step = 2.4

def main():

    st.title("Maka Simulator Click DAY 2024")
    # LOGIN: Creating a login widget (show only if it not yet authenticated)
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)

    if st.session_state["authentication_status"] is None:
        st.warning('Inserisci username e password per accedere')
        st.subheader('Non hai ancora un account?')
        with st.expander("Apri e Registrati"):
            st.markdown('NB: in "Name" inserisci nome e cognome completo')
            # # NEW USER REGISTRATION: Creating a new user registration widget
            try:
                (email_of_registered_user,
                    username_of_registered_user,
                    name_of_registered_user) = authenticator.register_user(pre_authorization=False)
                if email_of_registered_user:
                    st.success('Utente registrato con successo, esegui il Login')
            except RegisterError as e:
                st.error(e)

        if st.session_state["authentication_status"] is None:
            st.warning('Se hai problemi contatta: dani.doni74@gmail.com')
        
        # Saving config file
        with open('./config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style=False)

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password non sono corretti')

    if st.session_state["authentication_status"]:
        #APP CONTENT
        if st.session_state.step == 1:
            step1()
        elif st.session_state.step == 2.1:
            step2_1()
        elif st.session_state.step == 2.2:
            step2_2()
        elif st.session_state.step == 2.3:
            step2_3()
        elif st.session_state.step == 2.4:
            step2_4()
        elif st.session_state.step == 3:
            step3()


def step1():
    
    st.subheader('Benvenuto/a nel simulatore di Maka Consulting')
    multi = '''Questa web-app è stata concepita per darvi la possibilità di simulare il Click Day INAIL 2024 e comprenderne al meglio il funzionamento. \n
Sotto avete a disposizione tre diverse simulazioni che si possono provare quante volte si vuole. \n
    '''
    st.markdown(multi)
    col1, col2, col3 = st.columns(3)
    # Add button to proceed to Step 2
    with col1:
        st.button('SIMULAZIONE 1 (simil 2022)', on_click=go_to_second_page_1, type="primary")
    with col2:
        st.button('SIMULAZIONE 2 (simil 2021)', on_click=go_to_second_page_2, type="primary")
    with col3:
        st.button('SIMULAZIONE 3 (simil 2020)', on_click=go_to_second_page_3, type="primary")
    st.markdown(" \n")
    st.divider()
    authenticator.logout()

    with st.expander("Sezione SOLO ADMIN"):
        admins = ['admin', 'manu_angeloni', 'ddoninelli00']
        if st.session_state.username in admins:
            db_risultati = './risultati.csv'
            df = pd.read_csv(db_risultati, encoding='latin-1')
            df_perf = df.groupby('name').agg(
                N_trials=('performance', 'count'),
                P_avg=('performance', 'mean'),
                P_min=('performance', 'min'),
                P_max=('performance', 'max')
            ).reset_index()
            st.write("Tabella di aggregazione dei risultati per ogni utente (visibile solo dagli accounts admin):")
            st.dataframe(df_perf, use_container_width = True, )
            st.write("Tabella degli accessi e dei tentativi di ogni utente (visibile solo dagli accounts admin):")
            st.dataframe(df, use_container_width = True, )
    

def step2_1():
    st.session_state.domanda_1 = 0
    st.session_state.domanda_2 = 0
    st.session_state.domanda_3 = 0
    st.session_state.domanda_4 = 0
    st.session_state.domanda_5 = 0
    st.session_state.domanda_6 = 0
    st.session_state.domanda_7 = 0
    st.session_state.domanda_8 = 0
    st.session_state.domanda_9 = 0
    if 'warning' not in st.session_state:
        st.session_state.warning = 0

    st.subheader('BANDO SIMULATO - Convalida e invio della domanda')
    st.markdown('''i campi contrassegnati dal simbolo * sono obbligatori''')
    with st.container(border=True):
        st.markdown(st.session_state.start_time)
        st.markdown('''INSERIMENTO DATI\n''')
        st.markdown('''Per procedere con l'invio della domanda è necessario completare i seguenti campi.\n''')
    
        # question 1
        question_1 = '''Selezionare 2024, l'anno del Bando al quale si sta partecipando*'''
        options_1 = ["1989", "2042", "2024", "2204"]
        user_answer_1 = st.radio(question_1, options_1, index=None)
        if user_answer_1 is not None:
            if "2024" in user_answer_1:
                st.session_state.domanda_1 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_1} è sbagliata. Seleziona quella corretta per procedere all'invio")
        

        # question 2
        question_2 = '''Selezionare il carattere iniziale del codice identificativo "-" (meno): *'''
        options_2 = ['''€''', '''?''', '''ç''', '''\-''', '''\+''', '''°''', '''£''', '''\*''']
        user_answer_2 = st.radio(question_2, options_2, index=None)
        if user_answer_2 is not None:
            if "-" in user_answer_2:
                st.session_state.domanda_2 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_2} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 3
        question_3 = '''Selezionare -3645asifnuhfnskfarucjnskfriauljnsldkcn/& il codice identificativo senza considerare il "+"(più) o il "-"(meno): *'''
        options_3 = ["asifn4536uhfnskfarucjnskfriauljnsldkcn/&", "b6455u23juhfnskfarucjnskfriauljnsldkcw3534", "3645bgrasfnskfarucjnskfriauljnsldkcn9)0=", "5nj23hj32)=)jnskfriauljnsldkcn/&","3645asifnuhfnskfarucjnskfriauljnsldkcn/&","=?£$Fnuhfnskfarucjnskfriaul44bhjb", "asifn4536uhfnskfarucjnskfriauljnsldkcn/&", "b6455u23juhfnskfarucjnskfriauljnsldkcw3534"]
        user_answer_3 = st.selectbox(question_3, options_3, index=None, placeholder="Seleziona una risposta",)
        if user_answer_3 is not None:
            if "3645asifnuhfnskfarucjnskfriauljnsldkcn/&" in user_answer_3:
                st.session_state.domanda_3 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_3} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 4
        question_4 = '''Selezionare INAIL, l'istituto che eroga il finanziamento:*'''
        options_4 = ["INLAI","IANIL","NIAL","INPS","INAILL","IMAIL","NIAIL","INAIL","AILIN","INPS","IRES"]
        user_answer_4 = st.selectbox (question_4, options_4, index=None, placeholder="Seleziona una risposta",)
        if user_answer_4 is not None:
            if "INAIL" in user_answer_4:
                st.session_state.domanda_4 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_4} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 5
        question_5 = "Selezionare 330, il numero composto della prima, seconda e quarta cifra dello stanziamento del bando: *"
        options_5 = ["303", "333", "330", "33","30","03"]
        user_answer_5 = st.radio(question_5, options_5, index=None)
        if user_answer_5 is not None:
            if "330" in user_answer_5:
                st.session_state.domanda_5 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_5} è sbagliata. Seleziona quella corretta per procedere all'invio")

        # question 6
        question_6 = "Selezionare i 20 minuti del Momento 6:*"
        options_6 = ["20","21","23","24","26","25","27","29","30","22"]
        user_answer_6 = st.selectbox (question_6, options_6, index=None, placeholder="Seleziona una risposta",)
        if user_answer_6 is not None:
            if "20" in user_answer_6:
                st.session_state.domanda_6 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_6} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 7
        question_7 = "Selezionare http://inail.it l'indirizzo del sito INAIL*"
        options_7 = ['''http://inali.it''','''http://inail.ti''','''http://inali.ti''','''http://inala.it''','''http://inail.ti''','''http://inail.it''','''http://inail.com''']
        user_answer_7 = st.selectbox (question_7, options_7, index=None, placeholder="Seleziona una risposta")
        if user_answer_7 is not None:
            if "http://inail.it" in user_answer_7:
                st.session_state.domanda_7 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_7} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 8
        question_8 = "Dichiaro di aver preso visione delle regole tecniche*"
        user_answer_8 = st.checkbox(question_8, value=False)
        if user_answer_8 is True:
            st.session_state.domanda_8 = 1
        else:
            if st.session_state.warning == 1:
                st.error(f"❌ Seleziona questo campo")
        
        # question 9
        question_9 = "Non sono un robot*"
        user_answer_9 = st.checkbox(question_9, value=False)
        if user_answer_9 is True:
            st.session_state.domanda_9 = 1
        else:
            if st.session_state.warning == 1:
                st.error(f"❌ Seleziona questo campo")
     
        # List of user_answer variables
        user_answers = [user_answer_1, user_answer_2, user_answer_3, user_answer_4, user_answer_5, user_answer_6, user_answer_7, user_answer_8, user_answer_9]
        questions = [question_1, question_2, question_3, question_4, question_5, question_6, question_7]
        user_answers_s = [user_answer_1, user_answer_2, user_answer_3, user_answer_4, user_answer_5, user_answer_6, user_answer_7]

        # Create a DataFrame
        data = {'Domande': questions, 'Risposte': user_answers_s}
        st.session_state.recap = pd.DataFrame(data)

        # Check if every questions has been answered
        if all(answer is not None and answer is not False for answer in user_answers):
            not_equal_to_1 = [key for key, value in st.session_state.items() if key.startswith('domanda_') and value != 1]
            if st.session_state.warning == 1:
                st.markdown("Alcune risposte non sono corrette, correggile e premi invio di nuovo")
            st.button('Invia', on_click=check_results(not_equal_to_1), type="primary")
               
def step2_2():
    st.session_state.domanda_1 = 0
    st.session_state.domanda_2 = 0
    st.session_state.domanda_3 = 0
    st.session_state.domanda_4 = 0
    st.session_state.domanda_5 = 0
    st.session_state.domanda_6 = 0
    st.session_state.domanda_7 = 0
    st.session_state.domanda_8 = 0
    st.session_state.domanda_9 = 0
    if 'warning' not in st.session_state:
        st.session_state.warning = 0

    st.subheader('BANDO SIMULATO - Convalida e invio della domanda')
    st.markdown('''i campi contrassegnati dal simbolo * sono obbligatori''')
    with st.container(border=True):
        st.markdown('''INSERIMENTO DATI\n''')
        st.markdown('''Per procedere con l'invio della domanda è necessario completare i seguenti campi.\n''')
    
        # question 1
        username = st.session_state.username
        question_1 = f'''Seleziona il tuo username di accesso ({username})*'''
        options_1 = ["pincopallo", username, "username", "name@gmail.coom"]
        user_answer_1 = st.selectbox(question_1, options_1, index=None, placeholder="Seleziona una risposta",)
        if user_answer_1 is not None:
            if username in user_answer_1:
                st.session_state.domanda_1 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_1} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 7
        question_7 = "Selezionare, a partire dal segno includendo gli estremi, dal quarto (4°) al non (15°) carattere del codice identificativo +2ascjnnrgiusndfknfjiaknroasdm (scjnnrgiusnd)*"
        options_7 = ['''7scjnnrgiusnd''','''scjnnrgiusn90''','''bcjnnrgiusnt''','''scjnnrgiusnd''','''scjnnrgiuuuusnd''','''scnnrgiusnd78''','''srtgjnnrgiusnd''']
        user_answer_7 = st.selectbox (question_7, options_7, index=None, placeholder="Seleziona una risposta")
        if user_answer_7 is not None:
            if "scjnnrgiusnd" in user_answer_7:
                st.session_state.domanda_7 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_7} è sbagliata. Seleziona quella corretta per procedere all'invio")
        

        # question 2
        question_2 = '''Selezionare le vocali del mese di Giugno in cui si terrà il Click Day (iuo): *'''
        options_2 = ['''oiu''', '''ioi''', '''iuo''', '''iao''', '''uio''', '''iou''', '''iio''', '''aio''']
        user_answer_2 = st.selectbox(question_2, options_2, index=None, placeholder="Seleziona una risposta",)
        if user_answer_2 is not None:
            if "iuo" in user_answer_2:
                st.session_state.domanda_2 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_2} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 3
        question_3 = '''Selezionare le ultime due cifre dell'anno del bando (24): *'''
        options_3 = ["23","22","20","21","19","24"]
        user_answer_3 = st.selectbox(question_3, options_3, index=None, placeholder="Seleziona una risposta",)
        if user_answer_3 is not None:
            if "24" in user_answer_3:
                st.session_state.domanda_3 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_3} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 4
        question_4 = '''Selezionare il bando alla quale si sta partecipando (Bando Isi 2023):*'''
        options_4 = ["Blando ISI 2023","Bando ISSI 2023","Bando ISI 202","Bando Isi 2023","Bando Isi 2034","Bando SIS 2024","Blando ISI 2024","Bando ISI 2023","Band ISI 2023","ISI Bando 2024","Bando ISI"]
        user_answer_4 = st.selectbox (question_4, options_4, index=None, placeholder="Seleziona una risposta",)
        if user_answer_4 is not None:
            if "Bando Isi 2023" in user_answer_4:
                st.session_state.domanda_4 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_4} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 5
        question_5 = '''Seleziona l'importo (508.400.000,00) dello stanziamento del bando*'''
        options_5 = ["508.400.000,00", "508.000.000,00", "508.040.000,00", "508.000.004,00","508.400.400,00","500.400.000,00"]
        user_answer_5 = st.selectbox(question_5, options_5, index=None, placeholder="Seleziona una risposta")
        if user_answer_5 is not None:
            if "508.400.000,00" in user_answer_5:
                st.session_state.domanda_5 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_5} è sbagliata. Seleziona quella corretta per procedere all'invio")

        # question 6
        question_6 = "Selezionare il numero di assi di finanziamento (5):*"
        options_6 = ["4","5","6","7","8"]
        user_answer_6 = st.selectbox (question_6, options_6, index=None, placeholder="Seleziona una risposta",)
        if user_answer_6 is not None:
            if "5" in user_answer_6:
                st.session_state.domanda_6 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_6} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 8
        question_8 = "Dichiaro di aver preso visione delle regole tecniche*"
        user_answer_8 = st.checkbox(question_8, value=False)
        if user_answer_8 is True:
            st.session_state.domanda_8 = 1
        else:
            if st.session_state.warning == 1:
                st.error(f"❌ Seleziona questo campo")
        
        # question 9
        question_9 = "Non sono un robot*"
        user_answer_9 = st.checkbox(question_9, value=False)
        if user_answer_9 is True:
            st.session_state.domanda_9 = 1
        else:
            if st.session_state.warning == 1:
                st.error(f"❌ Seleziona questo campo")
     
        # List of user_answer variables
        user_answers = [user_answer_1, user_answer_2, user_answer_3, user_answer_4, user_answer_5, user_answer_6, user_answer_7, user_answer_8, user_answer_9]
        questions = [question_1, question_2, question_3, question_4, question_5, question_6, question_7]
        user_answers_s = [user_answer_1, user_answer_2, user_answer_3, user_answer_4, user_answer_5, user_answer_6, user_answer_7]

        # Create a DataFrame
        data = {'Domande': questions, 'Risposte': user_answers_s}
        st.session_state.recap = pd.DataFrame(data)

        # Check if every questions has been answered
        if all(answer is not None and answer is not False for answer in user_answers):
            not_equal_to_1 = [key for key, value in st.session_state.items() if key.startswith('domanda_') and value != 1]
            if st.session_state.warning == 1:
                st.markdown("Alcune risposte non sono corrette, correggile e premi invio di nuovo")
            st.button('Invia', on_click=check_results(not_equal_to_1), type="primary")

def step2_3():
    st.session_state.domanda_1 = 0
    st.session_state.domanda_2 = 0
    st.session_state.domanda_3 = 0
    st.session_state.domanda_4 = 0
    st.session_state.domanda_5 = 0
    st.session_state.domanda_6 = 0
    st.session_state.domanda_7 = 0
    st.session_state.domanda_8 = 0
    st.session_state.domanda_9 = 0
    if 'warning' not in st.session_state:
        st.session_state.warning = 0

    st.subheader('BANDO SIMULATO - Convalida e invio della domanda')
    st.markdown('''i campi contrassegnati dal simbolo * sono obbligatori''')
    with st.container(border=True):
        st.markdown('''INSERIMENTO DATI\n''')
        st.markdown('''Per procedere con l'invio della domanda è necessario completare i seguenti campi.\n''')
    
        # question 1
        question_1 = '''Selezionare il tipo di bando a cui si desidera partecipare*'''
        options_1 = ["BANDO SIMULATO 2024"]
        user_answer_1 = st.selectbox(question_1, options_1, index=None, placeholder="Seleziona una risposta")
        if user_answer_1 is not None:
            if "BANDO SIMULATO 2024" in user_answer_1:
                st.session_state.domanda_1 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_1} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        st.markdown("Il codice identificativo assegno è: skdnj4ktn4k3wln2jemmeio13kle1n2je12mel3")
        # question 2
        question_2 = '''Scrivi gli ultimi sei caratteri del codice identificativo assegno*'''
        user_answer_2 = st.text_input(question_2)
        if user_answer_2 is not None:
            if user_answer_2 == "12mel3" :
                st.session_state.domanda_2 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_2} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 3
        question_3 = '''Scrivi i primi otto caratteri del codice identificativo assegno*'''
        user_answer_3 = st.text_input(question_3)
        if user_answer_3 is not None:
            if user_answer_3 == "skdnj4kt" :
                st.session_state.domanda_3 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_3} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 4
        today = datetime.now()
        today = today.date()
        today
        question_4 = '''Selezionare la data di oggi:*'''
        fake_date =  date(2019, 7, 6)
        user_answer_4 = st.date_input (question_4, fake_date)
        if user_answer_4 is not None:
            if user_answer_4 == today:
                st.session_state.domanda_4 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_4} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        st.markdown("Le iscrizioni al bando terminano Sabato 01 Giugno 2024")
        # question 5
        question_5 = "Selezionare il mese in cui terminano le iscrizioni al bando *"
        options_5 = ["Aprile", "Maggio", "Giungo", "Luglio","Agosto","Giugno"]
        user_answer_5 = st.radio(question_5, options_5, index=None)
        if user_answer_5 is not None:
            if "Giugno" in user_answer_5:
                st.session_state.domanda_5 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_5} è sbagliata. Seleziona quella corretta per procedere all'invio")

        # question 6
        question_6 = "Selezionare il giorno della settimana in cui terminano le iscrizioni al bando*"
        options_6 = ["Sabato","Domenica","Sabatu","Lunedì","Martedì"]
        user_answer_6 = st.selectbox (question_6, options_6, index=None, placeholder="Seleziona una risposta",)
        if user_answer_6 is not None:
            if "Sabato" in user_answer_6:
                st.session_state.domanda_6 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_6} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 7
        question_7 = "Selezionare http://inail.it l'indirizzo del sito INAIL*"
        options_7 = ['''http://inali.it''','''http://inail.ti''','''http://inali.ti''','''http://inala.it''','''http://inail.ti''','''http://inail.it''','''http://inail.com''']
        user_answer_7 = st.selectbox (question_7, options_7, index=None, placeholder="Seleziona una risposta")
        if user_answer_7 is not None:
            if "http://inail.it" in user_answer_7:
                st.session_state.domanda_7 = 1
            else:
                if st.session_state.warning == 1:
                    st.error(f"❌ L'opzione' {user_answer_7} è sbagliata. Seleziona quella corretta per procedere all'invio")
        
        # question 8
        question_8 = "Dichiaro di aver preso visione delle regole tecniche*"
        user_answer_8 = st.checkbox(question_8, value=False)
        if user_answer_8 is True:
            st.session_state.domanda_8 = 1
        else:
            if st.session_state.warning == 1:
                st.error(f"❌ Seleziona questo campo")
        
        # question 9
        question_9 = "Non sono un robot*"
        user_answer_9 = st.checkbox(question_9, value=False)
        if user_answer_9 is True:
            st.session_state.domanda_9 = 1
        else:
            if st.session_state.warning == 1:
                st.error(f"❌ Seleziona questo campo")
     
        # List of user_answer variables
        user_answers = [user_answer_1, user_answer_2, user_answer_3, user_answer_4, user_answer_5, user_answer_6, user_answer_7, user_answer_8, user_answer_9]
        questions = [question_1, question_2, question_3, question_4, question_5, question_6, question_7]
        user_answers_s = [user_answer_1, user_answer_2, user_answer_3, user_answer_4, user_answer_5, user_answer_6, user_answer_7]

        # Create a DataFrame
        data = {'Domande': questions, 'Risposte': user_answers_s}
        st.session_state.recap = pd.DataFrame(data)

        # Check if every questions has been answered
        if all(answer is not None and answer is not False for answer in user_answers):
            not_equal_to_1 = [key for key, value in st.session_state.items() if key.startswith('domanda_') and value != 1]
            if st.session_state.warning == 1:
                st.markdown("Alcune risposte non sono corrette, correggile e premi invio di nuovo")
            st.button('Invia', on_click=check_results(not_equal_to_1), type="primary")

def step2_4():
    
    st.subheader('BANDO SIMULATO - Convalida e invio della domanda')
    st.markdown('''i campi contrassegnati dal simbolo * sono obbligatori''')
    with st.container(border=True):
        st.markdown(st.session_state.start_time)  
        st.markdown('''INSERIMENTO DATI\n''')
        st.markdown('''Riepilogo dati inseriti.\n''')

        df = st.session_state.recap
        st.table(df.style.set_table_styles([dict(selector="th",props=[("border", "0")]),
                                        dict(selector="td",props=[("border", "0")])]))
    
    # question 10
    question_10 = "Informativa: i dati inseriti potrebbero essere oggetti a verifica durante la lavorazione della domanda*"
    user_answer_10 = st.checkbox(question_10, value=False)
    if user_answer_10 is True:
        st.button('Invia', on_click=go_to_third_page(), type="primary")

def step3():
    st.session_state.start_time 
    total_time = st.session_state.finish_time - st.session_state.start_time
    st.subheader('Hai terminato la simulazione!')
    st.subheader(f"Hai impiegato: {total_time} secondi")
    if total_time <= 60:
        st.success("Complimenti! Hai impiegato meno di 60 secondi. Con questo tempo la probabilità di vincere il Click Day è molto alta!")
    else:
        st.info("Hai impiegato più di 60 secondi. Fai attenzione, con questo tempo la probabilità di vincere il Click Day è molto bassa. Allenati ancora per migliorare il tuo tempo e avere più possibilità di vincere!")
    
    # Add button to come back to step 1
    st.button('Torna alla Home e ripeti simulazione', on_click=go_to_first_page)


if __name__ == "__main__":
    main()
