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
      submitLate: submitLate,
      submitAbsence: submitAbsence,
      determineAttendanceStatus: determineAttendanceStatus
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
      });
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
      });
    }

    function submitOnTime(attendance) {
      attendance.is_late = false;
      if (attendance.assigned || (!attendance.assigned && attendance.id)) {
        return $http.put(
          '/api/v1/attendance/event_attendance/' + attendance.id + '/',
          attendance);
      } else {
        return $http.post(
          '/api/v1/attendance/unassigned/',
          attendance);
      }
    }

    function submitLate(attendance) {
      attendance.is_late = true;
      if (attendance.assigned || (!attendance.assigned && attendance.id)) {
        return $http.put(
          '/api/v1/attendance/event_attendance/' + attendance.id + '/',
          attendance);
      } else {
        return $http.post(
          '/api/v1/attendance/unassigned/',
          attendance);
      }
    }

    function submitAbsence(attendance) {
      attendance.is_late = false;
      return $http.put(
        '/api/v1/attendance/event_attendance/' + attendance.id + '/',
        attendance);
    }

    function determineAttendanceStatus(attendance, event) {
      if (attendance.points) {
        if (attendance.check_in_time) {
          var eventTime = new Date(event.time);
          var timeDelta = attendance.check_in_time - eventTime;
          var minutesLate = Math.round((timeDelta / 1000) / 60);
          var minutesLateFifteen = Math.ceil(minutesLate / 15) * 15;
          attendance.status = minutesLateFifteen.toString().concat(' minutes late');
        } else if (attendance.is_absence) {
          attendance.status = 'Absent';
        } else {
          attendance.status = 'On time';
        }
      }
    }
  }
})();
