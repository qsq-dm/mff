


    function addMarker(lnglatXY) {
      map.clearMap();
      marker = new AMap.Marker({
        icon: "http://webapi.amap.com/images/marker_sprite.png",
        position: lnglatXY
      });
      marker.setMap(map);
      map.setCenter(new AMap.LngLat(lnglatXY[0], lnglatXY[1]));
      return marker
    }

    function init_map() {
        var map = new AMap.Map('mapContainer', {
          // 设置中心点
          //center: [116.397428, 39.90923],
    
          // 设置缩放级别
          zoom: 12
        });
        //在地图中添加ToolBar插件
        map.plugin(["AMap.ToolBar"], function () {
          toolBar = new AMap.ToolBar();
          map.addControl(toolBar);
        });
        window.map = map;
    
        function geocoder_CallBack(data) {
            window.data     = data;
            var resultStr = "";
            var poiinfo = "";
            var address;
            //返回地址描述
            address = data.regeocode.formattedAddress;
            console.log(address);
            document.getElementById("addr").value = address;
        }
    
        //为地图注册click事件获取鼠标点击出的经纬度坐标
        var clickEventListener = map.on( 'click', function(e) {
            document.getElementById("lngX").value = e.lnglat.getLng();
            document.getElementById("latY").value = e.lnglat.getLat();
    
            AMap.service(["AMap.Geocoder"], function() {
                window.MGeocoder = new AMap.Geocoder({
                    radius: 1000,
                    extensions: "all"
                });
            });
            //逆地理编码
            var lnglatXY = [document.getElementById("lngX").value, document.getElementById("latY").value]
            addMarker(lnglatXY);
            MGeocoder.getAddress(lnglatXY, function(status, result) {
                if (status === 'complete' && result.info === 'OK') {
                    geocoder_CallBack(result);
                }
            })
        });
    }