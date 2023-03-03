from tkinter import Tk, Frame, Button, Label, Entry, StringVar
from PIL import ImageTk, Image
from random import shuffle

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

        self.num_players = 4
        # Distributing cards among players
        self.player_cards = {}
        self.deal_cards()

        self.player_names = {}

        self.DECK = []
        self.player_button = {}
        self.score_label = {}
        self.current_card_image = None
        self.deck_label = None

        # Creating frames for different screens
        self.player_details_frame = Frame(master=self.root)
        self.set_player_details_frame()
        self.game_frame = Frame(master=self.root)
        self.set_game_frame()
        self.player_details_frame.pack()

        self.GAME = False
        self.TURN = 0

    def set_player_details_frame(self):
        '''Initialises frame with the player details screen'''
        
        # Creating player Entries
        entry = {}
        for i in range(self.num_players):
            self.player_names[i] = StringVar()
            self.player_names[i].set(f"Player {i+1}")
            entry[i] = Entry(self.player_details_frame, textvariable=self.player_names[i], font=("Helvetica", 24, "bold"))
            entry[i].pack(pady=20, padx=20)

        # Adding start button
        self.start_button = Button(self.player_details_frame, text="Start", font=("Helvetica", 16), command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        """Initialising the game layout"""
        self.GAME = True
        self.win_button = {}

        self.player_details_frame.pack_forget()
        # Adding player labels and cards left
        for i in range(4):
            name = self.player_names[i].get()+": "
            self.player_button[i] = Button(root, text=name, font=("Helvetica", 24, "bold"), command=lambda i=i :self.player_loses(i))
            self.player_button[i].grid(row=i, column=0, pady=20)
            self.score_label[i] = Label(root, text=f"{len(self.player_cards[i])} cards left", font=("Helvetica", 24, "bold"))
            self.score_label[i].grid(row=i, column=1, pady=20)
        
        # Indicating Turn
        self.player_button[self.TURN].config(fg='red')
        
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
            image = Image.open(f"images/{card.lower()}.png")
            self.card_images[card] = ImageTk.PhotoImage(image)

    def deal_cards(self):
        '''Deal cards to players'''
        no_of_cards = len(self.cards) // self.num_players if (self.num_players >= 5) else 12
        shuffle(self.cards)
        for i in range(self.num_players):
            self.player_cards[i] = self.cards[no_of_cards * i:no_of_cards * (i+1)]

    def set_game_frame(self):
        '''Initialises frame with game details and controls'''
        # Adding player labels and cards left
        game = Frame(self.game_frame)

        players = Frame(game)
        player_frames = {}
        for i in range(self.players):
            player_frames[i] = Frame(players)
            name = self.player_names[i].get() + ": "
            self.player_button[i] = Button(player_frames[i], text=name, font=("Helvetica", 24, "bold"), command=lambda i=i:self.player_loses(i))
            self.player_button[i].grid(row=0, column=0)
            self.score_label[i] = Label(player_frames[i], text=f"{len(self.player_cards[i])} cards left", font=("Helvetica", 24, "bold"))
            self.score_label[i].grid(row=0, column=1)
            player_frames[i].pack(pady=20)
        players.pack(side="left")

        deck = Frame(game)
        self.current_card_image = Label(deck, image=self.card_images["Cover"])
        self.current_card_image.pack(padx=20, pady=20)
        self.deck_label = Label(deck, text="Deck: 0", font=("Helvetica", 24, "bold"), justify="center")
        self.deck_label.pack(side="bottom", pady=20)
        deck.pack(side="left")

        game.pack()
        
        self.reset_button = Button(self.game_frame, text="Reset", font=("Helvetica", 16), command=self.reset_game)
        self.reset_button.pack(side="bottom", padx=20, pady=10)

    def player_loses(self, player):
        """When a player loses a round"""
        
        # Check if deck is empty
        if self.DECK == []:
            return
        
        # player gets all the cards from the deck
        self.player_cards[player].extend(self.DECK)

        # Disabling the win button
        if self.win_button[player]["state"] == "active":
            self.win_button[player]["state"] = "disabled"

        #Updating the Deck
        self.DECK = []
        self.deck_label.config(text=f"Deck: 0")

        #Updating the player's cards
        self.score_label[player].config(text=f"{len(self.player_cards[player])} cards left")
        self.player_button[self.TURN].config(fg='SystemButtonText')

        # Updating the turn
        self.TURN = (player+1)%4
        self.player_button[self.TURN].config(fg='red')

    def player_wins(self, player):
        "When a player wins the game"
        print(player)
        pass

    def reset_game(self):
        """Resets the game and takes the user back to the entry screen"""
        # Destroy all widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)
        
    def next_card(self, event):
        """Changing the turn and updating the next card"""
        if self.GAME == False:
            return
        prev = self.TURN

        if len(self.player_cards[self.TURN]) != 0:

            # Draw a card from the player's cards
            current_card = self.player_cards[self.TURN].pop(0)

            # Activate win Button if player has 0 cards left
            if len(self.player_cards[self.TURN]) == 0 and self.win_button[self.TURN]["state"] == "disabled":
                self.win_button[self.TURN]["state"] = "active"
            
            # Updating the score
            self.score_label[self.TURN].config(text=f"{len(self.player_cards[self.TURN])} cards left")

            # Updating the deck
            self.current_card_image.config(image=self.card_images[current_card])
            self.DECK.append(current_card)
            self.deck_label.config(text=f"Deck: {len(self.DECK)}")

        # Updating the turn
        self.TURN = (self.TURN+1)%4
        self.player_button[prev].config(fg='SystemButtonText')
        self.player_button[self.TURN].config(fg='red')


if __name__ == '__main__':
    root = Tk()
    game = Game(root)
    root.mainloop()