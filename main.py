import typer
import joblib
import tensorflow as tf
from typing import Dict
import os

WIDTH, HEIGHT = (256, 256)

app = typer.Typer(no_args_is_help=True)

print("Loading model from pickle file...")
model = joblib.load("model.pkl")
print("Model loading complete!")


@app.command(short_help="Predicts probability of rat detected in image at path.")
def predict_image(image_path: str) -> float:
    image = tf.keras.utils.load_img(
        image_path,
        target_size=(WIDTH, HEIGHT)
    )

    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = tf.expand_dims(input_arr, 0)
    input_arr = tf.image.rgb_to_grayscale(input_arr)

    prediction = model.predict(input_arr)[0][1]

    print(f"""
File at path: {image_path} \nRat presence prediction: {prediction:2f}
    """)

    return prediction


@app.command(short_help="Predicts probabilities for all images in a folder")
def batch_prediction(folder_path: str) -> Dict[str, float]:
    preds = {}
    for file in os.listdir(folder_path):
        pred = predict_image(f"{folder_path}/{file}")
        preds[file] = pred
    # TODO: Output these predictions to a csv
    return preds


if __name__ == "__main__":
    app()
    # predict_image("./test_images/empty_0001.JPG")
