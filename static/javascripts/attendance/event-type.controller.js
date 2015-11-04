/**
* EventTypeController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('EventTypeController', EventTypeController);

  EventTypeController.$inject = ['$location', '$scope', 'Attendance'];

  /**
  * @namespace EventTypeController
  */
  function EventTypeController($location, $scope, Attendance) {
    var vm = this;

    vm.createEventType = createEventType;

    /**
    * @name createEventType
    * @desc Create an event type
    * @memberOf band-dash.attendance.EventTypeController
    */
    function createEventType() {
      Attendance.createEventType(vm.name, vm.points, vm.rtp);
    }
  }
})();
