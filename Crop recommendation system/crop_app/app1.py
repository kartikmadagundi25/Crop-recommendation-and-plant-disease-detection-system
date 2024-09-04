import os
import numpy as np
import joblib
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = Flask(__name__)

# Load models
disease_model = load_model('E:\\Crop-Recommendation-system--main - Copy\\Crop-Recommendation-system--main\\Crop recommendation system\\crop_app\\model.h5')
print('Disease Model loaded.')
crop_model = joblib.load('E:\\Crop-Recommendation-system--main - Copy\\Crop-Recommendation-system--main\\Crop recommendation system\\crop_app\\crop_app')
print('Crop Recommendation Model loaded.')

# Labels for disease prediction
labels = {0: 'Healthy', 1: 'Powder', 2: 'Yellow mosaic'}

# Function to get disease prediction result
def get_disease_result(image_path):
    img = load_img(image_path, target_size=(225, 225))
    x = img_to_array(img)
    x = x.astype('float32') / 255.
    x = np.expand_dims(x, axis=0)
    predictions = disease_model.predict(x)[0]
    return labels[np.argmax(predictions)]

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    return render_template('Index.html')

@app.route('/form', methods=["POST"])
def crop_recommendation():
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Temperature = float(request.form['Temperature'])
    Humidity = float(request.form['Humidity'])
    Ph = float(request.form['ph'])
    Rainfall = float(request.form['Rainfall'])
    
    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]
    
    if 0 < Ph <= 14 and Temperature < 100 and Humidity > 0:
        arr = [values]
        prediction = crop_model.predict(arr)
        return render_template('prediction.html', prediction=str(prediction[0]))
    else:
        return "Sorry... Error in entered values. Please check the values and fill the form again."

@app.route('/predict_disease', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        predicted_label = get_disease_result(file_path)
        return render_template('predict_dis.html', prediction=predicted_label)
    return render_template('predict_leaf_disease.html')

if __name__ == '__main__':
    app.run(debug=True)
