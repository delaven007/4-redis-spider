```python
# 一级页面
1、景点基准xpath节点对象:
  //ul[@class="thebox clearfix"]/li
  
标题(title): './/span[@class="main-tit"]/@name'
链接(link):  './div/a/@href'
价格(price): './/div[@class="tnPrice"]/em/text()'
是否为新产品: './/div[@class="new-pro"]'
满意度(satisfaction): './/div[@class="comment-satNum"]//i/text()'
出游人数(travelNum): './/p[@class="person-num"]/i/text()'
满意度(reviewNum): './/p[@class="person-comment"]/i/text()'
景点(recommended): './/span[@class="overview-scenery"]/text()'
供应商(supplier): './/span[@class="brand"]/span/text()'
  
# 二级页面
优惠信息(coupons):'//div[@class="detail-favor-coupon-desc"]/@title'
景点点评(cp_comments):  
```

