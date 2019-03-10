# coding:utf-8
from django.shortcuts import render
from dss.Serializer import serializer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tempinfo
from django.views.generic import ListView
from dss.Mixin import MultipleJsonResponseMixin
from PIL import Image, ImageDraw, ImageFont
from small1.settings import BASE_DIR
import datetime
import os
import re
from django.core.paginator import Paginator


# 获取模板列表
class GetTempList(MultipleJsonResponseMixin, ListView):
    model = Tempinfo
    queryset = Tempinfo.objects.all()
    paginate_by = 4


def show_photo(request, url):
    route = BASE_DIR + '\work\\'
    route = route + url + '.jpg'
    with open(route, 'rb') as f:
        img_data = f.read()
    return HttpResponse(img_data, content_type='image/jpg')


def show_create_photo(request, url):
    route = BASE_DIR + '\work\\'
    route = route + url
    with open(route, 'rb') as f:
        img_data = f.read()
    return HttpResponse(img_data, content_type='image/jpg')


# 模板列表视图
def get_templist(request):
    result = Tempinfo.objects.values()
    paginator = Paginator(result, 4)
    page_ = request.GET.get('page')
    if page_:
        page = paginator.page(int(page_))
        next_ = int(page_) + 1
        total = len(result)
        num = total % 4
        if num < next_ - 1:
            next_ = ''
    else:
        page = ''
        next_ = ''
    return JsonResponse({'tempinfo_list': list(page), 'next': next_})


# 模板详情视图
@csrf_exempt
def get_temp_deatil(request):
    if request.method == "POST":
        id = int(request.POST.get("tid", ""))
        if id is not '':
            try:
                detail = Tempinfo.objects.filter(id=id).values('img', 'hint')
                # detail = serializer(detail, datetime_format='string')
                data = list(detail)[0]
                data.update({'id': id})
                return JsonResponse({'success': True, 'data': data})
            except Exception as e:
                return JsonResponse({'success': False, 'data': str(e)})
        else:
            return JsonResponse({'success': False, 'data': '没有数据'})


# 照片生成视图
@csrf_exempt
def generate_photo(request):
    if request.method == 'POST':
        id = request.POST.get('tid', '')
        content = request.POST.get('content', '')
        if id != '' and content != '':
            try:
                temp = Tempinfo.objects.get(id=id)
                fontpath = r"C:\Windows\Fonts\STHUPO.TTF"
                ttfont = ImageFont.truetype(fontpath, int(temp.fontsize))
                # 图片大小
                imgsize = temp.imgsize
                imgsize_list = re.findall(r'\d+', imgsize)
                try:
                    bg = Image.new('RGB', (int(imgsize_list[0]), int(imgsize_list[1])))
                except Exception as e:
                    return JsonResponse({'success': False, 'data': '图片大小出错:' + str(e)})
                im = Image.open(temp.img)
                draw2 = Image.blend(bg, im, 1.0)
                draw = ImageDraw.Draw(draw2)
                try:
                    textplace = temp.textplace
                    textplace_list = re.findall(r'\d+', textplace)
                    textcolor = temp.textcolor
                    textcolor_list = re.findall(r'\d+', textcolor)
                    draw.text((int(textplace_list[0]), int(textplace_list[1])), content, fill=(int(textcolor_list[0]), int(textcolor_list[1]), int(textcolor_list[2])), font=ttfont)
                except Exception as e:
                    return JsonResponse({'success': False, 'data': '文字颜色位置出错：' + str(e)})
                if temp.text2 != None:
                    text2place = temp.text2place
                    draw.text((int(text2place[0]), int(text2place[1])),
                              datetime.date.strftime(datetime.date.today(), "%Y-%m-%d"),
                              fill=(int(textcolor[0]), int(textcolor[1]), int(textcolor[2])),
                              font=ttfont)
                filename = str(datetime.datetime.today()).replace(':', '-').replace(' ', '-').replace('.', '')
                photoname = os.path.join(BASE_DIR, 'work/photo/{0}.jpg'.format(filename))
                draw2.save(photoname)
                return JsonResponse({'success': True, 'data': 'work/photo/{0}.jpg'.format(filename)})
            except Exception as e:
                return JsonResponse({'success': False, 'data': str(e)})
    else:
        return JsonResponse({'success': False, 'data': '不能为空'})
