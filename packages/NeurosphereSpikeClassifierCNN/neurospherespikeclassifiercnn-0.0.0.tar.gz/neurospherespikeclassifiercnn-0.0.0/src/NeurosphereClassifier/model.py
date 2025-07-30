"""
Model class, allows waveform classification, model debugging and weight adjustements. Copyright (C) 2025 Ylan A. CLODINE-FLORENT, Tissue Engineering Group - HEPIA

This file is part of the NeuralSpikeClassifierCNN package.
NeuralSpikeClassifierCNN is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
NeuralSpikeClassifierCNN is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with NeuralSpikeClassifierCNN. If not, see <https://www.gnu.org/licenses/>
"""

import os 
import time
import keras
import numpy as np
import matplotlib.pyplot as plt

from NeurosphereClassifier.utils import get_timestamp, create_folder
from NeurosphereClassifier.plot import plot_cutout
from NeurosphereClassifier.dataset import save_as_csv


class ModelClassifier:
    """
    Create a new model instance before each analysis to avoid data loss.
    """
    def __init__(self, path, filename):
        self.model = keras.models.load_model(os.path.join(path, filename))
        self.compile()
        self.conv = self.get_layer("conv")
        
        self.folder = os.path.join(path, f"model instance {get_timestamp()}")
        create_folder(self.folder)
        print(self.folder)

    def get_layer(self, name):
        """
        get layer by name : 'conv', 'dense', 'norm'
        """
        selected_layers = []
        for layer in self.model.layers:
            if name in layer.name: selected_layers.append(layer)
        return selected_layers

    def compile(self, optimizer="adam", loss="categorical_crossentropy", metrics="accuracy"):
        self.model.compile(optimizer, loss, metrics)
    
    def predict(self, cutouts):
        pred = []
        percent = []
        pred_folder = os.path.join(self.folder, "predictions")
        create_folder(pred_folder)

        # prediction
        prediction = self.model.predict(np.array(cutouts, dtype=np.float32))
    
        for i in range(len(prediction)):
            pred.append([int(round(prediction[i][0])), int(round(prediction[i][1]))])
            percent.append([round(prediction[i][0], 2), round(prediction[i][1], 2)])

        filename = f"model predictions {get_timestamp()}"
        save_as_csv([cutouts, pred, percent], ["cutouts", "predictions", "percent"], pred_folder, filename)

    def train(self, cutouts, labels, batch_size=32, epochs=10, save_folder="", filename="training"):

        if save_folder == "" : save_folder = os.path.join(self.folder, "training")
        create_folder(save_folder)
        checkpoints_folder = os.path.join(save_folder, "checkpoints")
        create_folder(checkpoints_folder)
        
        # Training
        callbacks = [
            keras.callbacks.ModelCheckpoint(filepath=os.path.join(checkpoints_folder, "model_at_epoch_{epoch}.keras")),
            keras.callbacks.EarlyStopping(monitor="val_loss", patience=5),
        ]

        history = self.model.fit(
            np.array(cutouts, dtype=np.float32),
            np.array(labels, dtype=np.int32),
            batch_size=batch_size,
            epochs=epochs,
            validation_split=0.2,
            callbacks=callbacks)
        
        self.save_history(history, filename) # history is saved as png and csv
        self.save(save_folder, filename)


    def rectify(self, cutouts=list, epochs=1, batch_size=32):
        new_pred_percent = []
        new_pred_binary = []
        seen_cutouts = []
        correction = []

        # create folder
        rectify_folder = os.path.join(self.folder, "rectification")
        create_folder(rectify_folder)

        # prediction
        prediction = self.model.predict(np.array(cutouts, dtype=np.float32))

        # rectification
        for i in range(len(prediction)):

            # save prediction
            noise = prediction[i][0]
            signal =prediction[i][1]

            # Ask for rectification
            pred_txt = f"Cutout n°{i}: NOISE ={ round(noise*100, 2)} % | SIGNAL = {round(signal*100, 2)}%"
            plot_cutout(cutouts[i], lab="Cutout", title=pred_txt)
            time.sleep(0.2)

            # re-label cutouts 
            answer = input(" 'type '1' for signal, or '0' for noise. Press 'Q' to stop. Press any key to pass'.")
            if answer == '1': 
                correction.append([0,1])
            elif answer == '0': 
                correction.append([1,0])
            elif answer == 'Q': break
            else : pass
            
            # save data only if an answer was given
            if answer == '1' or answer == '0':
                # saving seen cutouts, allowing the user to leave before the end of the list
                seen_cutouts.append(cutouts[i]) 

                # save predictions
                new_pred_percent.append([round(noise, 2), round(signal, 2)])
                new_pred_binary.append([int(round(noise)), int(round(signal))])

        # training 
        if len(seen_cutouts) < batch_size: batch_size = len(seen_cutouts) # if num of re-labeled cutouts is lower than batch size, batch size = num re-labeled cutouts
        self.train(seen_cutouts, correction, batch_size, epochs, rectify_folder, "rectification") # model and history are saved

        # save rectification
        save_as_csv([seen_cutouts, new_pred_percent, new_pred_binary, correction], ["cutouts", "pred (percent)", "pred (binary)", "correction"], rectify_folder, f"model rectification {get_timestamp()}")


    def saliency(self, cutouts=list):
        saliency_folder = os.path.join(self.folder, "saliency")
        create_folder(saliency_folder)

        # plot feature maps
        for i in range(len(cutouts)):
            print(f"image {i}")
            fig, axs = plt.subplots(len(self.conv), figsize=(10, 10))
            axs = np.array(axs)

            for j in range(len(self.conv)):

                print(f"conv {j}")
                # create model
                model_conv = keras.Model(inputs=self.model.inputs, outputs=self.conv[j].output)

                # get feature map output
                cutout = np.reshape(cutouts[i], (1, 75))
                feature_maps = model_conv.predict(cutout)
                prediction = self.model.predict(cutout)
                print(prediction.shape)
                pred_lab = f"prediction: NOISE = {round(prediction[0][0]*100, 4)}% | SIGNAL = {round(prediction[0][1]*100, 4)}%"
                conv_shape = self.conv[j].output.shape
                y = conv_shape[1:2][0]
                z = conv_shape[2:3][0]

                # order filters
                sorted = np.sort(feature_maps[0], axis=1)
            
                # plot filter
                ax_list = axs.reshape(-1)
                ax_list[j].set_title(f"conv {j+1} : {z} filters represented as {y}-long vectors")
                ax_list[j].grid(True)
                img = ax_list[j].imshow(np.transpose(sorted), cmap="jet", aspect="auto", extent=(0,75,min(cutouts[i]), max(cutouts[i])))
                ax_list[j].plot(np.linspace(0, 75, 75), cutouts[i], color="black", linewidth=5)
                ax_list[j].plot(np.linspace(0, 75, 75), cutouts[i], color="white", linewidth=2)
                fig.colorbar(img)
                fig.suptitle(pred_lab)
            
            # save figure    
            fig.tight_layout()
            fig.savefig(os.path.join(saliency_folder, f"{i} saliency.png"))
            print(f"figure {i} saved : {saliency_folder}")
            plt.show()
            time.sleep(0.2) # wait 200ms before prompting the user. Let the image display.
            answer = input("press any key to continue, or 'Q' to quit.")
            if answer == 'Q': break
 
        
    def filters(self):
        # summarize filter shapes
        convolution_filters = []
        filter_shapes = []

        for layer in self.conv:
            # get filter weights
            filters, biases = layer.get_weights()
            print(layer.name, filters.shape)

            # normalize filter values to 0-1 so we can visualize them
            f_min, f_max = filters.min(), filters.max()
            filters = (filters - f_min) / (f_max - f_min)

            # dimensions should be n filters of shape (x, y) -> (n, x, y)
            convolution_filters.append(np.transpose(filters))
            filter_shapes.append(np.transpose(filters).shape)


        for conv, shape in zip(convolution_filters, filter_shapes):

            i = 0
            fig, ax = plt.subplots(nrows=len(conv),figsize=(40, 80))

            for filter in conv:
                #ax = plt.subplot(len(conv), 1, ix)
                ax[i].set_title(f"filter {i} | shape : {shape}")
                ax[i].set_xticks([])
                ax[i].set_yticks([])

                # plot filter channel in grayscale
                im = ax[i].imshow(np.transpose(filter), cmap='gray')
                i += 1

            plt.tight_layout()
            plt.show()


    def save(self, save_folder, filename):
        self.model.save(os.path.join(save_folder, f"model {filename} {get_timestamp()}.keras"))  

    def save_history(self, history, filename):
        from matplotlib.ticker import MaxNLocator

        # create folder
        save_folder = os.path.join(self.folder, "history")
        create_folder(save_folder)

        # summarize history for accuracy
        fig, ax = plt.subplots()
        n = len(history.history['accuracy'])
        Xval = np.linspace(1, n, n)
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True)) # force plt to show x axis as integers
        ax.plot(Xval, history.history['accuracy'])
        ax.plot(Xval, history.history['val_accuracy'])
        ax.plot(Xval, history.history['loss'])
        ax.plot(Xval, history.history['val_loss'])
        ax.set_title('learning curve')
        ax.set_ylabel('accuracy')
        ax.set_xlabel('epoch')
        ax.legend(['training accuracy', 'validatition accuracy', 'training loss', 'validation loss'], loc='center right')
        ax.grid(True)
        fig.savefig(os.path.join(save_folder, f"history {filename}.png"))
        print(f"history.png saved : {save_folder}")
        plt.close()

        # save history as csv
        save_as_csv(
            arrays=[history.history['loss'], history.history['val_loss'], history.history['accuracy'], history.history['val_accuracy']], 
            colnames=['training loss', 'validation loss', 'training accuracy', 'validation accuracy'], 
            path=save_folder, filename=f"history {filename}"
            )
        

    def auc(self, y_test, y_pred):
        """
        use the AUC score to show the ratio of true and false positive
        y_test : array of labels from the test dataset
        y_pred : array of AUC score
        """
        from sklearn.metrics import roc_curve, auc

        # convert y_test and y_pred into 1d arrays
        y_test_1d = []
        y_pred_1d = []

        for labels in y_test:
            if labels[0] == 0: y_test_1d.append(1)
            else: y_test_1d.append(0)

        for score in y_pred:
            y_pred_1d.append(np.argmax(score))

        fpr, tpr, _ = roc_curve(y_test_1d, y_pred_1d)
        roc_auc = auc(fpr, tpr)

        plt.figure(figsize=(7, 5))
        plt.grid(True)
        plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}')
        plt.plot([0, 1], [0, 1], 'r--', label='Random Guess')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves for Two Models')
        plt.legend()
        plt.savefig(os.path.join(self.folder, "auc.png"))
        print(f"auc.png saved : {self.folder}")
        
        plt.show()
        plt.close()




