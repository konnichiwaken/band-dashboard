/**
* Register controller
* @namespace band-dash.authentication
*/
(function () {
  'use strict';

  angular
    .module('band-dash.authentication')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $scope, Authentication) {
    var vm = this;

    vm.addAccountRow = addAccountRow;
    vm.createAccounts = createAccounts;

    activate();

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     * @memberOf thinkster.authentication.controllers.RegisterController
     */
    function activate() {
      vm.accounts = [];
      vm.addAccountRow();
    }

    function addAccountRow() {
      vm.accounts.push({'first_name': "", 'last_name': "", 'email': "", 'section': ""});
    }

    function createAccounts() {
      Authentication.createAccounts(vm.accounts);
    }
  }
})();
