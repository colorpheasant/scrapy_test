#自定义文件存储类
from  django.core.files.storage import Storage
from django.conf import settings
from  fdfs_client.client import Fdfs_client
import os
#Django默认保存文件时，会调用Storage类中的save方法
#_save()方法的返回只会保存在表的image字段中
class FDFSStorage(Storage):
    def __init__(self,client_conf=None,nginx_url=None):
        if client_conf is None:
                client_conf=settings.FDFS_CLIENT_CONF
        self.clinet_conf=client_conf
        if nginx_url is None:
                nginx_url =settings.FDFS_NGINX_URL
        self.nginx_url=nginx_url
    def _save(self,name,content):
        """保持文件使用"""
        #name:上传文件的名称 a.txt
        # content:File类的对象，包含了上传文件的内容
        #保存文件到Fdfs文件存储系统
        # client=Fdfs_client(os.path.join(settings.BASE_DIR,'utils/fdfs/client.conf'))
        client=Fdfs_client(self.clinet_conf)
        #获取上传文件的内容
        file_content=content.read()
        #上传文件
        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,文件的id
        #     'Status': 'Upload successed.',#上传是否成功
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # } if success else None
        response=client.upload_by_buffer(file_content)
        if response is None or response.get('Status') !='Upload successed.':
            raise Exception('上传文件到 fast dfs系统失败')
        file_id=response.get('Remote file_id')
        return file_id
    def exists(self, name):
        """判断文件是否存在"""
        return False
    def url(self, name):
        """返回可访问到文件的url地址"""
        # return 'http://192.168.206.145:8888/'+name
        return self.nginx_url+name