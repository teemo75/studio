import uuid

import matplotlib.pyplot as plt
from typing import List, Any, Union

from brightics.common.image import *
import glob
import pandas as pd
import random
import os
import pyarrow as pa
import pyarrow.parquet as pq
import pathlib
import time
import cv2
from brightics.common.datatypes.image import Image


#
# labelling
# dir : (label)/files....
# none : no label
# file_prefix : (label)_files...
#
def image_load(path, labeling='dir', image_col='image', n_sample=None):

    if labeling == 'dir':
        images_file_list = glob.glob('''{}/*/*'''.format(path))
        if n_sample is not None:
            images_file_list = random.sample(images_file_list, n_sample)
        label = [os.path.split(os.path.dirname(os.path.abspath(x)))[1] for x in images_file_list]
    else:
        images_file_list = glob.glob('''{}/*'''.format(path))
        if n_sample is not None:
            images_file_list = random.sample(images_file_list, n_sample)
        label = None

    images = [(cv2.imread(x), x) for x in images_file_list]
    # encoded_images = [img_to_byte(x) for x in images]
    encoded_images = [Image(cv2.imread(x), origin=x).tobytes() for x in images_file_list]
    # encoded_images = [Image(x[0], origin=x[1], mode=None).tobytes() for x in images]

    # sample_idx = random.randint(0, len(images_file_list))
    # print('''image_path : {}'''.format(images_file_list[sample_idx]))
    # print('''encoded_image : {}'''.format(encoded_images[sample_idx]))
    # print('''labeling : {}'''.format(labeling))
    # print('''label : {}'''.format(label[sample_idx]))

    out_df = pd.DataFrame({image_col: encoded_images})
    if label is not None:
        out_df['label'] = label

    return {'out_table': out_df}

# def import_image(in_path, out_path, image_type='npy', labeling='label'):
#     images_file_list = glob.glob('''{}/*/*'''.format(in_path))
#
#     if labeling == 'label':
#         label = [os.path.split(os.path.dirname(os.path.abspath(x)))[1] for x in images_file_list]
#     else:
#         label = list(range(0, images_file_list))
#
#     images = [(plt.imread(x), i) for i, x in enumerate(images_file_list)]
#     # image_files_name = range(0, len(images_file_list))
#
#     if os.path.exists(out_path):
#         os.remove(out_path)
#
#     data_file_path = '{}/data.pq'.format(out_path)
#     image_dir = '{}/images'.format(out_path)
#     pathlib.Path(image_dir).mkdir(parents=True, exist_ok=True)
#
#     tt = 0.0
#
#     if image_type == 'npy':
#         for i, img_path in enumerate(images_file_list):
#             img = plt.imread(img_path)
#             ts = time.perf_counter()
#             image_filename = '{}/{}'.format(image_dir, i)
#             np.save(image_filename, img)
#             tt = tt + (time.perf_counter() - ts)
#
#         print('time for save images : {}'.format(tt))
#         out_table = pd.DataFrame({'images': ['images/{}.{}'.format(x[1], image_type) for x in images], 'label': label})
#         pq.write_table(pa.Table.from_pandas(out_table), data_file_path)
#
#     else:
#         image_list = np.array([plt.imread(x) for x in images_file_list])
#         print('shape : {}'.format(image_list.shape))
#         np.save('{}/images'.format(image_dir), image_list)
#         out_table = pd.DataFrame({'images': range(0, len(images_file_list)), 'label': label})
#         pq.write_table(pa.Table.from_pandas(out_table), data_file_path)
#
#     return {'out_table': out_table}