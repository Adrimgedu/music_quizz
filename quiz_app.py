import streamlit as st
import json

st.set_page_config(page_title="Quizz IA Music", page_icon="🎤")

with open('quiz.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)
num_questions = len(quiz_data)

# Inicializar variables de sesión
if 'answers' not in st.session_state:
    st.session_state.answers = [None] * num_questions
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'review_mode' not in st.session_state:
    st.session_state.review_mode = False
if 'score' not in st.session_state:
    st.session_state.score = 0

# Función para pasar a la siguiente pregunta
def next_question():
    if st.session_state.current_index < num_questions - 1:
        st.session_state.current_index += 1
    else:
        st.session_state.review_mode = True

# Función para reiniciar el quiz
def restart_quiz():
    st.session_state.answers = [None] * num_questions
    st.session_state.current_index = 0
    st.session_state.review_mode = False
    st.session_state.score = 0

# Función para corregir respuestas
def submit_review():
    score = 0
    for i, q in enumerate(quiz_data):
        if st.session_state.answers[i] == q['answer']:
            score += 10
    st.session_state.score = score

st.title("Quizz IA Music - Revisión 🎤")
progress_bar_value = (st.session_state.current_index + 1) / num_questions
st.progress(progress_bar_value)

if not st.session_state.review_mode:
    # Pregunta actual
    q_idx = st.session_state.current_index
    question_item = quiz_data[q_idx]
    st.subheader(f"Pregunta {q_idx+1} de {num_questions}")
    st.write(question_item['question'])
    st.write("Selecciona tu respuesta:")
    selected = st.session_state.answers[q_idx]
    for opt in question_item['options']:
        btn_style = "background:#2563eb;color:#fff;" if selected == opt else "background:#fff;color:#222;"
        if st.button(opt, key=f"ans_{q_idx}_{opt}", use_container_width=True):
            st.session_state.answers[q_idx] = opt
            selected = opt

   # Centrar el botón siguiente
    col_next = st.columns([1,2,1])[1]
    with col_next:
        avanzar = st.button("Siguiente", key=f"next_{q_idx}")

    if avanzar:
        if not st.session_state.answers[q_idx]:
            st.warning("Selecciona una opción antes de continuar.")
        else:
            if q_idx < num_questions - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.review_mode = True
            st.rerun()  # <- fuerza el rerun inmediato
else:
    st.header("Revisión de respuestas")
    for i, question_item in enumerate(quiz_data):
        st.write(f"**{question_item['question']}**")
        st.session_state.answers[i] = st.selectbox(
            "Selecciona tu respuesta:",
            question_item['options'],
            index=question_item['options'].index(st.session_state.answers[i]) if st.session_state.answers[i] else 0,
            key=f"review_{i}"
        )
        st.markdown("---")
    if st.button("Enviar respuestas y corregir", key="submit_review"):
        submit_review()
    if st.session_state.score > 0:
        st.success(f"Puntuación final: {st.session_state.score} / {num_questions * 10}")
    if st.button("Reiniciar", key="restart_quiz"):
        restart_quiz()
