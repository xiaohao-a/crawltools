import requests
import cchardet
import traceback

def downloader(url,headers=None,timeout=10,debug=False,binary=False):
    """
    主要封装requests的响应内容的编码判断
    :param url:抓取的网页
    :param headers:默认为IE9的User-Agent
    :param timeout:默认超时10秒
    :param debug:若请求出错返回详细信息，默认为False
    :param binary:true返回字节串数据
    :return:响应状态，网页内容，从定向地址
    """
    _headers = {
        'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)'
    }
    if headers:
        _headers = headers
    try:
        response = requests.get(url,headers=_headers,timeout=timeout)
        if binary:
            html = response.content
        else:
            # detect的输出：{'encoding': 'UTF-8', 'confidence': 0.9381250143051147}
            encoding = cchardet.detect(response.content)['encoding']
            html = response.content.decode(encoding)
        status = response.status_code
        # 若网址被重定向
        redirected_url = response.url
    except:
        if debug:
            traceback.print_exc()
        print('get error with %s' % url)
        if binary:
            html = b''
        else:
            html = ''
        status = 0
        redirected_url = url
    return status,html,redirected_url


if __name__ == '__main__':
    url = 'https://news.sina.com.cn/'
    status,html,redi_url = downloader(url,debug=True)
    print(status,len(html),redi_url,)