/**
* EventListController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('EventListController', EventListController);

  EventListController.$inject = ['$location', '$scope', '$http', 'Authentication'];

  /**
  * @namespace EventListController
  */
  function EventListController($location, $scope, $http, Authentication) {
    var vm = this;
    vm.attendances = {};
    vm.events = [];

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.EventListController
    */
    function activate() {
      var account = Authentication.getAuthenticatedAccount();
      $http.get('/api/v1/attendance/event_attendance/?account_id=' + account.id).success(function(response) {
        for (var i = 0; i < response.length; i++) {
          var attendance = response[i];
          vm.attendances[attendance.event_id] = attendance;
        }
        $http.get('/api/v1/attendance/event/').success(function(response) {
          for (var i = 0; i < response.length; i++) {
            var event = response[i];
            if (event.id in vm.attendances) {
              var attendance = vm.attendances[event.id];
              if (attendance.assigned) {
                var status = "Assigned event";
                if (attendance.allows_substitution) {
                  event.allowsSubstitution = true;
                }
              } else {
                var status = "Unassigned event";
              }

              event.status = status;
            }

            vm.events.push(event);
          }
        });
      })
    }
  }
})();
