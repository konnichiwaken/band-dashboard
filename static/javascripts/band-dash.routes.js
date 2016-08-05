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
      .state('edit_all_attendance', {
        url: '/attendance/edit',
        controller: 'AttendanceController',
        controllerAs: 'vm',
        data: {
          permissions: {
            only: ['director', 'president', 'secretary']
          }
        },
        templateUrl: '/static/templates/attendance/edit-attendance.html'
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
      .state('view_attendance', {
        url: '/attendance/all',
        controller: 'MemberAttendanceController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/attendance/view-attendance.html'
      })
      .state('event_list', {
        url: '/events/all',
        controller: 'EventListController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/attendance/event-list.html'
      })
      .state('event_substitution_form', {
        url: '/event/substitution/:event',
        controller: 'SubstitutionFormController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/attendance/substitution-form.html'
      })
      .state('pending_substitution_forms', {
        url: '/attendance/substitution_forms',
        controller: 'PendingSubstitutionFormController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/attendance/pending-substitution-forms.html'
      })
      .state('confirm_account', {
        url: '/confirm/:token',
        controller: 'ConfirmAccountController',
        controllerAs: 'vm',
        templateUrl: '/static/templates/authentication/confirm-account.html'
      });
  }
})();
