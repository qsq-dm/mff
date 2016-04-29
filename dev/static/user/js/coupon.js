//未使用
var has_more1;
var offset1=undefined;
var has_more2;
var offset2=undefined;
var has_more3;
var offset3=undefined;
function donCoupon(){
	if(offset1){
		var Url="http://"+getHostName()+"/user/my_coupons/?cat=1"+token+"&offset="+offset1
	}else{
		var Url="http://"+getHostName()+"/user/my_coupons/?cat=1"+token;
	}
	$.ajax({
		xhrFields: {withCredentials: true},
		type:"post",
		url:Url,
		dataType:'json',
		success:function(data){
			var span='';
			var infos=data.infos;
			if(infos.length==0){
				if(!offset1){
					$('#item1mobile .noCoupon').show();	
				}
		
			}
			has_more1=data.has_more;
			offset1=data.offset;
			for(var i=0;i<infos.length;i++){
				var scope=infos[i].cat_str;			
				if(infos[i].is_trial==1){
					span="<span>全免</span>"
				}else{					
					span="<span>￥"+infos[i].price+"</span>"
				}	
				str=$('<div class="coupon-cont"><div class="fl yellow">'+span+'</div><div class="fr"><ul><li><h4>'+infos[i].title+'</h4></li><li><span class="color-grey">使用范围:</span><span class="color-black">'+scope+'</span></li><li><span class="color-grey">有效期:</span><span class="color-black">'+infos[i].remain_str+'</span></li></ul></div></div>');
				if (i>0) {
					str.addClass('has-m-top');
				};
				$('#item1mobile').append(str);
			}
		},error:function(){
			alert('网络开小差了');
		}
	});
}

//已经使用
function useCoupon(){
	if(offset2){
		var Url="http://"+getHostName()+"/user/my_coupons/?cat=2"+token+"&offset="+offset2
	}else{
		var Url="http://"+getHostName()+"/user/my_coupons/?cat=2"+token;
	}
	$.ajax({
		xhrFields: {withCredentials: true},
		type:"post",
		url:Url,
		dataType:'json',
		success:function(data){
			var span='';
			var infos=data.infos;
			if(infos.length==0){
				if(!offset2){
					$('#item2mobile .noCoupon').show();	
				}
		
			}
			has_more2=data.has_more;
			offset2=data.offset;		
			for(var i=0;i<infos.length;i++){
				var scope=infos[i].cat_str;
				if(infos[i].is_trial==0){
					span="<span>全免</span>"
				}else{					
					span="<span>￥"+infos[i].price+"</span>"
				}
				str=$('<div class="coupon-cont"><div class="fl blue">'+span+'</div><div class="fr used"><ul><li><h4>'+infos[i].title+'</h4></li><li><span class="color-grey">使用范围:</span><span class="color-black">'+scope+'</span></li><li><span class="color-grey">有效期:</span><span class="color-black">'+infos[i].remain_str+'</span></li></ul></div></div>');
				if (i>0) {
					str.addClass('has-m-top');
				};
				$('#item2mobile').append(str);
			}
		},error:function(){
			alert('网络开小差了');
		}
	});
}

//已经过期
function overdueCoupon(){
	if(offset3){
		var Url="http://"+getHostName()+"/user/my_coupons/?cat=3"+token+"&offset="+offset3
	}else{
		var Url="http://"+getHostName()+"/user/my_coupons/?cat=3"+token;
	}
	$.ajax({
		xhrFields: {withCredentials: true},
		type:"post",
		url:"http://"+getHostName()+"/user/my_coupons/?cat=3"+token,
		dataType:'json',
		success:function(data){	
			var span='';
			var infos=data.infos;
			if(infos.length==0){
				if(!offset3){
					$('#item3mobile .noCoupon').show();	
				}
		
			}
			has_more3=data.has_more;
			offset3=data.offset;	
			for(var i=0;i<infos.length;i++){
				var scope=infos[i].cat_str;			
				if(infos[i].is_trial==0){
					span="<span>全免</span>"
				}else{					
					span="<span>￥"+infos[i].price+"</span>"
				}
				str=$('<div class="coupon-cont"><div class="fl grey">'+span+'</div><div class="fr pased"><ul><li><h4>'+infos[i].title+'</h4></li><li><span class="color-grey">使用范围:</span><span class="color-black">'+scope+'</span></li><li><span class="color-grey">有效期:</span><span class="color-black">'+infos[i].remain_str+'</span></li></ul></div></div>');
				if (i>0) {
					str.addClass('has-m-top');
				};
				$('#item3mobile').append(str);
			}
		},error:function(){
			alert('网络开小差了');
		}
	});
}


donCoupon()
useCoupon()
overdueCoupon()

			//获取滚动条当前的位置 
			function getScrollTop() { 
				var scrollTop = 0; 
				if (document.documentElement && document.documentElement.scrollTop) { 
					scrollTop = document.documentElement.scrollTop; 
				} 
				else if (document.body) { 
					scrollTop = document.body.scrollTop; 
				} 
				return scrollTop; 
			} 
			
	//获取当前可是范围的高度 
	function getClientHeight() { 
		var clientHeight = 0; 
		if (document.body.clientHeight && document.documentElement.clientHeight) { 
			clientHeight = Math.min(document.body.clientHeight, document.documentElement.clientHeight); 
		} 
		else { 
			clientHeight = Math.max(document.body.clientHeight, document.documentElement.clientHeight); 
		} 
		return clientHeight; 
	} 
	
	//获取文档完整的高度 
	function getScrollHeight() { 
		return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight); 
	};

	window.onscroll = function () { 
		if (getScrollTop() + getClientHeight() == getScrollHeight()) { 
			if (has_more1) {
				donCoupon()
			};
			if (has_more2) {
				useCoupon()
			};
			if (has_more3) {
				overdueCoupon()
			};
		} 
	} 
	//新增转增优惠券功能
			$('#segmentedControl .mui-control-item').on('tap',function(){
				var index=$(this).index();
				var $mui_bar=$('nav.mui-bar');
				if(index!=0){
					$mui_bar.hide();
					$('.mui-content').css("padding-bottom","0px")
				}else{
					$mui_bar.show();
					$('.mui-content').css("padding-bottom","50px")
				}
			})
