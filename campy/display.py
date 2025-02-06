"""

"""
import sys, time, logging, warnings
import numpy as np
import matplotlib as mpl
warnings.filterwarnings("ignore")
mpl.use('Qt5Agg') # ignore qtapp warning...
import matplotlib.pyplot as plt
import screeninfo


def DrawFigure(num, screen_index=1):
    mpl.rcParams['toolbar'] = 'None'

    figure = plt.figure(num)
    ax = plt.axes([0, 0, 1, 1], frameon=False)

    plt.axis('off')
    plt.autoscale(tight=True)
    plt.ion()

    imageWindow = ax.imshow(np.zeros((1, 1, 3), dtype='uint8'),
                            interpolation='none')

    # Get screen information
    monitors = screeninfo.get_monitors()
    # Ensure there is a second screen; use index 0 for primary if not
    screen = monitors[screen_index] if len(monitors) > screen_index else monitors[0]
    screen_width, screen_height = screen.width, screen.height

    # Calculate position based on grid
    grid_size = (2, 2)  # Example: 2x2 grid
    tile_width = screen_width // grid_size[0]
    tile_height = screen_height // grid_size[1]

    x_pos = ((num-1) % grid_size[0]) * tile_width
    y_pos = ((num-1) // grid_size[0]) * tile_height

    manager = plt.get_current_fig_manager()
    # Adjust position by the screen offset
    manager.window.setGeometry(screen.x + x_pos, screen.y + y_pos, tile_width, tile_height)

    figure.canvas.draw()
    plt.show(block=False)

    return figure, imageWindow


def DisplayFrames(cam_params, dispQueue):
    n_cam = cam_params['n_cam']
    if sys.platform == "win32" and cam_params['cameraMake'] == 'basler':
	    # Display on Basler cameras uses the Pylon image window handled by cameras/basler.py
        pass
    else:
        figure, imageWindow = DrawFigure(n_cam+1, screen_index=1) # Specify secondary display
        
        while(True):
            try:
                if dispQueue:
                    img = dispQueue.popleft()
                    try:
                        imageWindow.set_data(img)
                        figure.canvas.draw()
                        figure.canvas.flush_events()
                    except Exception as e:
                        # logging.error('Caught exception at display.py DisplayFrames: {}'.format(e))
                        pass
                else:
                    time.sleep(0.01)
            except KeyboardInterrupt:
                break
        plt.close(figure)