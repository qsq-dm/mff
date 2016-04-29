//if(sessionStorage.getItem('school')){
//	$('#school').text(sessionStorage.getItem('school'));
//}
//if(sessionStorage.getItem('enrollment_time')){
//	$('.entrance').text(sessionStorage.getItem('enrollment_time'));
//}
//if(sessionStorage.getItem('graduate_time')){
//	$('.graduation').text(sessionStorage.getItem('graduate_time'));
//}
//if(sessionStorage.getItem('stu_education')){
//	$('#xueli').find('option:selected').text(sessionStorage.getItem('stu_education'))
//}
//$('#name').val(sessionStorage.getItem('name'));
//$('#professional').val(sessionStorage.getItem('major'));
//$('#address').val(sessionStorage.getItem('addr'));
//$('#eldersPhone').val(sessionStorage.getItem('parent_contact'));
//$('#account').val(sessionStorage.getItem('chsi_name'));
//$('#passwd').val(sessionStorage.getItem('chsi_passwd'));
//$('#cardNum').val(sessionStorage.getItem('id_no'));
//$('#StudentNum').val(sessionStorage.getItem('stu_no'));
//$('#school-name').on('click',function(){
//	sessionStorage.setItem('name',$('#name').val())
//	sessionStorage.setItem('major',$('#professional').val())
//	sessionStorage.setItem('school',$('#school-name').text())
//	sessionStorage.setItem('stu_education',$('#xueli').find('option:selected').text())
//	sessionStorage.setItem('addr',$('#address').val())
//	sessionStorage.setItem('parent_contact',$('#eldersPhone').val())
//	sessionStorage.setItem('chsi_name',$('#account').val())
//	sessionStorage.setItem('chsi_passwd',$('#passwd').val())
//	sessionStorage.setItem('enrollment_time',$('.entrance').text())
//	sessionStorage.setItem('graduate_time',$('.graduation').text())	
//	sessionStorage.setItem('id_no',$('#cardNum').val())
//	sessionStorage.setItem('stu_no',$('#StudentNum').val())
//})

$.ajax({
		xhrFields: {withCredentials: true},
		type:"post",
		url:"http://"+getHostName()+"/user/my_apply/?",
		dataType:'json',
		success:function(data){
			var data=data.data;
			$('#name').val(data.name);
			$('#professional').val(data.major);
			$('#school').val(data.school);
			$('#xueli').find('option:selected').text(data.stu_education);
			$('#address').val(data.addr);
			$('#eldersPhone').val(data.parent_contact);
			$('#account').val(data.chsi_name);
			$('#passwd').val(data.chsi_passwd);
			$('.graduation').text(data.graduate_time.substring(0,7));
			$('#cardNum').val(data.id_no);
			$('#StudentNum').val(data.stu_no);
			$('.entrance').text(data.enrollment_time.substring(0,7));			
		},
		error:function(){
			
		}
	});




$('#nextStep').on('click',function(){
	var name=$('#name').val();
	var major=$('#professional').val();
	var school=$('#school').val();
	var stu_education=$('#xueli').find('option:selected').text();
	var addr=$('#address').val();
	var parent_contact=$('#eldersPhone').val();
	var chsi_name=$('#account').val();
	var chsi_passwd=$('#passwd').val();
	var graduate_time=$('.graduation').text();
	var id_no=$('#cardNum').val();
	var stu_no=$('#StudentNum').val();
	var enrollment_time=$('.entrance').text();
	var cardId=/(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
	var ptest = /^((?:13\d|14\d|15[\d]|17[\d]|18[\d])-?\d{5}(\d{3}|\*{3}))$/;
	var body_choice_id = $('.choice-entry.active').attr('data')
	var body_choice_text = $('#choice-other-text').val();

//	alert(enrollment_time)
	if(!name){
		alert('请输入姓名');
		return;
	};
	if(!cardId.test(id_no)){
		alert('请输正确的身份证号码');
		return;
	}
	if(school.trim()==''){
		alert('请选择就读学校名称');
		return;
	}
	if(enrollment_time.trim()=='请选择你入学时间'){
		alert('请选择你入学时间');
		return;
	}
	if(graduate_time.trim()=='请选择你毕业时间'){
		alert('请选择毕业时间');
		return;
	}
	if(stu_education.trim()=='请选择你的学历'){
		alert('请选择您的学历');
		return;
	}
	if(!major){
		alert('请输入您的专业')
		return;
	}
	if(!stu_no){
		alert('请输入您的学号');
		return;
	}
	if(!addr){
		alert('请输入您的地址');
		return;
	}
	if(!chsi_name){
		alert('请输入学信网账号');
		return;
	}
	if(!chsi_passwd){
		alert('请输入学信网密码');
		return;
	}
	if(parent_contact=='' || isNaN(parent_contact)){
		alert('请输入正确的父母联系方式')
		return;
	}
	$.ajax({
		xhrFields: {withCredentials: true},
		type:"post",
		url:"http://"+getHostName()+"/user/apply_credit_post/?"+token,
		dataType:'json',
		data:{
			name:name,
			major:major,
			school:school,
			stu_education:stu_education,
			addr:addr,
			parent_contact:parent_contact,
			chsi_name:chsi_name,
			chsi_passwd:chsi_passwd,
			graduate_time:graduate_time,
			id_no:id_no,
			stu_no:stu_no,
			enrollment_time:enrollment_time			
		},
		success:function(data){
			if(data.code==0){
				location.href='/static/user/applyer-pic.html';
			}
		},
		error:function(){
			
		}
	});
});
