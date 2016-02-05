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
    'Attendance',
    'Snackbar'
  ];

  /**
  * @namespace EditAttendanceController
  */
  function EditAttendanceController(
    $location,
    $scope,
    $http,
    $routeParams,
    Attendance,
    Snackbar) {
    var vm = this;

    vm.submitOnTime = submitOnTime;
    vm.submitLate = submitLate;
    vm.submitAbsence = submitAbsence;
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
                Attendance.determineAttendanceStatus(response[i], vm.event);
                if (response[i].assigned) {
                  if (!response[i].unexcused) {
                    response[i].unexcused = false;
                  }

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
      attendance.unexcused = false;
      attendance.is_absence = false;
      if (!attendance.assigned) {
        attendance.event_id = vm.event.id;
        attendance.member_id = attendance.member.id;
      }

      Attendance.submitOnTime(attendance).then(submitOnTimeSuccessFn, submitOnTimeErrorFn);

      /**
      * @name submitOnTimeSuccessFn
      * @desc Log that on time attendance has been submitted successfully
      */
      function submitOnTimeSuccessFn(data, status, headers, config) {
        var newAttendance = data.data;
        if (newAttendance) {
          attendance.check_in_time = null;
          attendance.status = 'On time';
          if (!attendance.id) {
            attendance.id = newAttendance.id;
          }
        }

        Snackbar.show('Attendance submitted successfully');
      }

      /**
      * @name submitOnTimeErrorFn
      * @desc Log that error occurred when submitting on time attendance
      */
      function submitOnTimeErrorFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }
    }

    function submitLate(attendance) {
      attendance.is_absence = false;
      if (!attendance.assigned) {
        attendance.event_id = vm.event.id;
        attendance.member_id = attendance.member.id;
      }

      Attendance.submitLate(attendance).then(submitLateSuccessFn, submitLateErrorFn);

      /**
      * @name submitLateSuccessFn
      * @desc Log that late attendance has been submitted successfully
      */
      function submitLateSuccessFn(data, status, headers, config) {
        var newAttendance = data.data;
        if (newAttendance) {
          attendance.check_in_time = new Date(newAttendance.check_in_time);
          attendance.points = newAttendance.points;
          Attendance.determineAttendanceStatus(attendance, vm.event);
          if (!attendance.id) {
            attendance.id = newAttendance.id;
          }
        }

        Snackbar.show('Attendance submitted successfully');
      }

      /**
      * @name submitLateErrorFn
      * @desc Log that error occurred when submitting late attendance
      */
      function submitLateErrorFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }
    }

    function submitAbsence(attendance) {
      attendance.is_absence = true;
      attendance.event_id = vm.event.id;
      attendance.member_id = attendance.member.id;

      Attendance.submitAbsence(attendance).then(submitAbsenceSuccessFn, submitAbsenceErrorFn);

      /**
      * @name submitAbsenceSuccessFn
      * @desc Log that on time attendance has been submitted successfully
      */
      function submitAbsenceSuccessFn(data, status, headers, config) {
        var newAttendance = data.data;
        if (newAttendance) {
          attendance.check_in_time = null;
          attendance.status = 'Absent';
          if (!attendance.id) {
            attendance.id = newAttendance.id;
          }
        }

        Snackbar.show('Absence submitted successfully');
      }

      /**
      * @name submitAbsenceErrorFn
      * @desc Log that error occurred when submitting on time attendance
      */
      function submitAbsenceErrorFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }
    }

    function addUnassignedMember() {
      var unassignedAttendance = {};
      unassignedAttendance.member = angular.copy(vm.unassignedMember);
      unassignedAttendance.assigned = false;
      vm.unassignedAttendances.push(unassignedAttendance);
      var index = vm.unassignedMembers.indexOf(vm.unassignedMember);
      vm.unassignedMembers.splice(index, 1);
    }
  }
})();
