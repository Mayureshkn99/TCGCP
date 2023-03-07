from tkinter import Tk, Frame, Button, Label, Entry, StringVar
from PIL import ImageTk, Image
from random import shuffle
from utils import PlayerIterator

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

        # Distributing cards among players
        self.player_cards = {}

        self.DECK = []
        self.player_names = {}
        self.win_button = {}
        self.player_button = {}
        self.score_label = {}
        self.current_card_image = None
        self.deck_label = None

        # Creating frames for different screens
        self.num_players_frame = None
        self.players_entry_frame = None
        self.game_frame = None

        # Getting player details
        self.set_player_details()

        self.GAME = False
        self.TURN = 0

    def set_player_details(self):
        """Initialises frames on the player details screen"""
        
        # Setting the initial frame to get number of players
        self.num_players_frame = Frame(master=self.root)
        self.num_players = StringVar()
        self.num_players.set('4')
        self.num_players_label = Label(self.num_players_frame, text="Enter the number of players:", font=("Helvetica", 24, "bold"))
        self.num_players_label.pack()
        self.num_players_entry = Entry(self.num_players_frame, textvariable=self.num_players, font=("Helvetica", 24, "bold"), width=10)
        self.num_players_entry.pack(side='left', padx=60)
        self.submit_button = Button(self.num_players_frame, text="Submit", font=("Helvetica", 15, "bold"), command=self.add_players)
        self.submit_button.pack(side='left')
        self.num_players_frame.pack(pady=20)
        self.players_entry_frame = None

    def add_players(self):
        """Add player Entries"""

        # Getting number of players
        self.players = int(self.num_players.get())

        # Destroying existing frame
        if self.players_entry_frame:
            self.players_entry_frame.destroy()

        # Generating player entries
        self.players_entry_frame = Frame(master=self.root)
        self.player_name_label = Label(self.players_entry_frame, text=f"Enter the name of {self.players} players:", font=("Helvetica", 15, "bold"))
        self.player_name_label.pack()
        for i in range(self.players):
            self.player_names[i] = StringVar()
            self.player_names[i].set(f"Player {i+1}")
            player_entry = Entry(self.players_entry_frame, textvariable=self.player_names[i], font=("Helvetica", 15, "bold"))
            player_entry.pack(pady=10)
        self.play_button = Button(self.players_entry_frame, text="Play", font=("Helvetica", 15, "bold"), command=self.start_game)
        self.play_button.pack(pady=20)
        self.players_entry_frame.pack()

    def start_game(self):
        """Initialising the game layout"""
        self.GAME = True

        self.deal_cards()

        self.num_players_frame.pack_forget()
        self.players_entry_frame.pack_forget()
        self.set_game_frame()
        
        # Indicating Turn
        self.player_button[self.TURN].config(fg='red')
        
        # Bind the function to the space bar event
        root.bind("<space>", self.next_card)

    def load_images(self):
        """Load images for cards"""
        image = Image.open(f"images/cover.png")
        image = image.resize((500, 281))
        self.card_images["Cover"] = ImageTk.PhotoImage(image)
        for card in set(self.cards):
            image = Image.open(f"images/{card.lower()}.png")
            self.card_images[card] = ImageTk.PhotoImage(image)

    def deal_cards(self):
        """Deal cards to players"""
        cards_per_player = len(self.cards) // self.players if (self.players >= 5) else 12
        shuffle(self.cards)
        for i in range(self.players):
            self.player_cards[i] = self.cards[cards_per_player * i:cards_per_player * (i+1)]

    def set_game_frame(self):
        '''Initialises frame with game details and controls'''
        # Adding player labels and cards left
        self.game_frame = Frame(master=self.root)
        game = Frame(self.game_frame)
        buttons = Frame(self.game_frame)
        players_frame = Frame(game)
        
        player_frames = {}
        for i in range(self.players):
            player_frames[i] = Frame(players_frame)
            name = self.player_names[i].get() + ": "
            self.win_button[i] = Button(player_frames[i], text="WIN", state="disabled", font=("Helvetica", 15, "bold"), command=lambda i=i :self.player_wins(i))
            self.win_button[i].grid(row=0, column=0, padx=10, pady=10)
            self.player_button[i] = Button(player_frames[i], text=name, font=("Helvetica", 24, "bold"), command=lambda i=i:self.player_loses(i))
            self.player_button[i].grid(row=0, column=1)
            self.score_label[i] = Label(player_frames[i], text=f"{len(self.player_cards[i])} cards left", font=("Helvetica", 24, "bold"))
            self.score_label[i].grid(row=0, column=2)
            player_frames[i].pack(pady=20)
        self.pool = PlayerIterator(self.players)
        players_frame.pack(side="left")

        deck = Frame(game)
        self.current_card_image = Label(deck, image=self.card_images["Cover"])
        self.current_card_image.pack(padx=20, pady=20)
        self.deck_label = Label(deck, text="Deck: 0", font=("Helvetica", 24, "bold"), justify="center")
        self.deck_label.pack(side="bottom", pady=20)
        deck.pack(side="left")

        game.pack()
        
        self.reset_button = Button(buttons, text="Reset", font=("Helvetica", 16), command=self.reset_game)
        self.reset_button.pack(side="left", padx=50, pady=10)
        self.play_again_button = Button(buttons, text="Play Again", font=("Helvetica", 16), command=self.play_again)
        self.play_again_button.pack(side="left", padx=50, pady=10)
        buttons.pack()

        self.game_frame.pack()

    def player_loses(self, player):
        """When a player loses a round"""
        
        # Check if deck is empty
        if self.DECK == []:
            return
        
        # player gets all the cards from the deck
        self.player_cards[player].extend(self.DECK)

        # Disabling the win button
        self.win_button[player].config(state="disabled")

        #Updating the Deck
        self.DECK = []
        self.deck_label.config(text=f"Deck: 0")

        #Updating the player's cards
        self.score_label[player].config(text=f"{len(self.player_cards[player])} cards left")
        self.player_button[self.TURN].config(fg='SystemButtonText')

        # Updating the turn
        self.pool.set_loser(player)
        self.TURN = self.pool.next()
        self.player_button[self.TURN].config(fg='red')

    def player_wins(self, player):
        """When a player wins the game"""    

        # Updating the turn    
        if self.TURN == player:
            self.TURN = self.pool.next()
        self.player_button[self.TURN].config(fg='red')
        
        self.pool.player_wins(player)
        
        # Disabling Buttons and Label
        self.win_button[player].config(state="disabled")
        self.player_button[player].config(state="disabled")


    def reset_game(self):
        """Resets the game and takes the user back to the entry screen"""
        # Destroy all widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)
    
    def play_again(self):
        """Restart the game with the existing players"""

        # Dealing cards
        self.deal_cards()

        # Disabling win button and updating number of cards
        for i in range(self.players):
            self.win_button[i].config(state="disabled")
            self.player_button[i].config(state="normal", fg='SystemButtonText')
            self.score_label[i].config(text=f"{len(self.player_cards[self.TURN])} cards left")

        # Updating deck
        self.DECK = []
        self.deck_label.config(text=f"Deck: 0")
        
        #Updating players
        self.pool = PlayerIterator(self.players)
        
        # Updating turn
        self.TURN = 0
        self.player_button[self.TURN].config(fg='red')

        # Updating card image
        self.current_card_image.config(image=self.card_images["Cover"])

    def next_card(self, event):
        """Changing the turn and updating the next card"""
        if self.GAME == False:
            return

        if len(self.player_cards[self.TURN]) != 0:

            # Draw a card from the player's cards
            current_card = self.player_cards[self.TURN].pop(0)

            # Activate win Button if player has 0 cards left
            if len(self.player_cards[self.TURN]) == 0 and self.win_button[self.TURN].cget("state") == "disabled":
                self.win_button[self.TURN].config(state="normal")
            
            # Updating the score
            self.score_label[self.TURN].config(text=f"{len(self.player_cards[self.TURN])} cards left")

            # Updating the deck
            self.current_card_image.config(image=self.card_images[current_card])
            self.DECK.append(current_card)
            self.deck_label.config(text=f"Deck: {len(self.DECK)}")

        # Updating the turn
        self.player_button[self.TURN].config(fg='SystemButtonText')
        self.TURN = self.pool.next()
        self.player_button[self.TURN].config(fg='red')


if __name__ == '__main__':
    root = Tk()
    game = Game(root)
    root.mainloop()