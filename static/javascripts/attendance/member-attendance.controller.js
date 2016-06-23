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
      vm.members = {};
      $http.get('/api/v1/attendance/event_attendance/').success(function(response) {
        var attendances = response;
        for (var i = 0; i < attendances.length; i++) {
          var attendance = attendances[i];
          var member = attendance.member;
          if (attendance.unexcused || attendance.unexcused === false) {
            attendance.excused = !attendance.unexcused;
          } else {
            attendance.excused = null;
          }
          if (attendance.check_in_time) {
            attendance.check_in_time = new Date(attendance.check_in_time);
          }
          Attendance.determineAttendanceStatus(attendance, attendance.event);
          if (member.id in vm.members) {
            vm.members[member.id]['attendances'].push(attendance);
          } else {
            vm.members[member.id] = {};
            vm.members[member.id]['attendances'] = [attendance];
            vm.members[member.id]['name'] = member.full_name;
          }
        }
      });
    }
  }
})();
