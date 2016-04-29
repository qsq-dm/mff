//判断页面是不是从下期账单详情进来的，是的话当前应该显示下期账单；
$('.mui-control-item').on('tap',function(){
	var index=$(this).index();
	sessionStorage.setItem('tab',index);
	$(this).addClass('mui-active').siblings().removeClass('mui-active');
	$('.mui-control-content').eq(index).addClass('mui-active').siblings().removeClass('mui-active');
})
if (sessionStorage.getItem('tab')==1) {
	$('.mui-control-item').eq(1).trigger('tap');
}else if(sessionStorage.getItem('tab')==2){
	$('.mui-control-item').eq(2).trigger('tap');
}
else if(sessionStorage.getItem('tab')==3){
	$('.mui-control-item').eq(3).trigger('tap');
}
//全部的订单
var has_more1;
var offset1=undefined;
var has_more2;
var offset2=undefined;
var has_more3;
var offset3=undefined;
var has_more4;
var offset4=undefined;
function createNodes(id,cat,oft){
	if(oft){
		var Url="http://"+getHostName()+"/user/my_orders?cat="+cat+"&offset="+oft
	}else{
		var Url="http://"+getHostName()+"/user/my_orders?cat="+cat
	}
	$.ajax({
		xhrFields: {withCredentials: true},
		type:"post",
		url:Url,
		dataType:'json',
		data:{},
		success:function(data){

			var infos=data.infos;
//			$(id).find('ul').remove();
			if(infos.length==0){
				if(cat==0){
					if(!offset1){
						$(id).find('.noJudge').show()
					}
				}else if(cat==1){
					if(!offset2){
						$(id).find('.noJudge').show()
					}
				}else if(cat==2){
					if(!offset3){
						$(id).find('.noJudge').show()
					}
				}else if(cat==3){
					if(!offset4){
						$(id).find('.noJudge').show()
					}
				}				
				
			}
			if(cat==0){
			has_more1=data.has_more;
			offset1=data.offset;
			}else if(cat==1){
			has_more2=data.has_more;
			offset2=data.offset;			
			}else if(cat==2){
			has_more3=data.has_more;
			offset3=data.offset;				
			}else if(cat==3){
			has_more4=data.has_more;
			offset4=data.offset;				
			}
			
			for(var i=0;i<infos.length;i++){
				window.infos=infos;
				var totalPrice=(infos[i].period_amount+infos[i].period_fee).toFixed(2);
				var node='';
				if (infos[i].status==0 || infos[i].status==1) {
					var pay_link = '/user/order_pay/?order_id=' + infos[i].id;
					node='<button class="mui-btn mui-btn-outlined mui-btn-negative" onclick="' + "location='" + pay_link + "'" + '" >去支付</button>'
				}else if (infos[i].status==2) {
					node='<a class="mui-btn mui-btn-outlined mui-btn-negative" href="tel:'+infos[i].hospital.phone+'">预约</a>';
				}
				else if (infos[i].status==3) {
					node='<button class="mui-btn mui-btn-outlined mui-btn-negative" style="display:none;">支付异常</button>'
				}
				else if (infos[i].status==5) {
					node='<a class="mui-btn mui-btn-outlined mui-btn-negative" href="judge-edit.html?order_id='+infos[i].id+'">追加评价</a>'
				}
				else if (infos[i].status==6) {
					node='<a class="mui-btn mui-btn-outlined mui-btn-negative" href="judge-edit.html?order_id='+infos[i].id+'">去评价</a>'
				}

				else if (infos[i].status==7) {
					node='<a class="mui-btn mui-btn-outlined mui-btn-negative" href="detail.html?item_id='+infos[i].item.id+'">重新购买</a>'
				}else if (infos[i].status==8) {
					node='<a class="mui-btn mui-btn-outlined mui-btn-negative" href	="/user/menu_credit_apply/">查看进度</a>'
				}
				else if (infos[i].status==9) {
					node='<button class="mui-btn mui-btn-outlined mui-btn-negative done" data='+infos[i].id+'>已完成</button>'
				}else if(infos[i].status==10){
					node='<a class="mui-btn mui-btn-outlined mui-btn-negative" href="detail.html?item_id='+infos[i].item.id+'">重新购买</a>';
				}else if(infos[i].status==11){
					node='<a class="mui-btn mui-btn-outlined mui-btn-negative" href="/user/menu_credit_apply/">查看</a>';
				}
				var fenqi='<p class="color-grey">分期:￥'+totalPrice+'(含服务费￥'+infos[i].period_fee+') × '+infos[i].period_count+'</p>';
				var	first='<p class="color-grey">首付:<span class="color-red">￥'+infos[i].price+'</span></p>'
				if (infos[i].credit_choice_id==0) {
					fenqi='<p class="color-grey">直购:￥'+infos[i].total+'</p>';
					first='';
				};
				if (infos[i].price==0) {
					first='';
				};
				var str=$('<ul class="mui-table-view has-m-top"><li class="mui-table-view-cell"><a href=' + "/static/user/order_detail.html?order_id=" + infos[i].id + ' class="mui-navigate-right">'+infos[i].status_label+'</a></li><li class="mui-table-view-cell mui-media"><a href="' + "/static/user/detail.html?item_id=" + infos[i].item.id+ '"><img class="mui-media-object mui-pull-left" src="' + infos[i].item.image + '"><div class="mui-media-body"><h4>'+infos[i].item.title+'</h4><p class="mui-ellipsis"><span>'+infos[i].hospital.name+'</span></p><p class="mui-ellipsis">售价：<span>￥'+infos[i].total+'</span></p></div></a></li><li class="mui-table-view-cell mui-media">'+first+''+fenqi+''+node+'</li></ul>');


				$(id).append(str)
			}
		},
		error:function(){
			
		}
	});
}

createNodes('#item1mobile','0',offset1);
createNodes('#item2mobile','1',offset2);
createNodes('#item3mobile','2',offset3);
createNodes('#item4mobile','3',offset4);
$(document).on('click','.done',function(){
	var order_id=$(this).attr('data');
	$.ajax({
		xhrFields: {withCredentials: true},
		type:"post",
		url:"http://"+getHostName()+"/user/finish_order/",
		dataType:'json',
		data:{order_id:order_id},
		success:function(data){
			if(data.code==0){
				alert(data.msg);
				window.location=location;
			}else{
				alert(data.msg);
			}
			
		},error:function(){
			
		}
	});	
})

	window.onscroll = function () { 
		if (getScrollTop() + getClientHeight() == getScrollHeight()) { 
			if(offset1){
				createNodes('#item1mobile','0');
			}
			if(offset2){
				createNodes('#item2mobile','1');
			}	
			if(offset3){
				createNodes('#item3mobile','2');
			}	
			if(offset4){
				createNodes('#item4mobile','3');
			}	
	} 
}