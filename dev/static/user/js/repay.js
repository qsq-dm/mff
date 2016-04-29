$('#check_all').attr('checked',false);//初始化全选开关不选折
$('#Nextcheck_all').attr('checked',false);//初始化全选开关不选折

//判断页面是不是从下期账单详情进来的，是的话当前应该显示下期账单；
$('.mui-control-item').on('tap',function(){
	var index=$(this).index();
	sessionStorage.setItem('tap',index);
	$(this).addClass('mui-active').siblings().removeClass('mui-active');
	$('.mui-control-content').eq(index).addClass('mui-active').siblings().removeClass('mui-active');
})
if (sessionStorage.getItem('tap')==1) {
	$('.mui-control-item').eq(1).trigger('tap');
}else if(sessionStorage.getItem('tap')==2){
	$('.mui-control-item').eq(2).trigger('tap');
}


var onOff = true;//本期全选开关
var Onoff = true;//下期全选开关
$("#check_all").on("click",function(){
	if(onOff){
		$(".benqi .unrepay .mycar_input").prop("checked",true);
		onOff=false;
		//本期的金额
		Calculate('.benqi .unrepay .mycar_input','#no-1')
	}else{
		$(".benqi .unrepay .mycar_input").prop("checked",false);
		onOff=true;
		$('#no-1').html('￥0');
	}
});
//下期全选开关
$("#Nextcheck_all").on("click",function(){
	if(Onoff){
		$(".unrepay .mycar_input").prop("checked",true);
		Onoff=false;
		Calculate('.xiaqi .mycar_input','#no-2')
	}else{
		$(".unrepay .mycar_input").prop("checked",false);
		Onoff=true;
		$('#no-2').html('￥0');
	}
});

//本期账单
$.ajax({
	xhrFields: {withCredentials: true},
	type:"post",
	url:"http://"+getHostName()+"/user/my_period_bill/?cat=1"+token,
	dataType:'json',
	success:function(data){
		var infos=data.infos;
		var flage=false;
		$('.billAmount').html(data.total);
		$('.alsoAmount').html(data.remain);
		$('#current-title').html(data.title);
		$('#current-deadline').html(data.deadline);
		if(infos.length==0){
			$('#item1mobile .no-coupon').show()
			$('#item1mobile .repay-top').hide()
			$('#item1mobile .mui-table-view').hide()
			$('#item1mobile .check-all-cont').hide()
		}else{
			$('#item1mobile .repay-top').show()
			$('#item1mobile .mui-table-view').show()
			$('#item1mobile .check-all-cont').show()
		}
		for(var i=0;i<infos.length;i++){
			var  totalAmount=(infos[i].amount+infos[i].punish+infos[i].fee).toFixed(2);
			var  totalAmount_val=(infos[i].amount+infos[i].punish+infos[i].fee).toFixed(2);
			var repayed_str = '未还';
			var time=infos[i].create_time.split(' ')[0]
			if(infos[i].status==1) {
				repayed_str = '已还';
				totalAmount_val=0;
			}
			var str=$('<li class="mui-table-view-cell mui-checkbox mui-left"><input name="checkbox" type="checkbox" value='+totalAmount_val+' class="mycar_input"><div class="mui-navigate-right" style="padding-left:10px;"><a class="mui-media-body" href="repay-detail.html?order_id='+infos[i].order.id+'"><span class="color-red">￥'+totalAmount+'</span><span style="color:#FF6565;vertical-align: 1px;font-size:12px;" class="overdue">(逾期'+infos[i].delayed_days+'天，账单金额'+infos[i].amount+'+滞纳金'+infos[i].punish+')</span><h4>'+infos[i].item.title+'</h4><p class="mui-ellipsis"><span>'+time+'（'+infos[i].period_pay_index+'/'+infos[i].period_count+'期）</span><span class="color-black">'+repayed_str+'</span></p></a></div></li>');
			if (!infos[i].delayed) {
				str.find('.overdue').hide()
			};
			if (infos[i].status==1) {
				str.addClass('repayed')
				str.find('input').attr({
					'checked': 'checked',
					'disabled': 'disabled'
				});
			}else{
				str.addClass('unrepay');
				flage=true;
			}
			str.attr({
				'log-id': infos[i].id,
				'log-fee': infos[i].fee,
				'log-amount':infos[i].amount,
				'log-punish':infos[i].punish
			});	

			$('.mui-table-view.benqi').append(str);
		}
		if (!flage) {
			$('#check_all').attr({
				'checked': 'checked',
				'disabled': 'disabled'
			});
		};	
	},error:function(){
		alert('网络已开小差，请稍后再试')
	}
});
//下期账单
$.ajax({
	xhrFields: {withCredentials: true},
	type:"post",
	url:"http://"+getHostName()+"/user/my_period_bill/?cat=2",
	dataType:'json',
	success:function(data){
		var infos=data.infos;
		var flage=false;
		$('.nextAmount').html(data.total);
		$('.nextAlsoAmount').html(data.remain);
		$('#next-title').html(data.title);
		$('#next-deadline').html(data.deadline);
		if(infos.length==0){
			$('#item2mobile .no-coupon').show()
			$('#item2mobile .repay-top').hide()
			$('#item2mobile .mui-table-view').hide()
			$('#item2mobile .check-all-cont').hide()
		}else{
			$('#item2mobile .repay-top').show()
			$('#item2mobile .mui-table-view').show()
			$('#item2mobile .check-all-cont').show()
		}     
		for(var i=0;i<infos.length;i++){
			var  totalAmount=(infos[i].amount+infos[i].punish+infos[i].fee).toFixed(2);
			var  totalAmount_val=(infos[i].amount+infos[i].punish+infos[i].fee).toFixed(2);
			var time=infos[i].create_time.split(' ')[0]
			var repayed_str = '待还'
			if (infos[i].status==1) {
				repayed_str = '已还';
				totalAmount_val=0;
			}

			var str=$('<li class="mui-table-view-cell mui-checkbox mui-left"><input name="checkbox" type="checkbox" value='+totalAmount_val+' class="mycar_input"><div class="mui-navigate-right" style="padding-left:10px;"><a class="mui-media-body" href="repay-detail.html?order_id='+infos[i].order.id+'"><span class="color-red">￥'+totalAmount+'</span><span style="color:#FF6565;vertical-align: 1px;font-size:12px;" class="overdue">(逾期'+infos[i].delayed_days+'天，账单金额'+infos[i].amount+'+滞纳金'+infos[i].punish+')</span><h4>'+infos[i].item.title+'</h4><p class="mui-ellipsis"><span>'+time+'（'+infos[i].period_pay_index+'/'+infos[i].period_count+'期）</span><span class="color-black">'+repayed_str+'</span></p></a></div></li>');
			if (!infos[i].delayed) {
				str.find('.overdue').hide()
			};
			if (infos[i].status==1) {
				str.addClass('repayed')
				str.find('input').attr({
					'checked': 'checked',
					'disabled': 'disabled'
				});
			}else{
				str.addClass('unrepay');
				flage=true;
			}

			str.attr({
				'log-id': infos[i].id,
				'log-fee': infos[i].fee,
				'log-amount':infos[i].amount,
				'log-punish':infos[i].punish
			});	

			$('.mui-table-view.xiaqi').append(str)
		}
		console.log(flage)
		if (!flage) {
			$('#Nextcheck_all').attr({
				'checked': 'checked',
				'disabled': 'disabled'
			});
		};	
	},error:function(){
		alert('网络已开小差，请稍后再试')
	}
});
//历史还款
$.ajax({
	xhrFields: {withCredentials: true},
	type:"post",
	url:"http://"+getHostName()+"/user/my_repayments/?",
	dataType:'json',
	success:function(data){
		var infos=data.infos; 		
		if(infos.length==0){
			$('#item3mobile .no-coupon').show()
			$('#item3mobile .mui-table-view').hide()
		}else{
			$('#item3mobile .mui-table-view').show()
		}
		for(var i=0;i<infos.length;i++){
			var  totalAmount=(infos[i].amount+infos[i].punish+infos[i].fee).toFixed(2);
			var repayment_time=infos[i].create_time.split(' ')[0];
			var totalPrice=(infos[i].amount+infos[i].fee+infos[i].punish).toFixed(2);
			var time=infos[i].create_time.split(' ')[0];
			var str=$('<li class="mui-table-view-cell mui-left"><div class="mui-navigate-right"><a class="mui-media-body" href="repay-detail.html?order_id='+infos[i].order.id+'"><span class="color-red">￥'+totalAmount+'</span><h4>'+infos[i].item.title+'</h4><p class="mui-ellipsis"><span>'+time+'（'+infos[i].period_pay_index+'/'+infos[i].period_count+'期）</span><span class="color-black">已还</span></p></a></div></li>');
			$('#item3mobile ul').append(str);
		}
		
	},error:function(){
		alert('网络已开小差，请稍后再试')
	}
});
//立刻还款
$('#like').on('click',function(){
	var data=[];
	if ($('.benqi .unrepay input:checked').length==0) {
		alert('请选择需要付款的项目');
		return;
	}else{
		alert($('.benqi .unrepay input:checked').length);
		for(var i=0;i<$('.benqi .unrepay input:checked').length;i++){
			var tmp = {};
			tmp['id'] = $('.benqi .unrepay input:checked').eq(i).parent('li').attr('log-id');
			tmp['fee'] = $('.benqi .unrepay input:checked').eq(i).parent('li').attr('log-fee')
			tmp['amount'] = $('.benqi .unrepay input:checked').eq(i).parent('li').attr('log-amount')
			tmp['punish']= $('.benqi .unrepay input:checked').eq(i).parent('li').attr('log-punish')
			data.push(tmp)
		}
	};
	data_str = JSON.stringify(data);
	$.ajax({
		xhrFields: {withCredentials: true},
		url: 'http://'+getHostName()+'/user/repayment/?'+token,
		type: 'post',
		dataType: 'json',
		data:{'data':data_str},
		success:function(data){
			if(data.code==0){
				location.href='http://'+getHostName()+'/user/repayment_pay/?repayment_id='+data.repayment_id;
			}
		},error:function(){

		}
	})

})
//提前还款
$('#tiqian').on('click',function(){
	var data=[];
	var oLength = 0;
	for (var x = 0; x < $('.xiaqi .unrepay input:checked').length; x++) {
		if (!$('.xiaqi input:checked').eq(x).parent('li').hasClass('repayed')) {
			oLength++;
		}
	}
	if (oLength==0) {
		alert('请选择需要付款的项目');
		return;
	}else{
		for(var i=0;i<$('.xiaqi .unrepay input:checked').length;i++){
			if($('.xiaqi input:checked').eq(i).parent('li').hasClass('repayed')){
				continue;
			}else{
				var tmp = {};
				tmp['id'] = $('.xiaqi .unrepay input:checked').eq(i).parent('li').attr('log-id');
				tmp['fee'] = $('.xiaqi .unrepay input:checked').eq(i).parent('li').attr('log-fee')
				tmp['amount'] = $('.xiaqi .unrepay input:checked').eq(i).parent('li').attr('log-amount')
				tmp['punish']= $('.xiaqi .unrepay input:checked').eq(i).parent('li').attr('log-punish')
				data.push(tmp)		
			}
			
		}
	};	
	data_str = JSON.stringify(data);
	$.ajax({
		xhrFields: {withCredentials: true},
		url: 'http://'+getHostName()+'/user/repayment/?'+token,
		type: 'post',
		dataType: 'json',
		data:{'data':data_str},
		success:function(data){
			if(data.code==0){
				location.href='http://'+getHostName()+'/user/repayment_pay/?repayment_id='+data.repayment_id;
			}
		},error:function(){
			alert('网络出现小差，请稍后再试');
		}
	})
})

function Calculate(name,id){
	var num=0;
	for(var i=0;i<$(name).length;i++){
		num+=parseFloat($(name).eq(i).val())					
	}
	num=num.toFixed(2)
	$(id).html('￥'+num);
}
$(document).on('change','.benqi input',function(){

	Calculate('.benqi input:checked','#no-1');
});

$(document).on('change','.xiaqi input',function(){
	Calculate('.xiaqi input:checked','#no-2');
});













