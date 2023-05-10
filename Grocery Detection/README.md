Test : python run_live_demo.py mb1-ssd  models/mb1-ssd-v1.pth models/labels.txt


Train : python train_ssd.py --dataset-type=voc --data=data/version1/ --num-epochs=25 --pretrained-ssd=models/mb1-ssd-Epoch-12-Loss-2.060021884739399.pth --workers=0 --validation-epochs=1