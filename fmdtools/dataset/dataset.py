import xmltodict
import os

def datapreprocessing(data_dir: str = None):
    if data_dir is None:
        raise ValueError('Data directory should not be none')
    
    xml_names = os.listdir(f'{data_dir}/annotations') 
    image_names = os.listdir(f'{data_dir}/images')
    
    return image_names, xml_names

