#  coding=utf-8
import re
import urllib
import json
import types
import os


def gethtml(url):   # 获取网页内容
    page = urllib.urlopen(url)
    # print page.getcode()
    html = page.read()
    html = html[22:(len(html) - 1)]   # 将获取的内容截取为json格式
    return html


def geturl(urllist):
    global videocounts,photocounts,outside,errows,videos,photos
    # print type(urllist['video-player'])
    if urllist['type'] == 'video': # 判断格式是否为视频
        if type(urllist['video-player']) is not types.BooleanType: # 判断是否为无效视频
           if  (urllist['video-player'].count("video/mp4") > 0) : # 判断是否为tumblr本地资源
                videourl = re.findall(re.compile(r'<source src="(.+?)" type="'), urllist['video-player'])[0]  # 获取视频地址
                # videourl = urllist['video-player']
                # print  videourl,"\r", # 输出视频地址
                videolist.append(videourl+"\n")
                videocounts=videocounts+1
        else:
            outside = outside + 1
    elif urllist['type'] == 'photo': # 判断格式为照片
        if len(urllist['photos']) == 0: # 判断是否为单张照片
            photourl = urllist['photo-url-1280'] # 获取最高分辨率照片
            # print  photourl,"\r", # 输出照片地址
            photolist.append(photourl+"\n")
            photocounts = photocounts+1
        else:
            for ss in urllist['photos']: # 获取多张照片地址
                # print  ss['photo-url-1280'],"\r", # 输出照片地址
                photourl = ss['photo-url-1280']
                photolist.append(photourl+"\n")
                photocounts = photocounts+1
    # else:
        # print "no media,post type: "+urllist['type']



videocounts = 0
photocounts = 0
outside = 0
errows = 0
videolist = [""]
photolist = [""]

website = raw_input("please input tumblr user:") # 输入tumblr用户名
postsfrom ="http://"+str(website)+".tumblr.com" # 匹配为完整域名
print postsfrom
html = gethtml(postsfrom+"/api/read/json?start=0&num=0") # 获取该用户的总帖子数

#  decode = html
try:
    decode = json.loads(html)
except:
    # print "decode json err!"
    errows = errows + 1
#  print type(decode)
#  print json.dumps(decode,sort_keys=True,indent = 4)
#  print decode['posts'][0]['video-player']
#  videourl = re.findall(re.compile(r'<source src="(.+?)" type="'),decode['posts'][0]['video-player'])[0]

#  print videourl
else:
    print "total posts:", decode['posts-total']
    total = decode['posts-total']
    for counts in range(0,total+40,40):  #  每次获取40个帖子的内容
        urls = gethtml(postsfrom+"/api/read/json?start="+str(counts)+"num=40")  #  获取网页内容
        try:
            decodeurl = json.loads(urls)  # 转码为json
        except:
            errows = errows + 1
            # print "json decode err!:",counts
        else:
            ss=0
            for x in decodeurl['posts']: # 获取帖子对应的内容
                print counts+ss,"/",total,"\r",
                ss = ss + 1
                geturl(x)

# for x in decode['posts']:
    #  print "posttype:",x['type']
#     geturl(x)

print "all have "+str(photocounts)+" photos and "+str(videocounts)+" videos and "+str(outside)+ " outside medias ",errows,"errors" # 输入各种媒体文件的数量

foutput = open(website+"_v.txt","w")
foutput.writelines(videolist)
foutput.close
foutput = open(website+"_p.txt","w")
foutput.writelines(photolist)
foutput.close
print "done! check",website+"_p.txt  for all photos and",website+"_v.txt for all videos."
os.system("pause")