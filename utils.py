import streamlit as st

def _get_user_string(message):
    user_string = f"""<div style='display:flex;align-items:center;justify-content:flex-end;margin-bottom:10px;'>
                     <div style='background-color:#DCF8C6;border-radius:10px;padding:10px;'>
                     <p style='margin:0;font-weight:bold;'>You</p>
                     <p style='margin:0;'>{message}</p>
                     </div>
                     <img src='https://i.imgur.com/kT9OOOh.jpeg' style='width:50px;height:50px;border-radius:50%;margin-left:10px;'>
                     </div>"""

    return user_string


def _get_bot_string(message, bot_name):
    bot_string = f"""<div style='display:flex;align-items:center;margin-bottom:10px;'>
                    <img src='https://i.imgur.com/rKTnxVN.png' style='width:50px;height:50px;border-radius:50%;margin-right:10px;'>
                    <div style='background-color:#F0F0F0;border-radius:10px;padding:10px;'>
                    <p style='margin:0;font-weight:bold;'>{bot_name}</p>
                    <p style='margin:0;'>{message}</p>
                    </div>
                    </div>"""

    return bot_string

class message:
    def __init__(self, text, actor="user"):
        self.container = st.empty()
        self.actor = actor
        self.write(text)

    def write(self, text):
        if self.actor == "user":
            self.container.write(_get_user_string(text), unsafe_allow_html=True)

        elif self.actor == "assistant":
            self.container.write(_get_bot_string(text, "Bot"), unsafe_allow_html=True)

class Chat:
    def __init__(self, prompt):
        self.answer = st.empty()
        self.question = st.empty()

        N = len(prompt)
        for i in range(0, N - 1, 2):
            ix = N - 2 - i
            ixx = N - 1 - i
            question = prompt[ix]
            answer = prompt[ixx]
            message(question["content"], actor=question["role"])
            message(answer["content"], actor=answer["role"])
    
    def update_question(self, text):
        self.answer.write(_get_user_string(text), unsafe_allow_html=True)

    def update_answer(self, text):
        self.question.write(_get_bot_string(text, "Bot"), unsafe_allow_html=True)