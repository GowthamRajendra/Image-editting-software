# calculates the correct size for the other dimension. if height, returns correct width. if width, returns height.
def calc(old_height, old_width, new_height=0, new_width=0):
    if new_height == 0:
        ratio = old_height/old_width

        new_height = int(new_width * ratio)
        return new_height
    
    elif new_width == 0:
        ratio = old_width/old_height

        new_width = int(new_height * ratio)
        return new_width