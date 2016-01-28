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
      createEventType: createEventType,
      submitOnTime: submitOnTime,
      submitLate: submitLate
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

    function submitOnTime(attendance) {
      attendance.is_late = false;
      if (attendance.assigned || (!attendance.assigned && attendance.id)) {
        return $http.put(
          '/api/v1/attendance/event_attendance/' + attendance.id + '/',
          attendance).then(submitOnTimeSuccessFn, submitOnTimeErrorFn);
      } else {
        return $http.post(
          '/api/v1/attendance/unassigned/',
          attendance).then(submitOnTimeSuccessFn, submitOnTimeErrorFn);
      }

      /**
      * @name submitOnTimeSuccessFn
      * @desc Log that event type has been created successfully
      */
      function submitOnTimeSuccessFn(data, status, headers, config) {
        console.log('Attendance submitted successfully');
        return true;
      }

      /**
      * @name submitOnTimeErrorFn
      * @desc Log error to the console
      */
      function submitOnTimeErrorFn(data, status, headers, config) {
        console.error('Error when submitting attendance');
      }
    }

    function submitLate(attendance) {
      attendance.is_late = true;
      if (attendance.assigned || (!attendance.assigned && attendance.id)) {
        return $http.put(
          '/api/v1/attendance/event_attendance/' + attendance.id + '/',
          attendance).then(submitLateSuccessFn, submitLateErrorFn);
      } else {
        return $http.post(
          '/api/v1/attendance/unassigned/',
          attendance).then(submitLateSuccessFn, submitLateErrorFn);
      }

      /**
      * @name submitLateSuccessFn
      * @desc Log that event type has been created successfully
      */
      function submitLateSuccessFn(data, status, headers, config) {
        console.log('Attendance submitted successfully');
        return data.data;
      }

      /**
      * @name submitLateErrorFn
      * @desc Log error to the console
      */
      function submitLateErrorFn(data, status, headers, config) {
        console.error('Error when submitting attendance');
      }
    }
  }
})();
