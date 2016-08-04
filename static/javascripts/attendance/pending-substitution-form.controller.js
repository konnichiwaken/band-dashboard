/**
* ActiveSubstitutionFormController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('PendingSubstitutionFormController', PendingSubstitutionFormController);

  PendingSubstitutionFormController.$inject = ['$http', '$state', 'Attendance', 'Snackbar'];

  /**
  * @namespace PendingSubstitutionFormController
  */
  function PendingSubstitutionFormController($http, $state, Attendance, Snackbar) {
    var vm = this;

    vm.acceptSubstitution = acceptSubstitution;
    vm.declineSubstitution = declineSubstitution;

    activate();

    function activate() {
      $http.get('/api/v1/pending_substitution_forms/').success(
        function(response) {
          vm.requestedSubstitutionForms = response['requested'];
          vm.receivedSubstitutionForms = response['received'];
        }
      );
    }

    function acceptSubstitution(substitutionForm) {
      Attendance.acceptSubstitution(substitutionForm).then(
        acceptSubstitutionSuccessFn,
        acceptSubstitutionErrorFn);

      function acceptSubstitutionSuccessFn(data, status, headers, config) {
        Snackbar.show("Substitution form accepted");
        $state.reload();
      }

      function acceptSubstitutionErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.detail);
      }
    }

    function declineSubstitution(substitutionForm) {
      Attendance.declineSubstitution(substitutionForm).then(
        declineSubstitutionSuccessFn,
        declineSubstitutionErrorFn);

      function declineSubstitutionSuccessFn(data, status, headers, config) {
        Snackbar.show("Substitution form declined");
        $state.reload();
      }

      function declineSubstitutionErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.detail);
      }
    }
  }
})();
