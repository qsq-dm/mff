var para = Common.UrlGet();
var state;
$.ajax({
	xhrFields: {
		withCredentials: true
	},
	url: 'http://' + getHostName() + '/user/item_detail?item_id=' + para.item_id,
	type: 'post',
	dataType: 'json',
	success: function(data) {
		var infos = data.comments.infos;
		var hospital = data.hospital;
		var item = data.item;
		var pay_choices = data.pay_choices;
		wx.ready(function() {

			wx.onMenuShareTimeline({

				title: item.title, // 分享标题

				link: 'http://' + getHostName() + '/static/user/detail.html?item_id=' + item.id, // 分享链接

				imgUrl: item.photo_list[0], // 分享图标

				success: function() {

					console.log('success')

					// 用户确认分享后执行的回调函数

				},

				cancel: function() {

					console.log('cancel')

					// 用户取消分享后执行的回调函数

				}

			});

			wx.onMenuShareAppMessage({
				title: item.title, // 分享标题
				link: 'http://' + getHostName() + '/static/user/detail.html?item_id=' + item.id, // 分享链接
				imgUrl: item.photo_list[0], // 分享图标     
				desc: 'www.meifenfen.com', // 分享描述
				success: function() {

					console.log('success')

					// 用户确认分享后执行的回调函数

				},

				cancel: function() {

					console.log('cancel')

					// 用户取消分享后执行的回调函数

				}

			});

		});

		//		if(data.credit_amount<item.price){
		//			$('.shoufu').show();
		//			$('.check-stages').css('margin-bottom','0')
		//			$('.check-stages:after').css('height','0')
		//		}
		if (data.has_fav) {
			state = 0;
			$('#wish').html('移除心愿单');
		} else {
			state = 1;
			$('#wish').html('放入心愿单');
		}
		//假用户可以评价
		if (data.can_comment) {
			$('#fake-user-comment').click(function() {
				window.location = '/static/user/judge-edit.html' + location.search
			})

		}
		$('#item_note > pre').html(item.note);
		$('#item_use_time > pre').html(item.use_time);
		$('#phone').html('咨询电话:' + hospital.phone)
		$('#phone').on('click', function() {
			location = "tel:" + hospital.phone;
		})
		$('.hospital-link').attr('hospital-id', data.hospital.id)
		$('.hospital-link').click(function() {
			window.location = '/user/hospital_detail?hospital_id=' + data.hospital.id;
		})
		for (var i = 0; i < item.photo_list.length - 1; i++) {
			var e = $($('.swiper-slide')[0]);
			e.clone().insertAfter(e);
		}
		for (var i = 0; i < item.photo_list.length - 1; i++) {
			var e = $($('.swiper-pagination-bullet')[0]);
			e.clone().insertAfter(e);
		}
		for (var i = 0; i < item.photo_list.length; i++) {
			$('.img').eq(i).attr('src', item.photo_list[i]);
			$('.img').eq(i).attr('data', item.photo_list[i]);
		}; //替换banner背景图片
		var swiper = new Swiper('.swiper-container', {
			pagination: '.swiper-pagination',
			paginationClickable: true,
			autoplayDisableOnInteraction: false,
			autoplay: 3000,
			loop: true,
		});
		window.item_photos = item.photo_list;
		$('.img').click(wx_img_preview);
		$('#hospitalName').html(hospital.name);
		$('#hospitalTag').find('.aptitude').remove(); //先删除医院标签在动态添加
		for (var j = 0; j < hospital.tag_list.length; j++) {
			var hospitaList = $('<span class="aptitude color-blue size-sm">' + hospital.tag_list[j] + '</span>');
			$('#hospitalTag').append(hospitaList);
		}
		$('.user-judge').remove()

		$('#comment').find('a').html('用户评价(' + data.comments.total + ')');
		if (data.comments.total == 0) {
			$('.noJudge').show();
		}
		//动态修改医院信息
		for (var k = 0; k < infos.length; k++) {
			if (k > 0) {
				break
			}
			var str = '<div class="user-judge bg-white"><div class="fl"><img src="' + infos[k].user.avatar + '"/></div><div class="intro-cont"><div class="fr"><span class="color-grey p-name">' + infos[k].user.name + '</span>';
			for (var x = 0; x < 5; x++) {
				if (x < infos[k].rate)
					str += '<i class="iconfont color-gold star">&#xe602; </i>';
				else
					str += '<i class="iconfont color-grey star">&#xe602; </i>';
			}
			var photo_str = '';
			for (var q = 0; q < infos[k].photo_list.length; q++) {
				photo_str += '<span class="show-par"><img class="show-pic item-comment-img" src="' + infos[k].photo_list[q] + '"/></span>'
			}
			var additional = '';
			if (infos[k].is_re_comment) {
				additional = '<span style="vertical-align:1px;margin-left: 5px;">追加评价</span>'
			}
			str += '<h5 class="color-black mui-ellipsis-2 lower-line-height">' + infos[k].content + '</h5>' + photo_str + '<p class="size-sm"><i class="iconfont">&#xe63a;</i><span>' + infos[k].create_time + '</span>' + additional + '</p></div></div></div>';
			$('#comment').after(str);
		} //评论信息加载
		$('.item-comment-img').unbind('click');
		$('.item-comment-img').click(item_comment_img_preview);
		//主体title部分
		$('#mainTitle').html(item.title);
		$('#mainTitle').html(item.title);
		$('#yyname').html(hospital.name);
		$('#price').html(item.price);
		$('#oldPrice').html(item.orig_price);
		// $('#payment').html('需首付 '+data.need_pay+' 元')
		// if (data.need_pay==0) {
		// 	$('#payDetails').css('display','none')

		// };
		$('#payDetails').html('（首付金额＝总价－你的可用额度' + data.total_period_amount + '元）')
		$('.text-cont').remove()
		for (var j = pay_choices.length - 1; j >= 0; j--) {
			if (pay_choices[j].disable) {
				pay_choices[j].disable = 0;
			} else {
				pay_choices[j].disable = 1;
			}
			if (pay_choices[j].id == 0) {
				pay_choices[j].period_fee = '(直购)';
				var payNode = '<div class="text-cont" choice-id=' + pay_choices[j].id + ' need=' + pay_choices[j].need_pay + ' period=' + pay_choices[j].credit_used + '><p>￥' + pay_choices[j].period_total + '</p><p>' + pay_choices[j].period_fee + '</p><i class="iconfont">&#xe614;</i></div>';
			} else if (pay_choices[j].period_fee == 0) {
				pay_choices[j].period_fee = '(无服务费)';
				var payNode = '<div class="text-cont" choice-id=' + pay_choices[j].id + ' need=' + pay_choices[j].need_pay + ' period=' + pay_choices[j].credit_used + ' option=' + pay_choices[j].disable + '><p>' + "￥" + pay_choices[j].period_total + "x" + pay_choices[j].period_count + "期" + '</p><p>' + pay_choices[j].period_fee + '</p><i class="iconfont">&#xe614;</i></div>';
			} else {
				pay_choices[j].period_fee = '(含每期服务费￥' + pay_choices[j].period_fee + ')';
				var payNode = '<div class="text-cont" choice-id=' + pay_choices[j].id + ' need=' + pay_choices[j].need_pay + ' period=' + pay_choices[j].credit_used + ' option=' + pay_choices[j].disable + '><p>' + "￥" + pay_choices[j].period_total + "x" + pay_choices[j].period_count + "期" + '</p><p>' + pay_choices[j].period_fee + '</p><i class="iconfont">&#xe614;</i></div>';
			}


			$('#option').after(payNode);
		}

	},
	error: function() {

	}
});
// $(document).on('tap','.text-cont',function(){

// })
$('#buy').on('click', function(event) {
	if (!getCookie('sign_user')) {
		location.href = '/static/user/login.html?next=' + location.href;
		return;
	}
	event.preventDefault();
	var active = $('.text-cont.active').attr('choice-id');
	var option = $('.text-cont.active').attr('option');
	if (active) {
		if (option == 0) {
			alert('选择分期期数需小于现在到毕业前六个月的月数');
			return;
		}
		location.href = '/static/user/submit-order.html?period_choice_id=' + active + '&item_id=' + para.item_id;
	} else {
		alert('请选择分期')
	}
})
$('#wish').on('click', function() {
	if (!getCookie('sign_user')) {
		location.href = '/static/user/login.html?next=' + location.href;
		return;
	}
	$.ajax({
		xhrFields: {
			withCredentials: true
		},
		type: "post",
		url: "http://" + getHostName() + "/user/fav_item/?" + token,
		dataType: 'json',
		data: {
			item_id: para.item_id,
			status: state
		},
		success: function(data) {
			if (data.code == 0) {
				if (state == 0) {
					$('#wish').html('放入心愿单');
					alert(data.msg)
					state = 1;
				} else {
					$('#wish').html('移除心愿单');
					alert(data.msg)
					state = 0;
				}
			} else {
				alert(data.msg)
			}
		},
		error: function() {

		}
	});
})