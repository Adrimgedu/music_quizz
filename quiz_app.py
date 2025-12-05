

import streamlit as st
import json
st.set_page_config(page_title="ANALYTICS & IA MUSIC", page_icon="🎤")

# Custom CSS for the buttons and card
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #f43f5e 0%, #6366f1 100%);
}
.quiz-card {
    background: rgba(255,255,255,0.97);
    border-radius: 18px;
    box-shadow: 0 4px 16px rgba(99,102,241,0.12), 0 1.5px 8px rgba(244,63,94,0.10);
    padding: 6vw 4vw;
    margin: 6vw auto;
    max-width: 98vw;
    width: 100%;
    border: 2px solid #6366f1;
}
div.stButton > button {
    display: block;
    margin: 3vw auto;
    background: linear-gradient(90deg, #6366f1 0%, #f43f5e 100%);
    color: #fff;
    border-radius: 12px;
    font-weight: bold;
    font-size: 1.1em;
    padding: 4vw 0;
    border: none;
    box-shadow: 0 2px 8px rgba(99,102,241,0.10);
    transition: background 0.2s, transform 0.2s;
    width: 100%;
    max-width: 500px;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #f43f5e 0%, #6366f1 100%);
    transform: scale(1.04);
}
@media (max-width: 600px) {
    .quiz-card {
        padding: 7vw 2vw;
        margin: 4vw auto;
        border-radius: 12px;
        max-width: 100vw;
    }
    div.stButton > button {
        font-size: 1em;
        padding: 5vw 0;
        border-radius: 10px;
        max-width: 98vw;
    }
}
</style>
""", unsafe_allow_html=True)

with open('quiz.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)
num_questions = len(quiz_data)

# Inicializar variables de sesión
default_values = {
    'current_index': 0,
    'score': 0,
    'selected_option': None,
    'answer_submitted': False
}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

def submit_answer():
    if st.session_state.selected_option is not None:
        st.session_state.answer_submitted = True
        correct = quiz_data[st.session_state.current_index]['answer']
        if st.session_state.selected_option == correct:
            st.session_state.score += 10
    else:
        st.warning("Por favor selecciona una opción antes de enviar.")

def next_question():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

# Título y barra de progreso
st.title("El quizz de IA Music 🎤")
progress_bar_value = (st.session_state.current_index + 1) / num_questions
st.metric(label="Puntuación", value=f"{st.session_state.score} / {num_questions * 10}")
st.progress(progress_bar_value)

# Mostrar pregunta y opciones
question_item = quiz_data[st.session_state.current_index]
question = question_item['question']
options = question_item['options']
correct_answer = question_item['answer']

#st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
st.subheader(f"Pregunta {st.session_state.current_index + 1}")
st.title(f"{question}")
st.markdown(""" ___""")

if st.session_state.answer_submitted:
    for i, option in enumerate(options):
        label = option
        if option == correct_answer:
            st.success(f"{label} (Respuesta correcta)")
        elif option == st.session_state.selected_option:
            st.error(f"{label} (Respuesta incorrecta)")
        else:
            st.write(label)
else:
    for i, option in enumerate(options):
        if st.button(option, key=f"select_{i}", use_container_width=True):
            st.session_state.selected_option = option

st.markdown(""" ___""")

# Botón de envío y navegación
if st.session_state.answer_submitted:
    if st.session_state.current_index < num_questions - 1:
        st.button('Siguiente', on_click=next_question)
    else:
        st.write(f"<span style='font-size:1.3em;font-weight:bold;color:#f43f5e'>🎉 ¡Quiz terminado!</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size:1.2em;color:#6366f1'>Tu puntuación es: <b>{st.session_state.score} / {num_questions * 10}</b></span>", unsafe_allow_html=True)
        st.balloons()
        if st.button('🔄 Reiniciar', on_click=restart_quiz):
            pass
else:
    if st.session_state.current_index < num_questions:
        st.button('Enviar', on_click=submit_answer)

st.markdown('</div>', unsafe_allow_html=True)
