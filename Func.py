import time
from Main import query_deepseek
import streamlit as st

api_key = "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"

option = st.sidebar.radio(
    "Choose an option:",
    ("AdamGPT", "BigPekker", "MiniPekker")
)

if option == "AdamGPT":
    st.title("AdamGPT")
    st.write("Welcome to AdamGPT! It's literally ChatGPT but Adam")

    user_inp = st.text_input("What would you like to ask AdamGPT?")

    if len(user_inp) > 0:
        placeholder = st.empty()

        # animate ". .. ..." cycle
        for i in range(6):
            dots = "." * ((i % 3) + 1)
            placeholder.markdown(f"AdamGPT is thinking{dots}")
            time.sleep(0.5)

        # get response
        response = query_deepseek(f"{user_inp}", api_key)
        placeholder.empty()  # clear animation
        st.write(response)

elif option == "BigPekker":
    st.title("Big Pekker!")
    st.write("Welcome to the Big Pekker")

    st.image(
        "https://static.wikia.nocookie.net/clashroyale/images/d/d3/P.E.K.K.A_card.png",
        caption="Big Pekker in the flesh 💀"
    )

elif option == "MiniPekker":
    st.title("Mini Pekker!")
    st.write("Mini but mighty ⚔️🥶")
    st.image(
        "https://static.wikia.nocookie.net/clashroyale/images/5/5c/Mini_P.E.K.K.A_card.png",
        caption="Mini Pekker is here 🤖"
    )
