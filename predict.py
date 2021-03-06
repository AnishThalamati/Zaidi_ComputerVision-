import cv2
from keras.models import load_model
from keras.utils.generic_utils import CustomObjectScope

from models.unets import Unet2D
#from models.separable_unet import Separable_Unet2D
from models.deeplab import Deeplabv3, relu6, BilinearUpsampling, DepthwiseConv2D
from models.FCN import FCN_Vgg16_16s

from utils.learning.metrics import dice_coef
from utils.BilinearUpSampling import BilinearUpSampling2D
from utils.io.data import load_data, save_results, save_rgb_results, save_history, load_test_images, DataGen


# settings
input_dim_x = 224
input_dim_y = 224
color_space = 'rgb'
path = './data/Medetec_foot_ulcer_224/'
weight_file_name = 'training_history.hdf5'
pred_save_path = 'pathsave/'

data_gen = DataGen(path, split_ratio=0.0, x=input_dim_x, y=input_dim_y, color_space=color_space)
x_test, test_label_filenames_list = load_test_images(path)

# ### get unet model
# unet2d = Unet2D(n_filters=64, input_dim_x=input_dim_x, input_dim_y=input_dim_y, num_channels=3)
# model = unet2d.get_unet_model_yuanqing()
# model = load_model('./azh_wound_care_center_diabetic_foot_training_history/' + weight_file_name
#                , custom_objects={'dice_coef': dice_coef})

# ### get separable unet model
# sep_unet = Separable_Unet2D(n_filters=64, input_dim_x=input_dim_x, input_dim_y=input_dim_y, num_channels=3)
# model, model_name = sep_unet.get_sep_unet_v2()
# model = load_model('./azh_wound_care_center_diabetic_foot_training_history/' + weight_file_name
#                , custom_objects={'dice_coef': dice_coef,
#                                  'relu6':relu6,
#                                  'DepthwiseConv2D':DepthwiseConv2D,
#                                  'BilinearUpsampling':BilinearUpsampling})

# ### get VGG16 model
# model, model_name = FCN_Vgg16_16s(input_shape=(input_dim_x, input_dim_y, 3))
# with CustomObjectScope({'BilinearUpSampling2D':BilinearUpSampling2D}):
#     model = load_model('./azh_wound_care_center_diabetic_foot_training_history/' + weight_file_name
#                    , custom_objects={'dice_coef': dice_coef})'

# ### get mobilenetv2 model




#custom_objects= oomps

oomps = {'dice_coef': dice_coef,
                                 'relu6':relu6,
                                 'DepthwiseConv2D':DepthwiseConv2D,
                                 'BilinearUpsampling':BilinearUpsampling}
with CustomObjectScope(oomps):
    model = load_model('./azh_wound_care_center_diabetic_foot_training_history/' + weight_file_name)


model = Deeplabv3(input_shape=(input_dim_x, input_dim_y, 3), classes=1)
for image_batch, label_batch in data_gen.generate_data(batch_size=len(x_test), test=True):
    prediction = model.predict(image_batch, verbose=1)
    save_results(prediction, 'rgb', path + 'test/predictions/' + pred_save_path, test_label_filenames_list)
    break
