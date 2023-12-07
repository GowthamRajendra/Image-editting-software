# calculates the correct size for the other dimension. if height, returns correct width. if width, returns height.
def calc(old_height, old_width, new_height=0, new_width=0):

    print(f"oh: {old_height}, ow: {old_width}, nh: {new_height}, nw: {new_width}")
    if new_height == 0:
        new_height = int((old_height / float(old_width)) * new_width)
        return new_height
    
    elif new_width == 0:
        new_width = int((old_width / float(old_height)) * new_height)
        return new_width