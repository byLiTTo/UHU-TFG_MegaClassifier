#!/bin/bash

export PYTHONPATH=$PYTHONPATH:`pwd`/../tfmodels/research:`pwd`/../tfmodels/research/slim:`pwd`/../tfrecords:`pwd`/../detection_eval

EXPERIMENT=train_on_ss_inat_and_inat_night_balanced

DETECTION_TFRECORD_FILE=/ai4efs/models/object_detection/faster_rcnn_inception_resnet_v2_atrous/$EXPERIMENT/predictions/eccv_train_detections.tfrecord-00000-of-00001 

DETECTION_DICT_FILE=/ai4efs/models/object_detection/faster_rcnn_inception_resnet_v2_atrous/$EXPERIMENT/predictions/eccv_train.p

TF_RECORD_FILES=$(ls -1 /ai4efs/tfrecords/caltechcameratraps/oneclass/eccv_18/train* | tr '\n' ',')

python ../tfmodels/research/object_detection/inference/infer_detections.py --input_tfrecord_paths=$TF_RECORD_FILES --output_tfrecord_path=$DETECTION_TFRECORD_FILE --inference_graph=/ai4efs/models/object_detection/faster_rcnn_inception_resnet_v2_atrous/$EXPERIMENT/frozen_inference_graph.pb --discard_image_pixels

python ../tfrecords/read_from_tfrecords.py --input_tfrecord_file $DETECTION_TFRECORD_FILE --output_file $DETECTION_DICT_FILE 


