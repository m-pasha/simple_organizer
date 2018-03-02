(function() {
    'use strict';

    angular
        .module('accounts')
        .controller('accountsCtrl', accountsCtrl);

    function accountsCtrl($scope, $http, $localStorage, AuthService, VerifyTokenFactory, RefreshTokenFactory) {
//        initCtrl();
//
//        function initCtrl(){
//            AuthService.checkLocalStorage($localStorage.currentUser);
//        };

        this.title = 'Login';
        $scope.userdata = {
            email: '',
            password: ''
        };

        $scope.username = function() {
            if ($localStorage.currentUser){
                return $localStorage.currentUser.email
            } else {
                return 'Anonymous'
            }
        }

        $scope.logFacebook = function() {
            $http.get('http://localhost:8000/api-auth/login/facebook/')
        };

        $scope.verifyTokenS = function(){
            AuthService.verifyToken($localStorage.currentUser);
        };

        $scope.refreshTokenF = function(){
            RefreshTokenFactory.get($localStorage.currentUser);
        };

        $scope.status = function() {

            if (AuthService.checkLocalStorage($localStorage.currentUser)) {
                return 'Hello, ', $localStorage.currentUser.email
            } else {
                return 'Please login'
            }
        };

        $scope.currentu = function() {
            if ($localStorage.currentUser){
            }
        };

        $scope.logIn = function() {
            AuthService.login($scope.userdata);
            $scope.userdata = {};
        };

        $scope.logOut = function() {
            AuthService.logout();
        };

    }
})();
