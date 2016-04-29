var w,h;
function getSrceenWH(){
	w = $(window).width();
	h = $("html").height();
	$('#dialogBg').width(w).height(h);
}

window.onresize = function(){  
	getSrceenWH();
}  
$(window).resize();  
$(document).ready(function(){
	getSrceenWH();
//				顶部菜单颜色与图标变换
$(".drop-btn").on("click",function(){
//$(".drop-btn").removeClass("active").find("i").html("&#xe604;");
//$(this).addClass("active").find("i").html("&#xe603;");
	
	if ($(this).hasClass("active") ){
		console.log('deact')
		$('#drop-list1').addClass('is-dis')
		$('#right-side-menu').addClass('is-dis')
		// $('a').css('pointer-events','all')
		// $('.drop-btn').css('pointer-events','all')
		//$('li').unbind('click')
		$('html').css({'overflow':'auto','position':'static'});		
		$(".drop-list").css("top","-264px");
		$(".drop-btn").removeClass("active").find("i").html("&#xe604;");
		$("#dialogBg").fadeOut(300);
	}else{
	    console.log('act')
		$('#drop-list1').removeClass('is-dis')
		$('#right-side-menu').removeClass('is-dis')
		$('html').css({'overflow':'hidden','position':'fixed'});
		$(".drop-btn").removeClass("active").find("i").html("&#xe604;");
		$(this).addClass("active").find("i").html("&#xe603;");
	}
});

//				第一个菜单点击事件				
$("#drop1").on("click",function(){
	if($(this).hasClass('active')){
		$(".drop-list").css("top","-264px");
		$("#drop-list1").css("top","40px");
		$("#dialogBg").fadeIn(300);

	}else{
	 	$(".drop-list").css("top","-264px");
		$("#dialogBg").fadeOut(300);
	}
});




//				第二个菜单点击事件				
$("#drop2").on("click",function(){
	if($(this).hasClass('active')){
		$(".drop-list").css("top","-264px");
		$("#drop-list2").css("top","40px");
		$("#dialogBg").fadeIn(300);

	}else{
	 	$(".drop-list").css("top","-264px");
		$("#dialogBg").fadeOut(300);
	}
});
//				第二个下拉菜单点击事件

//				第三个菜单点击事件				

$("#drop3").on("click",function(){
	if($(this).hasClass('active')){
		$(".drop-list").css("top","-264px");
		$("#drop-list3").css("top","40px");
		$("#dialogBg").fadeIn(300);

	}else{
	 	$(".drop-list").css("top","-264px");
		$("#dialogBg").fadeOut(300);
	}

});
//				第三个下拉菜单点击事件
window.bind_menu_click = function bind_menu_click() {
	//				第一个菜单的左侧子菜单点击事件
	$(".tab-vertical li").on("click",function(){

		$(".tab-vertical li").removeClass("active");
		$(this).addClass("active");
		var cat_id=$(this).attr('cat-id');
		$('.select-operation li').hide();
		$('.select-operation .ding-'+cat_id).show()
		$('#drop-list1').scrollTop(0);
	});
	$("#drop-list3 li").on("click",function(){
		$('html').css({'overflow':'auto','position':'static'});	
		$(".drop-list").css("top","-264px");
		$("#drop3").find("span").html($(this).find("span").html());
		$("#drop-list3 li").removeClass("active").find("i").html("&#xe63e;");
		$(this).addClass("active").find("i").html("&#xe627;");
		//选择背景隐藏
		$("#dialogBg").fadeOut(300);	
			//选择的时候请求接口
		var city=$('#drop-list3 li.active').attr('data-id');
		var sort=$('#drop-list2 li.active').attr('data-id');
		var cat=$('.select-operation li.active').attr('data-id');
		option_sort(sort,cat,city);
		$("#drop3").click();
	});				
//				背景点击事件
	$("#dialogBg").on("click",function(event){
		$(".drop-list").css("top","-264px");
		$(".drop-btn").removeClass("active").find("i").html("&#xe604;");
		$("#dialogBg").fadeOut(300);
		$('html').css({'overflow':'auto','position':'static'});	
	});
	$("#drop-list2 li").on("click",function(){
		$('html').css({'overflow':'auto','position':'static'});	
		$(".drop-list").css("top","-264px");
		$("#drop2").find("span").html($(this).find("span").html());
		$("#drop-list2 li").removeClass("active").find("i").html("&#xe63e;");
		$(this).addClass("active").find("i").html("&#xe627;");
		//选择背景隐藏
		$("#dialogBg").fadeOut(300);
		
			//选择的时候请求接口
		var city=$('#drop-list3 li.active').attr('data-id');
		var sort=$('#drop-list2 li.active').attr('data-id');
		var cat=$('.select-operation li.active').attr('data-id');
		option_sort(sort,cat,city);
		$("#drop2").click();



	});

	//				第一个菜单的右侧子菜单点击事件
	$(".select-operation li").on("click",function(){
		$('#drop-list1').addClass('is-dis')
		$('#right-side-menu').addClass('is-dis')
		$('html').css({'overflow':'auto','position':'static'});	
		$(".select-operation li").removeClass("active").find("i").html("&#xe63e;");
		$(this).addClass("active").find("i").html("&#xe627;");
		$(".drop-list").css("top","-264px");

		//选中的li里面的文字截图出来
		var li_text=$('.select-operation .mui-table-view-cell.active').text();
		var l_length=$('.select-operation .mui-table-view-cell.active').text().length;
		var results=li_text.substring(0,l_length-1);
		console.log(results);

		$('#drop1').find('span').html(results)
		$('#drop1').removeClass('active');
		set_document_title(results);
		//点击背景隐藏
		$("#dialogBg").fadeOut(300);
			//选择的时候请求接口
			var city=$('#drop-list3 li.active').attr('data-id');
			var sort=$('#drop-list2 li.active').attr('data-id');
			var cat=$('.select-operation li.active').attr('data-id');
			option_sort(sort,cat,city);
					//$("#drop1").click();
		$(".drop-btn").removeClass("active").find("i").html("&#xe604;");
	});
}

});



//头部选择接口
function option_sort(sort,cat,city){
			$.ajax({
			type:"get",
			url:"http://"+getHostName()+"/user/item_list/?sort_type="+sort+"&sub_cat_id="+cat+"&city_id="+city,
			dataType:'json',
			success:function(data){
				$('.item-list li').remove();
				$('.tit').hide();
				//没有更多隐藏；
				var infos=data.infos;
						has_more=data.has_more;
						offset=data.offset;
						var infos=data.infos;
						if (!has_more){
							$('.loader-inner').hide();
						};
						if(infos.length==0){
							$('.noCoupon').show();
							$('.mui-card').hide()
						}else{
							$('.mui-card').show();
							$('.noCoupon').hide();
						}
						for(var i=0;i<infos.length;i++){
							var  free='';
							if (!infos[i].has_fee) {
								free='<img src="/static/user/free.png" class="free" alt="" style="position: absolute;width:25px;height:25px;top:0;left:0;" />'
							}
							var str=$('<li class="mui-table-view-cell mui-media no-after-dotted"><a href="/static/user/detail.html?item_id='+infos[i].id+'"><img class="mui-media-object mui-pull-left" src="'+infos[i].image+'"><div class="mui-media-body">'+infos[i].title+'<p class="mui-ellipsis"><span>'+infos[i].hospital.name+'</span></p><p class="mui-ellipsis">售价：<span class="color-red">￥'+infos[i].price+'</span>医院价：<span class="line-throu">￥'+infos[i].orig_price+'</span></p></div><div class="month-pay  month-pay-sm"><div class="tit">月供</div><div class="num"><p class="color-red"><b>￥'+infos[i].period_money+'</b><span>x '+infos[i].period_count+'</span></p></div></div></a>'+free+'</li>');
							if(i==infos.length-1){
								str.removeClass('no-after-dotted');
							}
							$('.item-list').append(str);
						}	
				
			},error:function(){
				
			}
		});
}
//			头部列表加载请求
function get_filters(callback) {
			$.ajax({
				type:"get",
				url:"http://"+getHostName()+"/user/item_filters/"+location.search,
				dataType:"json",
				success:function(data){
					//销量加载
					if(callback) { callback();}
					var order_choices=data.order_choices;
					var citys=data.citys;
					for(var x=0,xlg=order_choices.length;x<xlg;x++){						
						var order_str='';
						if(data.sort_type_obj.id==order_choices[x].id){
						order_str='<li class="mui-table-view-cell active" data-id="'+order_choices[x].id+'"><span>'+order_choices[x].name+'</span><i class="iconfont mui-pull-right">&#xe627;</i></li>'
						}else{
						order_str='<li class="mui-table-view-cell" data-id="'+order_choices[x].id+'"><span>'+order_choices[x].name+'</span><i class="iconfont mui-pull-right">&#xe63e;</i></li>'
						}
						$('#drop-list2').append(order_str);
					}
					//城市
					for(var j=0;j<citys.length;j++){
						var city='';
						if(data.city.id==citys[j].id){
						city='<li class="mui-table-view-cell active" data-id="'+citys[j].id+'"><span>'+citys[j].name+'</span><i class="iconfont mui-pull-right">&#xe627;</i></li>'
						}else{
						city='<li class="mui-table-view-cell" data-id="'+citys[j].id+'"><span>'+citys[j].name+'</span><i class="iconfont mui-pull-right">&#xe63e;</i></li>'
						}
						$('#drop-list3').append(city)
					}															
					// 推荐项目接口
					var bg_list=data.all_sub_cats;
					
//					for(var i=0;i<bg_list.length;i++){
//						for(var x=0;x<bg_list[i].sub_cats.length;x++){
//							var sub=bg_list[i].sub_cats[x]
//							var class_str='';
//							for(var j=0;j<sub.cat_id_list.length;j++){
//								var class_count=sub.cat_id_list[j];
//								class_str+='ding-'+class_count+' '
//							}
//							var node_str='';
//							if(data.subcat.id==sub.id){
//								node_str='<li class="mui-table-view-cell active no-after-dotted ding-'+bg_list[i].id+' '+class_str+'" data-id="'+sub.id+'">'+sub.name+'<i class="iconfont mui-pull-right">&#xe627;</i></li>'
//							}else{
//								node_str='<li class="mui-table-view-cell no-after-dotted ding-'+bg_list[i].id+' '+class_str+'" data-id="'+sub.id+'">'+sub.name+'<i class="iconfont mui-pull-right">&#xe63e;</i></li>'	
//							}
//							$('.select-operation').append(node_str);
//						}						
//					}
					for(var i=0;i<bg_list.length;i++){
						var class_str='';
						for(var k=0;k<bg_list[i].cat_id_list.length;k++){
							var class_count=bg_list[i].cat_id_list[k];
							class_str+='ding-'+class_count+' '
						}
						var node_str='';
					if(data.subcat.id==bg_list[i].id){
					node_str='<li class="mui-table-view-cell active no-after-dotted '+class_str+'" data-id="'+bg_list[i].id+'">'+bg_list[i].name+'<i class="iconfont mui-pull-right">&#xe627;</i></li>'

					}else{
					 node_str='<li class="mui-table-view-cell no-after-dotted '+class_str+'" data-id="'+bg_list[i].id+'">'+bg_list[i].name+'<i class="iconfont mui-pull-right">&#xe63e;</i></li>'
	
					}					
					$('.select-operation').append(node_str);
					};
					
					$('#drop1').find('span').html(data.subcat.name)
					$('#drop2').find('span').html(data.sort_type_obj.name);
					$('#drop3').find('span').html(data.city.name);
					set_document_title(data.subcat.name);
					
					//左边的开始菜单
					var data=data.data;
					var urlCurArr=[];// 当前红色图片；
					var urlArr=[];//  灰色图片；	
					for(var x=0;x<data.length;x++){
//						console.log(1);
						var left_str=$('<li cat-id='+data[x].id+'><span></span><p class="size-sm color-black">'+data[x].name+'</p></li>');								
						$('.tab-vertical').append(left_str);
						left_str.find('span').css({'background-image':"url("+data[x].icon+")"});
						urlCurArr.push(data[x].icon_active);
						urlArr.push(data[x].icon);
//						console.log(urlArr);
						
					};
					$('.tab-vertical li').on('click',function(){
						var index=$(this).index();
						$('.tab-vertical li').each(function(index,item){
							$(item).find('span').css({'background-image':"url("+urlArr[index]+")"})
						})
						$(this).find('span').css({'background-image':"url("+urlCurArr[index]+")"});
						
					})
				//左边结束
					bind_menu_click();

					//默认加载进来选择推荐
					$(".tab-vertical li").eq(0).trigger('click');
					$(".tab-vertical li").eq(0).addClass('active')

					
				},error:function(){
					
				}
			});

}

window.set_document_title = function (title) {

	document.title = title;
	// var $body = $('body');
 //    // hack在微信等webview中无法修改document.title的情况
 //    var $iframe = $('<iframe style="height:0;border:0" src="/favicon.ico" ></iframe>');
 //    $iframe.on('load',function() {
 //        setTimeout(function() {
 //            $iframe.off('load').remove();
 //        }, 0);
 //    }).appendTo($body);
}
//列表接口
var has_more;
var offset=undefined;
			// 请求接口
			function getList(){
				if(offset){
					var Url="http://"+getHostName()+"/user/item_list/?"+jQuery.param(Common.UrlGet())+"&offset="+offset
				}else{
					var Url="http://"+getHostName()+"/user/item_list/?"+jQuery.param(Common.UrlGet());
				}		 			
				$.ajax({
					xhrFields: {withCredentials: true},
					type:"get",
					url:Url,
					dataType:'json',
					data:{},
					success:function(data){
						has_more=data.has_more;
						offset=data.offset;
						var infos=data.infos;
						if (!has_more){
							$('.loader-inner').hide();
						};
						if(infos.length==0){
							$('.noCoupon').show();
						}else{
							$('.mui-card').show();
						}
						for(var i=0;i<infos.length;i++){
							var  free='';
							if (!infos[i].has_fee) {
								free='<img src="/static/user/free.png" class="free" alt="" style="position: absolute;width:25px;height:25px;top:0;left:0;" />'
							}
							var str=$('<li class="mui-table-view-cell mui-media no-after-dotted"><a href="/static/user/detail.html?item_id='+infos[i].id+'"><img class="mui-media-object mui-pull-left" src="'+infos[i].image+'"><div class="mui-media-body">'+infos[i].title+'<p class="mui-ellipsis"><span>'+infos[i].hospital.name+'</span></p><p class="mui-ellipsis">售价：<span class="color-red">￥'+infos[i].price+'</span>医院价：<span class="line-throu">￥'+infos[i].orig_price+'</span></p></div><div class="month-pay  month-pay-sm"><div class="tit">月供</div><div class="num"><p class="color-red"><b>￥'+infos[i].period_money+'</b><span>x '+infos[i].period_count+'</span></p></div></div></a>'+free+'</li>');
							if(i==infos.length-1){
								str.removeClass('no-after-dotted');
							}
							$('.item-list').append(str);
						}							
					},
					error:function(){
						//alert('网络出现小差，请稍后再试');
					}
				});	
}
get_filters(getList);

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
					if(has_more){						
						setTimeout(getList(),1000)						
					}else{
						$('.tit').show()
					}

				} 
			} 


$(document).ready(function(){
  bind_menu_click();
  $('#drop-list1').addClass('is-dis')
  $('#right-side-menu').addClass('is-dis')
});


