/**
* BandAssignmentController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('BandAssignmentController', BandAssignmentController);

  BandAssignmentController.$inject = ['$location', '$scope', '$http', 'Members', 'Snackbar'];

  /**
  * @namespace BandAssignmentController
  */
  function BandAssignmentController($location, $scope, $http, Members, Snackbar) {
    var vm = this;

    vm.updateBand = updateBand;
    vm.assignMember = assignMember;
    vm.unassignMember = unassignMember;

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

    function assignMember(memberID) {
      $http.post('/api/v1/band_assignments/', {
        member: memberID,
        band: vm.selectedBand,
        action: 'assign'
      }).then(assignMemberSuccessFn, assignMemberErrorFn);

      function assignMemberSuccessFn(data, status, headers, config) {
        var memberIndex = -1;
        for (var i = 0; i < vm.assignments[vm.selectedBand].unassigned.length; i++) {
          if (vm.assignments[vm.selectedBand].unassigned[i].id == memberID) {
            memberIndex = i;
            break;
          }
        }

        if (memberIndex != -1) {
          var member = vm.assignments[vm.selectedBand].unassigned.splice(memberIndex, 1)[0];
          vm.assignments[vm.selectedBand].assigned.push(member);
        }
      }

      function assignMemberErrorFn(data, status, headers, config) {
        Snackbar.error('Unable to assign member');
      }
    }

    function unassignMember(memberID) {
      $http.post('/api/v1/band_assignments/', {
        member: memberID,
        band: vm.selectedBand,
        action: 'unassign'
      }).then(unassignMemberSuccessFn, unassignMemberErrorFn);

      function unassignMemberSuccessFn(data, status, headers, config) {
        var memberIndex = -1;
        for (var i = 0; i < vm.assignments[vm.selectedBand].assigned.length; i++) {
          if (vm.assignments[vm.selectedBand].assigned[i].id == memberID) {
            memberIndex = i;
            break;
          }
        }

        if (memberIndex != -1) {
          var member = vm.assignments[vm.selectedBand].assigned.splice(memberIndex, 1)[0];
          vm.assignments[vm.selectedBand].unassigned.push(member);
        }
      }

      function unassignMemberErrorFn(data, status, headers, config) {
        Snackbar.error('Unable to unassign member');
      }
    }
  }
})();
