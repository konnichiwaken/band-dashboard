/**
* Create accounts controller
* @namespace band-dash.authentication
*/
(function () {
  'use strict';

  angular
    .module('band-dash.authentication')
    .controller('CreateAccountsController', CreateAccountsController);

  CreateAccountsController.$inject = ['$location', '$scope', 'Authentication', 'Snackbar'];

  /**
  * @namespace CreateAccountsController
  */
  function CreateAccountsController($location, $scope, Authentication, Snackbar) {
    var vm = this;

    vm.addAccountRow = addAccountRow;
    vm.createAccounts = createAccounts;

    activate();

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     * @memberOf thinkster.authentication.controllers.CreateAccountsController
     */
    function activate() {
      vm.accounts = [];
      vm.addAccountRow();
    }

    function addAccountRow() {
      vm.accounts.push({'first_name': "", 'last_name': "", 'email': "", 'section': "", 'instrument_number': ""});
    }

    function createAccounts() {
      var accounts = vm.accounts.slice(0);
      var row_number = 1;
      for (var i = 0; i < accounts.length; i++) {
        var account = accounts[i];
        if (!account.first_name && !account.last_name && !account.email && !account.section) {
          accounts.splice(i, 1);
          i--;
        } else if (!account.first_name) {
          Snackbar.error("Please enter a first name for account in row " + row_number);
          return;
        } else if (!account.last_name) {
          Snackbar.error("Please enter a last name for account in row " + row_number);
          return;
        } else if (!account.email) {
          Snackbar.error("Please enter an email for account in row " + row_number);
          return;
        } else if (!account.section) {
          Snackbar.error("Please enter a section for account in row " + row_number);
          return;
        }

        row_number++;
      }

      if (!accounts.length) {
        Snackbar.error("Please enter at least one account to create");
        return;
      }

      Authentication.createAccounts(accounts).then(createAccountsSuccessFn, createAccountsErrorFn);

      /**
      * @name createAccountsSuccessFn
      * @desc Reset account creation table
      */
      function createAccountsSuccessFn(data, status, headers, config) {
        Snackbar.show("Accounts created successfully");
        vm.accounts = [];
        vm.addAccountRow();
      }

      /**
      * @name createAccountsErrorFn
      * @desc Log that there was a failure when attempting to create accounts
      */
      function createAccountsErrorFn(data, status, headers, config) {
        Snackbar.error("Couldn't create accounts");
      }
    }
  }
})();
