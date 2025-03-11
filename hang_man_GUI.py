from hang_man import HangMan
import customtkinter as ctk
from tkinter import messagebox

class HangManGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("HangManBot v1.0")
        self.geometry("750x500")
        ctk.set_appearance_mode('light')

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
        instructions_title = ctk.CTkLabel(self.settings_frame, text="Instructions:", font=("Arial", 25, "bold"), justify="center")
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
            if word_length <= 0 or word_length > 15:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a word length between 2 and 15 inclusive.")
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
        self.guess_frame = ctk.CTkFrame(self.game_frame, bg_color="transparent", fg_color='transparent')
        self.guess_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.guess_frame.grid_rowconfigure(0, weight=1)
        self.guess_frame.grid_columnconfigure(0, weight=1)

        # Proceed Button:
        self.proceed_button = ctk.CTkButton(self.game_frame, 
                                            text="Proceed", 
                                            font=("Arial", 16, "bold"),
                                            height=35,
                                            fg_color="#137dd9",
                                            hover_color="#0066cc",
                                            corner_radius=5,
                                            command=self.proceed)
        self.proceed_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Hangman Display:
        self.hangman_display = ctk.CTkFrame(self.game_frame, bg_color='transparent', fg_color='transparent')
        self.hangman_display.grid(row=1, column=2, rowspan=3, padx=5, pady=5, sticky='nsew')
        self.hangman_display.grid_rowconfigure(0, weight=1)
        self.hangman_display.grid_columnconfigure(0, weight=1)

        # Information:
        self.info_display = ctk.CTkFrame(self.game_frame, bg_color="transparent", border_color='black', border_width=1)
        self.info_display.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.info_display.grid_rowconfigure(0, weight=1)
        self.info_display.grid_rowconfigure(1, weight=1)
        self.info_display.grid_rowconfigure(2, weight=1)
        self.info_display.grid_rowconfigure(3, weight=1)
        self.info_display.grid_columnconfigure(0, weight=1)


    def initialise_game(self, word_length):
        self.game = HangMan(word_length)
        self.letter_boxes = []
        self.missed_guesses = []
        self.word = ['_']*word_length

        self.initialise_word_display()
        self.initialise_computer_guess()
        self.initialise_hangman_drawing()
        self.initialise_information()
    
    def initialise_word_display(self):
        for i in range(self.game.n):
            btn = ctk.CTkButton(
                self.word_frame,
                text='_',
                text_color='black',
                bg_color='transparent',
                fg_color='white',
                hover_color='#137dd9',
                width=40,
                height=40,
                font=("Arial", 20, "bold"),
                corner_radius=5,
                command=lambda i=i: self.toggle_letter(i)
            )
            btn.pack(side="left", padx=5)
            self.letter_boxes.append(btn)

    def toggle_letter(self, ind):
        if self.word[ind] == '_':
            self.word[ind] = self.game.last_guess
            self.letter_boxes[ind].configure(text=self.game.last_guess.upper(), fg_color='#ffff80', hover_color='#ffff00')
        else:
            self.word[ind] = '_'
            self.letter_boxes[ind].configure(text='_', fg_color='white', hover_color='#137dd9')

    def initialise_computer_guess(self):
        comp_guess = self.game.guess()

        self.guess_label = ctk.CTkLabel(
                self.guess_frame,
                text=f"Computer Guess: {comp_guess.upper()}",
                font=('Arial', 24, 'bold'),
                justify="center"
            )
        self.guess_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def computer_guess(self):
        comp_guess = self.game.guess()

        if len(comp_guess) == 1:
            self.guess_label.configure(text=f'Computer Guess: {comp_guess.upper()}')
        else:
            HangManMessageBox(self, "Game Over", f"The word is: {comp_guess.upper()}")

    def initialise_hangman_drawing(self):
        self.canvas = ctk.CTkCanvas(self.hangman_display, bg='gray86', highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="snew", padx=5, pady=5)
        self.canvas.bind("<Configure>", self.scale_hangman)

        self.incorrect_guesses = 0
        self.scale_hangman()

    def draw_hangman(self):
        self.canvas.delete("all")
        for i in range(self.incorrect_guesses):
            self.drawing_steps[i]()

    def scale_hangman(self, event=None):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Base:
        base_x1, base_x2, base_y = 0.1*w, 0.9*w, 0.9*h
        # Pole:
        pole_x, pole_y1, pole_y2 = 0.3*w, 0.9*h, 0.1*h
        # Bar:
        bar_x1, bar_x2, bar_y = 0.3*w, 0.7*w, 0.1*h
        # Support:
        support_x1, support_x2, support_y1, support_y2 = 0.3*w, 0.467*w, 0.25*h, 0.1*h
        # Rope:
        rope_x, rope_y1, rope_y2 = 0.7*w, 0.1*h, 0.3*h
        # Head:
        r = 0.045*h
        head_x1, head_x2, head_y1, head_y2 = rope_x - r, rope_x + r, rope_y2, rope_y2 + 2*r
        # Body:
        body_x, body_y1, body_y2 = rope_x, head_y2, head_y2 + 3*r
        # Arm1:
        arm1_x1, arm1_x2, arm1_y1, arm1_y2 = rope_x, rope_x + 1.5*r, head_y2 + r, head_y2
        # Arm2:
        arm2_x1, arm2_x2, arm2_y1, arm2_y2 = rope_x, rope_x - 1.5*r, head_y2 + r, head_y2
        # Leg1:
        leg1_x1, leg1_x2, leg1_y1, leg1_y2 = rope_x, rope_x + r, body_y2, body_y2 + 2*r
        # Leg2:
        leg2_x1, leg2_x2, leg2_y1, leg2_y2 = rope_x, rope_x - r, body_y2, body_y2 + 2*r

        self.drawing_steps = [
            lambda: self.canvas.create_line(base_x1, base_y, base_x2, base_y, width=4),                # Base
            lambda: self.canvas.create_line(pole_x, pole_y1, pole_x, pole_y2, width=4),                # Pole
            lambda: self.canvas.create_line(bar_x1, bar_y, bar_x2, bar_y, width=4),                    # Bar
            lambda: self.canvas.create_line(support_x1, support_y1, support_x2, support_y2, width=4),  # Support
            lambda: self.canvas.create_line(rope_x, rope_y1, rope_x, rope_y2, width=4),                # Rope
            lambda: self.canvas.create_oval(head_x1, head_y1, head_x2, head_y2, width=4),              # Head
            lambda: self.canvas.create_line(body_x, body_y1, body_x, body_y2, width=4),                # Body
            lambda: self.canvas.create_line(arm1_x1, arm1_y1, arm1_x2, arm1_y2, width=4),              # Arm1
            lambda: self.canvas.create_line(arm2_x1, arm2_y1, arm2_x2, arm2_y2, width=4),              # Arm2
            lambda: self.canvas.create_line(leg1_x1, leg1_y1, leg1_x2, leg1_y2, width=4),              # Leg1
            lambda: self.canvas.create_line(leg2_x1, leg2_y1, leg2_x2, leg2_y2, width=4),              # Leg2
        ]

        self.draw_hangman()

    def initialise_information(self):
        info_title = ctk.CTkLabel(self.info_display, text='Information:', font=('Arial', 20, 'bold'), justify='center')
        info_title.grid(row=0, padx=5, pady=5)

        # missed_guess_count
        self.missed_guesses_count = ctk.CTkLabel(self.info_display, text='# Missed Guesses = 0', font=('Arial', 15), justify='center')
        self.missed_guesses_count.grid(row=1, padx=5, pady=5)

        # missed_letters
        self.missed_letters = ctk.CTkLabel(self.info_display, text='', font=('Arial', 15), justify='center')
        self.missed_letters.grid(row=2, padx=5, pady=5)

        # words_remaining
        self.words_remaining = ctk.CTkLabel(self.info_display, text=f'Remaining Words = {len(self.game.dictionary)}', font=('Arial', 15), justify='center')
        self.words_remaining.grid(row=3, padx=5, pady=5)

    def update_information(self):
        self.missed_guesses_count.configure(text=f'# Missed Guesses = {self.incorrect_guesses}')
        self.missed_letters.configure(text=" ".join(self.missed_guesses))
        self.words_remaining.configure(text=f'Remaining Words = {len(self.game.dictionary)}')

    def proceed(self):
        # Construct current word:
        word = ''
        flag = False
        for i, btn in enumerate(self.letter_boxes):
            letter = btn.cget('text').lower()
            word += letter
            if letter == self.game.last_guess:
                flag = True
                self.letter_boxes[i].configure(fg_color='#009933', hover_color='#009933', command=lambda: None)
        # Update dictionary
        if flag:
            try:
                self.game.update(word)
            except ValueError:
                HangManMessageBox(self, "Error", "No word exists in the dictionary with that letter placement")
        else:
            try:
                self.game.update()
            except ValueError:
                HangManMessageBox(self, "Error", "No word exists in the dictionary with that letter placement")
            self.missed_guesses.append(self.game.last_guess.upper())
            if self.incorrect_guesses < 11:
                self.incorrect_guesses += 1
                self.draw_hangman()
            else:
                self.draw_hangman()
                HangManMessageBox(self, "Game Over", f"The Hangman is complete. You win!")
        # run ncessary update functions
        self.computer_guess()
        self.update_information()


class HangManMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.exit_game)
        
        # Message:
        self.label = ctk.CTkLabel(self, text=message, font=("Arial", 14))
        self.label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self, bg_color='transparent', fg_color='transparent')
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.pack(pady=10)
        # Retry Button:
        self.retry_button = ctk.CTkButton(self.button_frame, text="retry", command=self.retry_game)
        self.retry_button.grid(row=0, column=0, padx=10)
        # Exit Button:
        self.exit_button = ctk.CTkButton(self.button_frame, text="exit", command=self.exit_game)
        self.exit_button.grid(row=0, column=1, padx=10)

        self.wait_window(self)

    def retry_game(self):
        self.destroy()
        self.quit()

    def exit_game(self):
        self.destroy()
        self.quit()


if __name__ == "__main__":
    game = HangManGUI()
    game.mainloop()
