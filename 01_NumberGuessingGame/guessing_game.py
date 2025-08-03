import random

def number_guessing_game():
    number_to_guess = random.randint(1, 100)
    attempts = 0

    print("🎮 Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100. Can you guess it?")

    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < number_to_guess:
                print("📉 Too low!")
            elif guess > number_to_guess:
                print("📈 Too high!")
            else:
                print(f"🎉 Congratulations! You guessed it in {attempts} attempts.")
                break
        except ValueError:
            print("🚫 Please enter a valid number.")

    play_again = input("🔁 Do you want to play again? (yes/no): ").lower()
    if play_again == "yes":
        number_guessing_game()
    else:
        print("👋 Thanks for playing!")

number_guessing_game()
