/**
* Attendance
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .factory('Attendance', Attendance);

  Attendance.$inject = ['$http'];

  /**
  * @namespace Attendance
  * @returns {Factory}
  */
  function Attendance($http) {
    /**
    * @name Attendance
    * @desc The Factory to be returned
    */
    var Attendance = {
      createEventType: createEventType
    };

    return Attendance;

    ////////////////////

    /**
    * @name createEventType
    * @desc Try to create a new event type
    * @param {string} name The event type name entered by the user
    * @param {string} points The number of points entered by the user
    * @param {string} rtp The RTP for the event type entered by the user
    * @returns {Promise}
    * @memberOf band-dash.attendance.Attendance
    */
    function createEventType(name, points, rtp) {
      return $http.post('/api/v1/attendance/event_type/', {
        name: name,
        points: points,
        ready_to_play: rtp
      }).then(createEventTypeSuccessFn, createEventTypeErrorFn);

      /**
      * @name createEventTypeSuccessFn
      * @desc Log that event type has been created successfully
      */
      function createEventTypeSuccessFn(data, status, headers, config) {
        console.log('Event type created successfully')
      }

      /**
      * @name createEventTypeErrorFn
      * @desc Log error to the console
      */
      function createEventTypeErrorFn(data, status, headers, config) {
        console.error('Error when creating event type');
      }
    }
  }
})();
