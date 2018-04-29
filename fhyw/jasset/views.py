from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from utils.pages import page
from jasset import models
from django.db.models import Q
from jasset.api.asset import DealResponseAsset
# Create your views here.

@login_required
def asset_list(request):
    asset_objs = models.Asset.objects.select_related()
    page_objs = page(request, asset_objs)
    return render(request, "jasset/asset_list.html", {"page_objs": page_objs})


@login_required
def host_list(request):
    host_objs = models.Host.objects.select_related()
    page_objs = page(request, host_objs)
    return render(request, "jasset/host_list.html", {"page_objs": page_objs})

@csrf_exempt
def asset_api(request):
    """处理客户端反馈回的数据"""
    deal_asset_obj=DealResponseAsset(request)
    deal_asset_obj.execute()

    return HttpResponse("OK")

@login_required
def asset_info(request,asset_id):

    host_obj=models.Host.objects.filter(asset_id=asset_id).first()
    try:
        record_objs=host_obj.asset.assetrecord.all().order_by("-create_time")
    except:
        record_objs=None

    return render(request,"jasset/asset_info.html",locals())

@login_required
def assetrecord_list(request):
    if request.method=="GET":
        assetrecord_objs=models.AssetRecord.objects.select_related().order_by("create_time")
        page_objs=page(request,assetrecord_objs,page_number=20)
    if request.method=="POST":
        host_ip=request.POST.get("host_ip")
        assetrecord_objs=models.AssetRecord.objects.filter(asset__host__host_ip=host_ip).select_related().order_by("create_time")
        page_objs=page(request,assetrecord_objs,page_number=20)
    return render(request,"jasset/asset_record_list.html",locals())

@login_required
def asseterrorlog_list(request):
    if request.method=="GET":
        asset_error_log_objs=models.ErrorLog.objects.select_related().order_by("create_time")
        page_objs=page(request,asset_error_log_objs,page_number=20)
    if request.method=="POST":
        host_ip=request.POST.get("host_ip")
        asset_error_log_objs=models.ErrorLog.objects.filter(asset__host__host_ip=host_ip).select_related().order_by("create_time")
        page_objs=page(request,asset_error_log_objs,page_number=20)
    return render(request,"jasset/asset_error_log_list.html",locals())