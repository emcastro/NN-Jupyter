from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

def dump_model(model):
    model.summary()
    return SVG(model_to_dot(model).create(prog='dot', format='svg'))
