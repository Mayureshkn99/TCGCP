from tkinter import *
from PIL import ImageTk, Image
import random

class Game:
    def __init__(self, root):
        # Initializing window
        self.root = root
        self.root.title("Taco Cat Goat Cheese Pizza")
        self.root.resizable(True, True)

        # Initializing cards
        self.cards = ["Taco", "Cat", "Goat", "Cheese", "Pizza"]*11
        self.cards.extend(["Narwhal", "Gorilla", "Groundhog"]*3)

        # Loading card images
        self.card_images = {}
        self.load_images()

        self.players = 4
        # Distributing cards among players
        self.player_cards = {}
        self.deal_cards()

        # Displaying player entrys
        self.player_names = {}
        self.player_details_frame = Frame(master=self.root)
        self.set_pd_frame()
        self.player_details_frame.pack()

        self.GAME = False
        self.TURN = 0

    def start_game(self):
        self.GAME = True
        self.DECK = []
        self.player_label = {}
        self.score_label = {}

        self.player_details_frame.pack_forget()
        # Adding player labels and cards left
        for i in range(4):
            name = self.player_names[i].get()+": "
            self.player_label[i] = Button(root, text=name, font=("Helvetica", 24, "bold"), command=lambda i=i :self.player_loses(i))
            self.player_label[i].grid(row=i, column=0, pady=20)
            self.score_label[i] = Label(root, text=f"{len(self.player_cards[i])} cards left", font=("Helvetica", 24, "bold"))
            self.score_label[i].grid(row=i, column=1, pady=20)
        
        # Indicating Turn
        self.player_label[self.TURN].config(fg='red')
        
        # Replace start with reset button
        self.start_button.grid_forget()
        self.reset_button = Button(root, text="Reset", font=("Helvetica", 16), command=self.reset_game)
        self.reset_button.grid(row=5, column=0, columnspan=3, padx=20, pady=10)

        self.current_card_image = Label(root, image=self.card_images["Cover"])
        self.current_card_image.grid(row=0, column=2, rowspan=3, padx=20, pady=20)
        self.deck_label = Label(root, text="Deck: 0", font=("Helvetica", 24, "bold"), justify="center")
        self.deck_label.grid(row=3, column=2, pady=20)
        
        # Bind the function to the space bar event
        root.bind("<space>", self.next_card)

    def load_images(self):
        '''Load images for cards'''
        image = Image.open(f"images/cover.jpg")
        image = image.resize((500, 281))
        self.card_images["Cover"] = ImageTk.PhotoImage(image)
        for card in set(self.cards):
            image = Image.open(f"images/{card.lower()}.jpg")
            self.card_images[card] = ImageTk.PhotoImage(image)

    def deal_cards(self):
        '''Deal cards to players'''
        no_of_cards = len(self.cards) // self.players if (self.players >= 5) else 12
        random.shuffle(self.cards)
        for i in range(self.players):
            self.player_cards[i] = self.cards[no_of_cards * i:no_of_cards * (i+1)]

    def set_pd_frame(self):
        '''Initialises frame with the player details screen'''
        entry = {}
        for i in range(self.players):
            self.player_names[i] = StringVar()
            self.player_names[i].set(f"Player {i+1}")
            entry[i] = Entry(self.player_details_frame, textvariable=self.player_names[i], font=("Helvetica", 24, "bold"))
            entry[i].pack(pady=20)

        # Adding start button
        self.start_button = Button(self.player_details_frame, text="Start", font=("Helvetica", 16), command=self.start_game)
        self.start_button.pack(pady=10)

    def player_loses(self, player):
        self.player_cards[player].extend(self.DECK)
        self.DECK = []
        self.deck_label.config(text=f"Deck: 0")
        self.score_label[player].config(text=f"{len(self.player_cards[player])} cards left")
        self.player_label[self.TURN].config(fg='SystemButtonText')
        self.TURN = (player+1)%4
        self.player_label[self.TURN].config(fg='red')

        
    def reset_game(self):
        # Destroy all widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)
        
    
    
    def next_card(self, event):
        if self.GAME == False:
            return
        prev = self.TURN
        if len(self.player_cards[self.TURN]) == 0:
            # Updating the turn
            self.TURN = (self.TURN+1)%4
            self.player_label[prev].config(fg='SystemButtonText')
            self.player_label[self.TURN].config(fg='red')
            return
        current_card = self.player_cards[self.TURN].pop(0)
        
        # Updating the score
        self.score_label[self.TURN].config(text=f"{len(self.player_cards[self.TURN])} cards left")

        # Updating the deck
        self.current_card_image.config(image=self.card_images[current_card])
        self.DECK.append(current_card)
        self.deck_label.config(text=f"Deck: {len(self.DECK)}")

        # Updating the turn
        self.TURN = (self.TURN+1)%4
        self.player_label[prev].config(fg='SystemButtonText')
        self.player_label[self.TURN].config(fg='red')


if __name__ == '__main__':
    root = Tk()
    game = Game(root)
    root.mainloop()