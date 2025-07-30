import os
import time
import pickle
import sys
import shutil
import itertools

import numpy as np
from mss import mss
from PIL import Image
import keyboard
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from pynput.keyboard import Key, Controller

# Initalize the PYNPUT controller
kb = Controller()

# VARIABLES

KEYS_TO_STRING_LIST = {
    "WASD": ["a", "d", "w", "s"],
    "ARROW": ["left", "right", "up", "down"]
}
KEYS_TO_PYNPUT_LIST = {
    "WASD": ["w", "d", "w", "s"],
    "ARROW": [Key.left, Key.right, Key.up, Key.down]
}

KEYS_ONE_HOT = list(itertools.product([True, False], repeat=4))
ONE_HOT_LENGTH = 16

IMAGES_PER_AUGMENT = 5

# FUNCTIONS

def augment_image(image, size, num_augments=IMAGES_PER_AUGMENT, max_shift=100):
    """
    Augments the provided image array by randomly shifting the image up to max_shift pixels
    in any direction. Fills empty space with black.
    """
    original = Image.fromarray(image)
    results = [np.array(original.resize(size, Image.BICUBIC))]  # Include the original

    width, height = size

    for _ in range(num_augments - 1):
        # Random shift in x and y, can be negative or positive
        shift_x = np.random.randint(-max_shift, max_shift + 1)
        shift_y = np.random.randint(-max_shift, max_shift + 1)

        # Create a new grayscale image
        shifted = Image.new("L", (width, height), 0)
        # Paste the original image at the shifted position
        shifted.paste(original.resize(size, Image.BICUBIC), (shift_x, shift_y))
        results.append(np.array(shifted))

    return results

# CLASSES

class CNN(nn.Module):
    def __init__(self, input_shape=(1, 128, 128)):
        """
        CNN for grayscale image input and multi-key classification.

        input_shape: (channels, height, width)
        num_actions: number of keys to predict (e.g., 4 for WASD)
        """
        super().__init__()
        C, H, W = input_shape
        self.num_actions = 4

        # Convolutional layers
        self.conv1 = nn.Conv2d(C, 32, kernel_size=3, stride=1, padding=1)
        self.bn1   = nn.BatchNorm2d(32)
        
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.bn2   = nn.BatchNorm2d(64)
        
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.bn3   = nn.BatchNorm2d(128)

        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Dynamically compute flattened feature size
        with torch.no_grad():
            dummy = torch.zeros(1, *input_shape)
            x = self.pool(F.relu(self.bn1(self.conv1(dummy))))
            x = self.pool(F.relu(self.bn2(self.conv2(x))))
            x = self.pool(F.relu(self.bn3(self.conv3(x))))
            self.flattened_size = x.view(1, -1).shape[1]

        # Fully connected layers
        self.fc1 = nn.Linear(self.flattened_size, 256)
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(256, self.num_actions)

    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        assert x.shape[1] == self.num_actions, f"Invalid output shape: {x.shape}, expected (_, {self.num_actions})"
        return x


class GeneralTMLearning:
    def __init__(self,
                 name:str="tmlearn_bot",
                 keys:str="WASD",
                 data_capture_interval:int | float=0.1,
                 exec_capture_interval:int | float=0.05,
                 save_frequency:int | None=100,
                 img_size:tuple=(128, 128),
                 cnn_test_percentage:float=0.2,
                 cnn_epochs:int=25,
                 cnn_batch_size:int=35,
                 verbose:bool=True
                 ):
        """
        Parameters:
            name (str): The name of the bot. The files will be put in a folder with this name.
            keys (str): Should be "WASD" or "ARROW". Which set of keys you will be pressing as input.
            data_capture_interval (int | float): The delay in seconds to capture frames when creating a dataset.
            exec_capture_interval (int | float): The delay in seconds to capture frames when using the model.
            save_frequency (int | None): The frequency to save the dataset when creating a dataset. Set to None for no auto-saving.
            img_size (tuple): The size the image should be scaled to when formatted as training data.
            cnn_test_percentage (float): The percentage of the dataset to hold for testing.
            cnn_epochs (int): The number of epochs to train the model for.
            cnn_batch_size (int): The batch size to use for training the model.
            verbose (bool): Wether to allow printing debug data. Some critical information will be printed regardless.
        """
        self.name = name
        self.folder = "{}_bot".format(self.name)
        self.data_file_name = os.path.join(self.folder, "{}_data.pkl".format(self.name))
        self.model_file_name = os.path.join(self.folder, "{}_cnn.keras".format(self.name))
        self.config_file_name = os.path.join(self.folder, "{}_config.pkl".format(self.name))

        self.input_keys = KEYS_TO_STRING_LIST[keys]
        self.output_keys = KEYS_TO_PYNPUT_LIST[keys]

        self._data_capture_interval = data_capture_interval
        self._exec_capture_interval = exec_capture_interval
        self._save_frequency = save_frequency

        self._img_size = img_size
        self._cnn_test_percentage = cnn_test_percentage
        self._cnn_epochs = cnn_epochs
        self._cnn_batch_size = cnn_batch_size

        self._verbose = verbose

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        self._create_or_use_config_file()

    # CONFIG ACTIONS

    # If any of the variables are changed, the config file should be updated.

    @property
    def data_capture_interval(self):
        return self._data_capture_interval
    @data_capture_interval.setter
    def data_capture_interval(self, val):
        self._data_capture_interval = val
        self._save_config_file()

    @property
    def exec_capture_interval(self):
        return self._exec_capture_interval
    @exec_capture_interval.setter
    def exec_capture_interval(self, val):
        self._exec_capture_interval = val
        self._save_config_file()

    @property
    def save_frequency(self):
        return self._save_frequency
    @save_frequency.setter
    def save_frequency(self, val):
        self._save_frequency = val
        self._save_config_file()

    @property
    def img_size(self):
        return self._img_size
    @img_size.setter
    def img_size(self, val):
        self._img_size = val
        self._save_config_file()

    @property
    def cnn_test_percentage(self):
        return self._cnn_test_percentage
    @cnn_test_percentage.setter
    def cnn_test_percentage(self, val):
        self._cnn_test_percentage = val
        self._save_config_file()

    @property
    def cnn_epochs(self):
        return self._cnn_epochs
    @cnn_epochs.setter
    def cnn_epochs(self, val):
        self._cnn_epochs = val
        self._save_config_file()

    @property
    def cnn_batch_size(self):
        return self._cnn_batch_size
    @cnn_batch_size.setter
    def cnn_batch_size(self, val):
        self._cnn_batch_size = val
        self._save_config_file()

    @property
    def verbose(self):
        return self._verbose
    @verbose.setter
    def verbose(self, val):
        self._verbose = val
        self._save_config_file()

    def _save_config_file(self):
        """ Create/modify the config file """
        var = {
            "input_keys": self.input_keys,
            "output_keys": self.output_keys,

            "data_capture_interval": self.data_capture_interval,
            "exec_capture_interval": self.exec_capture_interval,
            "save_frequency": self.save_frequency,

            "img_size": self.img_size,
            "cnn_test_percentage": self.cnn_test_percentage,
            "cnn_epochs": self.cnn_epochs,
            "cnn_batch_size": self.cnn_batch_size,

            "verbose": self.verbose
        }
        
        with open(self.config_file_name, "wb") as f:
            pickle.dump(var, f)

    def _create_or_use_config_file(self):
        """ Creates a config file to store the variable preferences in. """

        if os.path.exists(self.config_file_name):
            # Load the variables from the config file
            with open(self.config_file_name, "rb") as f:
                var = pickle.load(f)

            self.input_keys = var["input_keys"]
            self.output_keys = var["output_keys"]

            self.data_capture_interval = var["data_capture_interval"]
            self.exec_capture_interval = var["exec_capture_interval"]
            self.save_frequency = var["save_frequency"]

            self.img_size = var["img_size"]
            self.cnn_test_percentage = var["cnn_test_percentage"]
            self.cnn_epochs = var["cnn_epochs"]
            self.cnn_batch_size = var["cnn_batch_size"]

            self.verbose = var["verbose"]

            self.print("Loaded config from file.")
        else:
            self._save_config_file()

            self.print("Config file created. If you want to re-initialize a GeneralTMLearning class with the same name with different settings, you must call `tml.delete_config_file()` to erase the previous settings.")

    def delete_files(self,
            model_file:bool=False,
            data_file:bool=False,
            config_file:bool=False,
        ):
        if model_file:
            try:
                os.remove(self.model_file_name)
            except:
                pass
        if data_file:
            try:
                os.remove(self.data_file_name)
            except:
                pass
        if config_file:
            try:
                os.remove(self.data_file_name)
            except:
                pass

        # If deleting all files, also delete the folder
        if model_file and data_file and config_file:
            shutil.rmtree(self.folder)

        if model_file:
            print(f"Deleted the model file of {self.name}")
        if data_file:
            print(f"Deleted the dataset of {self.name}")
        if config_file:
            print(f"Deleted the config file of {self.name}")
        if model_file and data_file and config_file:
            print(f"Deleted all of {self.name} and its folder.")

    def delete_all_files(self):
        """
        Deletes all of the files of this bot.
        """
        self.delete_files(True, True)
        print(f"Deleted all {self.name} data.")

    def delete_config_file(self):
        """
        Deletes the config file. If a mistake is made when initilizing the class.
        """
        self.delete_files(config_file=True)

    def delete_dataset_file(self):
        """
        Deletes the dataset, but not the trained model.
        """
        self.delete_files(data_file=True)

    def print(self, text, newline:bool=False):
        """ Print the text if verbose. """
        if self.verbose:
            print(text, "\n" if newline else "")
            sys.stdout.flush()

    # DATASET

    def _load_dataset(self) -> tuple:
        try:
            with open(self.data_file_name, "rb") as f:
                data = pickle.load(f)
                self.print(f"Loaded {len(data["images"])} existing entries.")
        except (FileNotFoundError, EOFError):
            data = {"images": [], "keys": []}
            self.print("No existing data found, starting new list.")

        assert len(data["images"]) == len(data["keys"]), "Error in data: {} images but {} keys.".format(len(data["images"]), len(data["keys"]))
        return data["images"], data["keys"]

    def _save_dataset(self, images, keys):
        with open(self.data_file_name, "wb") as f:
            pickle.dump({"images": np.array(images), "keys": np.array(keys)}, f)

    def create_dataset(self):
        """
        Creates/adds to the existing dataset.
        You will be prompted to press [ENTER], and a 5 second countdown will commence. When it ends, data (screenshots + keys)
        will start being recorded. Hold the stop key, 'z' for about twice your data_capture_interval to stop and save.
        """
        images, keys = self._load_dataset()

        # Convert the images and keys to linked lists for appending
        images = list(images)
        keys = list(keys)

        # Wait for the user
        input(f"You will have 5 seconds to switch to TM.\nHold 'x' for about {self.data_capture_interval * 2} seconds to stop.\nDO NOT keyboard interrupt.\nPress [ENTER] to begin recording.\n")
        for i in range(5, 0, -1):
            self.print(f"{i}...", newline=False)
            time.sleep(1)

        self.print("GO!")

        # Initalize the variables
        sct = mss()
        frames = 0
        while True:
            start = time.time()

            # Check if the stop key is pressed
            if keyboard.is_pressed("z"):
                self.print("Stopping and saving.")
                break

            # Take a screenshot
            sct_img = sct.grab(sct.monitors[0])
            img = np.array(Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").resize(self.img_size).convert("L"))

            # Get the key states, for WASD or ARROW
            state = (
                keyboard.is_pressed(self.input_keys[0]),
                keyboard.is_pressed(self.input_keys[1]),
                keyboard.is_pressed(self.input_keys[2]),
                keyboard.is_pressed(self.input_keys[3])
            )

            # Convert the state to a one-hot vector
            idx = KEYS_ONE_HOT.index(state)
            one_hot = [0] * ONE_HOT_LENGTH
            one_hot[idx] = 1

            # Add the image and the state
            images.append(img)
            keys.append(state)

            # Print a debug message, proving that the keys are working.
            frames += 1
            self.print("Capture {} complete ({} augmented images). State: {}".format(frames, frames * IMAGES_PER_AUGMENT, state))

            # Auto-save if requested
            if self.save_frequency:
                if  frames % self.save_frequency == 0:
                    self._save_dataset(images, keys)
                    self.print("Auto-saving data.")

            # Calculate the desired time to wait, and sleep.
            desired_time = start + self.data_capture_interval
            time_left = desired_time - start
            time.sleep(time_left)

        # When broken, save the dataset
        self._save_dataset(images, keys)

    # TRAIN MODEL

    def _get_prepared_dataset(self):
        # Load the dataset
        images, keys = self._load_dataset()
        assert len(images) == len(keys)
        if not images.shape[0]:
            raise ValueError("No entries in dataset.")
        
        # Augment the samples
        aug_x = np.zeros((images.shape[0] * IMAGES_PER_AUGMENT, self.img_size[0], self.img_size[1]))
        aug_y = np.zeros((images.shape[0] * IMAGES_PER_AUGMENT, 4))
        for image_idx, image in enumerate(images):
            aug = augment_image(image, self.img_size)
            for i in range(IMAGES_PER_AUGMENT):
                aug_x[image_idx + i,:,:,] = aug[i]
                aug_y[image_idx + i,:,] = (keys[image_idx])
        aug_x = np.array(aug_x)
        aug_y = np.array(aug_y)

        assert len(aug_x) == len(aug_y)

        # Convert the images to grayscale, 256x256 images (or whatever size the user chose)
        X, y = [], []
        for img, keys in zip(aug_x, aug_y):
            arr = np.array(np.array(Image.fromarray(img)), dtype=np.float32) / 255.0

            X.append(arr)
            y.append([int(k) for k in keys])

        X = np.array(X)# [..., np.newaxis]  # shape: (n, h, w, 1)
        y = np.array(y, dtype=np.int8)

        assert len(X) == len(y)
        
        # Shuffle the samples
        idx = np.argsort(np.random.random(X.shape[0]))
        X = X[idx]
        y = y[idx]

        assert len(X) == len(y)

        # Split the samples into test/train
        #X_train, y_train, X_test, y_test = train_test_split(
        #    X, y,
        #    test_size = self.conv_test_percentage
        #)

        # Split the samples into test/train
        test_size = int(self.cnn_test_percentage * len(X))
        
        # Split the dataset into the four catagories
        X_test, y_test = X[:test_size], y[:test_size]
        X_train, y_train = X[test_size:], y[test_size:]

        assert len(X_train) == len(y_train), (len(X_train), len(y_train))
        assert len(X_test) == len(y_test), (len(X_train), len(y_train))

        # Create and return two dataloader objects
        return self._to_data_loaders(X_train, y_train), self._to_data_loaders(X_test, y_test)

    def _to_data_loaders(self, X, y):
        """ Converts the data into a Torch DataLoader object"""

        # Add the needed dimension to convert into torch tensor objects
        X = X[:, None, :, :]

        # Convert the samples into torch tensors
        X = torch.tensor(X, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32)

        # Create a TensorDataset object
        train_dataset = TensorDataset(X, y)

        # Create a DataLoader object
        train_loader = DataLoader(train_dataset, batch_size=self.cnn_batch_size, shuffle=False)

        # Return the result
        return train_loader

    def train_model(self):
        """
        Trains the CNN on the captured image-key dataset.
        """
        # This library uses a Torch CNN, which isn't as easy as Keras, however,
        # Keras currently doesn't support Python 3.12. I decided to use Torch instead of downgrading
        # the library to Python 3.11.

        # Load the dataset
        self.print("Loading and formatting data...")
        train_loader, test_loader = self._get_prepared_dataset()
        self.print(f"Loaded dataset.")

        # Print a CUDA/CPU message
        self.print(f"Training using {"CUDA with the GPU" if self.device == torch.device("cuda") else "the CPU"}.")

        # Define the CNN Model
        model = CNN(input_shape=(1, *self.img_size)).to(self.device)

        # Setup the loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        # Train the model
        for epoch in range(self.cnn_epochs):
            model.train()
            for batch_idx, (images, keys) in enumerate(train_loader):
                images, keys = images.to(self.device), keys.to(self.device)

                # Perform the forward pass on the model
                outputs = model(images)
                loss = criterion(outputs, keys)

                # Perform the backward pass and backprop
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            self.print(f"Epoch {epoch + 1}/{self.cnn_epochs}, loss: {loss.item()}")

        # Test the model
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for images, keys in test_loader:
                # Make the predictions
                images, keys = images.to(self.device), keys.to(self.device)
                outputs = model(images)
                _, pred = torch.max(outputs.data, 1)

                # Find the predicted keys
                pred = (pred > 0.5).squeeze().bool().tolist()
                print("Pred, keys", pred, keys)

                # Evaluate the result
                total += 1
                if pred == keys:
                    correct += 1

        self.print(f"Test accuracy: {100 * correct / total:.2f}%")

        # Save the model
        torch.save(model.state_dict(), self.model_file_name)
        self.print(f"Model saved to {self.model_file_name}")

    # RUN MODEL

    def _load_model(self):
        if not os.path.exists(self.model_file_name):
            raise FileNotFoundError(f"Model file '{self.model_file_name}' not found. Use `tml.train_model()` to train, or see docs.")
        
        model = CNN(input_shape=(1, *self.img_size)).to(self.device)
        model.load_state_dict(torch.load(self.model_file_name, map_location=torch.device("cpu")))
        model.eval()

        return model
    
    def _get_prediction(self, dataloader, model):
        with torch.no_grad():
            for images, keys in dataloader:
                # Convert all the data to the same device
                images, keys = images.to(self.device), keys.to(self.device)

                # Make the prediction
                output = model(images)

                # Find the predicted keys
                pred = (output > 0.5).squeeze().bool().tolist()
        return pred
    
    def _get_single_frame(self):
        """ Return a formatted screenshot. """
        # Get the screenshot
        sct = mss()
        sct_img = sct.grab(sct.monitors[0])

        # Format the image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img = img.convert('L').resize(self.img_size)
        arr = np.array(img, dtype=np.float32).flatten() / 255.0

        # Create a fake dataset
        X = np.array([img])
        y = np.array([[0, 0, 0, 0]])

        # Convert to dataloader
        return self._to_data_loaders(X, y)
    
    def _rel_all_keys(self):
        for key in self.output_keys:
            kb.release(key)
    
    def _apply_keys(self, state):
        # State is a tuple of 4 bools
        self._rel_all_keys()

        for idx, key in enumerate(self.output_keys):
            if state[idx]:
                kb.press(key)

    def run_model(self):
        """
        Uses the model.
        """
        # Load the CLF
        model = self._load_model()

        # Wait for the user
        input("Press [ENTER] to begin. You will have 5 seconds to switch to TM.\n")
        for i in range(5, 0, -1):
            self.print(f"{i}... ")
            time.sleep(1)
        print("GO! (Ctrl+C to stop)")

        # Try and loop, failing if keyboard interrupt
        try:
            while True:
                # Get the dataloader for the screenshot
                dataloader = self._get_single_frame()

                # Make the prediction
                pred = self._get_prediction(dataloader, model)

                # Press the keys and set the state variables
                state = tuple(bool(x) for x in pred)
                self._apply_keys(state)

                self.print(f"Prediction (left, down, up, right): {state}")

                # Wait
                time.sleep(self.exec_capture_interval)

        except KeyboardInterrupt:
            print("\nStopping. Releasing all keys.")

            # Release all keys
            for idx, key in enumerate(self.output_keys):
                kb.release(key)
            
            # Finished
            print("Done")
            exit()