from app.models.tortoise import TextSentiment

from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import os

model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

weightsPath = os.path.join(os.path.dirname(__file__), "data/bert_weights.h5")

model.load_weights(weightsPath)

async def predict_sentiment(sentiment_id: int, sentiment: str) -> None:
    
    tf_batch = tokenizer([sentiment], max_length=128, padding=True, truncation=True, return_tensors='tf')
    tf_outputs = model(tf_batch)
    tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
    sentiment = tf.argmax(tf_predictions, axis=1)
    sentiment = sentiment.numpy()[0]
    
    await TextSentiment.filter(id=sentiment_id).update(sentiment=bool(sentiment))