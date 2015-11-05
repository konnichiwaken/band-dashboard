(function () {
  'use strict';

  angular
    .module('band-dash.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
    $routeProvider.when('/register', {
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/register.html'
    }).when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/login.html'
    }).when('/attendance/create/event_type', {
      controller: 'EventTypeController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/attendance/create-event-type.html'
    }).when('/attendance/create/event', {
      controller: 'EventController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/attendance/create-event.html'
    }).otherwise('/');
  }
})();
