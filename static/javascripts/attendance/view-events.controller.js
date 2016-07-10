/**
* AllEventsController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('AllEventsController', AllEventsController);

  AllEventsController.$inject = ['$location', '$scope', '$http'];

  /**
  * @namespace AllEventsController
  */
  function AllEventsController($location, $scope, $http) {
    var vm = this;
    vm.attendances = {};
    vm.events = [];

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.AllEventsController
    */
    function activate() {
      $http.get('/api/v1/attendance/event_attendance/').success(function(response) {
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
                var status = "Assigned attendance";
              } else {
                var status = "Unassigned attendance";
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
