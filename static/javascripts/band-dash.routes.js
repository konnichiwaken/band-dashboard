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
    }).when('/event_type/create', {
      controller: 'EventTypeController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/attendance/create-event-type.html'
    }).when('/event/create', {
      controller: 'EventController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/attendance/create-event.html'
    }).when('/band/create', {
      controller: 'BandController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/members/create-band.html'
    }).when('/attendance/view_all', {
      controller: 'AttendanceController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/attendance/view-events.html'
    }).when('/band/assign', {
      controller: 'BandAssignmentController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/members/band-assignment.html'
    }).when('/event/edit_attendance/:event', {
      controller: 'EditAttendanceController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/attendance/event-attendance.html'
    }).when('/attendance/members/all', {
      controller: 'MemberAttendanceController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/attendance/view-all-member-attendance.html'
    }).otherwise('/');
  }
})();
