angular
	.module('addCandidate', [])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '../static/addCandidateForm.html',
                controller: 'addCandidateCtrl'
            	})
            .otherwise({ redirectTo: '/addCandidate' });
    }])
    .controller('addCandidateCtrl', ['$scope', '$http', function($scope, $http){
        $scope.dataReady = false;
            $http.get('/getCustomerList')
                .success(function(data, status, headers, config){
                    $scope.dataReady = true;
                    $scope.customerArray = data.customerArray;
                }).error(function(){
                    //windowAlert("Sorry, something went wrong ....")
                })
    		
    }]);