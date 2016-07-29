/**
* ActiveSubstitutionFormController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('PendingSubstitutionFormController', PendingSubstitutionFormController);

  PendingSubstitutionFormController.$inject = ['$http'];

  /**
  * @namespace PendingSubstitutionFormController
  */
  function PendingSubstitutionFormController($http) {
    var vm = this;

    activate();

    function activate() {
      $http.get('/api/v1/pending_substitution_forms/').success(
        function(response) {
          vm.requestedSubstitutionForms = response['requested'];
          vm.receivedSubstitutionForms = response['received'];
        }
      );
    }
  }
})();
