#-*- coding: utf-8 -*-
'''
Created on 2016年10月23日

@author: 武明辉
'''
from django import template

register=template.Library()


@register.assignment_tag
def pagination(current_page,num_of_display=12,num_of_backpages=5):
    ''' 1.Paginator.Page 实例
        2.paginator 是实例 
    '''
    front_page=num_of_display-num_of_backpages-1
    html=r''
    #当总页数小于等于显示页数时候全部显示
    if current_page.paginator.num_pages<=num_of_display:
        for i in range(1,current_page.paginator.num_pages+1):
            if current_page.number==i:
                print 
                html+='<li class="active"><a href="?page=%s">%s</a></li>'%(i,i)
            else:
                html+='<li><a href="?page=%s">%s</a></li>'%(i,i)
        return html
    else:
        #的一种情况：当页数1到5，没有省略页，切位置内容不变
        if current_page.number<=num_of_display-num_of_backpages:
            for i in range(1,num_of_display+1):
                if current_page.number==i:
                    html+='<li class="active"><a href="?page=%s">%s</a></li>'%(i,i)
                else:
                    html+='<li><a href="?page=%s">%s</a></li>'%(i,i)
            html+='<li class="disables"><a href="#">...</a></li>'
            return html
        elif current_page.number<=current_page.paginator.num_pages-num_of_backpages:
            #当前页大于5但是没有超过最后的5页时候。位置1，2不变，当前页码一直处于5
            html='<li class="disables"><a href="#">...</a></li>'
            for i in range(current_page.number-front_page,current_page.number+num_of_backpages+1):
                if current_page.number==i:
                    html+='<li class="active"><a href="?page=%s">%s</a></li>'%(i,i)
                else:
                    html+='<li><a href="?page=%s">%s</a></li>'%(i,i)
            html+='<li class="disables"><a href="#">...</a></li>'
            return html
        else:
            #当接近末尾时候：
            html='<li class="disables"><a href="#">...</a></li>'
            for i in range(current_page.paginator.num_pages-num_of_backpages-front_page,current_page.paginator.num_pages+1):
                if current_page.number==i:
                    html+='<li class="active"><a href="?page=%s">%s</a></li>'%(i,i)
                else:
                    html+='<li><a href="?page=%s">%s</a></li>'%(i,i)
            return html   
                
            
            
            
            