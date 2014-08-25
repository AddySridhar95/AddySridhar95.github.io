angular
	.module('addCustomer', [])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '../static/addCustomerForm.html',
                controller: 'addCustomerCtrl'
            	})

    }])
    .controller('addCustomerCtrl', ['$scope', '$http', function($scope, $http){
        console.log("SOMETHING IS TERRIBLY WRONG");
    	$scope.showFTP = false;
        $scope.client = "";
    	$scope.$watch('ftp', function(){
    		if($scope.ftp == "yes"){
    			$scope.showFTP = true;
    		}
    		else{
    			$scope.showFTP = false;}
    	   });


        $scope.formPageOne = true;
        $scope.formPageChange = function(){  //take pageNo as parameter in case of multiple pages
            $scope.formPageOne = !$scope.formPageOne;
        };

        $scope.addUserProfile = function(){
            console.log("addUserProfile");
            $http.get('/AddUserProfile/'+$scope.client).success(function(data, status, headers, config){
                console.log(data);
                alert(data);
            }).error(function(){
                console.log("error");
            });
        }
    }]);	