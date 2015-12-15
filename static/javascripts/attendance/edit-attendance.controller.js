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

    vm.submitOnTime = submitOnTime;
    vm.submitLate = submitLate;
    vm.addUnassignedMember = addUnassignedMember;

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.EditAttendanceController
    */
    function activate() {
      vm.assignedAttendances = [];
      vm.unassignedAttendances = [];
      $http.get('/api/v1/attendance/event/?id=' + $routeParams.event).success(
        function(response) {
          vm.event = response[0];

          $http.get('/api/v1/attendance/event_attendance/?event_id=' + $routeParams.event).success(
            function(response) {
              for (var i = 0; i < response.length; i++) {
                if (response[i].check_in_time) {
                  response[i].check_in_time = new Date(response[i].check_in_time);
                }
                determineAttendanceStatus(response[i]);
                if (response[i].assigned) {
                  vm.assignedAttendances.push(response[i]);
                } else {
                  vm.unassignedAttendances.push(response[i]);
                }
              }
            }
          );
        }
      );

      $http.get('/api/v1/members/unassigned/?event_id=' + $routeParams.event).success(
        function(response) {
          vm.unassignedMembers = response;
        }
      );
    }

    function submitOnTime(attendance) {
      Attendance.submitOnTime(attendance).then(function(success) {
        if (success) {
          attendance.check_in_time = null;
          attendance.status = 'On time';
        }
      });
    }

    function submitLate(attendance) {
      Attendance.submitLate(attendance).then(function(new_attendance) {
        if (new_attendance) {
          attendance.check_in_time = new Date(new_attendance.check_in_time);
          attendance.points = new_attendance.points;
          determineAttendanceStatus(attendance);
        }
      });
    }

    function addUnassignedMember() {
      var unassignedAttendance = [];
      unassignedAttendance.member = angular.copy(vm.unassignedMember);
      vm.unassignedAttendances.push(unassignedAttendance);
      var index = vm.unassignedMembers.indexOf(vm.unassignedMember);
      vm.unassignedMembers.splice(index, 1);
    }

    function determineAttendanceStatus(attendance) {
      if (attendance.points) {
        if (attendance.check_in_time) {
          var eventTime = new Date(vm.event.time);
          var timeDelta = attendance.check_in_time - eventTime;
          var minutesLate = Math.round((timeDelta / 1000) / 60);
          var minutesLateFifteen = Math.ceil(minutesLate / 15) * 15;
          attendance.status = minutesLateFifteen.toString().concat(' minutes late');
        } else {
          attendance.status = 'On time';
        }
      }
    }
  }
})();
