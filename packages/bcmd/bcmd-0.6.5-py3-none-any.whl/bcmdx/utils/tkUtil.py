import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from typing import Callable
from uuid import uuid4

# version 2026-0621


class TkForm(tk.Tk):

    _row = -1
    _initFocusItem: tk.Widget | None = None

    RADIO_NOTHING = uuid4().hex

    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.bind("<Map>", self._onMap)

    def _onMap(self, event: tk.Event):
        if self._initFocusItem:
            self._initFocusItem.focus_set()
            self._initFocusItem = None

    def add(self, desc: str, widget: tk.Widget):
        self._row += 1
        tk.Label(text=desc).grid(row=self._row, column=0, padx=10, pady=5, sticky='n')
        widget.grid(row=self._row, column=1, padx=10, pady=5, sticky='w')

    def addFrame(self, frame: tk.Frame):
        self._row += 1
        frame.grid(row=self._row, column=0, columnspan=2, padx=10, pady=5)

    def run(self):
        self.center()
        self.mainloop()

    def center(self):
        self.withdraw()  # 先隐藏窗口，避免闪动
        self.update_idletasks()  # 确保获取正确的窗口尺寸
        width = self.winfo_width()  # 获取窗口宽度
        height = self.winfo_height()  # 获取窗口高度
        screen_width = self.winfo_screenwidth()  # 屏幕宽度
        screen_height = self.winfo_screenheight()  # 屏幕高度
        x = (screen_width - width) // 2  # 水平居中
        y = (screen_height - height) // 2  # 垂直居中
        self.geometry(f"+{x}+{y}")  # 设置窗口位置
        self.deiconify()  # 恢复显示窗口

    def addLabel(self, desc: str, text: str):
        self.add(desc, tk.Label(text=text))

    def addBtn(self, label: str, command: Callable[..., None], *, width: int = 20, focus: bool = False):
        frame = tk.Frame(self)
        self.addFrame(frame)
        btn = tk.Button(frame, text=label, width=width, command=command)
        btn.pack(side="left", expand=True, padx=15)
        if focus:
            self._initFocusItem = btn

    def addRadioBtn(self, desc: str, selectionList: list[str], *, selectedIndex: int | None = None, focusIndex: int | None = None):
        frame = tk.Frame()
        self.add(desc, frame)
        var = tk.StringVar(value=selectionList[selectedIndex] if selectedIndex is not None else self.RADIO_NOTHING)
        radioBtnList: list[tk.Radiobutton] = []
        for version in selectionList:
            radioBtn = tk.Radiobutton(frame, text=version, variable=var, value=version)
            radioBtn.pack(side="left", padx=(0, 15))
            radioBtnList.append(radioBtn)
        if focusIndex is not None:
            self._initFocusItem = radioBtnList[focusIndex]
        return var

    def addEntry(self, desc: str, text: str = '', *, width: int = 60, focus: bool = False):
        entry = tk.Entry(self, width=30)
        entry.insert(0, text)
        self.add(desc, entry)
        if focus:
            self._initFocusItem = entry
        return entry

    def addScrolledText(self, desc: str, text: str = '', *, width: int = 60, height: int = 20, focus: bool = False):
        scrolledText = ScrolledText(self, width=width, height=height)
        scrolledText.insert("1.0", text)
        self.add(desc, scrolledText)
        if focus:
            self._initFocusItem = scrolledText
        return scrolledText

    def addCheckBox(self, text: str, value: bool = False):
        remember_var = tk.BooleanVar(value=value)
        check_btn = tk.Checkbutton(text=text, variable=remember_var)
        self.add("", check_btn)
        return remember_var

    def addPasswordInput(self, desc: str, *, width: int = 60, command: Callable[..., None] | None = None):
        password_entry = tk.Entry(self, show="*", width=width)  # 使用 show="*" 隐藏输入内容
        if command:
            password_entry.bind('<Return>', lambda event: command())
        self.add(desc, password_entry)
        return password_entry


''' 例子
app = TkForm()
app.title('更新版本信息')
app.addLabel('当前版本号', '3.11.8')
app.addLabel('上次更新时间', '2025-06-16 16:00:00')
version_var = app.addRadioBtn(
    '请选择新版本',
    ['3.11.8', '3.11.9', '3.11.10'],
    2,
)
log_text = app.addScrolledText('更新日志', '123\n23454asd这个')
vara = app.addCheckBox('记住密码', False)
varb = app.addCheckBox('阿萨德法师大润发', True)
passwordInput = app.addPasswordInput('密码', command=lambda: onBtn())


def onBtn():
    print(version_var.get())
    print(log_text.get('1.0', "end-1c").split('\n'))
    app.destroy()


app.addBtn('确定', onBtn)
app.bind("<Visibility>", lambda e: passwordInput.focus_set())
app.run()
'''
