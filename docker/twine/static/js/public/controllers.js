angular.module('butternut.public.controllers', [])

    .controller('loginController', ['$scope', 'loginAPI', 
        function ($scope, loginAPI) {
        var vm = this; 
            vm.form_data = {};
        	// DataService.get_profiles();
            vm.login = function(){
                loginAPI.query(vm.form_data).$promise.then(function(result){
                    console.log(result);
                });
            }

    }])
;
