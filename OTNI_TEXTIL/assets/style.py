from tkinter import ttk

#PALETA DE COLORES
BG_MAIN = "#EBBED0" #fondo pantalla de inicio y headers
BG_GRAL = "#B1A2A8" #fondo para el fondo de las pantallas
BG ="#f0f0f0" #fondo blanco general
FG_BLACK = "#070707" #color de letra 
BUTTON_LOGIN = "#FA8CC8"

def aplicar_estilos(style: ttk.Style):
    style.theme_use("clam")

    style.configure("Main.TFrame", background=BG_MAIN)
    style.configure("Menu.TFrame", background=BG_GRAL)

    #login
    style.configure(
        "Header.TFrame", 
        background=BG_MAIN
    )

    style.configure(
        "HeaderTitle.TLabel", 
        background=BG_MAIN, 
        foreground=FG_BLACK, 
        font=("segoe UI", 16, "bold")
    )

    style.configure(
        "HeaderSubTitle.TLabel", 
        background=BG_MAIN, 
        foreground=FG_BLACK, 
        font=("segoe UI", 14, "bold")
    )
    
    style.configure(
        "Card.TLabel", 
        background=BG_MAIN, 
        foreground=FG_BLACK, 
        font=("segoe UI", 11, "bold"),
    )

    style.configure(
        "Card.TEntry", 
        fieldbackground=BG, 
        foreground=FG_BLACK, 
        font=("segoe UI", 12, "bold"), 
        padding=(8, 6)
    )

    style.configure(
        "Button.TButton", 
        background=BUTTON_LOGIN, 
        foreground=FG_BLACK, 
        font=("segoe UI", 12, "bold"), 
        padding=(16, 8), 
        borderwidth=0
    )

    style.map(
        "Button.TButton", 
        background=[("active", BG), ("pressed", FG_BLACK)], 
        foreground=[("active", FG_BLACK), ("pressed", BG)]
    )

    #menu

    style.configure(
        "Title.TLabel", 
        background=BG_MAIN, 
        foreground=FG_BLACK, 
        font=("Arial", 11, "bold")
    )

    style.configure(
        "SubTitle.TLabel",
        background=BG_MAIN, 
        foreground=FG_BLACK,
        font=("Arial", 10, "bold")
    )

    style.configure(
        "Menu.TButton", 
        background=BG, 
        foreground=FG_BLACK,
        font=("arial", 11)
    )

    style.map(
        "Menu.TButton", 
        background=[("active", BG), ("pressed", FG_BLACK)], 
        foreground=[("active", FG_BLACK), ("pressed", BG)]
    )

    

