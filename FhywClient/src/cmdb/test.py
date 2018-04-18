# _*_ coding:utf-8 _*_
__author__ = "lixiang"
import re
str1="Vendor: 1401-02  Model: 80H10931304A0    Rev: 1404"

sp=str1.split("Model:")
print(sp[0].split(":")[1])
print(sp[1].split("Rev:")[0])