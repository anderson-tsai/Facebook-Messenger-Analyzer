from tkinter import *
import analyzer
import chatbot

window = Tk()

def run_analyzer():
    output['text'] = analyzer.get_from_gui(show_most_active.get(), show_most_used.get(), show_first_message.get())

def run_chatbot():
    chatbot.run_from_gui(chat_name.get())

window.title('Facebook Messenger Analyzer')
Label(window, text='Chatbot', font=('times', 50)).grid(row=0, sticky=W)
chat_name = Entry(window)
chat_name.insert(0, 'Enter chat name here')
chat_name.grid(row=1, sticky=W)
Button(window, text='Run Chatbot', command=run_chatbot).grid(row=2, sticky=W)
Label(window, text='Toggle Features', font=('times', 50)).grid(row=3, sticky=W)
show_most_active = IntVar()
Checkbutton(window, text='Most Active Chat', variable=show_most_active).grid(row=4, sticky=W)
show_most_used = IntVar()
Checkbutton(window, text='Most used word/phrase/reactions', variable=show_most_used).grid(row=5, sticky=W)
show_first_message = IntVar()
Checkbutton(window, text='First Message Ever', variable=show_first_message).grid(row=6, sticky=W)
Button(window, text='Analyze', command=run_analyzer).grid(row=7, sticky=W)
Label(window, text='Output', font=('times', 50)).grid(row=8, sticky=W)
output = Label(window, text='Select options and the click run to see results here', font=('times', 12))
output.grid(row=9, sticky = W)
window.geometry('1920x1080')
window.mainloop()