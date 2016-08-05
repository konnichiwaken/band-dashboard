/**
* EventController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('EventController', EventController);

  EventController.$inject = ['$location', '$scope', '$http', 'Attendance', 'Snackbar'];

  /**
  * @namespace EventController
  */
  function EventController($location, $scope, $http, Attendance, Snackbar) {
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

      $http.get('/api/v1/members/band/').success(function(response) {
        vm.bands = response;
      });
    }

    /**
    * @name createEvent
    * @desc Create an event type
    * @memberOf band-dash.attendance.EventController
    */
    function createEvent() {
      if (!vm.title) {
        Snackbar.error("Please enter a title");
        return;
      } else if (!vm.time) {
        Snackbar.error("Please enter an event time");
      } else if (!vm.type) {
        Snackbar.error("Please enter an event type");
        return;
      } else if (!vm.points && vm.points !== 0) {
        Snackbar.error("Please enter points for event");
        return;
      }

      Attendance.createEvent(
        vm.title,
        vm.time,
        vm.type.id,
        vm.assignedBand,
        vm.points,
        vm.rtp).then(createEventSuccessFn, createEventErrorFn);

      /**
      * @name createEventSuccessFn
      * @desc Log that event has been created successfully
      */
      function createEventSuccessFn(data, status, headers, config) {
        Snackbar.show('Event created successfully');
        vm.title = null;
        vm.time = null;
        vm.type = null;
        vm.assignedBand = null;
        vm.points = null;
        vm.rtp = null;
      }

      /**
      * @name createEventErrorFn
      * @desc Log that error occurred when trying to create event
      */
      function createEventErrorFn(data, status, headers, config) {
        Snackbar.error("Error when creating event");
      }
    }

    /**
    * @name updateEventType
    * @desc Updates event type fields in form
    * @memberOf band-dash.attendance.EventController
    */
    function updateEventType() {
      vm.points = parseFloat(vm.type.points);
      vm.rtp = vm.type.ready_to_play;
    }
  }
})();
