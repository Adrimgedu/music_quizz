import streamlit as st
import pandas as pd


# Estilos personalizados
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    .main {
        background-color: rgba(255,255,255,0.8);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    }
    .stButton > button {
        background: #6366f1;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 8px 24px;
        border: none;
        margin-top: 12px;
    }
    .stRadio label {
        font-size: 1.1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

quiz_df = pd.read_csv('quiz.csv')

st.set_page_config(page_title="ANALYTICS & IA MUSIC", page_icon="🎤")


# Inicializar el estado de la sesión
if 'current_question' not in st.session_state:

    import streamlit as st
    import pandas as pd

    st.set_page_config(page_title="Streamlit Quiz App", page_icon="❓")

    # Custom CSS for the buttons and card
    st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f43f5e 0%, #6366f1 100%);
    }
    .quiz-card {
        background: rgba(255,255,255,0.95);
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(99,102,241,0.18), 0 1.5px 8px rgba(244,63,94,0.10);
        padding: 40px 32px;
        margin: 32px auto;
        max-width: 540px;
        border: 2px solid #6366f1;
    }
    div.stButton > button {
        display: block;
        margin: 16px auto;
        background: linear-gradient(90deg, #6366f1 0%, #f43f5e 100%);
        color: #fff;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.15em;
        padding: 16px 36px;
        border: none;
        box-shadow: 0 2px 8px rgba(99,102,241,0.10);
        transition: background 0.2s, transform 0.2s;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #f43f5e 0%, #6366f1 100%);
        transform: scale(1.04);
    }
    </style>
    """, unsafe_allow_html=True)

    # Cargar el CSV
    quiz_df = pd.read_csv('quiz.csv')
    num_questions = len(quiz_df)

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
            correct = quiz_df.iloc[st.session_state.current_index]['Correct Option']
            if st.session_state.selected_option == correct:
                st.session_state.score += 10
        else:
            st.warning("Por favor selecciona una opción antes de enviar.")

    def next_question():
        st.session_state.current_index += 1
        st.session_state.selected_option = None
        st.session_state.answer_submitted = False

    # Título y barra de progreso
    st.title("❓ Streamlit Quiz App")
    progress_bar_value = (st.session_state.current_index + 1) / num_questions
    st.metric(label="Puntuación", value=f"{st.session_state.score} / {num_questions * 10}")
    st.progress(progress_bar_value)

    # Mostrar pregunta y opciones
    row = quiz_df.iloc[st.session_state.current_index]
    question = row['Question']
    options = [row[f'Option {i}'] for i in range(1, 14) if pd.notna(row.get(f'Option {i}'))]
    correct_answer = row['Correct Option']

    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
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
        cols = st.columns(1)
        for i, option in enumerate(options):
            btn_style = ""
            # Si la opción está seleccionada, destacar el botón
            if st.session_state.selected_option == option:
                btn_style = "background: linear-gradient(90deg, #f43f5e 0%, #6366f1 100%); color: #fff; border: 2px solid #6366f1; box-shadow: 0 2px 8px rgba(99,102,241,0.18);"
            else:
                btn_style = "background: #fff; color: #6366f1; border: 2px solid #f43f5e;"
            st.markdown(f"""
            <div style='margin-bottom:12px;'>
                <button style='width:100%;font-size:1.1em;padding:16px 0;border-radius:12px;{btn_style}' onclick="window.location.href='#{i}'">{option}</button>
            </div>
            """, unsafe_allow_html=True)
            # El botón real para la lógica
            if st.button(f"Seleccionar: {option}", key=f"select_{i}", use_container_width=True):
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
