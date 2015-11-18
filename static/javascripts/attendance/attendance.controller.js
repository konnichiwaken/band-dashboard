/**
* AttendanceController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('AttendanceController', AttendanceController);

  AttendanceController.$inject = ['$location', '$scope', '$http', 'Attendance'];

  /**
  * @namespace AttendanceController
  */
  function AttendanceController($location, $scope, $http, Attendance) {
    var vm = this;

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.AttendanceController
    */
    function activate() {
      $http.get('/api/v1/attendance/event/').success(function(response) {
        vm.events = response;
      });
    }
  }
})();
