# coding=utf-8
import os
import pathlib
from urllib.request import urlretrieve

import math

from com_zxl_spider_db.StarDB import StarDB
from frsclient import AuthInfo, FrsClient, FaceSetService


def urllib_download(name, img_url):

    dir_path = './image'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    img_path = './image/%s.png' % name
    file_exist = os.path.exists(img_path)
    print('urllib_download', img_path, file_exist)
    if file_exist:
        os.remove(img_path)

    pathlib.Path(img_path).touch()
    urlretrieve(img_url, img_path)

    return img_path


if __name__ == "__main__":
    ak = "FIC1EXY74NXMOELTXLZC"
    sk = "1xEplN2aedTj7uhPRbZTxgF09Wt1jU0H3c17Ci7i"
    project_id = "05819bf0a6800f662ff8c0169b5c9fbc"
    end_point = "https://face.cn-north-1.myhuaweicloud.com"
    proxy = {"http": "http://127.0.0.1:1234", "https": "http://127.0.0.1:1234"}

    auth_info = AuthInfo(ak=ak, sk=sk, end_point=end_point)
    frs_client = FrsClient(auth_info=auth_info, project_id=project_id)

    face_set_service = frs_client.get_face_set_service()
    # result = face_set_service.delete_face_set('zxl_test_1')
    # print("delete_face_set result::", result.get_eval_result())

    # result = face_set_service.create_face_set('zxl_test_1')
    # print("create_face_set result::", result.get_eval_result())

    result = face_set_service.get_face_set('zxl_test_1')
    print("get_face_set result::", result.get_eval_result())

    face_service = frs_client.get_face_service()
    starDB = StarDB()
    star_info_all_count = starDB.query_all_star_info_count()
    star_info_all_count = int(star_info_all_count[0])
    print("star_info_all_count::", star_info_all_count)
    star_info_all_count = 30
    page_size = 10
    for page in range(math.ceil(star_info_all_count / page_size)):
        print("page::", page)
        star_info_list = starDB.query_all_star_info((page * page_size), page_size)
        print("star_info_list len::", len(star_info_list))
        for star_info in star_info_list:
            print(star_info)

            img_path = urllib_download(star_info['star_name'], star_info['star_img_url'])

            result = face_service.add_face_by_file('zxl_test_1', img_path)
            result = result.get_eval_result()
            print("add_face_by_file result::", result)

            result_face = result['faces']
            if len(result_face) > 0:
                face_id = result_face[0]['face_id']
                print('face_id::', face_id)
                star_info['face_id'] = face_id
                starDB.update_star_face_id(star_info)

            os.remove(img_path)

    starDB.close_db()

    # #./image/迪丽热巴.png  'face_id': 'Jc7B1XkP'  'face_id': 'FgjX0i3G'
    # face_search_service = frs_client.get_search_service()
    # result = face_search_service.search_face_by_file('zxl_test_1', './image/dlrb.jpg')
    # print("search_face_by_file result::", result.get_eval_result())

    #{'face_set_name': 'zxl_test_1', 'face_set_id': 'M4zBzrhC', 'faces': [{'bounding_box': {'top_left_x': 26, 'width': 132, 'height': 132, 'top_left_y': 44}, 'external_image_id': 'weNMhur7', 'face_id': 'OkbcF0Mu', 'external_fields': {}}]}
    #{'face_set_name': 'zxl_test_1', 'face_set_id': 'M4zBzrhC', 'faces': [{'face_id': 'kXSZMXFh', 'external_image_id': 'FogiC7bb', 'external_fields': {}, 'bounding_box': {'top_left_x': 26, 'height': 132, 'width': 132, 'top_left_y': 44}}]}

