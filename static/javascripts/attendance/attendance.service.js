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
      createEvent: createEvent,
      createEventType: createEventType
    };

    return Attendance;

    ////////////////////

    /**
    * @name createEvent
    * @desc Try to create a new event
    * @param {string} title The event title entered by the user
    * @param {string} time The date and time entered by the user
    * @param {string} type The event type entered by the user
    * @param {string} assignedBand The assigned band for the event entered by the user
    * @param {string} points The points for the event entered by the user
    * @param {string} rtp The RTP for the event entered by the user
    * @returns {Promise}
    * @memberOf band-dash.attendance.Attendance
    */
    function createEvent(title, time, type, assignedBand, points, rtp) {
      return $http.post('/api/v1/attendance/event/', {
        title: title,
        time: time,
        type_id: type,
        band_id: assignedBand,
        points: points,
        ready_to_play: rtp
      }).then(createEventSuccessFn, createEventErrorFn);

      /**
      * @name createEventSuccessFn
      * @desc Log that event has been created successfully
      */
      function createEventSuccessFn(data, status, headers, config) {
        console.log('Event created successfully')
      }

      /**
      * @name createEventErrorFn
      * @desc Log error to the console
      */
      function createEventErrorFn(data, status, headers, config) {
        console.error('Error when creating event');
      }
    }

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
