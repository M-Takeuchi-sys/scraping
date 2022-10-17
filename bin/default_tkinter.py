import tkinter


class Application(tkinter.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=400, height=300)
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        store_label = tkinter.Label(self)
        store_label['text'] = '店舗ID'
        store_label.place(x=50, y=50)
        min_label = tkinter.Label(self)
        min_label['text'] = '価格（Min）'
        min_label.place(x=50, y=80)
        max_label = tkinter.Label(self)
        max_label['text'] = '価格（Man）'
        max_label.place(x=50, y=110)

        store_form = tkinter.Entry(self)
        store_form.place(x=130, y=50, width=200)
        min_form = tkinter.Entry(self)
        min_form.place(x=130, y=80, width=200)
        max_form = tkinter.Entry(self)
        max_form.place(x=130, y=110, width=200)

        quit_btn = tkinter.Button(self)
        quit_btn['text'] = '閉じる'
        quit_btn['command'] = self.root.destroy
        quit_btn.place(x=125, y=180, width=150, height=40)
        quit_btn.pack(side='bottom')

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('タイトル')
    root.geometry('400x300')
    app = Application(root=root)
    app.mainloop()
