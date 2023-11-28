from helpers import to_bytes

# replace old image with new im on a canvas
def draw_im(im, canvas, canvas_h):
    im_data = to_bytes.im_to_data(im)
    canvas.erase() # replace old loaded image
    canvas.set_size((im.shape[1], im.shape[0]))
    canvas.draw_image(data=im_data, location=(0, canvas_h))