## TMLearning

**TMLearning** is a Python library for training and deploying custom TrackMania AIs using machine learning. It works with any TrackMania version—or any game that uses only arrow keys—by training a convolutional neural network (CNN) to imitate your driving style from screenshots and predict the next key presses.

> **Note:** To capture keyboard input when TrackMania is not in focus, you must run the application running `TMLearning` with administrator privileges.

---

### Features

| Feature                                   | Status                     |
| ----------------------------------------- | -------------------------- |
| Digital Inputs / Outputs                  | ✅ Supported                |
| Analog Inputs / Outputs                   | ❌ Not supported            |
| Car Data (rotation, speed, position)      | 🟨 Coming soon (TMNF only) |
| Convolutional Neural Network architecture | ✅ Supported                |

---

### Installation

```bash
pip install tmlearning
```

---

### Quickstart

1. **Input Testing**

   ```python
   from tmlearning import wasd_key_test, arrow_key_test

   # Test WASD input
   wasd_key_test()

   # Test arrow-key input
   arrow_key_test()
   ```

   Press your chosen keys to confirm they’re detected correctly.

2. **Initialize the Bot**

   ```python
   from tmlearning import GeneralTMLearning
   bot = GeneralTMLearning(
       name="my_bot",
       keys="ARROW",                 # or "WASD"
       data_capture_interval=0.1,
       exec_capture_interval=0.1,
       save_frequency=None,
       img_size=(160, 120),
       cnn_test_percentage=0.2,
       cnn_epochs=10,
       cnn_batch_size=32,
       verbose=True
   )
   ```

3. **Create a Dataset**

   ```python
   bot.create_database()
   ```

   * Press **Enter** to start.
   * After a 5‑second countdown, drive in TrackMania.
   * Hold your stop key (default `z`) for \~2× `data_capture_interval` seconds to stop and save.

4. **Train the Model**

   ```python
   bot.train_model()
   ```

5. **Run the Model**

   ```python
   bot.run_model()
   ```

   * Press **Enter**, switch to TrackMania within 5 seconds, and let it drive for you.
   * Use **Ctrl+C** to stop.

---

### File Structure

When you instantiate `GeneralTMLearning(name="my_bot")`, a folder named `my_bot_bot/` is created containing:

| File Name           | Description                                 |
| ------------------- | ------------------------------------------- |
| `my_bot_data.pkl`   | Pickled dataset (screenshots + key labels). |
| `my_bot_cnn.keras`  | Saved CNN model weights.                    |
| `my_bot_config.pkl` | Pickled configuration parameters.           |

---

### Configuration

* On first initialization, `my_bot_config.pkl` records all parameters.
* Re-initializing with the same `name` loads existing settings.
* Changing any attribute (e.g. `bot.img_size = (200,150)`) automatically updates the config file.

---

### File Management

| Method                      | Deletes                     |
| --------------------------- | --------------------------- |
| `bot.delete_dataset_file()` | `my_bot_data.pkl`           |
| `bot.delete_config_file()`  | `my_bot_config.pkl`         |
| `bot.delete_all_files()`    | Entire `my_bot_bot/` folder |

---

### CNN Architecture (v1.2.0)

*Currently fixed; customization coming in v1.3.*

| Layer       | Parameters               |
| ----------- | ------------------------ |
| Conv1       | kernel=3×3, stride=1     |
| BatchNorm   | —                        |
| Conv2       | kernel=3×3, stride=1     |
| BatchNorm   | —                        |
| Conv3       | kernel=3×3, stride=1     |
| BatchNorm   | —                        |
| MaxPooling  | kernel=2×2, stride=2     |
| Dense (FC1) | 256 units                |
| Dropout     | p=0.3                    |
| Dense (FC2) | 4 units (output classes) |

---

### Version History

* **1.2.0**

  * Switched to CNN architecture.
  * Added file‑deletion methods (`delete_all_files`, `delete_config_file`, `delete_dataset_file`).
  * Renamed main class to `GeneralTMLearning` in preparation for `TMNFLearning`.

* **1.1.0**

  * Initial release.