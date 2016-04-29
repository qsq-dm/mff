//获取验证码
$('#get-btn').on('click',function(){
	var phone=$('#phone').val();
	var code=$('#code').val();
	var password=md5($('#password').val(),'meifenfen');
	var ptest = /^((?:13\d|14\d|15[\d]|17[\d]|10[\d]|18[\d])-?\d{5}(\d{3}|\*{3}))$/;
	if (!ptest.test(phone)) {
		alert('请输入正确的手机号码');
		return;
	}
	$.ajax({
		xhrFields: {withCredentials: true},
		url: 'http://'+getHostName()+'/user/get_reg_vcode/',
		type: 'post',
		dataType: 'json',
		data: {phone:phone},
		success:function(data){
			if(data.code==0){
				var oBtn=document.getElementById('get-btn');
				var num=60;
				var timer=null;				
				oBtn.disabled=true;
				timer=setInterval(function(){
					num--;
					oBtn.innerHTML=num;
					if(num==0){
						num=60;
						oBtn.innerHTML='获取验证码';
						clearInterval(timer);
						oBtn.disabled=false;
					}
				},1000);
				;

			} else {
				alert(data.msg)
			}
			
		},error:function(){
			alert('网络出现小差，请稍后再试');
		}
	})
	
});
var onOff=true;
$('#agree').click(function(){
	if(onOff){
		$('#agree').html('&#xe61a;');
		$('#agree').css('color','#FF4200')
		$('#agree').addClass('act')
		onOff=false;
	}else{
		$('#agree').html('&#xe607;');
		$('#agree').css('color','#9B9B9B')
		$('#agree').removeClass('act')
		onOff=true;
	}
});
$('#agree').trigger('click')
//提交请求
$('#submit').on('click',function(){
	var phone=$('#phone').val();
	var code=$('#code').val();
	var password=md5($('#password').val(),'meifenfen');
	var ptest = /^((?:13\d|14\d|15[\d]|10[\d]|17[\d]|18[\d])-?\d{5}(\d{3}|\*{3}))$/;
	if (!ptest.test(phone)) {
		alert('请输入正确的手机号码');
		return;
	}
	if(!$('#agree').hasClass('act')){
		alert('请选择美分分用户协议');
		return;
	}
	$.ajax({
		xhrFields: {withCredentials: true},
		url: 'http://'+getHostName()+'/user/signup_post/',
		type: 'post',
		dataType: 'json',
		data: {phone:phone,vcode:code,passwd:password},
		success:function(data){
			if(data.code==0){
				if(sessionStorage.getItem('reg_pay_item_id')||sessionStorage.getItem('reg_pay_choice_id')){
					//alert(data.msg)
					location.href="/static/user/submit-order.html?item_id="+sessionStorage.getItem('reg_pay_item_id')+"&period_choice_id="+sessionStorage.getItem('reg_pay_choice_id')
				}else{
					//alert(data.msg);
					if (Common.UrlGet().next) {
						location.href=Common.UrlGet().next;
					}else{
						location.href="/user/index/";
					}
					
				}
			}else{
				alert(data.msg)
			}		
		},error:function(){
			alert('网络出现小差，请稍后再试')
		}
	})
})