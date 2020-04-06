from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt
from gluoncv.data import VOCDetection
import cv2
from gluoncv.data.transforms import presets
from gluoncv import utils
from mxnet import nd
from gluoncv.data.batchify import Tuple, Stack, Pad
from mxnet.gluon.data import DataLoader
import mxnet as mx
from mxnet import gluon

class VOCLike(VOCDetection):
    CLASSES = ['billboard', 'traffic light', 'electricity post', 'street lamp', 'traffic sign', 'surveillance camera']
    def __init__(self, root, splits, transform=None, index_map=None, preload_label=True):
        super(VOCLike, self).__init__(root, splits, transform, index_map, preload_label)


def CustomSSD(img):
    net = model_zoo.get_model('ssd_512_resnet50_v1_voc', classes=6, pretrained_base=False, pretrained=False)
    net.load_parameters('ssd_512_resnet50_v1_voc_best.params')

    x, img = data.transforms.presets.ssd.transform_test(img, short=512)

    class_IDs, scores, bounding_boxes = net(x)

    #if scores[0][0][0][0] > 0.7:
        # ax = utils.viz.cv_plot_bbox(img, bounding_boxes[0], scores[0],
        #                          class_IDs[0], class_names=net.classes)
        # cv2.imwrite('output/' + str(i) + '.png', ax)

    ax = utils.viz.cv_plot_bbox(img, bounding_boxes[0], scores[0],
                             class_IDs[0], class_names=net.classes)
    cv2.imwrite('output/' + str(i) + '.png', ax)

# PRETRAINED DATASETS
def preTrainedSSD(img, i):

    net = model_zoo.get_model('ssd_512_resnet50_v1_voc', pretrained=True)

    x, img = data.transforms.presets.ssd.transform_test(img, short=512)

    class_IDs, scores, bounding_boxes = net(x)

    if scores[0][0][0][0] > 0.7:
        ax = utils.viz.cv_plot_bbox(img, bounding_boxes[0], scores[0],
                                 class_IDs[0], class_names=net.classes)
        cv2.imwrite('output/' + str(i) + '.png', ax)

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



def FCNSemanticSegmentation(img, i):

    ctx = mx.cpu(0)

    img = presets.segmentation.test_transform(img, ctx)

    model = model_zoo.get_model('fcn_resnet101_voc', pretrained=True)

    output = model.predict(img)
    predict = mx.nd.squeeze(mx.nd.argmax(output, 1)).asnumpy()

    mask = utils.viz.get_color_pallete(predict, 'pascal_voc')

    mask.save('output/semanticOutput/FCNTEST/' + str(i) + '.jpg')
