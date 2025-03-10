from hang_man import HangMan
import customtkinter as ctk
from tkinter import messagebox

class HangManGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("HangManBot v1.0")
        self.geometry("750x500")
        ctk.set_appearance_mode('dark')

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SettingsPage, GamePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
            self.frames[page_name] = frame

        self.show_frame('SettingsPage')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Outer Frame to Center Content
        self.settings_frame = ctk.CTkFrame(self, corner_radius=15)
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.settings_frame.grid_rowconfigure(0, weight=1)
        self.settings_frame.grid_rowconfigure(1, weight=1)
        self.settings_frame.grid_rowconfigure(2, weight=1)
        self.settings_frame.grid_rowconfigure(3, weight=1)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(1, weight=1)

        # Title:
        title = ctk.CTkLabel(self.settings_frame, text="Start Menu", font=("Arial", 34, "bold"))
        title.grid(row=0, column=0, pady=20, sticky="n", columnspan=2)

        # Instructions:
        instructions_title = ctk.CTkLabel(
        self.settings_frame, text="Instructions:", font=("Arial", 25, "bold"), justify="center"
        )
        instructions_title.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky="n")

        instructions_text = "\n1. Think of a word, and type in its length."+\
        "\n2. Let the computer guess letters."+\
        "\n3. For correct guesses, toggle the locations of said letter."+\
        "\n4. For incorrect guesses, no adjustments need to be made."+\
        "\n5. press proceed to continue the game."
        instructions = ctk.CTkLabel(self.settings_frame, text=instructions_text, font=("Arial", 16), justify="left")
        instructions.grid(row=2, column=0, pady=10, padx=20, sticky="nsew", columnspan=2)

        # Word Length Entry
        word_length_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        word_length_frame.grid(row=3, column=0, columnspan=2, pady=15)

        self.word_length_label = ctk.CTkLabel(word_length_frame, text="Word Length:", font=("Arial", 16))
        self.word_length_label.pack(side="left", padx=8)

        self.word_length_entry = ctk.CTkEntry(word_length_frame, width=100, height=35, font=("Arial", 14), corner_radius=10, placeholder_text='e.g. 5')
        self.word_length_entry.pack(side="left")

        # Start Button
        self.start_button = ctk.CTkButton(
            self.settings_frame, 
            text="Start Game", 
            font=("Arial", 16, "bold"),
            height=45, 
            corner_radius=10, 
            fg_color="#137dd9", 
            hover_color="#1565C0", 
            command=self.start_game
        )
        self.start_button.grid(row=4, column=0, pady=20, columnspan=2)

    def start_game(self):
        try:
            word_length = int(self.word_length_entry.get())
            if word_length <= 0 or word_length > 31:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid word length.")
            return

        # Pass word length to the game page
        self.controller.frames["GamePage"].initialise_game(word_length)
        self.controller.show_frame("GamePage")


class GamePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Outer Frame to Center Content
        self.game_frame = ctk.CTkFrame(self, corner_radius=15)
        self.game_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.game_frame.grid_rowconfigure(0, weight=1)
        self.game_frame.grid_rowconfigure(1, weight=1)
        self.game_frame.grid_rowconfigure(2, weight=1)
        self.game_frame.grid_rowconfigure(3, weight=1)
        self.game_frame.grid_columnconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(1, weight=1)
        self.game_frame.grid_columnconfigure(2, weight=1)

        # Word Display:
        self.word_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent", bg_color="transparent")
        self.word_frame.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        # Computer guess:
        self.guess_frame = ctk.CTkLabel(self.game_frame, text="Computer Guess = _", font=('Arial', 24, 'bold'), justify='center')
        self.guess_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')

        # Proceed Button:
        self.proceed_button = ctk.CTkButton(self.game_frame, text="Proceed", command=self.proceed)
        self.proceed_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Hangman Display:
        self.hangman_display = ctk.CTkFrame(self.game_frame, bg_color='transparent', fg_color='white')
        self.hangman_display.grid(row=1, column=2, rowspan=3, padx=5, pady=5, sticky='nsew')

        # Information:
        self.info_display = ctk.CTkFrame(self.game_frame)


    def initialise_game(self, word_length):
        self.word_length = word_length
        self.game = HangMan(word_length)

        self.last_guess = 'A'
        self.letter_boxes = []
        self.initialise_word_display()
    
    def initialise_word_display(self):
        for i in range(self.word_length):
            btn = ctk.CTkButton(
                self.word_frame,
                text='',
                text_color='black',
                bg_color='transparent',
                fg_color='white',
                width=40,
                height=40,
                font=("Arial", 20, "bold"),
                corner_radius=5,
                command=lambda i=i: self.toggle_letter(i)
            )
            btn.pack(side="left", padx=5)
            self.letter_boxes.append(btn)

    def toggle_letter(self, ind):
        if self.game.word[ind] == '_':
            self.game.word[ind] = self.last_guess
            self.word_update_display(ind, self.last_guess)
        elif self.game.word[ind] == self.last_guess:
            self.game.word[ind] = '_'
            self.word_update_display(ind, '')
        else: pass

    def word_update_display(self, ind, chr):
        self.letter_boxes[ind].configure(text=chr)

    def computer_guess(self):
        pass

    def proceed(self):
        pass

if __name__ == "__main__":
    game = HangManGUI()
    game.mainloop()
