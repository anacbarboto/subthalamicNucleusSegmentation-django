import os 
import subprocess
import ants
import numpy as np 
import SimpleITK as sitk
import nibabel as nib

from keras.models import load_model
from PIL import Image


#Constantes
folderT1_path = 'public/media/uploads/images/1/'
folderT2_path = 'public/media/uploads/images/2/'
segmentations_path = 'public/media/segmentations/result-'
normalize_path = 'public/media/normalizeImage/normalize-'
numpy_path = 'public/media/numpyImage/'
template = 'public/media/uploads/templates/MNI152_T1_1mm_brain.nii.gz'
modelNA = 'public/media/uploads/models/model_unet1_iteracion2.h5'
modelt = load_model(modelNA)
rows_standard = 240
cols_standard = 240
num_labels = 5

def convertirNiiGz(rmiT1):
    ruta_img = folderT1_path+rmiT1
    ruta_img_destino = folderT1_path+rmiT1+'.gz'
    img = nib.load(ruta_img)
    nib.save(img, ruta_img_destino)

#Funciones
def normalizeImage(rmiT1, rmiT2):
    moving_T1 = ants.image_read(folderT1_path+rmiT1)
    moving_T2 = ants.image_read(folderT2_path+rmiT2)
    fixed = ants.image_read(template)

    img_resample = ants.resample_image(moving_T2,(0.8,0.8,0.8))
    img_denoise = ants.denoise_image(img_resample, noise_model = "gaussian")
    img_with_bias = ants.n4_bias_field_correction(img_denoise)
    mytx1 = ants.registration(fixed=fixed , moving=moving_T1, type_of_transform='ElasticSyn')
    mywarpedimaget1 = ants.apply_transforms(fixed=fixed, moving=img_with_bias, transformlist = mytx1['fwdtransforms'])
    mytx2 = ants.registration(fixed=fixed , moving=moving_T2, type_of_transform='ElasticSyn')
    mywarpedimaget2 = ants.apply_transforms(fixed=fixed, moving=img_with_bias, transformlist = mytx2['fwdtransforms'])
    ants.image_write(mywarpedimaget2, normalize_path+rmiT2)
    ants.image_write(mywarpedimaget1, normalize_path+rmiT1)

    return normalize_path+rmiT1


def general_preprocessing(image):
    num_selected_slice = np.shape(image)[0]
    image_rows_Dataset = np.shape(image)[1]
    image_cols_Dataset = np.shape(image)[2]
    image = np.float32(image)

    if image_rows_Dataset >= rows_standard and image_cols_Dataset >= cols_standard:
        image = image[..., :rows_standard, :cols_standard]

    elif image_rows_Dataset >= rows_standard and image_cols_Dataset < cols_standard:
        result = np.zeros((num_selected_slice, rows_standard, cols_standard), dtype=np.float32)

        image = image[...,:rows_standard,:]
        result[:image.shape[0], :image.shape[1], :image.shape[2]] = image
        image = result
    
    elif image_rows_Dataset < rows_standard and image_cols_Dataset >= cols_standard:
        result = np.zeros((num_selected_slice, rows_standard, cols_standard), dtype=np.float32)
        result[:image.shape[0], :image.shape[1], :image.shape[2]] = image
        image = result

    elif image_rows_Dataset < rows_standard and image_cols_Dataset < cols_standard:
        result = np.zeros((num_selected_slice, rows_standard, cols_standard), dtype=np.float32)
        result[:image.shape[0], :image.shape[1], :image.shape[2]] = image
        image = result
     
    return image


def read_img_sitk(img):
    inputImage = sitk.ReadImage(img)
    inputImage = sitk.Cast(inputImage, sitk.sitkFloat32)
    image = sitk.GetArrayFromImage(inputImage).astype(int) 
    return image

def getNumpyImage(img_path):
    img = os.path.join(img_path) 
    np_img = read_img_into_numpy(img)
    np_img = np.stack((np_img,)*5, axis=-1)
    nimg = os.path.join(numpy_path,  os.path.basename(img_path[:-7])+'.npy')
    np.save(nimg, np_img)
    return nimg

#Obtiene la matriz de la imagen normalizada
def read_img_into_numpy(img_path):
    np_image=np.zeros((182, 240, 240), dtype=np.int)
    
    if (not os.path.isfile(img_path)):
        print(img_path,' ruta no encontrada')
        return None
    
    np_image = read_img_sitk(img_path).astype(int)
    np_image = general_preprocessing(np_image)

    return np_image


def normalize_3D_image(img):
    for z in range(img.shape[0]):
        for k in range(5):
            if (img[z,:,:,k].max()>0):
                img[z,:,:,k] /= img[z,:,:,k].max()
    return img


def predict_3D_img_prob(np_file):
    np_img = np.load(np_file)
    for_pred_img = np.zeros((182, 240, 240, 5), np.float32)
    for_pred_img = normalize_3D_image(np_img)
    mdl_pred_img =  modelt.predict(for_pred_img)
    return mdl_pred_img

def prediction_from_probabily_3D(img): 
    int_image = get_pred(img)
    resultado = lbl_from_cat(int_image)
    return resultado

def get_pred(img, threshold=0.5):
    out_img=img.copy()
    out_img=np.where(out_img>threshold, 1,0)
    return out_img

def lbl_from_cat(cat_lbl):
    
    lbl=0
    if (len(cat_lbl.shape)==3):
        for i in range(1,5):
            lbl = lbl + cat_lbl[:,:,i]*i
    elif (len(cat_lbl.shape)==4):
        for i in range(1,5):
            lbl = lbl + cat_lbl[:,:,:,i]*i
        
    else:
        print('Error in lbl_from_cat', cat_lbl.shape)
        return None
    return lbl


def getSegmentation(rmiT1, rmiT2):
    rmi_path = normalizeImage(rmiT1, rmiT2)
    npImage_path = getNumpyImage(rmi_path)
    pred_stats = predict_3D_img_prob(npImage_path)
    pred = prediction_from_probabily_3D(pred_stats)
    segmentediImage = nib.Nifti1Image(pred, np.eye(4))
    nib.save(segmentediImage, os.path.join('./', segmentations_path+rmiT1))
    
    return segmentations_path+rmiT1

print('path del resultado del modelo:')
print(getSegmentation('IXIHH012.nii.gz', 'IXI012-HH-1211-T2_brain.nii.gz'))
#print(getSegmentationOption2('IXIHH012.nii.gz', 'IXI012-HH-1211-T2_brain.nii.gz'))