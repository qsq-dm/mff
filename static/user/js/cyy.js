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
		$('#drop-list1').css('pointer-events','none')
		$('#right-side-menu').css('pointer-events','none')
		// $('a').css('pointer-events','all')
		// $('.drop-btn').css('pointer-events','all')
		//$('li').unbind('click')
		$('html').css({'overflow':'auto','position':'static'});		
		$(".drop-list").css("top","-264px");
		$(".drop-btn").removeClass("active").find("i").html("&#xe604;");
		$("#dialogBg").fadeOut(300);
	}else{
				console.log('act')
		$('#drop-list1').css('pointer-events','all')
		$('#right-side-menu').css('pointer-events','all')
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
		//alert(0)
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
		$('#drop-list1').css('pointer-events','none')
		$('#right-side-menu').css('pointer-events','none')
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
//接口
function option_sort(sort,cat,city){
			$.ajax({
			type:"get",
			url:"http://"+getHostName()+"/user/hospital_list/?sort_type="+sort+"&sub_cat_id="+cat+"&city_id="+city,
			dataType:'json',
			success:function(data){
				$('.item-list li').remove();
				var infos=data.infos;
				if(infos.length==0){
					$('.mui-card').hide();
					$('.noCoupon').show();
				}else{
					$('.mui-card').show();
					$('.noCoupon').hide();
				}
					for(var i=0,lg=infos.length;i<lg;i++){
					var child='';
					var text='';
					for(var k=0,lgk=infos[i].tag_list.length;k<lgk;k++){
						if(k<2){
						child+='<span class="aptitude color-blue size-sm">'+infos[i].tag_list[k]+'</span>'	
						}else{
							break;
						}						
					}
					for(var j=0,lgj=infos[i].cats.length;j<lgj;j++){
						text+=infos[i].cats[j].name+'、'
					}
					text=text.substring(0,text.length-1)
					var str='<li class="mui-table-view-cell no-after-dotted mui-media" style="display: block;""><a href="/user/hospital_detail/?hospital_id='+infos[i].id+'"><img class="mui-media-object mui-pull-left" src="'+infos[i].image+'"><div class="mui-media-body"><div class="h4" style="overflow: hidden;margin:6px 0 3px;"><span class="mui-pull-left mui-ellipsis yytitle" style="width:85%;">'+infos[i].name+'</span><span class="mui-pull-right">'+infos[i].rate+'</span></div><p>'+child+'</p><p class="mui-ellipsis top15" style="font-size: 12px;">'+infos[i].addr+'</p></div><div class="warp"><p>'+text+'，共'+infos[i].item_count+'个整形项目</p></div></a></li>'
					$('.item-list').append(str);
				}			
			},error:function(){
				
			}
		});
}


		$(function(){
			var has_more1;
			var offset1=undefined;
			function ReasetAjax(offset){
				if(offset){
						var Url="http://"+getHostName()+"/user/hospital_list/"+location.search+"&offset="+offset
					}else{
						var Url="http://"+getHostName()+"/user/hospital_list/"+location.search
				}							
				$.ajax({
					type:"get",
					url:Url,
					dataType:'json',
					success:function(data){
						var infos=data.infos;
						has_more1=data.has_more;
						if (!has_more1){
							$('.loader-inner').hide();
						};
						if(infos.length==0 && offset==undefined){
							$('.noCoupon').show();
							$('.mui-card').hide();
						}						
						for(var i=0,lg=infos.length;i<lg;i++){
							var child='';
							var text='';
							for(var k=0,lgk=infos[i].tag_list.length;k<lgk;k++){
								if(k<2){
								child+='<span class="aptitude color-blue size-sm">'+infos[i].tag_list[k]+'</span>'	
								}else{
									break;
								}
								
							}
							for(var j=0,lgj=infos[i].cats.length;j<lgj;j++){
								text+=infos[i].cats[j].name+'、'
							}
							text=text.substring(0,text.length-1)
							var str='<li class="mui-table-view-cell no-after-dotted mui-media" style="display: block;""><a href="/user/hospital_detail/?hospital_id='+infos[i].id+'"><img class="mui-media-object mui-pull-left" src="'+infos[i].image+'"><div class="mui-media-body"><div class="h4" style="overflow: hidden;margin:6px 0 3px;"><span class="mui-pull-left mui-ellipsis yytitle" style="width:85%;">'+infos[i].name+'</span><span class="mui-pull-right">'+infos[i].rate+'</span></div><p>'+child+'</p><p class="mui-ellipsis top15" style="font-size: 12px;">'+infos[i].addr+'</p></div><div class="warp"><p>'+text+'，共'+infos[i].item_count+'个整形项目</p></div></a></li>'
							$('.item-list').append(str);
						}
						
						console.log(text)
	
					},
					error:function(){
	
					}
				});				
			};
			ReasetAjax(offset1);
			
			$.ajax({
				type:"get",
				url:"http://"+getHostName()+"/user/hospital_filters/",
				dataType:"json",
				success:function(data){
					//销量加载
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
					};
					//城市
					for(var j=0;j<citys.length;j++){
						var city='';
						if(data.city.id==citys[j].id){
						city='<li class="mui-table-view-cell active" data-id="'+citys[j].id+'"><span>'+citys[j].name+'</span><i class="iconfont mui-pull-right">&#xe627;</i></li>'
						}else{
						city='<li class="mui-table-view-cell" data-id="'+citys[j].id+'"><span>'+citys[j].name+'</span><i class="iconfont mui-pull-right">&#xe63e;</i></li>'
						}
						$('#drop-list3').append(city)
					};															
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
					
					$('#drop1').find('span').html(data.subcat.name);
					$('#drop2').find('span').html(data.sort_type_obj.name);
					$('#drop3').find('span').html(data.city.name);
					
					
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
			//加载更多代码
			window.onscroll = function () { 
            	if (getScrollTop() + getClientHeight() == getScrollHeight()) { 
            		if(offset1){
            			RasetDate(1,'#item1mobile',offset1);
            		}
            	} 
            }	

		})



$(document).ready(function(){
  bind_menu_click();
});


