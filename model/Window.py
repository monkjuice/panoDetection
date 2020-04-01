from model.database import connect

class Window:
  def __init__(self, ATV=None, ATH=None, center=None, number=None, bbox_upper_left_x=None, bbox_upper_left_y=None, bbox_lower_right_x=None, bbox_lower_right_y=None, postprocessed_image_properties_id=None):
    self.ATV = ATV
    self.ATH = ATH
    self.center = center
    self.number = number
    self.bbox_upper_left_x = bbox_upper_left_x
    self.bbox_upper_left_y = bbox_upper_left_y
    self.bbox_lower_right_x = bbox_lower_right_x
    self.bbox_lower_right_y = bbox_lower_right_y
    self.postprocessed_image_properties_id = postprocessed_image_properties_id

  def store(self):
    db = connect()
    cursor = db.cursor()
    sql = """INSERT INTO windows_in_image
            (
            number,
            ATV,
            ATH,
            center,
            bbox_upper_left_x,
            bbox_upper_left_y,
            bbox_lower_right_x,
            bbox_lower_right_y
            )
            VALUES
            (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
            )"""

    val = (self.number, self.ATV, self.ATH, str(self.center), self.bbox_upper_left_x, self.bbox_upper_left_y, self.bbox_lower_right_x, self.bbox_lower_right_y)

    cursor.execute(sql, val)
    db.commit()

  def get(self):
      db = connect()
      cursor = db.cursor()
      sql = 'select * from windows_in_image where number = %s and postprocessed_image_properties_id = %s'
      val = (self.number, self.postprocessed_image_properties_id)

      cursor.execute(sql,val)
      tempwindow = cursor.fetchone()

      self.bbox_upper_left_x = tempwindow[2]
      self.bbox_upper_left_y = tempwindow[3]
      self.bbox_lower_right_x = tempwindow[4]
      self.bbox_lower_right_y = tempwindow[5]
      self.center = tempwindow[6]
      self.ATV = tempwindow[7]
      self.ATH = tempwindow[8]


      return self

  def print(self):
      print(self.ATV, self.ATH, self.center, self.number, self.bbox_upper_left_x, self.bbox_upper_left_y, self.bbox_lower_right_x, self.bbox_lower_right_y)
