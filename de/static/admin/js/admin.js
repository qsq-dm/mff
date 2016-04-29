
var app = angular.module("MyApp",['ui.router', 'ngProgress', 'ngDialog', 'angularInlineEdit', 'ui-notification', 'ui.bootstrap', 'ui.bootstrap.datetimepicker', 'aMap', 'localytics.directives', 'ui.sortable', 'textAngular', 'toggle-switch'])


app.factory('authorization', ['$q', '$http', '$timeout', '$state',
      function($q, $http, $timeout, $state) {
        var _identity = undefined,
          _authenticated = false;
        return {
          isLoggedin: function() {
            return angular.isDefined(_identity);
          },
          isAuthenticated: function() {
            return Boolean(getCookie('token'));
          },
          goSignin: function () {
            $state.go('signin');
          },
          logout: function () {
            console.log('logout');

            $state.go('signin');
          },
          getName: function() {
            return $cookieStore.get('name');
          },
          getRole: function() {
            return $cookieStore.get('role');
          },
          authenticate: function(identity) {
            _identity = identity;
            _authenticated = identity != null;
          }
        };
      }
    ])

app.config(
    function setupConfig( $httpProvider ) {

        $httpProvider.interceptors.push( interceptHttp);

        function interceptHttp( $q) {
            return({
                response: response,
                responseError: responseError
            });
       
            function response( response ) {
                console.log(response);
                console.log('intercept');
                console.log(response.headers()['content-type']);
                if(response.headers()['content-type'] === "application/json; charset=utf-8"){
                    console.log(response);
                    if (response.data.code==-1) {
                        console.log('goto login');
                        window.location='/admin/#/signin';
                    }
                }
                return( response );
            }
            function responseError( response ) {
                return( $q.reject( response ) );
            }
        }
    }
);

app
.controller('appController', ['$http', '$scope', '$state', 'ngProgress', 'Notification', function($http, $scope,$state,ngProgress,Notification) {
    window.progress = ngProgress;
    window.notification = Notification;
    window.progress.color('#2a6496');
    window.app_scope = $scope;
    $scope.token = getCookie('token');
    $scope.name = getCookie('name');
    $scope.loginForm = {
        'name':'',
        'passwd':''
    };
    $scope.isRoot = function () {
        var role  = getCookie('cat');
        if(!role) { return false }
        role  = parseInt(role)
        return role==0
    }
    $scope.isEditor = function () {
        var role  = getCookie('cat');
        if(!role) { return false }
        role  = parseInt(role)
        return role==1;
    }
    $scope.isPromoter = function () {
        var role  = getCookie('cat');
        if(!role) { return false }
        role  = parseInt(role)
        return role==2;
    }
    $scope.isMarketer = function () {
        var role  = getCookie('cat');
        if(!role) { return false }
        role  = parseInt(role)
        return role==3;
    }
    $scope.isTester = function () {
        var role  = getCookie('cat');
        if(!role) { return false }
        role  = parseInt(role)
        return role==4;
    }
    $scope.isCustom = function () {
        var role  = getCookie('cat');
        if(!role) { return false }
        role  = parseInt(role)
        return role==5;
    }
    
    
    
    function callback(data) {
        console.log('call');
        if(data.code==0) {
            $state.go('index');
        }else {
            notification.error(data.msg||'用户名或密码错误');
        }
    };
    $scope.login = function() {
        $http.post('/admin/login/', $scope.loginForm)
        .success(callback);
    };
    $http.get('/admin/refresh_qntoken/');
}])


app.config(function($stateProvider, $urlRouterProvider){
 
    console.log('admin config');

    $urlRouterProvider.otherwise('/index');
    $stateProvider
    .state('signin',{
            url: '/signin',
            templateUrl: '/static/admin/tpl/signin.html?version=9',
            controller: ''
        })
    .state('index',{
            url: '/index',
            templateUrl: '/static/admin/tpl/index.html?version=9',
            controller: 'IndexCtrl'
        })
    .state('index.city_list',{
            url: '/city_list',
            templateUrl: '/static/admin/tpl/city_list.html?version=9',
            controller: 'CityListCtrl'
        })
    .state('index.new_city',{
            url: '/new_city',
            templateUrl: '/static/admin/tpl/city_edit.html?version=9',
            controller: 'NewCityCtrl'
        })
    .state('index.new_period_pay_choice',{
            url: '/new_period_pay_choice',
            templateUrl: '/static/admin/tpl/new_period_pay_choice.html?version=9',
            controller: 'NewPeriodPayChoiceCtrl'
        })
    .state('index.item_list',{
            url: '/item_list?page&hospital_id&keyword&sub_cat_id&activity_id&is_recommend',
            templateUrl: '/static/admin/tpl/item_list.html?version=9',
            controller: 'ItemListCtrl'
        })
    .state('index.trial_list',{
            url: '/trial_list?page',
            templateUrl: '/static/admin/tpl/trial_list.html?version=9',
            controller: 'TrialListCtrl'
        })
    .state('index.new_item',{
            url: '/new_item',
            templateUrl: '/static/admin/tpl/item_edit.html?version=9',
            controller: 'ItemEditCtrl'
        })
    .state('index.new_trial',{
            url: '/new_trial',
            templateUrl: '/static/admin/tpl/trial_edit.html?version=9',
            controller: 'TrialEditCtrl'
        })
    .state('index.item_edit',{
            url: '/item_edit/:item_id',
            templateUrl: '/static/admin/tpl/item_edit.html?version=9',
            controller: 'ItemEditCtrl'
        })
    .state('index.trial_edit',{
            url: '/trial_edit/:item_id',
            templateUrl: '/static/admin/tpl/trial_edit.html?version=9',
            controller: 'TrialEditCtrl'
        })
    .state('index.new_coupon',{
            url: '/new_coupon',
            templateUrl: '/static/admin/tpl/coupon_edit.html?version=9',
            controller: 'CouponEditCtrl'
        })
    .state('index.new_tutorial',{
            url: '/new_tutorial',
            templateUrl: '/static/admin/tpl/tutorial_edit.html?version=9',
            controller: 'TutorialEditCtrl'
        })
    .state('index.new_daily_coupon',{
            url: '/new_daily_coupon',
            templateUrl: '/static/admin/tpl/daily_coupon_edit.html?version=9',
            controller: 'DailyCouponEditCtrl'
        })
    .state('index.city_edit',{
            url: '/city_edit/:item_id',
            templateUrl: '/static/admin/tpl/city_edit.html?version=9',
            controller: 'CityEditCtrl'
        })
    .state('index.daily_coupon_edit',{
            url: '/daily_coupon_edit/:item_id',
            templateUrl: '/static/admin/tpl/daily_coupon_edit.html?version=9',
            controller: 'DailyCouponEditCtrl'
        })
    .state('index.coupon_edit',{
            url: '/coupon_edit/:item_id',
            templateUrl: '/static/admin/tpl/coupon_edit.html?version=9',
            controller: 'CouponEditCtrl'
        })
    .state('index.tutorial_edit',{
            url: '/tutorial_edit/:item_id',
            templateUrl: '/static/admin/tpl/tutorial_edit.html?version=9',
            controller: 'TutorialEditCtrl'
        })
    .state('index.school_list',{
            url: '/school_list?page&city_name',
            templateUrl: '/static/admin/tpl/school_list.html?version=9',
            controller: 'SchoolListCtrl'
        })
    .state('index.cat_list',{
            url: '/cat_list?page',
            templateUrl: '/static/admin/tpl/cat_list.html?version=9',
            controller: 'CatListCtrl'
        })
    .state('index.subcat_list',{
            url: '/subcat_list?page&cat_id&is_recommend',
            templateUrl: '/static/admin/tpl/subcat_list.html?version=9',
            controller: 'SubcatListCtrl'
        })
    .state('index.hospital_list',{
            url: '/hospital_list?page&keyword&is_recommend',
            templateUrl: '/static/admin/tpl/hospital_list.html?version=9',
            controller: 'HospitalListCtrl'
        })
    .state('index.tutorial_list',{
            url: '/tutorial_list?page&keyword',
            templateUrl: '/static/admin/tpl/tutorial_list.html?version=9',
            controller: 'TutorialListCtrl'
        })
    .state('index.new_hospital',{
            url: '/new_hospital',
            templateUrl: '/static/admin/tpl/hospital_edit.html?version=9',
            controller: 'HospitalEditCtrl'
        })
    .state('index.hospital_edit',{
            url: '/hospital_edit/:item_id',
            templateUrl: '/static/admin/tpl/hospital_edit.html?version=9',
            controller: 'HospitalEditCtrl'
        })
    .state('index.apply_list',{
            url: '/apply_list?page&apply_status',
            templateUrl: '/static/admin/tpl/apply_list.html?version=9',
            controller: 'ApplyListCtrl'
        })
    .state('index.activity_list',{
            url: '/activity_list?page',
            templateUrl: '/static/admin/tpl/activity_list.html?version=9',
            controller: 'ActivityListCtrl'
        })
    .state('index.order_list',{
            url: '/order_list?page&keyword&hospital_id&sub_cat_id&order_status',
            templateUrl: '/static/admin/tpl/order_list.html?version=9',
            controller: 'OrderListCtrl'
        })
    .state('index.user_list',{
            url: '/user_list?page&keyword&promoter_id',
            templateUrl: '/static/admin/tpl/user_list.html?version=9',
            controller: 'UserListCtrl'
        })
    .state('index.promoter_list',{
            url: '/promoter_list?page&keyword',
            templateUrl: '/static/admin/tpl/promoter_list.html?version=9',
            controller: 'PromoterListCtrl'
        })
    .state('index.hospital_user_list',{
            url: '/hospital_user_list?page&hospital_id',
            templateUrl: '/static/admin/tpl/hospital_user_list.html?version=9',
            controller: 'HospitalUserListCtrl'
        })
    .state('index.coupon_list',{
            url: '/coupon_list?page',
            templateUrl: '/static/admin/tpl/coupon_list.html?version=9',
            controller: 'CouponListCtrl'
        })
    .state('index.daily_coupon_list',{
            url: '/daily_coupon_list?page',
            templateUrl: '/static/admin/tpl/daily_coupon_list.html?version=9',
            controller: 'DailyCouponListCtrl'
        })
    .state('index.advice_list',{
            url: '/advice_list?page',
            templateUrl: '/static/admin/tpl/advice_list.html?version=9',
            controller: 'AdviceListCtrl'
        })
    .state('index.period_pay_choice_list',{
            url: '/period_pay_choice_list?page',
            templateUrl: '/static/admin/tpl/period_pay_choice_list.html?version=9',
            controller: 'PeriodPayChoiceListCtrl'
        })
    .state('index.apply_detail',{
            url: '/apply_detail/:apply_id',
            templateUrl: '/static/admin/tpl/apply_detail.html?version=9',
            controller: 'ApplyDetailCtrl'
        })
    .state('index.advice_detail',{
            url: '/advice_detail/:advice_id',
            templateUrl: '/static/admin/tpl/advice_detail.html?version=9',
            controller: 'AdviceDetailCtrl'
        })
    .state('index.item_recommend_edit',{
            url: '/item_recommend_edit/:item_id',
            templateUrl: '/static/admin/tpl/item_recommend_edit.html?version=9',
            controller: 'ItemRecommendEditCtrl'
        })
    .state('index.item_activity_edit',{
            url: '/item_activity_edit/:item_id',
            templateUrl: '/static/admin/tpl/item_activity_edit.html?version=9',
            controller: 'ItemActivityEditCtrl'
        })
    .state('index.subcat_recommend_edit',{
            url: '/subcat_recommend_edit/:item_id',
            templateUrl: '/static/admin/tpl/subcat_recommend_edit.html?version=9',
            controller: 'SubcatRecommendEditCtrl'
        })
    .state('index.hospital_recommend_edit',{
            url: '/hospital_recommend_edit/:item_id',
            templateUrl: '/static/admin/tpl/hospital_recommend_edit.html?version=9',
            controller: 'HospitalRecommendEditCtrl'
        })
    .state('index.user_detail',{
            url: '/user_detail/:item_id',
            templateUrl: '/static/admin/tpl/user_detail.html?version=9',
            controller: 'UserDetailCtrl'
        })
    .state('index.new_itemcat',{
            url: '/new_itemcat',
            templateUrl: '/static/admin/tpl/itemcat_edit.html?version=9',
            controller: 'ItemCatEditCtrl'
        })
    .state('index.new_activity',{
            url: '/new_activity',
            templateUrl: '/static/admin/tpl/activity_edit.html?version=9',
            controller: 'ActivityEditCtrl'
        })
    .state('index.activity_edit',{
            url: '/activity_edit/:item_id',
            templateUrl: '/static/admin/tpl/activity_edit.html?version=9',
            controller: 'ActivityEditCtrl'
        })
    .state('index.new_itemsubcat',{
            url: '/new_itemsubcat?cat_id',
            templateUrl: '/static/admin/tpl/itemsubcat_edit.html?version=9',
            controller: 'ItemSubcatEditCtrl'
        })
    .state('index.itemcat_edit',{
            url: '/itemcat_edit/:item_id',
            templateUrl: '/static/admin/tpl/itemcat_edit.html?version=9',
            controller: 'ItemCatEditCtrl'
        })
    .state('index.itemsubcat_edit',{
            url: '/itemsubcat_edit/:item_id',
            templateUrl: '/static/admin/tpl/itemsubcat_edit.html?version=9',
            controller: 'ItemSubcatEditCtrl'
        })
    .state('index.period_pay_log_list', {
            url: '/period_pay_log_list?keyword&page&is_delayed',
            templateUrl: '/static/admin/tpl/period_pay_log_list.html?version=9',
            controller: 'PeriodPayLogListCtrl'
        })
    .state('index.trial_detail', {
            url: '/trial_detail?page&item_id',
            templateUrl: '/static/admin/tpl/trial_detail.html?version=9',
            controller: 'TrialDetailCtrl'
        })
    .state('index.daily_detail', {
            url: '/daily_detail?page&item_id',
            templateUrl: '/static/admin/tpl/daily_detail.html?version=9',
            controller: 'DailyDetailCtrl'
        })
    .state('index.send_user_coupon', {
            url: '/send_user_coupon?&phone',
            templateUrl: '/static/admin/tpl/send_user_coupon.html?version=9',
            controller: 'SendUserCouponCtrl'
        })
    .state('index.user_vcode', {
            url: '/user_vcode',
            templateUrl: '/static/admin/tpl/user_vcode.html?version=9',
            controller: 'UserVcodeCtrl'
        })
 });
 
 /*global angular */
(function (ng) {
  'use strict';

  app.directive('script', function() {
    return {
      restrict: 'E',
      scope: false,
      link: function(scope, elem, attr) {
        if (attr.type === 'text/javascript-lazy') {
          var code = elem.text();
          var f = new Function(code);
          console.log(code);
          f();
        }
      }
    };
  });

}(angular));


app.controller('IndexCtrl', ['$scope', '$http', '$state',function($scope, $http, $state) {
    if(!Boolean(getCookie('token'))) {
        $state.go('signin');
    }
}])


app.controller('CityListCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.infos = [];
    function callback(data) {
        $scope.infos = data.infos;
        $scope.page_info = data.page_info;
    }
    $scope.getPage = function(page) {
        $http.get('/admin/get_city_list',
            {params: {page:page}})
        .success(callback);
    }
    $scope.getPage(1);
}])


app.controller('ItemListCtrl', ['$scope', '$http', '$state', '$stateParams', function($scope, $http, $state, $stateParams) {
    $scope.infos        = [];
    var filters         = angular.copy($stateParams);
    if ($stateParams['sub_cat_id']) { //整型字段
        filters['sub_cat_id'] = parseInt($stateParams['sub_cat_id']);
    }
    if ($stateParams['hospital_id']) { //整型字段
        filters['hospital_id'] = parseInt($stateParams['hospital_id']);
    }
    if ($stateParams['activity_id']) {
        filters['activity_id'] = parseInt($stateParams['activity_id']);
    }
    if ($stateParams['is_recommend']=='1') {
        filters['is_recommend'] = 1;
    }
    $scope.filters      = filters;
    $scope.currentpage  = $stateParams.page || 1 ;
    function callback(data) {
        $scope.infos = data.infos;
        $scope.page_info = data.page_info;
    }
    $scope.refresh = function() {
        $http.get('/admin/get_item_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.removeItemActivity = function(item_id) {
        progress.start()
        function del_callback(data) {
            progress.complete();
            if(data.code==0) {
                notification.primary(data.msg);
                $state.reload();
            } else {
                notification.error(data.msg);
            }
        }
        $http.post('/admin/del_item_activity/',
            {'item_id':item_id})
        .success(del_callback);
    }
    $scope.routeTo = function(page) {
        var params              = {};
        var is_recommend        = undefined;
        if($scope.filters.is_recommend) {
            is_recommend        = 1
        }
        params['page']          = page;
        params['keyword']       = $scope.filters.keyword;
        params['sub_cat_id']    = $scope.filters.sub_cat_id;
        params['hospital_id']   = $scope.filters.hospital_id;
        params['activity_id']   = $scope.filters.activity_id;
        params['is_recommend']  = is_recommend;
        console.log(params);
        return $state.go('index.item_list', params);
    }
    $scope.reset   = function() {
        var params              = {}
        params['page']          = 1;
        params['keyword']       = undefined;
        params['sub_cat_id']    = undefined;
        params['hospital_id']   = undefined;
        params['activity_id']   = undefined;
        params['is_recommend']  = undefined;
        return $state.go('index.item_list', params);
    }
    $scope.topRecommend    = function(item_id) { //推荐置顶
        function top_callback(response) {
            progress.complete();
            console.log(response);
            if(response.code>0) {
                notification.error(response.msg);
            } else {
                notification.primary(response.msg);
                $state.reload();
            }
        }
        progress.start()
        $http.post('/admin/top_recommend_item/',
            {'item_id':item_id})
        .success(top_callback);
    }
    $scope.Recommend    = function(item_id, recommend) { //推荐
        function recommend_callback(response) {
            progress.complete();
            console.log(response);
            if(response.code>0) {
                notification.error(response.msg);
            } else {
                notification.primary(response.msg);
                $state.reload();
            }
        }
        progress.start()
        $http.post('/admin/recommend_item/',
            {'item_id':item_id, 'recommend':recommend})
        .success(recommend_callback);
    }
    $scope.Online       = function(item_id, status) { //上下线
        var msg = '';
        if(status==0) {
            msg = '确认下线吗?';
        } else {
            msg = '确认上线吗?';
        }
        if(confirm(msg)) {
            function online_callback(response) {
                progress.complete();
                if(response.code>0) {
                    notification.error(response.msg);
                } else {
                    notification.primary(response.msg);
                    $state.reload();
                }
            }
            progress.start()
            $http.post('/admin/set_item_status/',
                {'item_id':item_id, 'status':status})
            .success(online_callback);
        }
    }

    $scope.refresh();
}])


app.controller('TrialListCtrl', ['$scope', '$http', '$state', '$stateParams', function($scope, $http, $state, $stateParams) {
    $scope.infos        = [];
    var filters         = angular.copy($stateParams);
   
    $scope.filters      = filters;
    $scope.currentpage  = $stateParams.page || 1 ;
    function callback(data) {
        $scope.infos = data.infos;
        $scope.page_info = data.page_info;
        $scope.now      = data.now;
    }
    $scope.refresh = function() {
        $http.get('/admin/get_trial_list',
            {params: $stateParams})
        .success(callback);
    }

    $scope.routeTo = function(page) {
        var params              = {};

        params['page']          = page;
        console.log(params);
        return $state.go('index.trial_list', params);
    }
    $scope.reset   = function() {
        var params              = {}
        params['page']          = 1;
        params['keyword']       = undefined;
        params['sub_cat_id']    = undefined;
        params['activity_id']   = undefined;
        params['is_recommend']  = undefined;
        return $state.go('index.item_list', params);
    }
  
    $scope.refresh();
}])

app.controller('SchoolListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};
    $scope.currentpage  = $stateParams.page || 1;
    if ($stateParams.city_name) {
        $scope.filters['city_name'] = $stateParams.city_name;
    }
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        params = {page:page};
        if ($stateParams.city_name) {
            params['city_name'] = $stateParams.city_name;
        }
        $http.get('/admin/get_school_list',
            {params: params})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        params['city_name'] = $scope.filters.city_name;
        return $state.go('index.school_list', params);
    }
    $scope.getPage($scope.currentpage);
}])


app.controller('CatListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_cat_list',
            {params: {page:page}})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        return $state.go('index.cat_list', params);
    }
    $scope.getPage($scope.currentpage);
}])


app.controller('SubcatListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    //$scope.infos      = [];
    $scope.filters      = angular.copy($stateParams);
    var link            = '#/index/new_itemsubcat';
    if($scope.filters.cat_id) {
        $scope.filters.cat_id = parseInt($scope.filters.cat_id);
        link                  = '#/index/new_itemsubcat?cat_id='+$scope.filters.cat_id;
    }
    if($stateParams.is_recommend) {
        $scope.filters.is_recommend = 1;
    }
    window.subcatlistscope = $scope;
    $scope.sortableOptions = {
        containment: '#images-list-wrap',
        stop: function(e, vt) {
            console.log('stop drag cat');
        }
    };
    $scope.$on('ngRepeatFinished', function(ngRepeatFinishedEvent) {
                console.log('finish');
            });
    $scope.link         = link;
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.refresh = function() {
        progress.start()
        $http.get('/admin/get_subcat_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.optionsData = [];
    $scope.itemCatids = [];
    $scope.iditemMap = {};
    function cats_callback(data) {
        $scope.optionsData = data.infos; //optionsData在ngitemcat时不起作用?
        for(var i in $scope.optionsData) {
            var cat = $scope.optionsData[i];
            $scope.iditemMap[cat.id] = cat
            $scope.itemCatids.push(cat.id);
        }
           $scope.$watch('itemCatids', function(old, newval) {
           console.log(old)
           console.log(newval)
           if(old.join('')==newval.join('')) {
               return;
           }
           console.log('cat ids list');
           $http.post('/admin/set_cats_order/',
            $scope.itemCatids)
            .success(set_order_callback);
        }, true);
        
    }
    $http.get('/admin/get_cat_list')
        .success(cats_callback);

    function set_order_callback (data) {
        if(data.code==0) {
            notification.primary(data.msg)
        } else {
            notification.error(data.msg)
        }
    }
 

    $scope.setStatus = function (item_id, status) {
        progress.start()
        $http.post('/admin/subcat/set_status/',
            {'subcat_id':item_id, 'status':status})
        .success(post_callback);
    }
    function post_callback(data) {
        console.log('callback');
        progress.complete()
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.reload(); //state.go not working here! the same route not working here
        }
    }
    $scope.choose = function (cat_id) {
        if ($scope.filters.cat_id==cat_id) {
            $scope.filters.cat_id = undefined;
        } else {
            $scope.filters.cat_id = cat_id;
        }
        console.log($scope.filters);
        console.log(cat_id);
        $scope.routeTo(1);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        params['cat_id']    = $scope.filters.cat_id;
        var is_recommend    = undefined;
        if($scope.filters.is_recommend) {
            is_recommend    = 1;
        }
        params['is_recommend'] = is_recommend;
        console.log(params);
        return $state.go('index.subcat_list', params);
    }
    $scope.refresh();
    $scope.Recommend    = function(item_id, recommend) { //推荐
        function recommend_callback(response) {
            progress.complete();
            console.log(response);
            if(response.code>0) {
                notification.error(response.msg);
            } else {
                notification.primary(response.msg);
                $state.reload();
            }
        }
        progress.start()
        $http.post('/admin/recommend_subcat/',
            {'item_id':item_id, 'recommend':recommend})
        .success(recommend_callback);
    }
}])


app.controller('HospitalListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};
    if($stateParams.keyword) {
        $scope.filters.keyword = $stateParams.keyword;
    }
    if ($stateParams['is_recommend']=='1') {
        $scope.filters['is_recommend'] = 1;
    }
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_hospital_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        if($scope.filters.is_recommend) {
            params['is_recommend'] = 1;
        } else {
            params['is_recommend'] = undefined;
        }
        params['keyword']   = $scope.filters.keyword;
        return $state.go('index.hospital_list', params);
    }
    $scope.reset = function(page) {
        var params          = {};
        params['page']      = 1;
        params['keyword']   = undefined;
        params['is_recommend'] = undefined;
        return $state.go('index.hospital_list', params);
    }
    $scope.Online       = function(item_id, status) { //上下线
        var msg = '';
        if(status==0) {
            msg = '确认下线吗?';
        } else {
            msg = '确认上线吗?';
        }
        if(confirm(msg)) {
            function online_callback(response) {
                progress.complete();
                if(response.code>0) {
                    notification.error(response.msg);
                } else {
                    notification.primary(response.msg);
                    $state.reload();
                }
            }
            progress.start()
            $http.post('/admin/set_hospital_status/',
                {'item_id':item_id, 'status':status})
            .success(online_callback);
        }
    }
    $scope.Recommend    = function(item_id, recommend) { //推荐
        function recommend_callback(response) {
            progress.complete();
            console.log(response);
            if(response.code>0) {
                notification.error(response.msg);
            } else {
                notification.primary(response.msg);
                $state.reload();
            }
        }
        progress.start()
        $http.post('/admin/recommend_hospital/',
            {'item_id':item_id, 'recommend':recommend})
        .success(recommend_callback);
    }
    $scope.getPage($scope.currentpage);
}])

app.controller('TutorialListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};
    if($stateParams.keyword) {
        $scope.filters.keyword = $stateParams.keyword;
    }
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_tutorial_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        params['keyword']   = $scope.filters.keyword;
        return $state.go('index.tutorial_list', params);
    }
    $scope.reset = function(page) {
        var params          = {};
        params['page']      = 1;
        params['keyword']   = undefined;
        return $state.go('index.tutorial_list', params);
    }
    $scope.Online       = function(item_id, status) { //上下线
        var msg = '';
        if(status==0) {
            msg = '确认下线吗?';
        } else {
            msg = '确认上线吗?';
        }
        if(confirm(msg)) {
            function online_callback(response) {
                progress.complete();
                if(response.code>0) {
                    notification.error(response.msg);
                } else {
                    notification.primary(response.msg);
                    $state.reload();
                }
            }
            progress.start()
            $http.post('/admin/set_tutorial_status/',
                {'item_id':item_id, 'status':status})
            .success(online_callback);
        }
    }
    $scope.getPage($scope.currentpage);
}])


//逾期分期列表
app.controller('PeriodPayLogListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};
    if ($stateParams.keyword) {
        $scope.filters.keyword = $stateParams.keyword;
    }
    if ($stateParams.is_delayed=='true') {
        $scope.filters.is_delayed = 'true';
    }
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_period_pay_log_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        params['keyword']   = $scope.filters.keyword;
        params['is_delayed']= $scope.filters.is_delayed;
        return $state.go('index.period_pay_log_list', params);
    }
    $scope.reset = function(page) {
        var params          = {};
        params['page']      = 1;
        params['is_delayed']= undefined;
        params['keyword']   = undefined;
        return $state.go('index.period_pay_log_list', params);
    }
    $scope.getPage($scope.currentpage);
}])


app.controller('ActivityListCtrl', ['$scope', '$http', '$stateParams', '$state', 'ngDialog', function($scope, $http, $stateParams, $state, ngDialog) {
    $scope.infos        = [];
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_activity_list',
            {params: {page:page}})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        return $state.go('index.activity_list', params);
    }
    $scope.addActivityItem = function (activity_id) { //弹出框编辑活动商品列表
        progress.start()
        function get_list_ids(list){
            var ids = [];
            for(var i in list) {
                ids.push(list[i].id);
            }
            return ids;
        }
        $http.get('/admin/get_activity_items/?activity_id='+String(activity_id))
            .success(function(data) {
                progress.complete();
                window.s= $scope;
                $scope.choices   = data.infos;
                var selected     = []
                for(var i in $scope.choices) {
                    item         = $scope.choices[i]
                    if(item.selected) {
                        selected.push(item);
                    }
                }
                $scope.selected  = selected;
                ngDialog.open({
                    template:   '/static/admin/tpl/activity_items.html?version=9',
                    scope:      $scope,
                    controller: ['$scope', function($scope) {
                        
                        $scope.settings = {enableSearch: true};
                        
                        //$scope.customFilter = '';
        
                        $scope.Cancel = function () {
                            $scope.closeThisDialog();
                        }
        
                        $scope.Ok = function() {
                            function post_callback(data) {
                                progress.complete();
                                if(data.code==0) {
                                    notification.primary(data.msg);
                                } else {
                                    notification.error(data.msg);
                                }
                                $scope.closeThisDialog();
                            }
                            var data = {
                                activity_id: activity_id,
                                ids: get_list_ids($scope.selected)
                                }
                            progress.start();
                            $http.post('/admin/set_activity_items/',
                                data)
                            .success(post_callback);
                        }
                    }]
                    })
            }
            );
    }
    $scope.getPage($scope.currentpage);
}])


app.controller('OrderListCtrl', ['$scope', '$http', '$stateParams', '$state', 'ngDialog', function($scope, $http, $stateParams, $state, ngDialog) {
    $scope.infos        = [];
    $scope.filters      = {};
    $scope.currentpage  = $stateParams.page || 1;
    window.s = $scope;
    if($stateParams.hospital_id) {
        $scope.filters['hospital_id'] = parseInt($stateParams.hospital_id);
    }
    if($stateParams.sub_cat_id) {
        $scope.filters['sub_cat_id'] = parseInt($stateParams.sub_cat_id);
    }
    if($stateParams.order_status) {
        $scope.filters['order_status'] = parseInt($stateParams.order_status);
    }
    if($stateParams.keyword) {
        $scope.filters['keyword'] = $stateParams.keyword;
    }
    $scope.order_status_choices = [
    ];
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
        $scope.order_status_choices = data.order_status_choices;
    }
    $scope.refresh = function() {
        progress.start()
        $http.get('/admin/get_order_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params              = {};
        params['page']          = page||1;
        params['order_status']  = $scope.filters.order_status;
        params['keyword']       = $scope.filters.keyword;
        params['sub_cat_id']    = $scope.filters.sub_cat_id;
        params['hospital_id']   = $scope.filters.hospital_id;
        return $state.go('index.order_list', params);
    }
    $scope.chooseStatus = function (status) {
        if($scope.filters.order_status==status) {
            $scope.filters.order_status = undefined;
        } else {
            $scope.filters.order_status = status;
        }
        $scope.routeTo(1);
    }
    $scope.refund = function(order_id) {//退款
        progress.start();
        $http.get('/admin/get_refund_detail/?order_id='+order_id)
        .success( function (data) {
            progress.complete();
            if(data.code==0) {
                $scope.price = data.price;
                $scope.repayment_amount = data.repayment_amount;
                $scope.has_alipay = data.has_alipay;
                ngDialog.open({
                    template: '/static/admin/tpl/refund_dialog.html?version=9',
                    scope: $scope,
                    controller: ['$scope', function($scope) {
                        $scope.Cancel = function () {
                            $scope.closeThisDialog();
                        }
                        $scope.Ok = function() {
                            function post_callback(data) {
                                
                                progress.complete();
                                if(data.code==0) {
                                    notification.primary(data.msg);
                                } else {
                                    notification.error(data.msg);
                                }
                                $scope.closeThisDialog();
                                if(!data.has_alipay) {
                                    $state.reload();
                                } else {
                                    window.location = data.link;
                                }
                            }
                            var data = {
                                order_id: order_id
                                }
                            progress.start();
                            $http.post('/admin/refund_order/',
                                data)
                            .success(post_callback);
                        }
                    }]
                })
            } else {
                notification.error(data.msg)
            }
         });
    }
    $scope.reset = function() {
        var params = {
            page: 1,
            keyword: undefined,
            order_status: undefined,
            hospital_id: undefined,
            sub_cat_id: undefined
            }
        return $state.go('index.order_list', params);
    }
    $scope.refresh();
}])



app.controller('CouponListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};

    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_coupon_list/',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        return $state.go('index.coupon_list', params);
    }
    $scope.reset = function() {
        var params          = {};
        params['page']      = 1;
        return $state.go('index.coupon_list', params); 
    }
    $scope.getPage($scope.currentpage);
}])

app.controller('DailyCouponListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};

    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_daily_coupon_list/',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        return $state.go('index.daily_coupon_list', params);
    }
    $scope.reset = function() {
        var params          = {};
        params['page']      = 1;
        return $state.go('index.daily_coupon_list', params); 
    }
    $scope.getPage($scope.currentpage);
}])



app.filter('rawHtml', ['$sce', function($sce){
  return function(val) {
    return $sce.trustAsHtml(val);
  };
}]);
app.controller('TrialDetailCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id         = $stateParams.item_id;
    $scope.infos        = [];

    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.item         = data.item;
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }

    //赠送申请
    $scope.approve = function (apply_id) {
        progress.start();
        var params = {}
        params['apply_id'] = apply_id;
        params['item_id']  = item_id;
        $http.post('/admin/send_trial/',
            params)
        .success(function (data) {
            progress.complete();
            if(data.code==0) {
                notification.primary(data.msg);
                $state.reload();
            } else {
                notification.error(data.msg);
            }
        });
    }

    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/trial_applyer_list/?item_id='+item_id,
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        return $state.go('index.trial_detail', params);
    }
    $scope.reset = function() {
        var params          = {};
        params['page']      = 1;
        params['item_id']   = item_id;
        return $state.go('index.trial_detail', params); 
    }
    $scope.getPage($scope.currentpage);
}])


//每日优惠券详情
app.controller('DailyDetailCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id         = $stateParams.item_id;
    $scope.infos        = [];

    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.item         = data.item;
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }

    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/daily_applyer_list/?item_id='+item_id,
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        return $state.go('index.daily_detail', params);
    }

    $scope.getPage($scope.currentpage);
}])


//短信验证码
app.controller('UserVcodeCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {

    $scope.phone = '';
    function callback(data) {
        progress.complete();
        if (data.code==0) {
            $scope.vcode        = data.vcode;
            $scope.count        = data.count;
        } else {
            notification.error(data.msg);
        }
    }

    //获取验证码
    $scope.getVcode = function (cat) {

        var params = {}
        params['phone'] = $scope.phone;
        params['cat']  = cat;
        $http.post('/admin/get_user_vcode/',
            params)
        .success(function (data) {
            progress.complete();
            if(data.code==0) {
                $scope.vcode        = data.vcode;
                $scope.count        = data.count;
            } else {
                notification.error(data.msg);
            }
        });
    }

    //重置短信发送次数
    $scope.resetVcodeSent = function () {
        var params = {};
        params['phone'] = $scope.phone;
        $http.post('/admin/reset_user_vcode/',
            params)
        .success(function (data) {
            progress.complete();
            if(data.code==0) {
                notification.primary(data.msg);
                $state.reload();
            } else {
                notification.error(data.msg);
            }
        });
    }

}])


app.controller('UserListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};
    if($stateParams.keyword) {
        $scope.filters.keyword = $stateParams.keyword
    }
    if($stateParams.promoter_id) {
        $scope.filters.promoter_id = parseInt($stateParams.promoter_id);
    }
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_user_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        params['keyword']   = $scope.filters.keyword;
        params['promoter_id']   = $scope.filters.promoter_id;
        return $state.go('index.user_list', params);
    }
    $scope.reset = function() {
        var params          = {};
        params['page']      = 1;
        params['keyword']   = undefined
        params['promoter_id']   = undefined
        return $state.go('index.user_list', params); 
    }
    $scope.getPage($scope.currentpage);
}])


app.controller('PromoterListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};
    if($stateParams.keyword) {
        $scope.filters.keyword = $stateParams.keyword
    }

    $scope.tmp          = undefined;
    $scope.togglePromoter = function () {
        if($scope.tmp) {
            $scope.tmp = undefined;
        } else {
            $scope.tmp = {}
        }
    }
    $scope.addPromoter = function() {
        progress.start();
        $http.post('/admin/add_promoter/',
            $scope.tmp)
        .success(function (data) {
            if(data.code==0) {
                console.log(data);
                $state.reload();
            } else {
                notification.error(data.msg||'服务器异常');
            }
            progress.complete();
        });
    }
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_promoter_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        params['keyword']   = $scope.filters.keyword;
        return $state.go('index.promoter_list', params);
    }
    $scope.reset = function() {
        var params          = {};
        params['page']      = 1;
        params['keyword']   = undefined
        return $state.go('index.promoter_list', params); 
    }
    $scope.getPage($scope.currentpage);
}])


app.controller('HospitalUserListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.filters      = {};
    if($stateParams.hospital_id) {
        $scope.filters.hospital_id = parseInt($stateParams.hospital_id);
    }

    $scope.tmp          = undefined;
    $scope.toggleUser = function () {
        if($scope.tmp) {
            $scope.tmp = undefined;
        } else {
            $scope.tmp = {}
        }
    }
    $scope.addUser = function() {
        if(!($scope.tmp&&$scope.tmp.hospital_id)) {
            return notification.error('请选择医院');
        }
        progress.start();
        $http.post('/admin/add_hospital_admin/',
            $scope.tmp)
        .success(function (data) {
            if(data.code==0) {
                console.log(data);
                $state.reload();
            } else {
                notification.error(data.msg||'服务器异常');
            }
            progress.complete();
        });
    }
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_hospital_user_list/',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        params['hospital_id']      = $scope.filters.hospital_id;
        return $state.go('index.hospital_user_list', params);
    }
    $scope.reset = function() {
        var params          = {};
        params['page']      = 1;
        params['hospital_id'] = undefined;
        return $state.go('index.hospital_user_list', params); 
    }
    $scope.getPage($scope.currentpage);
}])


app.controller('AdviceListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_advice_list',
            {params: {page:page}})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        return $state.go('index.advice_list', params);
    }
    $scope.getPage($scope.currentpage);
}])

app.controller('PeriodPayChoiceListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.currentpage  = $stateParams.page || 1;
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_period_choice_list',
            {params: {page:page}})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        return $state.go('index.period_pay_choice_list', params);
    }
    $scope.getPage($scope.currentpage);
}])


app.controller('ApplyListCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    $scope.infos        = [];
    $scope.currentpage  = $stateParams.page || 1;
    $scope.filters      = {}
    if($stateParams.apply_status) {
        $scope.filters.apply_status = parseInt($stateParams.apply_status);
        }
    $scope.apply_status_choices = [
        {'id':1, 'title':'已通过'},
        {'id':2, 'title':'被拒绝'},
        {'id':3, 'title':'待审核'},
        {'id':4, 'title':'待补充'},
        ]
    $scope.chooseStatus = function (status) {
        if($scope.filters.apply_status==status) {
            $scope.filters.apply_status = undefined;
        } else {
            $scope.filters.apply_status = status;
        }
        $scope.routeTo(1);
    }
    function callback(data) {
        progress.complete();
        $scope.infos        = data.infos;
        $scope.page_info    = data.page_info;
        $scope.total        = data.total;
    }
    $scope.getPage = function(page) {
        progress.start()
        $http.get('/admin/get_apply_list',
            {params: $stateParams})
        .success(callback);
    }
    $scope.routeTo = function(page) {
        var params          = {};
        params['page']      = page||1;
        params['apply_status'] = $scope.filters.apply_status;
        return $state.go('index.apply_list', params);
    }
    $scope.getPage($scope.currentpage);
}])

//医院编辑
app.controller('HospitalEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_hospital/';
    if(item_id) { action    = '/admin/edit_hospital/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);

    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.go('index.hospital_list');
        }
    }
    $scope.addItem = function() {
        data = $('#hospitalform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_hospital/?item_id=' + String(item_id))
        .success(get_callback);
    }
    if(item_id) {
        $scope.getItem(item_id);
    } else {
        $scope.item             = {};
    }
}])


//商品编辑
app.controller('ItemEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_item/';
    $scope.textmenu = [
        ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'quote'],
        ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
        ['justifyLeft','justifyCenter','justifyRight','justifyFull','indent','outdent'],
        ['html', 'insertImage', 'insertLink', 'insertVideo']
    ];
    if(item_id) { action    = '/admin/edit_item/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    $scope.item             = {};
    window.ei   = $scope.item;
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.go('index.item_list');
        }
    }
    $scope.addItem = function() {
        data = $('#itemform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_item/?item_id=' + String(item_id))
        .success(get_callback);
    }
    $scope.subcat_choices = [
          {"id":1, "name":"双眼皮"},
          {"id":2, "name":"眉毛"}
        ];
    if(item_id) { $scope.getItem(item_id); }
}])


//试用编辑
app.controller('TrialEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_trial/';
    $scope.textmenu = [
        ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'quote'],
        ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
        ['justifyLeft','justifyCenter','justifyRight','justifyFull','indent','outdent'],
        ['html', 'insertImage', 'insertLink', 'insertVideo']
    ];
    if(item_id) { action    = '/admin/edit_trial/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    $scope.item             = {};
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.go('index.trial_list');
        }
    }

    $scope.addItem = function() {
        data = $('#trialform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }

    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_trial/?item_id=' + String(item_id))
        .success(get_callback);
    }

    if(item_id) { $scope.getItem(item_id); }
}])



//优惠券编辑
app.controller('CouponEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_coupon/';
    $scope.textmenu = [
        ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'quote'],
        ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
        ['justifyLeft','justifyCenter','justifyRight','justifyFull','indent','outdent'],
        ['html', 'insertImage', 'insertLink', 'insertVideo']
    ];
    if(item_id) { action    = '/admin/coupon_edit/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    $scope.item             = {};
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.go('index.coupon_list');
        }
    }
    $scope.addItem = function() {
        data = $('#couponform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_coupon/?item_id=' + String(item_id))
        .success(get_callback);
    }

    if(item_id) { $scope.getItem(item_id); }
}])


//城市编辑
app.controller('CityEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_city/';
    
    if(item_id) { action    = '/admin/city_edit/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    $scope.item             = {};
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.go('index.city_list');
        }
    }
    $scope.addItem = function() {
        data = $('#cityform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_city/?item_id=' + String(item_id))
        .success(get_callback);
    }

    if(item_id) { $scope.getItem(item_id); }
}])



//美攻略编辑
app.controller('TutorialEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_tutorial/';
    $scope.textmenu = [
        ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'quote'],
        ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
        ['justifyLeft','justifyCenter','justifyRight','justifyFull','indent','outdent'],
        ['html', 'insertImage', 'insertLink', 'insertVideo']
    ];
    if(item_id) { action    = '/admin/tutorial_edit/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    $scope.item             = {};
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.go('index.tutorial_list');
        }
    }
    $scope.addItem = function() {
        data = $('#tutorialform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_tutorial/?item_id=' + String(item_id))
        .success(get_callback);
    }

    if(item_id) { $scope.getItem(item_id); }
}])


//每日优惠券编辑
app.controller('DailyCouponEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_daily_coupon/';
    $scope.textmenu = [
        ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'quote'],
        ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
        ['justifyLeft','justifyCenter','justifyRight','justifyFull','indent','outdent'],
        ['html', 'insertImage', 'insertLink', 'insertVideo']
    ];
    if(item_id) { action    = '/admin/daily_coupon_edit/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    $scope.item             = {};
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            $state.go('index.daily_coupon_list');
        }
    }
    $scope.addItem = function() {
        data = $('#dailycouponform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_daily_coupon/?item_id=' + String(item_id))
        .success(get_callback);
    }

    if(item_id) { $scope.getItem(item_id); }
}])


//按用户发放优惠券
app.controller('SendUserCouponCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var phone = $stateParams.phone;
    
    $scope.item             = {};
    if(phone) {
        $scope.item.phone = phone;   
    }
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            notification.primary(data.msg);
            $state.go('index.send_user_coupon', {phone:$scope.item.phone});
        }
    }
    $scope.addItem = function() {
        data = $('#sendusercouponform').serializeObject();
        $http.post('/admin/send_user_coupon/',
            data)
        .success(post_callback);
    }

}])


//编辑活动／添加活动
app.controller('ActivityEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_activity/';
    if(item_id) { action    = '/admin/edit_activity/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            if (data.msg.length>0) {
                notification.primary(data.msg);
            }
            if(item_id) {
                $state.reload();
            } else {
                $state.go('index.activity_list');
            }
        }
    }
    $scope.addItem = function() {
        data = $('#activityform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_activity/?item_id=' + String(item_id))
        .success(get_callback);
    }
    if(item_id) { $scope.getItem(item_id); }
}])


app.controller('ItemCatEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_itemcat/';
    if(item_id) { action    = '/admin/edit_itemcat/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            if (data.msg.length>0) {
                notification.primary(data.msg);
            }
            if(item_id) {
                $state.reload();
            } else {
                $state.go('index.subcat_list');
            }
        }
    }
    $scope.addItem = function() {
        data = $('#itemcatform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_cat/?cat_id=' + String(item_id))
        .success(get_callback);
    }
    if(item_id) { $scope.getItem(item_id); }
}])

app.controller('ItemSubcatEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_itemsubcat/';
    if(item_id) { action    = '/admin/edit_itemsubcat/' + String(item_id) + '/'; }
    $scope.is_edit          = Boolean(item_id);
    function post_callback(data) {
        console.log('callback');
        progress.complete();
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            if (data.msg.length>0) {
                notification.primary(data.msg);
            }
            if(item_id) {
                $state.reload();
            } else {
                $state.go('index.subcat_list');
            }
        }
    }
    $scope.addItem = function() {
        progress.start();
        data = $('#itemsubcatform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_subcat/?sub_cat_id=' + String(item_id))
        .success(get_callback);
    }
    if(item_id) {
        $scope.getItem(item_id);
    } else {
        $scope.item = {};
        window.ss=$scope;
        if($stateParams.cat_id) {
            $scope.item['cat_id'] = parseInt($stateParams.cat_id);
        }
    }
}])

app.controller('SubcatRecommendEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/subcat_recommend_edit/'+String(item_id)+'/';

    function post_callback(data) {
        console.log('callback');
        progress.complete();
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            if (data.msg.length>0) {
                notification.primary(data.msg);
            }
            $state.reload();

        }
    }
    $scope.edit = function() {
        progress.start();
        data = $('#subcatrecommend').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_subcat_recommend/?sub_cat_id=' + String(item_id))
        .success(get_callback);
    }

    $scope.getItem(item_id);
    
}])


app.controller('HospitalRecommendEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/hospital_recommend_edit/'+String(item_id)+'/';

    function post_callback(data) {
        console.log('callback');
        progress.complete();
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            if (data.msg.length>0) {
                notification.primary(data.msg);
            }
            $state.reload();

        }
    }
    $scope.edit = function() {
        progress.start();
        data = $('#hospitalrecommend').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_hospital_recommend/?hospital_id=' + String(item_id))
        .success(get_callback);
    }

    $scope.getItem(item_id);
    
}])

app.controller('ItemRecommendEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action  = '/admin/item_recommend_edit/'+String(item_id)+'/';
    function post_callback(data) {
        console.log('callback');
        progress.complete();
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            if (data.msg.length>0) {
                notification.primary(data.msg);
            }
            if(item_id) {
                $state.reload();
            }
        }
    }
    $scope.edit = function() {
        progress.start();
        data = $('#itemrecommend').serializeObject();
        console.log(data);
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_item_recommend/?item_id=' + String(item_id))
        .success(get_callback);
    }
    $scope.getItem(item_id);

}])


app.controller('ItemActivityEditCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action  = '/admin/item_activity_edit/'+String(item_id)+'/';
    function post_callback(data) {
        console.log('callback');
        progress.complete();
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            if (data.msg.length>0) {
                notification.primary(data.msg);
            }
            if(item_id) {
                $state.reload();
            }
        }
    }
    $scope.edit = function() {
        progress.start();
        data = $('#itemactivity').serializeObject();
        console.log(data);
        $http.post(action,
            data)
        .success(post_callback);
    }
    $scope.getItem = function(item_id) {
        function get_callback(result) {
            $scope.item = result.data;
        }
        $http.get('/admin/get_item_activity/?item_id=' + String(item_id))
        .success(get_callback);
    }
    $scope.getItem(item_id);

}])


//内部使用七牛
app.directive('imagesField', ['$state', function ($state) {
    return {
        restrict: 'E',
        scope: {
            'images': '=',
            'fieldname': '='
        },
        link: function (scope, $scope) {
            window.iii = scope;
            scope.remove = function (image) {
                console.log('remove...'+image);
                image = image.split('/')
                image = image[image.length-1];
                scope.images = scope.images.replace(image+',', '');
                scope.images = scope.images.replace(','+image, '');
                scope.images = scope.images.replace(image, '');
            }
            scope.getImages = function(images) {
                if((!images)||images==''){ return [];}
                var images = scope.images.split(',');
                for (var i in images) {
                    images[i] = "http://7xnpdb.com2.z0.glb.qiniucdn.com/"+images[i];
                }
                return images;
            }
            scope.sortableOptions = {
                containment: '#images-list-wrap'
            };
            scope.$on('ngRepeatFinished', function(ngRepeatFinishedEvent) {
                console.log('finish');
            });
            scope.format_images = function (image_list) {
                var a= [];
                for (var i in image_list) {
                    var str = image_list[i].split('/');
                    var img = str[str.length-1];
                    a.push(img);
                }
                return a.join(',')
            }
            scope.$watch('images', function() {
               console.log('images changes');
               console.log(scope.images);
               scope.image_list = scope.getImages(scope.images);
            });
            if(!getCookie('qntoken')) {
                alert('七牛上传不了');
            }
            scope.image_list = scope.getImages(scope.images);
            var uploader = Qiniu.uploader({
            runtimes: 'html5,flash,html4',
            browse_button: 'qiniuuploads',
            container: 'images-container',
            drop_element: 'images-container',
            max_file_size: '100mb',
            flash_swf_url: 'js/plupload/Moxie.swf',
            dragdrop: true,
            chunk_size: '4mb',
            uptoken: eval(getCookie('qntoken')),
            domain: '127.0.0.1',
            auto_start: true,
            init: {
                'FilesAdded': function(up, files) {
                    $('table').show();
                    $('#success').hide();
                    plupload.each(files, function(file) {
                        var progress = new FileProgress(file, 'fsUploadProgress');
                        progress.setStatus("绛夊緟...");
                        progress.bindUploadCancel(up);
                    });
                },
                'BeforeUpload': function(up, file) {
                    var progress = new FileProgress(file, 'fsUploadProgress');
                    var chunk_size = plupload.parseSize(this.getOption('chunk_size'));
                    if (up.runtime === 'html5' && chunk_size) {
                        progress.setChunkProgess(chunk_size);
                    }
                },
                'UploadProgress': function(up, file) {
                    var progress = new FileProgress(file, 'fsUploadProgress');
                    var chunk_size = plupload.parseSize(this.getOption('chunk_size'));
                    progress.setProgress(file.percent + "%", file.speed, chunk_size);
                    console.log(file.percent);
                },
                'UploadComplete': function() {
                    $('#success').show();
                },
                'FileUploaded': function(up, file, info) {
                    var progress = new FileProgress(file, 'fsUploadProgress');
                    progress.setComplete(up, info);
                    console.log(info)
                    console.log(info.key);
                    var i  = JSON.parse(info);
                    console.log(i)
                    if((scope.images||'').length>0) {
                        if(scope.images.indexOf(i.key)==-1) {
                            scope.images = scope.images+ ','+i.key;
                        }
                    } else {
                        scope.images = i.key;
                    }
                    scope.image_list = scope.getImages(scope.images);
                    scope.$apply();//refresh ng-repeat
                    //$('#img_uploaded').append('<img class="uploaded-img" src="http://7xnpdb.com2.z0.glb.qiniucdn.com/'+i.key+'" </img>');
                },
                'Error': function(up, err, errTip) {
                    $('table').show();
                    var progress = new FileProgress(err.file, 'fsUploadProgress');
                    progress.setError();
                    progress.setStatus(errTip);
                },
                'Key': function(up, file) {
                    var key = "";
                    console.log(up);
                    console.log(file);
                    // do something with key
                    var list = (file.name || '').split('.')
                    var suffix = list[list.length-1] || 'jpg';
                    return up.id+ (new Date()).getTime()+'.' + suffix;
                }
                }
            });

            uploader.bind('FileUploaded', function() {
                console.log('hello man,a file is uploaded');
            });

        },
        templateUrl: '/static/admin/tpl/images_field.html?version=9'
    };
}]);


app.directive('onFinishRender', function ($timeout) {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            if (scope.$last === true) {
                $timeout(function () {
                    console.log('12');
                    scope.$emit('ngRepeatFinished');
                });
            }
        }
    }
});


//反馈详情
app.controller('AdviceDetailCtrl', ['$scope', '$http', '$timeout', '$stateParams', '$state', 'ngDialog', function($scope, $http, $timeout, $stateParams, $state, ngDialog) {
    var advice_id = $stateParams.advice_id;
    function callback(data) {
        $scope.item = data.data;
    }
    $http.get('/admin/get_advice_detail?advice_id='+advice_id)
        .success(callback);
}]);


app.controller('ApplyDetailCtrl', ['$scope', '$http', '$timeout', '$stateParams', '$state', 'ngDialog', function($scope, $http, $timeout, $stateParams, $state, ngDialog) {
    var apply_id = $stateParams.apply_id;
    function callback(data) {
        $scope.item     = data.apply;
        $scope.credit   = data.credit;
    }
    $scope.supply = {'apply_id': apply_id};
    $scope.is_edit_supply = false;

    $scope.toggleEditSupply = function () {
        $scope.is_edit_supply = !$scope.is_edit_supply;
        $scope.supply.id_no   = $scope.item.id_no;
        $scope.supply.stu_no  = $scope.item.stu_no;

        $scope.supply.graduate_time= $scope.item.graduate_time.substring(0,10);
        $scope.supply.enrollment_time= $scope.item.enrollment_time.substring(0,10);
        $scope.supply.stu_education= $scope.item.stu_education;
        $scope.supply.stu_years= $scope.item.stu_years;
        $scope.supply.school   = $scope.item.school;
        $scope.supply.name    = $scope.item.name;
        $scope.supply.major   = $scope.item.major;
    }

    $http.get('/admin/get_apply_detail?apply_id='+apply_id)
        .success(callback);
    $scope.viewImage  = function (image) {
        $scope.image  = image;
        $scope.angle  = 0;
         ngDialog.open({
            template:   '/static/admin/tpl/image_lightbox.html?version=9',
            scope:      $scope,
            controller: ['$scope', function($scope) {
                        window.img_scope = $scope;
                        $scope.rotateImg = function () {
                            $scope.angle = ($scope.angle+90)%360;
                            $('.img-lightbox').find('img')[0].className = "rotate"+$scope.angle;
                            console.log($scope.angle);
                        }
                       }],
            });
    }
    $scope.submitSupply = function (apply_id) {
        progress.start()
        function callback (data) {
            progress.complete();
            if(data.code==0) {
                $state.reload();
            } else {
                notification.error(data.msg);
            }
        }
        $http.post('/admin/supply_apply/', $scope.supply)
            .success(callback);
    
    }
    $scope.toSupply   = function (apply_id) { //学信网账号正确，去填充资料
        if(confirm('学信网账号确认可以登录吗，确认后将进入到补充资料页面?')) {
            progress.start()
            function callback (data) {
                progress.complete();
                if(data.code==0) {
                    $state.reload();
                } else {
                    notification.error(data.msg);
                }
            }
            $http.post('/admin/to_supply/', {'apply_id':apply_id})
                .success(callback);
        }
    }
    $scope.verifyChsi = function (user_id) {
        if ($scope.chsi_info) {
            ngDialog.open({
                template: '/static/admin/tpl/chsi_dialog.html?version=9',
                scope: $scope,
                })
            return;
        }
        function openDialog($scope) {
            ngDialog.open({
                template: '/static/admin/tpl/chsi_dialog.html?version=9',
                scope: $scope
                })
            return;    
        }
        window.openDialog = openDialog;
        function callback(response) {
            progress.complete()
            window.res = response;
            if(response.return_captcha) {
                notification.error('请输入验证码')
                $scope.return_captcha   = true;
                $scope.showCaptcha      = true;
                $scope.captcha_img      = response.data;
                ngDialog.open({
                    template: '/static/admin/tpl/chsi_captcha.html?version=9',
                    scope: $scope,
                    controller: ['$scope', function($scope) {
                        window.ss=$scope;
                        function refresh_callback(data) {
                            progress.complete()
                            $scope.captcha_img = data.data
                        }
                        $scope.refreshCaptcha = function () {
                            progress.start()
                            $http.get('/admin/refresh_chsi_captcha/?apply_id='+String(apply_id))
                                .success(refresh_callback);
                        }
                        $scope.Ok = function() {
                            //alert('拒绝');
                            function post_callback(data) {
                                
                                //$scope.closeThisDialog();
                                progress.complete();
                                if(data.success) {
                                    $scope.chsi_info = data.data;
                                    window.data = data;
                                    
                                    $scope.showCaptcha      = false;
                                } else {
                                    notification.error('验证码输入错误')
                                    $scope.refreshCaptcha();
                                }
                            }
                            var data = {
                                apply_id: $scope.item.id,
                                captcha: $scope.captcha
                                }
                            progress.start();
                            $http.post('/admin/set_chsi_captcha/',
                                data)
                            .success(post_callback);
                        }
                    }]
                    })
            } else if(!response.success) {
                notification.error(response.msg||'查询失败')
            } else {
                $scope.chsi_info = response.data;
                ngDialog.open({
                    template: '/static/admin/tpl/chsi_dialog.html?version=9',
                    scope: $scope
                    })
            }
        }
        progress.start()
        $http.get('/admin/verify_chsi/?user_id='+user_id)
            .success(callback);
    }
    $scope.Reject = function () {
        ngDialog.open({
            template: '/static/admin/tpl/apply_reject.html?version=9',
            scope: $scope,
            controller: ['$scope', function($scope) {
                    window.ss=$scope;
                    $scope.Ok = function() {
                        //alert('拒绝');
                        function post_callback(data) {
                            $scope.closeThisDialog();
                            progress.complete();
                            console.log('callback');
                            if(data.code!=0) {
                                notification.error(data.msg||'服务器异常');
                            }
                            else {
                                console.log('go to ');
                                $state.reload();
                            }
                        }
                        var data = {
                            apply_id: $scope.item.id,
                            reason: $scope.reason
                            }
                        progress.start();
                        $http.post('/admin/apply_reject/',
                            data)
                        .success(post_callback);
                    }
                    $scope.Cancel = function() {
                        $scope.closeThisDialog();
                    }
            }]
        });
    }
    $scope.Approve = function () {
        ngDialog.open({
            template: '/static/admin/tpl/apply_approve.html?version=9',
            scope: $scope,
            controller: ['$scope', function($scope) {
                    window.ss=$scope;
                    $scope.Ok = function() {
                        function post_callback(data) {
                            $scope.closeThisDialog();
                            progress.complete();
                            console.log('callback');
                            if(data.code!=0) {
                                notification.error(data.msg||'服务器异常');
                            }
                            else {
                                console.log('go to ');
                                $state.reload();
                            }
                        }
                        var data = {
                            apply_id: $scope.item.id,
                            total   : $scope.total,
                            }
                        progress.start();
                        $http.post('/admin/apply_approve/',
                            data)
                        .success(post_callback);
                    }
                    $scope.Cancel = function() {
                        $scope.closeThisDialog();
                    }
            }]
        });
    }
}])


app.controller('UserDetailCtrl', ['$scope', '$http', '$stateParams', '$state', 'ngDialog', function($scope, $http, $stateParams, $state, ngDialog) {
    var item_id = $stateParams.item_id;
    $scope.currentpage = 1;
    function callback(response) {
        $scope.item = response.data;
        $scope.apply = response.apply;
        $scope.location = response.location;
        $scope.wechat_info = response.wechat_info;
    }
    $http.get('/admin/get_user_detail?item_id='+item_id)
        .success(callback);

    $scope.routeTo  = function(page) {
        $http.get('/admin/get_user_list?same_user_id='+item_id+'&page='+page)
        .success(function (data){
            $scope.infos = data.infos;
            $scope.total = data.total;
            $scope.page_info = data.page_info;
            $scope.currentpage = page;
        });
    }
    $scope.routeTo(1);

}])


app.controller('NewCityCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_city/';

    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.go('index.city_list');
        }
    }
    $scope.addItem = function() {
        data = $('#cityform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    return false
}])


app.controller('NewPeriodPayChoiceCtrl', ['$scope', '$http', '$stateParams', '$state', function($scope, $http, $stateParams, $state) {
    var item_id = $stateParams.item_id;
    var action = '/admin/new_period_pay_choice/';

    function post_callback(data) {
        console.log('callback');
        if(data.code>0) {
            notification.error(data.msg||'服务器异常');
        }
        else {
            console.log('go to ');
            $state.go('index.period_pay_choice_list');
        }
    }
    $scope.addItem = function() {
        data = $('#periodpaychoiceform').serializeObject();
        $http.post(action,
            data)
        .success(post_callback);
    }
    return false
}])


app.controller("ngCity",function($scope, $http){
    var vm = $scope.vm = {};

    vm.optionsData = [];
    function callback(data) {
        $scope.optionsData = data.infos;
    }
    $http.get('/admin/get_city_list/')
        .success(callback);
})


app.directive('jsonText', function() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attr, ngModel) {            
          function into(input) {
            return JSON.parse(input);
          }
          function out(data) {
            return JSON.stringify(data);
          }
          ngModel.$parsers.push(into);
          ngModel.$formatters.push(out);

        }
    };
});


app.controller('AmapCtrl', ['$scope',
    function($scope) {

    }
]);

app.directive('positionField', function () {
    return {
        restrict: 'EA', //E = element, A = attribute, C = class, M = comment         
        scope: {
            //@ reads the attribute value, = provides two-way binding, & works with functions
            item: '=',
        },
        templateUrl: '/static/admin/tpl/position_field.html?version=9',
        controller: 'AmapCtrl',
        link: function (scope, $scope, element, attrs) { //DOM manipulation
            init_map();
            console.log(scope.item); //还未初始化

            if(scope.item.lng&&scope.item.lng>0) {
                console.log('center pos....');
                var lnglat = [parseFloat(scope.item.lng), parseFloat(scope.item.lat)];
                addMarker(lnglat);
            }

        }
    }
});

app.controller("ngItemSubcat",function($scope, $http){
    $scope.optionsData = [];
    function callback(data) {
        $scope.optionsData = data.infos;
    }
    $http.get('/admin/get_subcat_list')
        .success(callback);
})


app.controller("ngPeriodChoice",function($scope, $http){
    $scope.optionsData = [];
    function callback(data) {
        $scope.optionsData = data.infos;
    }
    $http.get('/admin/get_period_choice_list')
        .success(callback);
})


app.controller("ngHospital",function($scope, $http){
    $scope.optionsData = [];
    function callback(data) {
        $scope.optionsData = data.infos;
    }
    $http.get('/admin/get_hospital_list')
        .success(callback);
})


app.controller("ngSchoolCity",function($scope, $http){
    $scope.optionsData = [];
    function callback(data) {
        $scope.optionsData = data.infos;
    }
    $http.get('/admin/get_school_city_list/')
        .success(callback);
})


app.controller("ngItemCat",function($scope, $http, $state){
    window.ngitems = $scope;
    $scope.optionsData = [];
    $scope.itemCatids = [];
    $scope.iditemMap = {};
    function callback(data) {
        $scope.optionsData = data.infos;
        for(var i in $scope.optionsData) {
            var cat = $scope.optionsData[i];
            $scope.iditemMap[cat.id] = cat
            $scope.itemCatids.push(cat.id);
        }
    }
    $http.get('/admin/get_cat_list')
        .success(callback);
    $scope.editCat      = function($event, cat_id) {
        window.eve = $event;
        $event.stopPropagation();
        var params      = {'item_id': cat_id};
        $state.go('index.itemcat_edit', params);
    }
    $scope.sortableOptions = {
        containment: '#images-list-wrap',
        stop: function(e, vt) {
            console.log('stop drag cat');
        }
    };
    
    $scope.goAddSubCat  = function($event, cat_id) {
        window.eve = $event;
        $event.stopPropagation();
        var params      = {'cat_id': cat_id};
        $state.go('index.new_itemsubcat', params);
    }
})

app.controller("ngActivity", function($scope, $http, $state){
    $scope.optionsData = [];
    function callback(data) {
        $scope.optionsData = data.infos;
    }
    $http.get('/admin/get_activity_list')
        .success(callback);

})


app.controller("ngCoupon", function($scope, $http, $state){
    $scope.optionsData = [];
    function callback(data) {
        $scope.optionsData = data.infos;
    }
    $http.get('/admin/get_coupon_list')
        .success(callback);

})


app.controller("ngPromoter", function($scope, $http, $state){
    $scope.optionsData = [];
    function callback(data) {
        $scope.optionsData = data.infos;
    }
    $http.get('/admin/get_promoter_list')
        .success(callback);

})


//图片字段
//内部使用七牛
app.directive('imageField', ['$state', '$http', '$timeout', function ($state, $http, $timeout) {
    return {
        restrict: 'E',
        scope: {
            'image': '=',
            'fieldname': '='
        },
        link: function (scope, $scope) {
            scope.extractQiniuDomain = function (url) {
                if(!url) { return undefined }
                url = url.replace(/^.*\/\/[^\/]+\//, '')
                return url
            }

            window.sc=scope;
            $scope.image = scope.image;
            $scope.fieldname = scope.fieldname;
            scope.input_status = 'imageInput-'+scope.fieldname;
            scope.image_input_status = 'imageInput-'+scope.fieldname +'-input'
            
            console.log(scope.image_input_status);
            var handleFileSelect=function(evt) {
              console.log('image change');
              angular.element(document.querySelector(scope.input_status)).html('上传中...');
              var file=evt.currentTarget.files[0];
              console.log('file change;');
              var reader = new FileReader();
              reader.onload = function (evt) {
                myImage=evt.target.result;
                $http.post('/admin/upload_image/',  {image: myImage})
                    .then(function(res) {
                       if (res.status === 200) {
                            window.res=res;
                            scope.current_img = res.data.fullpath;
                            angular.element(document.querySelector('#'+scope.input_status)).html('上传成功');
                       } else {
                            notificatio.error((res.data||{}).msg||'服务器异常');
                       }
                     });
                };
              reader.readAsDataURL(file);
            };
            
            $timeout(function () {
                scope.current_img = scope.image;
                angular.element(document.querySelector('#'+scope.image_input_status)).on('change',handleFileSelect);
            }, 500);
        },
        templateUrl: '/static/admin/tpl/image_field.html?version=9'
    };
}]);

app.directive('draggable', function() {
    return function(scope, element) {
        // this gives us the native JS object
        var el = element[0];
        window.t = el;;
        //el.draggable = true;

        el.addEventListener(
            'dragstart',
            function(e) {
                console.log('start');
                el.cursor_start_x = e.clientX;
                el.cursor_start_y = e.clientY;
                el.current_x = parseInt($('.ngdialog-content').css('left'));
                el.current_y = parseInt($('.ngdialog-content').css('top'));
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('Text', this.id);
                this.classList.add('drag');
                $('.ngdialog-content').css('opacity', 0.1);                
                return false;
            },
            false
        );
        el.addEventListener(
            'dragover',
            function(e) {
                window.e = e;
                console.log(e.clientX);
                var offset_x = e.clientX - el.cursor_start_x;
                var offset_y = e.clientY - el.cursor_start_y;
                console.log(offset_x);
                console.log(offset_y);
                $('.ngdialog-content').css('left', el.current_x+offset_x*2);
                $('.ngdialog-content').css('top', el.current_y+offset_y*2);
                e.dataTransfer.dropEffect = 'move';
                // allows us to drop
                if (e.preventDefault) e.preventDefault();
                this.classList.add('over');
                return false;
            },
            false
        );
        el.addEventListener(
            'dragend',
            function(e) {
                console.log('end');
                this.classList.remove('drag');
                $('.ngdialog-content').css('opacity', 1);                
                return false;
            },
            false
        );
    }
});


app.controller('DateTimePickerDemoCtrl',
function ($scope, $timeout) {
  $scope.dateTimeNow = function() {
    $scope.date = new Date();
  };
  $scope.dateTimeNow();
  
  $scope.toggleMinDate = function() {
    $scope.minDate = $scope.minDate ? null : new Date();
  };
   
  $scope.maxDate = new Date('2014-06-22');
  $scope.toggleMinDate();

  $scope.dateOptions = {
    startingDay: 1,
    showWeeks: false
  };
  
  // Disable weekend selection
  $scope.disabled = function(calendarDate, mode) {
    return mode === 'day' && ( calendarDate.getDay() === 0 || calendarDate.getDay() === 6 );
  };
  
  $scope.hourStep = 1;
  $scope.minuteStep = 15;

  $scope.timeOptions = {
    hourStep: [1, 2, 3],
    minuteStep: [1, 5, 10, 15, 25, 30]
  };

  $scope.showMeridian = true;
  $scope.timeToggleMode = function() {
    $scope.showMeridian = !$scope.showMeridian;
  };
  
  $scope.$watch("date", function(value) {
    console.log('New date value:' + value);
  }, true);
  
  $scope.resetHours = function() {
    $scope.date.setHours(1);
  };
});


app.controller('DatetimePickerController', ['$scope', function($scope) {
  var that = this;
  var in10Days = new Date();
  in10Days.setDate(in10Days.getDate() + 10);
 
  // Disable weekend selection
  this.disabled = function(date, mode) {
    return (mode === 'day' && (new Date().toDateString() == date.toDateString()));
  };

  this.dateOptions = {
    showWeeks: false,
    startingDay: 1
  };
  
  this.timeOptions = {
    readonlyInput: false,
    showMeridian: false
  };
  
  this.dateModeOptions = {
    minMode: 'year',
    maxMode: 'year'
  };
  
  this.openCalendar = function(e) {
      $scope.is_open = true;
  };
  
  // watch date4 and date5 to calculate difference

  $scope.$on('$destroy', function() {
    that.calculateWatch();
  });
}]);


//日期字段
app.directive('datetimeField', ['$state', function ($state) {
    return {
        restrict: 'E',
        scope: {
            'val': '=',
            'fieldname': '='
        },
        link: function (scope, $scope) {
            window.s=scope;
        },
        templateUrl: '/static/admin/tpl/datetime_field.html?version=9'
    };
}]);


//开关
app.directive('switchField', ['$state', '$timeout', function ($state, $timeout) {
    return {
        restrict: 'E',
        scope: {
            'val': '=',
            'fieldname': '='
        },
        link: function (scope, $scope) {
            window.ss =scope;
            console.log('switch......');
            $timeout(function(){$("[name='"+scope.fieldname+"']").bootstrapSwitch();},10)
        },
        templateUrl: '/static/admin/tpl/switch.html?version=9'
    };
}]);

//inplace编辑排序
app.directive('orderField', ['$state', '$timeout', '$q', '$http', function ($state, $timeout, $q, $http) {
    return {
        restrict: 'E',
        scope: {
            'action': '=',
            'item': '='
        },
        link: function (scope, $scope) {
            scope.myModel = scope.item.sort_order;
            scope.validateOnServer = function(newValue) {
              var defer = $q.defer();
              function post_callback(data) {
                  if(data.code==0) {
                    defer.resolve();
                    notification.primary(data.msg||'修改成功');
                    $state.reload();
                  }else {
                    defer.reject();
                    notification.error(data.msg||'修改失败');
                  }
              }
              var data = {
                   'sort_order' : newValue,
                   'item_id'    : scope.item.id,
                 }
              $http.post(scope.action,
                data)
                .success(post_callback)
                .error(function () {
                    defer.reject()
                    notification.error('修改失败');
                    });
            
              return defer.promise;
            };
        },
        templateUrl: '/static/admin/tpl/inplace_edit.html?version=9'
    };
}]);






