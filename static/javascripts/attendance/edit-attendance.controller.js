/**
* EditAttendanceController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('EditAttendanceController', EditAttendanceController);

  EditAttendanceController.$inject = [
    '$location',
    '$scope',
    '$http',
    '$routeParams',
    'Attendance'
  ];

  /**
  * @namespace EditAttendanceController
  */
  function EditAttendanceController(
    $location,
    $scope,
    $http,
    $routeParams,
    Attendance) {
    var vm = this;

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.EditAttendanceController
    */
    function activate() {
      $http.get('/api/v1/attendance/event/?id=' + $routeParams.event).success(
        function(response) {
          vm.event = response[0];
        }
      );

      $http.get('/api/v1/attendance/event_attendance/?event_id=' + $routeParams.event).success(
        function(response) {
          vm.attendances = response;
        }
      );
    }

    function submitAttendance(attendanceID, attendanceCheckIn) {
      Attendance.submitAttendance(attendanceID, attendanceCheckIn);
    }
  }
})();
