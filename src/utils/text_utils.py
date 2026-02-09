def to_kebab(snake):
    return snake.replace("_", "-")

def abbreviate(snake_name):
    return "".join([word[0] for word in snake_name.split("_")])

def to_camel(pascal):
    return "".join(
        letter.lower() if ( # Inside a word, meaning :
            i == 0 or # First letter : lowercase with no leading underscore
            letter.islower() or # Non-first letters : stay lowercase
            (letter.isupper() and i < len(pascal) - 1 and pascal[i+1].isupper())
            # Acronyms : last for as long as the next letter is also uppercase
        )
        else "_" + letter.lower() # Between words
        for i, letter in enumerate(pascal)
    )
