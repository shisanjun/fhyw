# _*_ coding:utf-8 _*_
__author__ = "lixiang"
import re

def mb2gb(size):
    """MB转GB"""
    try:
        num=re.search(r"\d+",size).group()
        return str(int(num)/1024)
    except:
        return size

