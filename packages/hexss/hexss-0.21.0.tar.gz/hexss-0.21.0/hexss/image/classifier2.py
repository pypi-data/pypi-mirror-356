import os
import shutil
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import Union, Optional, Any, Dict, List, Tuple, Self
import concurrent.futures

import hexss
from hexss import json_load, json_dump, json_update
from hexss.constants import *
from hexss.path import shorten
from hexss.image import Image, ImageFont, PILImage
import numpy as np
import cv2
import matplotlib.pyplot as plt

try:
    import tensorflow as tf
    import keras
    from keras.models import load_model
except ImportError:
    hexss.check_packages('tensorflow', 'matplotlib', auto_install=True)
    import tensorflow as tf
    import keras
    from keras.models import load_model  # type: ignore


def default_layers(img_size: Tuple[int, int], num_classes: int) -> list[Any]:
    """
    Returns a default list of layers for model construction.
    """
    return [
        keras.layers.RandomFlip('horizontal', input_shape=(*img_size, 3)),
        keras.layers.RandomRotation(0.1),
        keras.layers.RandomZoom(0.1),
        keras.layers.Rescaling(1. / 255),
        keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
        keras.layers.MaxPooling2D(),
        keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
        keras.layers.MaxPooling2D(),
        keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
        keras.layers.MaxPooling2D(),
        keras.layers.Dropout(0.2),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(num_classes, name='outputs')
    ]


class Classification:
    """
    Holds prediction results for one classification.
    Attributes:
        predictions: Raw model output logits or probabilities.
        class_names: List of class labels.
        idx: Index of top prediction.
        name: Top predicted class name.
        conf: Confidence score of top prediction.
        group: Optional group name if mapping provided.
    """
    __slots__ = ('predictions', 'class_names', 'idx', 'name', 'conf', 'group')

    def __init__(
            self,
            predictions: np.ndarray,
            class_names: List[str],
            mapping: Optional[Dict[str, List[str]]] = None
    ) -> None:
        self.predictions = predictions.astype(np.float64)
        self.class_names = class_names
        self.idx = int(self.predictions.argmax())
        self.name = class_names[self.idx]
        self.conf = float(self.predictions[self.idx])
        self.group: Optional[str] = None
        if mapping:
            for group_name, labels in mapping.items():
                if self.name in labels:
                    self.group = group_name
                    break

    def expo_preds(self, base: float = np.e) -> np.ndarray:
        """
        Exponentiate predictions by `base` and normalize to sum=1.
        """
        exp_vals = np.power(base, self.predictions)
        return exp_vals / exp_vals.sum()

    def softmax_preds(self) -> np.ndarray:
        """
        Compute standard softmax probabilities.
        """
        z = self.predictions - np.max(self.predictions)
        e = np.exp(z)
        return e / e.sum()

    def __repr__(self) -> str:
        return (
            f"<Classification name={self.name!r} idx={self.idx} group={self.group!r}>"
        )


class Classifier:
    """
    Wraps a Keras model for image classification.
    """
    __slots__ = ('model_path', 'json_path', 'config', 'model', 'class_names', 'img_size', 'layers')

    def __init__(
            self,
            model_path: Union[Path, str],
            config: Optional[Dict[str, Any]] = None
    ) -> None:
        '''
        :param model_path: `.keras` file path
        :param config: data of `.keras` file
                        example
                        {
                            "class_names": ["ng", "ok"],
                            "img_size": [32, 32],
                            ...
                        }
        '''
        self.model_path = Path(model_path)
        self.json_path = self.model_path.with_suffix('.json')
        self.config = config or json_load(self.json_path, {'img_size': [180, 180], 'class_names': []})

        ############################ for support old data ############################
        if 'model_class_names' in self.config and 'class_names' not in self.config:
            self.config['class_names'] = self.config.pop('model_class_names')
        ###############################################################################

        self.class_names: List[str] = self.config.get('class_names', [])
        self.img_size: Tuple[int, int] = tuple(self.config.get('img_size'))
        self.layers: Optional[List[Any]] = None
        self.model: Optional[keras.Model] = None
        self.load_model()

    def load_model(self) -> Self:
        if not self.model_path.exists():
            print(f"Warning: Model file {self.model_path} not found. Train with .train()")
            return self

        self.model = keras.models.load_model(self.model_path)
        return self

    def _prepare_image(
            self,
            im: Union[Image, PILImage.Image, np.ndarray]
    ) -> np.ndarray:
        """
        Convert input to RGB array resized to `img_size` and batch of 1.
        """
        if isinstance(im, Image):
            arr = im.numpy('RGB')
        elif isinstance(im, PILImage.Image):
            arr = np.array(im.convert('RGB'))
        elif isinstance(im, np.ndarray):
            if im.ndim == 2 or (im.ndim == 3 and im.shape[2] == 1):
                arr = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
            else:
                arr = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        else:
            raise TypeError(f"Unsupported image type: {type(im)}")

        arr = cv2.resize(arr, self.img_size)
        if arr.shape[2] == 4:
            arr = arr[..., :3]

        return np.expand_dims(arr, axis=0)

    def classify(
            self,
            im: Union[Image, PILImage.Image, np.ndarray],
            mapping: Optional[Dict[str, List[str]]] = None
    ) -> Classification:
        """
        Run a forward pass and return a Classification.
        """
        if self.model is None:
            raise ValueError("Model is not loaded. Call train() or load an existing model.")
        batch = self._prepare_image(im)
        preds = self.model.predict(batch, verbose=0)[0]
        return Classification(
            predictions=preds,
            class_names=self.class_names,
            mapping=mapping
        )

    def predict(self, *args, **kwargs):
        return self.classify(*args, **kwargs)

    def train(
            self,
            data_dir: Union[Path, str],
            epochs: int = 50,
            img_size: Tuple[int, int] = (180, 180),
            batch_size: int = 64,
            validation_split: float = 0.2,
            seed: int = 123,
            layers: Optional[List[Any]] = None
    ) -> None:

        data_dir = Path(data_dir)
        self.img_size = img_size
        train_ds, val_ds = keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=validation_split,
            subset='both',
            seed=seed,
            image_size=self.img_size,
            batch_size=batch_size
        )
        self.class_names = train_ds.class_names
        start_time = datetime.now()
        # Build config
        self.config = json_dump(self.json_path, {
            'class_names': self.class_names,
            'img_size': list(self.img_size),
            'epochs': epochs,
            'batch_size': batch_size,
            'validation_split': validation_split,
            'seed': seed,
            'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
        })

        # Build model
        self.layers = layers or default_layers(self.img_size, len(self.class_names))
        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.cache().shuffle(1000).prefetch(AUTOTUNE)
        val_ds = val_ds.cache().prefetch(AUTOTUNE)
        self.model = keras.Sequential(self.layers)
        self.model.compile(
            optimizer='adam',
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
        self.model.summary()

        # Save model after each epoch
        checkpoint_callback = keras.callbacks.ModelCheckpoint(
            filepath=self.model_path.with_name(f'{self.model_path.stem}_epoch{{epoch:03d}}.keras'),
            save_freq='epoch',
            save_weights_only=False,
            verbose=0
        )

        # Train
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[checkpoint_callback]
        )

        # Save final model
        self.model.save(self.model_path)
        print(f"{GREEN}Model saved to {GREEN.UNDERLINED}{self.model_path}{END}")
        end_time = datetime.now()
        self.config.update({
            'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'time_spent_training': (end_time - start_time).total_seconds(),
            'history': history.history
        })
        json_update(self.json_path, self.config)

        # Plot training history
        acc = history.history.get('accuracy', [])
        val_acc = history.history.get('val_accuracy', [])
        loss = history.history.get('loss', [])
        val_loss = history.history.get('val_loss', [])
        epochs_range = range(len(acc))

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.savefig(self.model_path.with_name(f"{self.model_path.stem} Training and Validation Loss.png"))
        plt.close()

    def test(
            self,
            data_dir: Union[Path, str],
            threshold: float = 0.7,
            multiprocessing: bool = False,
    ) -> Tuple[int, int, int, int]:
        """
        Test model on images in each class subfolder and print results.
        Returns (correct, uncertain, wrong, total).
        """
        data_dir = Path(data_dir)
        total = 0
        results = []

        def _test_one(class_name: str, img_path: Path, i: int, total: int) -> str:
            im = Image.open(img_path)
            clf = self.classify(im)
            prob = clf.expo_preds(1.2)[clf.idx]
            is_match = (clf.name == class_name)
            is_confident = is_match and prob >= threshold
            short = shorten(img_path, 2, 3)
            if is_confident:
                print(end=f'\r{class_name}({i}/{total}) {GREEN}{clf.name},{prob:.2f}{END} {short}')
                return 'correct'
            elif is_match:
                print(end=f'\r{class_name}({i}/{total}) {YELLOW}{clf.name},{prob:.2f}{END} {short}\n')
                return 'uncertain'
            else:
                print(end=f'\r{class_name}({i}/{total}) {RED}{clf.name},{prob:.2f}{END} {short}\n')
                return 'wrong'

        for class_name in self.class_names:
            folder = data_dir / class_name
            if not folder.exists():
                continue
            images = [f for f in folder.iterdir() if f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}]
            total = len(images)
            if total == 0:
                continue

            if multiprocessing:
                with concurrent.futures.ThreadPoolExecutor() as ex:
                    futures = [
                        ex.submit(_test_one, class_name, img_path, i + 1, total)
                        for i, img_path in enumerate(images)
                    ]
                    results = [f.result() for f in futures]
            else:
                for i, img_path in enumerate(images):
                    results.append(_test_one(class_name, img_path, i + 1, len(images)))
        print("\r")

        correct = results.count('correct')
        uncertain = results.count('uncertain')
        wrong = results.count('wrong')
        print(f"\rTest complete: {correct} correct, {uncertain} uncertain, {wrong} wrong")
        return correct, uncertain, wrong, total

    def __repr__(self) -> str:
        return (
            f"<Classifier path={self.model_path} loaded={'yes' if self.model else 'no'}"
            f" classes={self.class_names}>"
        )


import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Union, Optional, Any, Dict, List, Tuple
import concurrent.futures

from hexss import json_load, json_dump, json_update
from hexss.constants import *
from hexss.path import shorten
from hexss.image import Image, PILImage


class MultiClassifier:
    """
    Manages multiple classifiers applied to subregions (frames) of full images.

    Structure:
    - loads frame definitions from 'frames pos.json'
    - maps each frame key to a model and optional result mapping
    - provides methods to classify frames, crop variants, train, and test
    """

    def __init__(self, base_path: Union[Path, str]) -> None:
        self.base_path = Path(base_path)
        self.json_config = json_load(self.base_path / 'frames pos.json')
        raw_frames = self.json_config.get('frames', {})
        self.frames: Dict[str, Dict[str, Any]] = self._normalize(raw_frames)

        # directories
        self.img_full_dir = self.base_path / 'img_full'
        self.img_frame_dir = self.base_path / 'img_frame'
        self.img_frame_log_dir = self.base_path / 'img_frame_log'
        self.model_dir = self.base_path / 'model'

        # load models
        self.models: Dict[str, Classifier] = {}
        for name in self.json_config.get('models', []):
            for ext in ('.keras', '.h5'):
                path = self.model_dir / f"{name}{ext}"
                if path.exists():
                    clf = Classifier(path)
                    clf.load_model()
                    self.models[name] = clf
                    break
            else:
                raise FileNotFoundError(f"Model '{name}' not found (.keras or .h5) in {self.model_dir}")

    @staticmethod
    def _normalize(frames: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Normalize legacy keys: 'xywh' → 'xywhn', 'model_used' → 'model', 'res_show' → 'resultMapping'.
        """
        normalized = {}
        for key, frame in frames.items():
            f = frame.copy()
            if 'xywh' in f:
                f['xywhn'] = f.pop('xywh')
            if 'model_used' in f:
                f['model'] = f.pop('model_used')
            if 'res_show' in f:
                f['resultMapping'] = f.pop('res_show')
            normalized[key] = f
        return normalized

    def classify_all(
            self,
            im: Union[Image, PILImage.Image, Any]
    ) -> Dict[str, Classification]:
        base_im = Image(im)
        results: Dict[str, Classification] = {}
        for key, frame in self.frames.items():
            model_name = frame.get('model')
            if not model_name or model_name not in self.models:
                continue

            crop = base_im.crop(xywhn=frame['xywhn'])
            mapping = frame.get('resultMapping')
            results[key] = self.models[model_name].classify(crop, mapping=mapping)
        return results

    def crop_images_all(
            self,
            img_size: Tuple[int, int],
            shift_values: Optional[List[int]] = None,
            brightness_values: Optional[List[float]] = None,
            contrast_values: Optional[List[float]] = None,
            sharpness_values: Optional[List[float]] = None,
    ) -> None:
        """
        For each image in img_full, crop frames, log originals, and save variants.
        Variations: shifts, brightness, contrast, sharpness.
        """
        shift_values = shift_values or [0]
        brightness_values = brightness_values or [1.0]
        contrast_values = contrast_values or [1.0]
        sharpness_values = sharpness_values or [1.0]

        def _process(model_name: str, file_stem: str) -> None:
            try:
                data = json_load(self.img_full_dir / f"{file_stem}.json")
                img = Image(self.img_full_dir / f"{file_stem}.png")
            except Exception as e:
                print(f"{RED}Error loading {file_stem}: {e}{END}")
                return

            for frame_key, status in data.items():
                frame = self.frames.get(frame_key)
                if not frame or frame.get('model') != model_name:
                    continue

                # Directories
                log_dir = self.img_frame_log_dir / model_name
                var_dir = self.img_frame_dir / model_name / status
                log_dir.mkdir(parents=True, exist_ok=True)
                var_dir.mkdir(parents=True, exist_ok=True)

                # Original crop
                xywhn = frame['xywhn']
                orig = img.crop(xywhn=xywhn)
                orig.save(log_dir / f"{status}_{frame_key}_{file_stem}.png")

                # Variations
                for sx in shift_values:
                    for sy in shift_values:
                        crop = orig.copy().crop(xywhn=xywhn, shift=(sx, sy)).resize(img_size)
                        for b in brightness_values:
                            for c in contrast_values:
                                for sh in sharpness_values:
                                    variant = crop.copy().brightness(b).contrast(c).sharpness(sh)
                                    name = f"{file_stem}!{frame_key}!{status}!{sx}!{sy}!{b}!{c}!{sh}.png"
                                    variant.save(var_dir / name)

        # Clear old outputs
        shutil.rmtree(self.img_frame_dir, ignore_errors=True)
        shutil.rmtree(self.img_frame_log_dir, ignore_errors=True)

        # Process each model separately
        for model_name in self.models:
            print(f"{CYAN}==== Processing {model_name} ===={END}")
            stems = sorted({p.stem for p in self.img_full_dir.glob("*.json")}, reverse=True)
            with concurrent.futures.ThreadPoolExecutor() as exe:
                exe.map(lambda stem: _process(model_name, stem), stems)

    def train_all(
            self,
            epochs: int = 10,
            img_size: Tuple[int, int] = (180, 180),
            batch_size: int = 64,
            validation_split: float = 0.2,
            seed: int = 123,
            layers: Optional[List[Any]] = None
    ) -> None:
        """
        Train each classifier on its frame variants.
        """
        self.img_frame_dir.mkdir(parents=True, exist_ok=True)
        self.model_dir.mkdir(parents=True, exist_ok=True)

        for name, clf in self.models.items():
            print(f"{CYAN}==== Training {name} ===={END}")
            clf.train(
                data_dir=self.img_frame_dir / name,
                epochs=epochs,
                img_size=img_size,
                batch_size=batch_size,
                validation_split=validation_split,
                seed=seed,
                layers=layers
            )

    def test_all(
            self,
            threshold: float = 0.7,
            multiprocessing: bool = False
    ) -> Dict[str, Tuple[int, int, int, int]]:
        """
        Test each model on its cropped frame dataset.
        Returns mapping: model_name → (correct, uncertain, wrong, total).
        """
        results: Dict[str, Tuple[int, int, int, int]] = {}
        for name in self.models:
            print(f"{CYAN}==== Testing {name} ===={END}")
            clf = self.models[name]
            metrics = clf.test(
                data_dir=self.img_frame_dir / name,
                threshold=threshold,
                multiprocessing=multiprocessing
            )
            results[name] = metrics
        return results

    def __repr__(self) -> str:
        return f"<MultiClassifier base_path={self.base_path} models={list(self.models)} frames={list(self.frames)}>"
