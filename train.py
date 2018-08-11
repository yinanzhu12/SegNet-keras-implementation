import argparse
from keras.utils import multi_gpu_model
from keras.models import Model
from keras.layers import Activation,Input
from custom_layers import MaxPoolingWithIndices,UpSamplingWithIndices,CompositeConv
import config as cf
from util import read_image_batch
from create_model import create_model

def main(args):
    my_model=create_model()
    my_model.compile(cf.optimizer,loss=cf.loss_function,metrics=cf.metrics)
    
    if args.resume:
        my_model.load_weights(cf.model_path+args.load_model_name)
    
    val_data=read_image_batch(cf.test_set_path,cf.batch_size)
    train_data=read_image_batch(cf.training_set_path,cf.batch_size)
    my_model.fit_generator(train_data,
                           steps_per_epoch=(cf.training_set_size+1)//cf.batch_size,
                           epochs=cf.epochs,validation_data=val_data,
                           validation_steps=(cf.test_set_size+1)//cf.batch_size)
    my_model.save_weights(cf.model_path+args.save_model_name)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save",default='my_model')
    parser.add_argument("--resume",action='store_true')
    parser.add_argument("--load",default='my_model')
    args = parser.parse_args()
    main(args)