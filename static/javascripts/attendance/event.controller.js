/**
* EventController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('EventController', EventController);

  EventController.$inject = ['$location', '$scope', '$http', 'Attendance'];

  /**
  * @namespace EventController
  */
  function EventController($location, $scope, $http, Attendance) {
    var vm = this;

    vm.createEvent = createEvent;
    vm.updateEventType = updateEventType;

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.EventController
    */
    function activate() {
      $http.get('/api/v1/attendance/event_type/').success(function(response) {
        vm.eventTypes = response;
      });
    }

    /**
    * @name createEvent
    * @desc Create an event type
    * @memberOf band-dash.attendance.EventController
    */
    function createEvent() {
      Attendance.createEvent(vm.title, vm.time, vm.type, vm.assignedBand, vm.type.points, vm.type.ready_to_play);
    }

    /**
    * @name createEvent
    * @desc Create an event type
    * @memberOf band-dash.attendance.EventController
    */
    function updateEventType() {
      vm.points = parseFloat(vm.type.points);
      vm.rtp = vm.type.ready_to_play;
    }
  }
})();
