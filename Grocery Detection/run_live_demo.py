from vision.ssd.vgg_ssd import create_vgg_ssd, create_vgg_ssd_predictor
from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
from vision.ssd.mobilenetv1_ssd_lite import create_mobilenetv1_ssd_lite, create_mobilenetv1_ssd_lite_predictor
from vision.ssd.squeezenet_ssd_lite import create_squeezenet_ssd_lite, create_squeezenet_ssd_lite_predictor
from vision.utils.misc import Timer
import cv2
import sys

if len(sys.argv) < 3:
    print('Usage: python run_ssd_example.py <net type>  <model path> <label path> [video file]')
    sys.exit(0)

net_type = sys.argv[1]
model_path = sys.argv[2]
label_path = sys.argv[3]

if len(sys.argv) >= 4:
    cap = cv2.VideoCapture(0)  # capture from file
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out = cv2.VideoWriter('videos/output_v5.wmv', fourcc, 20.0, (720,640))
else:
    cap = cv2.VideoCapture(1)   # capture from camera
    cap.set(3, 480)
    cap.set(4, 360)
#    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#    out = cv2.VideoWriter('out.mp4',fourcc, 20.0,(int(cap.get(3)),int(cap.get(4))))
class_names = [name.strip() for name in open(label_path).readlines()]
num_classes = len(class_names)



if net_type == 'mb1-ssd':
    net = create_mobilenetv1_ssd(len(class_names), is_test=True)

else:
    print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
    sys.exit(1)
net.load(model_path)

if net_type == 'mb1-ssd':
    predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)

else:
    print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
    sys.exit(1)



timer = Timer()
while True:
    ret, orig_image = cap.read()
    if orig_image is None:
        continue


    width = 720
    height = 640
    dim = (width,height)
    orig_image = cv2.resize(orig_image, dim, interpolation = cv2.INTER_AREA)
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    timer.start()
    boxes, labels, probs = predictor.predict(image, 10, 0.4)
    interval = timer.end()
    for i in range(boxes.size(0)):
        box = boxes[i, :]
        #label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
        label = f"{class_names[labels[i]]}"
        
        if probs[i]>=0.80:
            print('Time: {:.2f}s, Detect Objects: {:d}.'.format(interval, labels.size(0)))
            cv2.rectangle(orig_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 255, 0), 4)

            cv2.putText(orig_image, label,
                    (int(box[0])+20, int(box[1])+40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,  # font scale
                    (255, 0, 255),
                    2)  # line type
            
    out.write(orig_image)
    cv2.imshow('annotated', orig_image)
    #out.write(orig_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

