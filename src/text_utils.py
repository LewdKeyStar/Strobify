def to_kebab(snake):
    return snake.replace("_", "-")

def abbreviate(snake_name):
    return "".join([word[0] for word in snake_name.split("_")])
