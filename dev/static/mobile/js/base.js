$(document).ready(function() {
    
    var oHtml = document.documentElement;
        getFont();
        
        window.onresize = function(){
        getFont();
            

        }  
        function getFont(){
            var screenWidth = oHtml.clientWidth;
            /*if (screenWidth<=320) {
                oHtml.style.fontSize ='17.0667px';
            }else if (screenWidth>=750) {
                oHtml.style.fontSize ='40px';
            }else{
                oHtml.style.fontSize = screenWidth/(750/40)+'px';
            }*/
                oHtml.style.fontSize = screenWidth/(750/40)+'px';
            
        }
});