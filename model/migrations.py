import database

def runMigrations():
    db = database.connect()
    cursor = db.cursor()

    cursor.execute(""" CREATE TABLE postprocessed_image_properties
                   (
                    id INT(11) NOT NULL AUTO_INCREMENT,
                    CONSTRAINT postprocessed_image_properties_pk PRIMARY KEY (id),

                    original_width SMALLINT,
                    original_height SMALLINT,

                    height_crop_from SMALLINT,
                    height_crop_size SMALLINT,
                    width_crop_from SMALLINT,
                    width_crop_size SMALLINT,

                    sliding_window_step_size SMALLINT,
                    sliding_window_size_x SMALLINT,
                    sliding_window_size_y SMALLINT,

                    pyramid_scale DECIMAL(3,2),
                    pyramid_min_size_x SMALLINT,
                    pyramid_min_size_y SMALLINT

                   )""")

    cursor.execute(""" CREATE TABLE images
                   (
                    id INT(11) NOT NULL AUTO_INCREMENT,
                    CONSTRAINT images_pk PRIMARY KEY (id),

                    name varchar(80),
                    path varchar(300)

                   )""")

    cursor.execute(""" CREATE TABLE windows_in_image
                   (
                   id INT(11) NOT NULL AUTO_INCREMENT,
                   CONSTRAINT windows_in_image_pk PRIMARY KEY (id),

                   number INT(11) NOT NULL,

                   bbox_upper_left_x SMALLINT,
                   bbox_upper_left_y SMALLINT,

                   bbox_lower_right_x SMALLINT,
                   bbox_lower_right_y SMALLINT,

                   center VARCHAR(255),
                   ATV DECIMAL(18,15),
                   ATH DECIMAL(18,15),

                   postprocessed_image_properties_id int,
                   FOREIGN KEY (postprocessed_image_properties_id) REFERENCES postprocessed_image_properties(id)
                   )""")

    cursor.execute(""" CREATE TABLE prediction_models
                   (
                    id INT(11) NOT NULL AUTO_INCREMENT,
                    CONSTRAINT prediction_models_pk PRIMARY KEY (id),

                    name varchar(255)

                   )""")

    cursor.execute(""" CREATE TABLE image_predictions
                   (
                    id INT(11) NOT NULL AUTO_INCREMENT,
                    CONSTRAINT image_predictions_pk PRIMARY KEY (id),

                    class_id varchar(50),
                    class_description varchar(255),

                    prediction_model_id int,
                    FOREIGN KEY (prediction_model_id) REFERENCES prediction_models(id),

                    image_id int,
                    FOREIGN KEY (image_id) REFERENCES images(id),

                    window_number INT(11) NOT NULL,

                    confidence DECIMAL(8,7),

                   postprocessed_image_properties_id int,
                   FOREIGN KEY (postprocessed_image_properties_id) REFERENCES postprocessed_image_properties(id)
                   )""")

runMigrations()
