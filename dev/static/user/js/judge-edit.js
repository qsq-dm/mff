var total = 0;
var uploaded= 0;
var para=Common.UrlGet() 
var upload = function(_file) {
	var picLength=$('.judge-pic-cont li').length+_file.files.length
	if (_file.files.length === 0) {
		return;
	}
	if(picLength>7){
        return setTimeout(function(){alert('最多上传六张图片')},1000); //防止主线程block
    }
    if(picLength==7){
    	$('.file').hide();
    }
//	if (_file.files.length >6) {
//		alert('最多上传6张图片');
//		return
//	}
for(var j=0;j<_file.files.length;j++){
	
	(function(one_file) {
		var reader = new FileReader();  

		reader.readAsDataURL(one_file);
		reader.onload = function(e) { 
			var str=$('<li><img class="pic-no2" src="'+reader.result+'" uploading=true><i class="iconfont del">&#xe625;</i><div class="load-cont"><div class="load-bar"><div class="load-bar-inner" data-loading="0"></div></div></div></li>');
			//$('.judge-pic-cont').prepend(str[0]); 
			$('.after').before(str[0]);
			(function( file, str){
				var data = new FormData();
				data.append('file', file);
				data.append('image_cat', 'comment')
				var request = new XMLHttpRequest();
				
				request.onreadystatechange = function() {
					if (request.readyState == 4) {
						try {
							window.r = request.response;
							var resp = JSON.parse(request.response);
							$('.mask').hide();
							$('.load-cont').hide()
							str.find('img').attr('src',resp.fullpath);
							str.find('img').attr('path',resp.image)
							
							$(_file).attr('path', resp.image);
						} catch (e) {
							var resp = {
								status: 'error',
								data: 'Unknown error occurred: [' + request.responseText + ']'
							};
						}
						
					}
				};
				request.upload.addEventListener('progress', function(e) {
					console.log(parseInt(100 * e.loaded / e.total));
					$('.mask').find('span').html(parseInt(100 * e.loaded / e.total) + '%');
					str.find('.load-bar-inner').css('width',parseInt(100 * e.loaded / e.total) + '%')
					
					
				}, false);
				request.open('POST', 'http://'+getHostName()+'/user/upload_image/?' + token);
				request.send(data);
			})(one_file, str);
		}
	})(_file.files[j])
}	
}
//
$("#up-no1").change(function() {
	if ($(this)[0].files.length>6) {
		    setTimeout(function(){alert('最多上传六张图片')},1000); //防止主线程block
		    return;
		}
		upload($(this)[0]);
	});

$(document).on('touchend','.del',function(event){	
	event.stopPropagation();
	event.preventDefault();
	$(this).parent('li').remove()
	$('#up-no1').val('');
	$('.file').show()
});
var falg=true;
var codeName=0;
$('#niming').on('tap',function(){
	if(falg){
		falg=false;
		codeName=1;
	}else{
		falg=true;
		codeName=0;
	}
})
$('#submit').click(function(){
	var content=$('#tit').val();
	if(content.length==0){
		alert('请输入您的评价');
		return
	}
	var str='';
	var num=0;
	for(var x=0;x<$('#star img').length;x++){
		if($('#star img').eq(x).attr('src')=='star-on.png'){
			num++
		}
	}
	if(num==0){
		alert('请去打分');
		return;
	}
	for(var i=0;i<$('.pic-no2').length;i++){
		if($('.pic-no2').eq(i).attr('path')==undefined){
			alert('您的图片尚未上传完毕，稍后再次提交')
			return;						
		}else{
			str+=$('.pic-no2').eq(i).attr('path')+','
		}
		
	}
	if(str.length>0){
		str=str.substring(0,str.length-1)
	}else{
		str='';
	}
	$.ajax({
		type:"post",
		url:"http://"+getHostName()+"/user/comment_post/?"+token,
		dataType:'json',
		data:{
			order_id:para.order_id,
			item_id:para.item_id,
			content:content,
			photos:str,
			is_anonymous:codeName,
			rate:num
		},
		success:function(data){
			if(data.code==0){
				location.href='/static/user/judge-look.html?item_id='+data.item_id;				
			}else{
				alert(data.msg);
			}
		},error:function(){
			alert('网络出小差了请稍后再试');
		}
	});
})

















