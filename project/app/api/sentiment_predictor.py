from app.models.tortoise import TextSentiment
import tensorflow as tf
import pickle
import os
    

currentDir = os.path.join(os.path.dirname(__file__), 'data') 
    
with open(os.path.join(currentDir, 'encoder.bin'), 'rb') as file:
    encoder = pickle.load(file)

model = tf.keras.models.load_model(os.path.join(currentDir, 'sentiment-lstm.h5'))
model.load_weights(os.path.join(currentDir, 'sentiment-lstm-weights.h5'))

def pad_to_size(vec, size):
    zeros = [0] * (size - len(vec))
    vec.extend(zeros)
    return vec

def sample_predict(sentence, pad, model_):
    encoded_sample_pred_text = encoder.encode(sentence)
    if pad:
        encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
    encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
    predictions = model_.predict(tf.expand_dims(encoded_sample_pred_text,0))
    return predictions

async def predict_sentiment(sentiment_id: int, sentiment: str) -> None:
    
    prediction = int(round(sample_predict((sentiment), True, model)[0][0],1))
    
    await TextSentiment.filter(id=sentiment_id).update(sentiment=bool(prediction))