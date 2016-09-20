/**
* EditAccountController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('EditAccountController', EditAccountController);

  EditAccountController.$inject = [
    '$http',
    '$q',
    '$stateParams',
    'Authentication',
    'Members',
    'Snackbar',
  ];

  /**
  * @namespace EditAccountController
  */
  function EditAccountController($http, $q, $stateParams, Authentication, Members, Snackbar) {
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
      var account_id = parseInt($stateParams.account);
      if (Authentication.getAuthenticatedAccount().id === account_id) {
        vm.isEditingSelf = true;
      } else {
        vm.isEditingSelf = false;
      }

      $http.get('/api/v1/accounts/' + account_id + '/').success(function(response) {
        vm.account = response;
        vm.firstName = vm.account.first_name;
      });
    }

    function editAccount() {
      var error = '';
      if ((vm.password || vm.confirmedPassword) && vm.password !== vm.confirmedPassword) {
        error = 'Password and confirmed password do not match';
      } else if (!vm.account.first_name) {
        error = 'Please enter a first name';
      } else if (!vm.account.last_name) {
        error = 'Please enter a last name';
      } else if (!vm.account.email) {
        error = 'Please enter an email';
      }

      if (error) {
        Snackbar.error(error);
        return;
      }

      var editMemberPromise = Members.editMember(vm.account.band_member);
      var editAccountPromise = Authentication.editAccount(vm.account, vm.password);
      $q.all([editMemberPromise, editAccountPromise]).then(function() {
        vm.firstName = vm.account.first_name;
        Snackbar.show(`Successfully updated ${vm.account.first_name}'s information`);
      }).catch(function() {
        Snackbar.error(`Was not able to update ${vm.account.first_name}'s information`);
      });
    }
  }
})();
