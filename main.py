# PROJECT: Bicubic Interpolation for Image Resizing
# Look in features folder for "bicubic_spline.py" and "bicubic_convolution.py"
# 
# Ravichandra Pogaku - 100784105
# Gowtham Rajendra - 100785594
# Ivan Wang - 100785566

import PySimpleGUI as sg
import numpy as np
import cv2      
import matplotlib
matplotlib.use('TkAgg')
from pathlib import Path

from features import paintify, film_effects, nearest_neighbor, bilinear, average_blur, gauss_blur, hist_equalization, bicubic_spline, bicubic_convolution
from components import save_window, menu_bar, paintify_window, film_effects_window, resize_window, average_window, gauss_window
from helpers import draw, film_settings, constrain_size

def display_image(height, width, np_image=[]):
    
    new_height = new_width = 0

    image = [ # before image and after image
        [
            sg.Graph(
            canvas_size=(width, height),
            graph_bottom_left=(0, 0),
            graph_top_right=(width, height),
            key='-IMAGE-', # before image
            background_color='white',
        )
        ],
    ]

    # Define the layout
    layout = [
            [
                menu_bar.create_menu_bar(),
            ],
            [
            image,
            ],
            [sg.Text(f'Size: {new_width} x {new_height} px', key='-S_TEXT-')],
        ]

    # Create the window
    window = sg.Window('Image Editor', layout, finalize=True, resizable=True)
    editted_image = []

    # Event loop
    while True:
        event, values = window.read()

        if event == "Open Image":
            path = sg.popup_get_file(
                "Select image to load",
                file_types=[("Images", ".jpg .png")],
                keep_on_top=True
            )

            if path == None: # if cancel
                continue
            elif Path(path).is_file(): # if file exists
                new_image = cv2.imread(path) 
                new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
                draw.draw_im(new_image, window["-IMAGE-"], height)
                np_image = new_image
                editted_image = new_image
                window['-S_TEXT-'].Update(f'Size: {new_image.shape[1]} x {new_image.shape[0]} px')
            else:
                sg.popup_error("Invalid file")
        
        elif event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        # can only edit image after loading one
        elif len(np_image) > 0:
            if event == "Undo All":
                draw.draw_im(np_image, window["-IMAGE-"], height)
                editted_image = np_image
                window['-S_TEXT-'].Update(f'Size: {editted_image.shape[1]} x {editted_image.shape[0]} px')

            # save image
            elif event == "Save as":
                save_wind = save_window.create_save_window()
                save_file_name = ""

                while True:
                    save_event, save_values = save_wind.read()

                    if save_event == "Save":
                        forbidden_chars = "\\/:*?\"<>|"
                        # if input is len > 0 and input does not contain any forbbinden characters
                        if len(save_values["-S_INPUT-"]) > 0 and not any(c in forbidden_chars for c in save_values["-S_INPUT-"]):
                            save_file_name = save_values["-S_INPUT-"]
                            # if user has already resized the image
                            if len(editted_image) > 0:
                                # rgb -> bgr because that is how jpgs are stored
                                bgr_im = cv2.cvtColor(editted_image.astype(np.float32), cv2.COLOR_RGB2BGR)
                                cv2.imwrite(save_file_name+".jpg", bgr_im) # save to working directory
                                break
                            else:
                                sg.popup_error("Invalid file. You need to edit the original image before saving.", keep_on_top=True, modal=True)
                        else:
                            sg.popup_error(f"Invalid file name: {save_values['-S_INPUT-']}\nFile name should not be empty and should not contain \\/:*?\"<>| characters", keep_on_top=True, modal=True)
                    
                    elif save_event == sg.WINDOW_CLOSED or save_event == 'Cancel':
                        break
                save_wind.close()

            # paintify filter the image
            elif event == "Paintify":
                paintify_wind = paintify_window.create_paintify_window()

                while True:
                    paint_event, paint_values = paintify_wind.read()

                    if paint_event == "Paint":
                        s_len = int(paint_values["-S_LEN-"]) # stroke length
                        s_wid = int(paint_values["-S_WID-"]) # stroke width
                        threshold = int(paint_values["-THRESHOLD-"]) # gradient magnitude threshold
                        editted_image = paintify.drawStrokes(editted_image, threshold, s_len, s_wid)
                        draw.draw_im(editted_image, window["-IMAGE-"], height)
                    
                    elif paint_event == "Cancel" or paint_event == sg.WINDOW_CLOSED:
                        break
                paintify_wind.close()
            
            elif event == "Film Effects":
                film_wind = film_effects_window.create_film_window()
                pre_im = np.copy(editted_image) # image before applying film effects

                while True:
                    film_event, film_values = film_wind.read()

                    if film_event == "Apply":
                        pal_val = film_values["-PAL-"] # color palette
                        con_val = film_values["-CON-"] # contrast
                        sat_val = film_values["-SAT-"] # saturation

                        editted_image = film_effects.adjust_image(pre_im, pal_val, con_val, sat_val)
                        draw.draw_im(editted_image, window["-IMAGE-"], height)

                    elif film_event == "Reset":
                        draw.draw_im(pre_im, window["-IMAGE-"], height)
                        editted_image = pre_im
                        film_wind["-SAT-"].Update(0)
                        film_wind["-CON-"].Update(0)
                        film_wind["-PAL-"].Update(0)

                    elif film_event == "Save settings":
                        pal_val = film_values["-PAL-"] # color palette
                        con_val = film_values["-CON-"] # contrast
                        sat_val = film_values["-SAT-"] # saturation
                        film_settings.write(sat_val, con_val, pal_val)

                    elif film_event == "Load settings":
                        settings_file = Path("settings.yaml")
                        if settings_file.is_file(): # check if settings.yaml exists
                            sat_val, con_val, pal_val = film_settings.read()
                            film_wind["-SAT-"].Update(sat_val)
                            film_wind["-CON-"].Update(con_val)
                            film_wind["-PAL-"].Update(pal_val)
                        else:
                            sg.popup_error("No settings to load. Try savings settings first.", modal=True, keep_on_top=True)
                    elif film_event == "Cancel" or film_event == sg.WINDOW_CLOSED:
                        break
                film_wind.close()
            
            elif event == "Resize":
                resize_wind = resize_window.create_resize_window()

                while True:
                    resize_event, resize_values = resize_wind.read()

                    # if user types in height input
                    if resize_event == "-H_INPUT-":
                        if resize_values['-H_INPUT-'].isnumeric():
                            new_height = int(resize_values['-H_INPUT-'])
                        
                            if resize_values["-C_BOX-"]: # if constrained, update the width by ratio
                                new_width = constrain_size.calc(height, width, new_height=new_height)
                                resize_wind['-W_INPUT-'].Update(new_width)
                    
                    # if user types in width input
                    elif resize_event == "-W_INPUT-":
                        if resize_values['-W_INPUT-'].isnumeric():
                            new_width = int(resize_values['-W_INPUT-'])
                        
                            if resize_values["-C_BOX-"]: # if constrained, update the height by ratio
                                new_height = constrain_size.calc(height, width, new_width=new_width)
                                resize_wind['-H_INPUT-'].Update(new_height)
                    
                    elif resize_event == "Resize":
                        if resize_values["-INTER_CHOOSER-"] == 'Nearest Neighbor':
                            if new_height > 0 and new_width > 0:
                                editted_image = nearest_neighbor.resize(editted_image, new_height, new_width)

                                draw.draw_im(editted_image, window["-IMAGE-"], height)
                                window['-S_TEXT-'].Update(f'Size: {new_width} x {new_height} px')
                                break
                            else:
                                sg.popup_error(f'Invalid size: {new_height}x{new_width}')
                        
                        elif resize_values["-INTER_CHOOSER-"] == 'Bilinear':
                            if new_height > 0 and new_width > 0:
                                editted_image = bilinear.resize(editted_image, new_height, new_width)

                                draw.draw_im(editted_image, window["-IMAGE-"], height)
                                window['-S_TEXT-'].Update(f'Size: {new_width} x {new_height} px')
                                break
                            else:
                                sg.popup_error(f'Invalid size: {new_height}x{new_width}')
                        
                        # bicubic interpolation
                        elif resize_values["-INTER_CHOOSER-"] == "Bicubic Spline":
                            if new_height > 0 and new_width > 0:
                                editted_image = bicubic_spline.resize(editted_image, new_height, new_width)

                                draw.draw_im(editted_image, window["-IMAGE-"], height)
                                window['-S_TEXT-'].Update(f'Size: {new_width} x {new_height} px')
                                break
                            else:
                                sg.popup_error(f'Invalid size: {new_height}x{new_width}')
                        
                        elif resize_values["-INTER_CHOOSER-"] == "Bicubic Convolution":
                            if new_height > 0 and new_width > 0:
                                editted_image = bicubic_convolution.resize(editted_image, new_height, new_width)

                                draw.draw_im(editted_image, window["-IMAGE-"], height)
                                window['-S_TEXT-'].Update(f'Size: {new_width} x {new_height} px')
                                break
                            else:
                                sg.popup_error(f'Invalid size: {new_height}x{new_width}')
                    
                    elif resize_event == sg.WINDOW_CLOSED or resize_event == 'Cancel':
                        break

                resize_wind.close()
        
            elif event == "Average":
                avg_wind = average_window.create_average_window()
                pre_im = np.copy(editted_image)

                while True:
                    avg_event, avg_values = avg_wind.read()

                    if avg_event == "Apply":
                        half_w = avg_values["-AVG_SLIDER-"]
                        editted_image = average_blur.blur(pre_im, half_w)
                        draw.draw_im(editted_image, window["-IMAGE-"], height)
                    elif avg_event == "Reset":
                        draw.draw_im(pre_im, window["-IMAGE-"], height)
                        editted_image = pre_im
                        avg_wind["-AVG_SLIDER-"].Update(1)
                    elif avg_event == "Cancel" or avg_event == sg.WINDOW_CLOSED:
                        break
                avg_wind.close()
            
            elif event == "Gaussian":
                gau_wind = gauss_window.create_gauss_window()
                pre_im = np.copy(editted_image)

                while True:
                    gau_event, gau_values = gau_wind.read()

                    if gau_event == "Apply":
                        half_w = gau_values["-GAU_SLIDER-"]
                        editted_image = gauss_blur.blur(pre_im, half_w)
                        draw.draw_im(editted_image, window["-IMAGE-"], height)
                    elif gau_event == "Reset":
                        draw.draw_im(pre_im, window["-IMAGE-"], height)
                        editted_image = pre_im
                        gau_wind["-GAU_SLIDER-"].Update(1)
                    elif gau_event == "Cancel" or gau_event == sg.WINDOW_CLOSED:
                        break
                gau_wind.close()
            
            elif event == "Histogram Equalization":
                editted_image = hist_equalization.equalize(editted_image)
                draw.draw_im(editted_image, window["-IMAGE-"], height)

        else:
            sg.popup_ok("Please open an image", modal=True, keep_on_top=True)

    window.close()

def main():
    display_image(height=300, width=500) # size for default white square

if __name__ == '__main__':
    main()