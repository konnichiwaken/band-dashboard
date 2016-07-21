/**
* SubstitutionFormController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('SubstitutionFormController', SubstitutionFormController);

  SubstitutionFormController.$inject = ['$http', '$stateParams'];

  /**
  * @namespace SubstitutionFormController
  */
  function SubstitutionFormController($http, $stateParams) {
    var vm = this;

    activate();

    function activate() {
      $http.get('/api/v1/get_unassigned_members/?event_id=' + $stateParams.event).success(
        function(response) {
          vm.unassignedMembers = response;
        }
      )
    }
  }
})();
