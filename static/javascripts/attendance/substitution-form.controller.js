/**
* SubstitutionFormController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('SubstitutionFormController', SubstitutionFormController);

  SubstitutionFormController.$inject = ['$http', '$stateParams', 'Attendance', 'Snackbar'];

  /**
  * @namespace SubstitutionFormController
  */
  function SubstitutionFormController($http, $stateParams, Attendance, Snackbar) {
    var vm = this;

    vm.submitSubstitutionForm = submitSubstitutionForm;

    activate();

    function activate() {
      $http.get('/api/v1/get_unassigned_members/?event_id=' + $stateParams.event).success(
        function(response) {
          vm.unassignedMembers = response;
        }
      );

      $http.get('/api/v1/attendance/event/?id=' + $stateParams.event).success(
        function(response) {
          vm.event = response[0].title;
        }
      );
    }

    function submitSubstitutionForm() {
      if (!vm.selectedMember) {
        Snackbar.error("Please select a member to substitute for you");
        return;
      } else if (!vm.substitutionReason) {
        Snackbar.error("Please enter a substitution reason");
        return;
      }

      Attendance.submitSubstitutionForm(
        parseInt($stateParams.event),
        vm.selectedMember.id,
        vm.substitutionReason).then(submitSubstitutionFormSuccessFn, submitSubstitutionFormErrorFn);

      function submitSubstitutionFormSuccessFn(data, status, headers, config) {
        Snackbar.show('Substitution form submitted successfully');
        setTimeout(function() {
          window.location = "/events/all";
        }, 1500);
      }

      function submitSubstitutionFormErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.detail);
      }
    }
  }
})();
