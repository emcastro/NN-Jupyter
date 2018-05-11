import keras
from matplotlib import pyplot as plt
from IPython.display import clear_output

# updatable plot
# a minimal example (sort of)

class PlotLosses(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        
        self.fig = plt.figure()
        
        self.logs = []
        
        self.epoch_count = 0

    def on_epoch_end(self, epoch, logs={}):
        self.epoch_count += 1
        self.log(epoch, logs)
        if self.epoch_count % 10 == 0:
            self.draw()

    def on_train_end(self, epoch, logs={}):
        self.log(epoch, logs)
        self.draw()

    def log(self, epoch, logs):
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1

    def draw(self):    
        clear_output(wait=True)
        fig, (ax, bx) = plt.subplots(ncols = 2)
        ax.semilogy(self.x, self.losses, label="loss")
        ax.semilogy(self.x, self.val_losses, label="val_loss")
        bx.plot(self.x, self.losses, label="loss")
        bx.plot(self.x, self.val_losses, label="val_loss")
        fig.set_size_inches(14,4)
        plt.legend()
        plt.show()
        
plot_losses = PlotLosses()