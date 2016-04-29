$(document).ready(function (){
	if(getCookie('sign_user')){
		$('.Log').hide();
		$('#my').show();
		$('.notDone').hide()
		$('.done').show();
		$('#HK').attr('href','/static/user/repay.html');
		$('#WD').attr('href','/static/user/order-list.html');
		$('#DJQ').attr('href','/static/user/coupon.html');
		$('#XYD').attr('href','/static/user/wishOrder.html');
		$('#login').attr('href','/static/user/login.html')
		$('#reg').attr('href','/user/signup/')
		//
		$.ajax({
			xhrFields: {withCredentials: true},
			type: "post",
			url: "http://"+getHostName()+"/user/home/?",
			dataType: 'json',
			data: {
				
			},
			success: function(data) {
				$('.ky').html(data.remain);
				$('.zje').html(data.total)
				if(data.code==1) {
					$('.my-text-cont').show();
					$('#reimbursement').html('');
					$('.Log').show();
					$('#my').hide();
					$('.notDone').show()
					$('.done').hide()
					return;
				}
				var user = data.user;
				$('#my').find('img').attr('src', user.avatar);
				$('#my').find('span').html(user.name);
				$('#my').find('p').html('手机号:' + user.phone);
				//#0默认 1审核中 2审核通过 3被拒
				if(data.apply_status==0){
					$('.status').html('预计申请额度￥10000');
					$('.circle-btn').attr('href','/static/user/applyer-infor.html');
				}else if(data.apply_status==1){
					$('.status').html('审核中');
					$('.circle-btn').attr('href','http://www.meifenfen.com/user/menu_credit_apply/')
					$('.circle-btn').html('查看申请')
				}else if(data.apply_status==2){
					$('.status').html('￥'+data.remain);
					$('.circle-btn').hide();
					$('.my-text-cont').hide();
					$('#amount_parent').show();
				}else if(data.apply_status==3){
					$('.status').html('审核没通过，请重新申请');
					$('.circle-btn').attr('href','http://www.meifenfen.com/user/menu_credit_apply/')
					$('.circle-btn').html('查看申请')
				}
				$('#lines').html(data.total);
				$('#vouchers').html(data.coupon_count + '张');
				if (data.period_to_pay==0) {
					$('#reimbursement').html('');
				}else{
				    if(data.has_delayed) {
                       $('#reimbursement').html('本期应还余额:￥' + data.period_to_pay + '(包含已逾期部分)');
				    } else {
					   $('#reimbursement').html('本期应还余额:￥' + data.period_to_pay + '(剩余' + data.remain_days + '天)');
					}
				}
				
				if (data.can_edit_name) {
					$('#editor').show()
				} else {
					$('#editor').hide()
				}
			},
			error: function() {
				
			}				
		})
}else{
$('.Log').show();
$('#my').hide();
$('.notDone').show();
$('.done').hide();
$('#HK').attr('href','/static/user/login.html?next='+location.href);
$('#WD').attr('href','/static/user/login.html?next='+location.href);
$('#DJQ').attr('href','/static/user/login.html?next='+location.href);
$('#XYD').attr('href','/static/user/login.html?next='+location.href);

if(Common.UrlGet()['next']) {
    $('#login').attr('href','/static/user/login.html?next='+Common.UrlGet()['next'])
} else {
    $('#login').attr('href','/static/user/login.html?next='+location.href)

}
$('#reg').attr('href','/user/signup/?next='+location.href)

};
//上传图片
var upload = function(_file,btn){

	if(_file.files.length === 0){
		return;
	}    	
	var data = new FormData();
	data.append('file', _file.files[0]);
	data.append('image_cat', 'avatar')
	var request = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if(request.readyState == 4){
			try {window.r = request.response;
				var resp = JSON.parse(request.response);
				$('.mask').hide();
				btn.attr('src', resp.fullpath)
				$(_file).attr('path',resp.image)
			} catch (e){
				var resp = {
					status: 'error',
					data: 'Unknown error occurred: [' + request.responseText + ']'
				};
			}
			console.log(resp.status + ': ' + resp.data);
		}
	};

	request.upload.addEventListener('progress', function(e){
		console.log(parseInt(100*e.loaded/e.total));
//		$('.mask').find('span').html(parseInt(100*e.loaded/e.total)+'%')
	}, false);

	request.open('POST', 'http://'+getHostName()+'/user/upload_image/?'+token);
	request.send(data);
}
$("#ding").change(function() {
	upload($(this)[0], $('.photo'));
	$('.mask').show()

});




})
