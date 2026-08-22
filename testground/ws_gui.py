import ttkbootstrap as ttk

app = ttk.App(title="Log", size=(480, 320))

log = ttk.ScrolledText(app, auto_hide=True, padding=10)
log.pack(fill="both", expand=True)

log.text.insert("end", "Application started\n")
log.text.insert("end", "Loading data…\n")
log.text.see("end")            # scroll to the newest line

app.mainloop()