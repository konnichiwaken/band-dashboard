/**
* EventTypeController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('EventTypeController', EventTypeController);

  EventTypeController.$inject = ['$location', '$scope', 'Attendance', 'Snackbar'];

  /**
  * @namespace EventTypeController
  */
  function EventTypeController($location, $scope, Attendance, Snackbar) {
    var vm = this;

    vm.createEventType = createEventType;

    /**
    * @name createEventType
    * @desc Create an event type
    * @memberOf band-dash.attendance.EventTypeController
    */
    function createEventType() {
      Attendance.createEventType(vm.name, vm.points, vm.rtp).then(
        createEventTypeSuccessFn,
        createEventTypeErrorFn);

      /**
      * @name createEventTypeSuccessFn
      * @desc Log that event type has been created successfully
      */
      function createEventTypeSuccessFn(data, status, headers, config) {
        Snackbar.show('Event type created successfully');
      }

      /**
      * @name createEventTypeErrorFn
      * @desc Log that an error occurred when attempting to create event type
      */
      function createEventTypeErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.detail);
      }
    }
  }
})();
