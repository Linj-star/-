from DrissionPage import ChromiumOptions,ChromiumPage
import requests
"""
    这一段为drissionpage模块必配置的前提步骤，否则运行报错。
    只需运行一次 电脑永久保存此配置
    
# path = r'D:\Chrome\chrome.exe'  # 请改为电脑内Chrome可执行文件路径
# ChromiumOptions().set_browser_path(path).save()

"""

# 自动打开浏览器
dp = ChromiumPage()
# 监听数据包
dp.listen.start('web/aweme/post/')
# 自动打开网站（必须到达该博主的主页界面，网址自定义可改）
dp.get('https://www.douyin.com/user/MS4wLjABAAAAss4X6GmQjQokTWxrssQAlAyr_9UTHegrpa6mBvoLTi72WKAiWsKbnCoaDBLz3DVx?from_tab_name=main&vid=7490562723214920998')
# 自动翻页批量爬取
for item in range(1,21):    # 循环21次 就是看20页 想看多少页可改，页可以while True配合try..excpet异常处理即看全部页数
    print(f'正在爬取第{item}页的数据......') # 格式化字符串 显示看到了第几页
    # 等数据包加载
    s = dp.listen.wait()
    # 获得最终响应数据
    JSON = s.response.body
    # print(JSON)
    # 遍历数据
    video_list = JSON['aweme_list']
    for i in video_list:
        # 异常处理
        try:
            # print(i)
            # 提取视频名称
            name = i['desc'].split('\n')
            # 提取视频链接
            video_url = i['video']['play_addr']['url_list'][0]
            print(name,video_url,'\n')

            url = video_url
            # 请求头（可不写）
            headers = {
                'referer': 'https://www.douyin.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            }

            resp = requests.get(url=url,headers=headers)

            # 保存视频
            with open(f'此博主的所有视频\\{name}.mp4','wb') as file:
                file.write(resp.content)
        except:
            print('数据有误')
            pass
    #  dp模块的自动翻页
    dp.scroll.to_see('css:.ayFW3zux')   # 定位元素到抖音最底部