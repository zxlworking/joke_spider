# /usr/bin/python
# coding=utf-8


class StarInfoBean:

    def create_star_info_bean(self,
                         star_id,
                         star_name,
                         star_img_url,
                         star_detail_url,
                         face_id):
        bean = {'id': star_id,
                'star_name': star_name,
                'star_img_url': star_img_url,
                'star_detail_url': star_detail_url,
                'face_id': face_id}
        return bean