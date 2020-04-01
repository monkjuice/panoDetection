from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt
from gluoncv.data import VOCDetection


class VOCLike(VOCDetection):
    CLASSES = ['billboard', 'traffic light', 'electricity post', 'street lamp', 'traffic sign', 'surveillance camera']
    def __init__(self, root, splits, transform=None, index_map=None, preload_label=True):
        super(VOCLike, self).__init__(root, splits, transform, index_map, preload_label)


def PascalVOCTest():
    dataset = VOCLike(root='VOCtemplate', splits=((2020, 'train'),))
    print('length of dataset:', len(dataset))
    print('label example:')
    print(dataset[0][1])


def preTrainedSSD(img):

    net = model_zoo.get_model('ssd_512_resnet50_v1_voc', pretrained=True)

    x, img = data.transforms.presets.ssd.transform_test(img, short=512)

    print('Shape of pre-processed image:', x.shape)

    class_IDs, scores, bounding_boxes = net(x)

    ax = utils.viz.plot_bbox(img, bounding_boxes[0], scores[0],
                             class_IDs[0], class_names=net.classes)
    plt.show()



def preTrainedRCNN(img):

    net = model_zoo.get_model('faster_rcnn_resnet50_v1b_voc', pretrained=True)

    x, orig_img = data.transforms.presets.rcnn.transform_test(img)

    box_ids, scores, bboxes = net(x)
    ax = utils.viz.plot_bbox(orig_img, bboxes[0], scores[0], box_ids[0], class_names=net.classes)

    plt.show()


def preTrainedYOLO(img):

    net = model_zoo.get_model('yolo3_darknet53_voc', pretrained=True)

    x, img = data.transforms.presets.yolo.transform_test(img, short=512)

    class_IDs, scores, bounding_boxs = net(x)

    ax = utils.viz.plot_bbox(img, bounding_boxs[0], scores[0],
                             class_IDs[0], class_names=net.classes)
    plt.show()
