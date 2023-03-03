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

        self.player_names = {}

        self.DECK = []
        self.player_label = {}
        self.score_label = {}
        self.current_card_image = None
        self.deck_label = None

        # Creating frames for different screens
        self.player_details_frame = Frame(master=self.root)
        self.set_pd_frame()
        self.game_frame = Frame(master=self.root)
        self.set_game_frame()
        self.player_details_frame.pack()

        self.GAME = False
        self.TURN = 0

    def start_game(self):
        self.GAME = True

        self.player_details_frame.pack_forget()
        self.game_frame.pack()
        
        # Indicating Turn
        self.player_label[self.TURN].config(fg='red')
        
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

    def set_game_frame(self):
        '''Initialises frame with game details and controls'''
        # Adding player labels and cards left
        game = Frame(self.game_frame)

        players = Frame(game)
        player_frames = {}
        for i in range(self.players):
            player_frames[i] = Frame(players)
            name = self.player_names[i].get() + ": "
            self.player_label[i] = Button(player_frames[i], text=name, font=("Helvetica", 24, "bold"), command=lambda i=i:self.player_loses(i))
            self.player_label[i].grid(row=0, column=0)
            self.score_label[i] = Label(player_frames[i], text=f"{len(self.player_cards[i])} cards left", font=("Helvetica", 24, "bold"))
            self.score_label[i].grid(row=0, column=1)
            player_frames[i].pack(pady=20)
        players.pack(side=LEFT)

        deck = Frame(game)
        self.current_card_image = Label(deck, image=self.card_images["Cover"])
        self.current_card_image.pack(padx=20, pady=20)
        self.deck_label = Label(deck, text="Deck: 0", font=("Helvetica", 24, "bold"), justify="center")
        self.deck_label.pack(side=BOTTOM, pady=20)
        deck.pack(side=LEFT)

        game.pack()
        
        self.reset_button = Button(self.game_frame, text="Reset", font=("Helvetica", 16), command=self.reset_game)
        self.reset_button.pack(side=BOTTOM, padx=20, pady=10)

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