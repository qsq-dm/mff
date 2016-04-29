$(function(){
  $.ajax({
    url: "http://"+getHostName()+"/user",
    type: 'post',
    dataType: 'json',
    success:function(data){

     var banner=data.banner;			
     var activity=data.activity;
     var activity_items=data.activity_items;
     var recommend_items=data.recommend_items;
			// alert(recommend_items[0].item.has_fee)
			$('.img').remove();//先删除原先有的banner
      $('.mui-indicator').remove();
      for(var i=0;i<banner.length;i++){
        
        var item=$('<div class="mui-slider-item img"><a href="'+banner[i].link+'"><img src="'+banner[i].image+'"></a></div>');
        var itemList=$('<div class="mui-indicator"></div>');

           	$('#after').after(item);//动态加载banner节点元素
           	$('#append').append(itemList);
           	if (i==0) {
           		itemList.addClass('mui-active');
           	};
           	$('.mui-slider-item-duplicate img').attr('src',banner[0].image);//第一个和最后一个都用第一张图片
           };
           for(var j=0;j<recommend_items.length;j++){           
           	$('.title').eq(j).html(recommend_items[j].item.title);
           	$('h5').eq(j).html(recommend_items[j].desc)
           	$('.orig').eq(j).html('￥'+recommend_items[j].item.period_money);
           	$('.price').eq(j).html('x'+recommend_items[j].item.period_count);
           	$('.big-img').eq(j).attr('src',recommend_items[j].image);
           	var item_id = recommend_items[j].item.id;
           	var click_event = function (item_id) {
              var func =  function () {
                window.location = '/static/user/detail.html?item_id=' + item_id;
              }
              return func
            }(item_id)
            $('.big-img').eq(j).click(click_event)
          };
          for(var k=0;k<activity_items.length;k++){
           $('.list').find('h4').eq(k).html(activity_items[k].item.title);
           $('.list').find('.line-throu').eq(k).html(activity_items[k].item.orig_price);
           $('.list').find('.color-red').eq(k).html(activity_items[k].price);
           var item_id = activity_items[k].item.id;
           var click_event = function (item_id) {
             var func =  function () {
               window.location = '/static/user/detail.html?item_id=' + item_id;
             }
             return func
           }(item_id)
           $('.list').eq(k).click(click_event)
           if(activity_items[k].item.has_fee==false){
            $('.list').find('img').eq(k).css('display','none');
          }
          console.log($('.period').length);
          if (k>0) {
            $('.period').eq(k).html('月供:'+activity_items[k].item.period_money+'x'+activity_items[k].item.period_count)
          }else if(k==0){
            $('#yuegong').find('b').html('￥'+activity_items[k].item.period_money);
            $('#yuegong').find('span').html('x'+activity_items[k].item.period_count);
          }
        };
           //倒计时；
           console.log(activity.end_time);
           var timeList=activity.end_time.split(' ');
           var riqi=timeList[0].split('-');
           console.log(riqi[0])
           var time=riqi[1]+'/'+riqi[2]+'/'+riqi[0]+' '+timeList[1];
           console.log(time);
          //倒计时插件代码
          var end = new Date(time);
          var _second = 1000;
          var _minute = _second * 60;
          var _hour = _minute * 60;
          var _day = _hour * 24;
          var timer;
          function showRemaining() {
            var now = new Date();
            var distance = end - now;
            if (distance < 0) {
              clearInterval(timer);
                      // document.getElementById('countdown').innerHTML = 'EXPIRED!';
                      $('#at').html('活动已经结束');
                      return;
                    }
                    var days = Math.floor(distance / _day);
                    var hours = Math.floor((distance % _day) / _hour);
                    var minutes = Math.floor((distance % _hour) / _minute);
                    var seconds = Math.floor((distance % _minute) / _second);
                    $('#at').html('仅剩'+days + '天'+hours+'时'+minutes+'分'+seconds+'秒')
                    console.log() ;
                  }
                  timer = setInterval(showRemaining, 1000);

                },
                error:function(){
//               alert('网络出现小差，请稍后再试');
               }

             })
});