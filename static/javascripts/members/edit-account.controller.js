/**
* EditAccountController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('EditAccountController', EditAccountController);

  EditAccountController.$inject = ['$http', '$stateParams', 'Members'];

  /**
  * @namespace EditAccountController
  */
  function EditAccountController($http, $stateParams, Members) {
    var vm = this;

    vm.editAccount = editAccount;

    activate();

    function activate() {
      $http.get('/api/v1/accounts/' + $stateParams.account + '/').success(function(response) {
        vm.account = response;
      });
    }

    function editAccount() {
      Members.editMember(vm.account.band_member);
    }
  }
})();
