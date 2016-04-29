//经纬度转城市名
function lnglatToLocation(latitude, longitude, callback) {
    console.log('http://api.map.baidu.com/geocoder/v2/?ak=74136f02e6474fb72f3000e449e93c97&callback=renderReverse&location='+latitude+','+longitude+'&output=json&pois=1')
    $.ajax({  
        url: 'http://api.map.baidu.com/geocoder/v2/?ak=74136f02e6474fb72f3000e449e93c97&callback=renderReverse&location='+latitude+','+longitude+'&output=json&pois=1',  
        type: "get",  
        dataType: "jsonp",  
        jsonp: "callback",  
        success: function (data) {  
            console.log(data);
            var province            = data.result.addressComponent.province;  
            var city_name           = (data.result.addressComponent.city);  
            var district            = data.result.addressComponent.district;  
            var street              = data.result.addressComponent.street;  
            var street_number       = data.result.addressComponent.street_number;  
            var formatted_address   = data.result.formatted_address;
            var city_code           = data.result.cityCode;
            //alert(city_code);
            var data = {  
                latitude: latitude,  
                longitude: longitude,  
                city_code: city_code,
                city_name: city_name
            };
            if (typeof callback == "function") {  
                callback(data);  
            }
        }  
    });  
};


