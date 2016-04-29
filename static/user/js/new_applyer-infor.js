
//  同意并接受
var oAgree=document.getElementById('agree');
var onOff=true;
$('#agree').click(function(){
    if(onOff){
        $('#agree').html('&#xe61a;');
        $('#agree').css('color','#FF4200')
        $('#agree').addClass('active')
        onOff=false;
    }else{
        $('#agree').html('&#xe607;');
        $('#agree').css('color','#9B9B9B')
        $('#agree').removeClass('active')
        onOff=true;
    }
});


$('#nextStep').on('click',function(){
	var chsi_name=$('#account').val();
	var chsi_passwd=$('#passwd').val();
    var parent_contact=$('#eldersPhone').val();
    var graduate_time=$('.graduation').text();
    var body_choice_ids = []
    var active_entrys = $('.choice-entry.active');
    for(var i=0;i<active_entrys.length;i++) {
        body_choice_ids.push($(active_entrys[i]).attr('data'));
    }
    var body_choice_text = $('#input-other-text').val();

	if(!chsi_name){
		alert('请输入学信网账号');
		return;
	}
	if(!chsi_passwd){
		alert('请输入学信网密码');
		return;
	}

	
    if(graduate_time.trim()=='请选择你毕业时间'){
        alert('请选择毕业时间');
        return;
    }
    if(parent_contact=='' || isNaN(parent_contact)){
        alert('请输入紧急联系人方式')
        return;
    }
    if(!body_choice_ids.length>0) {
        alert('你希望自己哪个部位变得更美');
        return
    }
    if(body_choice_ids.indexOf('10')!=-1&&!body_choice_text.length>0) {
        alert('请输入其他内容');
        return
    }
    
    if(!$('#agree').hasClass('active')) {
        return alert('请同意美分分授信协议');
    }
	$.ajax({
		xhrFields: {withCredentials: true},
		type:"post",
		url:"http://"+getHostName()+"/user/apply_credit_post/",
		dataType:'json',
		data:{
			chsi_name:chsi_name,
			chsi_passwd:chsi_passwd,
			parent_contact: parent_contact,
			graduate_time: graduate_time,
			body_choice_ids: body_choice_ids.join(','),
			body_choice_text: body_choice_text
		},
		success:function(data){
			if(data.code==0){
				location.href='/user/menu_credit_apply/';
			} else {
			    alert(data.msg)
			}
		},
		error:function(){
			
		}
	});
});
