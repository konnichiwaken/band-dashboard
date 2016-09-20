/**
* EditAccountController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('EditAccountController', EditAccountController);

  EditAccountController.$inject = ['$http', '$stateParams', 'Authentication', 'Members'];

  /**
  * @namespace EditAccountController
  */
  function EditAccountController($http, $stateParams, Authentication, Members) {
    var vm = this;

    vm.editAccount = editAccount;
    vm.sections = [
      {value: 'bass', name: 'Bass'},
      {value: 'clarinet', name: 'Clarinet'},
      {value: 'drumline', name: 'Drumline'},
      {value: 'flute', name: 'Flute'},
      {value: 'mellophone', name: 'Mellophone'},
      {value: 'saxophone', name: 'Saxophone'},
      {value: 'trombone', name: 'Trombone'},
      {value: 'trumpet', name: 'Trumpet'},
    ];

    activate();

    function activate() {
      $http.get('/api/v1/accounts/' + $stateParams.account + '/').success(function(response) {
        vm.account = response;
        vm.firstName = vm.account.first_name;
      });
    }

    function editAccount() {
      Members.editMember(vm.account.band_member);
      Authentication.editAccount(vm.account);
      vm.firstName = vm.account.first_name;
    }
  }
})();
