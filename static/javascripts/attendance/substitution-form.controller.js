/**
* SubstitutionFormController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('SubstitutionFormController', SubstitutionFormController);

  SubstitutionFormController.$inject = ['$http', '$stateParams', 'Attendance'];

  /**
  * @namespace SubstitutionFormController
  */
  function SubstitutionFormController($http, $stateParams, Attendance) {
    var vm = this;

    vm.submitSubstitutionForm = submitSubstitutionForm;

    activate();

    function activate() {
      $http.get('/api/v1/get_unassigned_members/?event_id=' + $stateParams.event).success(
        function(response) {
          vm.unassignedMembers = response;
        }
      )
    }

    function submitSubstitutionForm() {
      Attendance.submitSubstitutionForm(
        parseInt($stateParams.event),
        vm.selectedMember.id,
        vm.substitutionReason);
    }
  }
})();
