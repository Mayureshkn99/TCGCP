from tkinter import *
from PIL import ImageTk, Image
import random

class Game:
    def __init__(self, root):
        # Initializing Window
        self.root = root
        self.root.title("Taco Cat Goat Cheese Pizza")
        self.root.resizable(True, True)

        # Initializing Cards
        self.cards = ["Taco", "Cat", "Goat", "Cheese", "Pizza"]*11
        self.cards.extend(["Narwhal"]*3)
        random.shuffle(self.cards)

        # Loading card Images
        self.card_images = {}
        for card in set(self.cards):
            image = Image.open(f"images/{card.lower()}.jpg")
            self.card_images[card] = ImageTk.PhotoImage(image)

        # Distributing Cards among players
        self.player_cards = {}
        for i in range(4):
            self.player_cards[i] = self.cards[16*i:16*(i+1)]

        # Displaying Player Entrys
        self.player_names = {}
        self.entry = {}
        for i in range(4):
            self.player_names[i] = StringVar()
            self.player_names[i].set(f"Player {i+1}")
            self.entry[i] = Entry(root, textvariable=self.player_names[i], font=("Helvetica", 24, "bold"))
            self.entry[i].grid(row=i, column=0, pady=20)

        # Adding Start Button
        self.start_button = Button(root, text="Start", font=("Helvetica", 16), command=self.start_game)
        self.start_button.grid(row=5, column=0, padx=20, pady=10)
        self.GAME = False
        self.TURN = 0
        
    def start_game(self):
        self.GAME = True
        self.player_label = self.score_label = {}

        # Adding Player Labels and Cards Left
        for i in range(4):
            name = self.entry[i].get()+": "
            self.entry[i].grid_forget()
            self.player_label[i] = Label(root, text=name, font=("Helvetica", 24, "bold"))
            self.player_label[i].grid(row=i, column=0, pady=20)
            self.score_label[i] = Label(root, text="16 cards left", font=("Helvetica", 24, "bold"))
            self.score_label[i].grid(row=i, column=1, pady=20)
        
        # Replace Start with Reset Button
        self.start_button.grid_forget()
        self.reset_button = Button(root, text="Reset", font=("Helvetica", 16), command=self.reset_game)
        self.reset_button.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

        self.current_card_label = Label(root, text=self.current_card, font=("Helvetica", 24, "bold"))
        self.current_card_label.grid(row=0, column=3, rowspan=4, padx=20, pady=20)
        
        # bind the function to the space bar event
        root.bind("<space>", self.next_card)

        
    def reset_game(self):
        pass
    
    
    def next_card(self, event):
        if self.GAME == False:
            return
        self.current_card = self.player_cards[self.TURN].pop()
        self.TURN = (self.TURN+1)%4


root = Tk()
game = Game(root)
root.mainloop()