import database

def runSeeds():
    image_properties_seeder()

def image_properties_seeder():
    db = database.connect()
    cursor = db.cursor()

    sql = "insert into postprocessed_image_properties (original_width, original_height, height_crop_from, height_crop_size,width_crop_from,width_crop_size,sliding_window_step_size,sliding_window_size_x,sliding_window_size_y,pyramid_scale,pyramid_min_size_x,pyramid_min_size_y) values (11264, 5632, 1300, 1200, null, null, 74, 224, 224, 1.5, 600, 600);"

    cursor.execute(sql)

    db.commit()

def windows_in_image_seeder():
    db = database.connect()
    cursor = db.cursor()
    

runSeeds()
