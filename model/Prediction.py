from model.database import connect

class Prediction:
  def __init__(self, class_id=None, class_description=None, prediction_model_id=None, image_id=None, window_number=None, postprocessed_image_properties_id=None, confidence=None):
    self.class_id = class_id
    self.class_description = class_description
    self.prediction_model_id = prediction_model_id
    self.image_id = image_id
    self.window_number = window_number
    self.postprocessed_image_properties_id = postprocessed_image_properties_id
    self.confidence = confidence

  def store(self):
    db = connect()
    cursor = db.cursor()
    sql = """INSERT INTO image_predictions
            (
            class_id,
            class_description,
            prediction_model_id,
            image_id,
            window_number,
            postprocessed_image_properties_id,
            confidence
            )
            VALUES
            (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
            )"""

    val = (self.class_id, self.class_description, self.prediction_model_id, self.image_id, self.window_number, self.postprocessed_image_properties_id, self.confidence)

    try:
        cursor.execute(sql, val)
        db.commit()
    except:
        print('Error' + cursor.statement)

  def get(self):
      db = connect()
      cursor = db.cursor()
      sql = 'select * from image_predictions where image_id = %s'
      image_id = (self.image_id,)

      cursor.execute(sql,image_id)

      return cursor.fetchall()

  def print(self):
      print(self.class_id, self.class_description, self.prediction_model_id, self.image_id, self.window_number, self.postprocessed_image_properties_id)
