from DeathBots import Bots  # Importing the Bots class from the DeathBots file

bots = Bots()  # Creating a variable

tokens = bots.get_and_check_tokens()  # Reading and checking tokens from the tokens.txt file
if tokens:  # If there are valid tokens
    print(f'Number of working tokens: {str(tokens)}')  # Print the count of working tokens

bots.send_msg(1094114642298667018, 'Hello, everyone!')  # Sending a message from all bots
