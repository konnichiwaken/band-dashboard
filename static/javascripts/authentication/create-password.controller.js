/**
* Register controller
* @namespace band-dash.authentication
*/
(function () {
  'use strict';

  angular
    .module('band-dash.authentication')
    .controller('CreatePasswordController', CreatePasswordController);

  CreatePasswordController.$inject = ['$location', '$scope', '$stateParams', 'Authentication', 'Snackbar'];

  /**
  * @namespace CreatePasswordController
  */
  function CreatePasswordController($location, $scope, $stateParams, Authentication, Snackbar) {
    var vm = this;

    vm.createPassword = createPassword;

    function createPassword() {
      if (!vm.password) {
        Snackbar.error("Please enter a password");
      } else if (!vm.confirmPassword) {
        Snackbar.error("Please confirm your password");
      } else if (vm.password !== vm.confirmPassword) {
        Snackbar.error("Passwords did not match");
      } else {
        Authentication.createPassword(vm.email, vm.password);
      }
    }
  }
})();
