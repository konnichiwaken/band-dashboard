/**
* MemberAttendanceController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('MemberAttendanceController', MemberAttendanceController);

  MemberAttendanceController.$inject = ['$location', '$scope', '$http', 'Attendance'];

  /**
  * @namespace MemberAttendanceController
  */
  function MemberAttendanceController($location, $scope, $http, Attendance) {
    var vm = this;

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.AttendanceController
    */
    function activate() {
      $http.get('/api/v1/attendance/event_attendance/').success(function(response) {
        var attendances = response;
        console.log(attendances);
      });
    }
  }
})();
