/**
* BandAssignmentController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('BandAssignmentController', BandAssignmentController);

  BandAssignmentController.$inject = ['$location', '$scope', '$http', 'Members'];

  /**
  * @namespace BandAssignmentController
  */
  function BandAssignmentController($location, $scope, $http, Members) {
    var vm = this;

    vm.updateBand = updateBand;

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.AttendanceController
    */
    function activate() {
      vm.bandSelected = false;

      $http.get('/api/v1/members/band/').success(function(response) {
        vm.bands = response;
      });

      $http.get('/api/v1/band_assignments/').success(function(response) {
        vm.assignments = response;
      });
    }

    function updateBand() {
      vm.bandSelected = true
      vm.assignedMembers = vm.assignments[vm.selectedBand].assigned;
      vm.unassignedMembers = vm.assignments[vm.selectedBand].unassigned;
    }
  }
})();
