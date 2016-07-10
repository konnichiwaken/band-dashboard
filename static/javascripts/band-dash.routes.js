(function () {
  'use strict';

  angular
    .module('band-dash.routes')
    .config(config);

  config.$inject = ['$stateProvider', '$urlRouterProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');

    $stateProvider
      .state('splash_page', {
        url: '/',
        templateUrl: '/static/templates/splash-page.html'
      })
      .state('register', {
        url: '/register',
        controller: 'RegisterController',
        controllerAs: 'vm',
        data: {
          permissions: {
            only: ['director', 'president', 'secretary']
          }
        },
        templateUrl: '/static/templates/authentication/register.html'
      })
      .state('login', {
        url: '/login',
        controller: 'LoginController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/authentication/login.html'
      })
      .state('event_type_create', {
        url: '/event_type/create',
        controller: 'EventTypeController',
        controllerAs: 'vm',
        data: {
          permissions: {
            only: ['director', 'president', 'secretary']
          }
        },
        templateUrl: '/static/templates/attendance/create-event-type.html'
      })
      .state('event_create', {
        url: '/event/create',
        controller: 'EventController',
        controllerAs: 'vm',
        data: {
          permissions: {
            only: ['director', 'president', 'secretary']
          }
        },
        templateUrl: '/static/templates/attendance/create-event.html'
      })
      .state('band_create', {
        url: '/band/create',
        controller: 'BandController',
        controllerAs: 'vm',
        data: {
          permissions: {
            only: ['director', 'president', 'secretary']
          }
        },
        templateUrl: '/static/templates/members/create-band.html'
      })
      .state('attendance_view_all', {
        url: '/attendance/view_all',
        controller: 'AttendanceController',
        controllerAs: 'vm',
        data: {
          permissions: {
            only: ['director', 'president', 'secretary']
          }
        },
        templateUrl: '/static/templates/attendance/view-events.html'
      })
      .state('band_assign', {
        url: '/band/assign',
        controller: 'BandAssignmentController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/members/band-assignment.html'
      })
      .state('event_edit_attendance', {
        url: '/event/edit_attendance/:event',
        controller: 'EditAttendanceController',
        controllerAs: 'vm',
        data: {
          permissions: {
            only: ['director', 'president', 'secretary']
          }
        },
        templateUrl: '/static/templates/attendance/event-attendance.html'
      })
      .state('attendance_members_all', {
        url: '/attendance/members/all',
        controller: 'MemberAttendanceController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/attendance/view-all-member-attendance.html'
      })
      .state('events_all', {
        url: '/events/all',
        controller: 'AllEventsController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/attendance/view-all-events.html'
      });
  }
})();
