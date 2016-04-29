function getCookie(c_name)
{
if (document.cookie.length>0)
  {
  c_start=document.cookie.indexOf(c_name + "=")
  if (c_start!=-1)
    { 
    c_start=c_start + c_name.length+1 
    c_end=document.cookie.indexOf(";",c_start)
    if (c_end==-1) c_end=document.cookie.length
    return unescape(document.cookie.substring(c_start,c_end))
    } 
  }
return ""
};


function setlocalCookie(c_name,value,expiredays) {  
  var exdate=new Date();  
  exdate.setDate(exdate.getDate()+expiredays);  
  document.cookie=c_name+ "=" +escape(value)+((expiredays==null) ? "" : ";expires="+exdate.toGMTString())+";path=/;";  
}  
function setCookie(c_name,value,expiredays) {  
  var exdate=new Date();  
  exdate.setDate(exdate.getDate()+expiredays);  
  document.cookie=c_name+ "=" +escape(value)+((expiredays==null) ? "" : ";expires="+exdate.toGMTString())+";path=/;domain=www.meifenfen.com";  
}  

Common = {};

//获取URL参数
Common.UrlGet = function () {
    var args = {};
    var query = location.search.substring(1);
    var pairs = query.split("&");
    for (var i = 0; i < pairs.length; i++) {
        var pos = pairs[i].indexOf('=');
        if (pos == -1) continue;
        var argname = pairs[i].substring(0, pos);
        var value = pairs[i].substring(pos + 1);
        value = decodeURIComponent(value);
        args[argname] = value;
    }
    return args;
}
// 
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
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "//hm.baidu.com/hm.js?61b678558a59e95c85431d0243d592ef";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();

function getHostName() {
	if (location.host=='127.0.0.1:8080') {
		return '139.196.6.231'
	} else {
		return location.host
	}

}