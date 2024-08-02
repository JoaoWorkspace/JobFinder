def get_integer_input(prompt,context='<- MAIN ->'):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print(f"{context} Invalid input. Please enter a valid integer.")