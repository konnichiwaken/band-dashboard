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

    activate();

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     * @memberOf band-dash.authentication.CreatePasswordController
     */
    function activate() {
      var token = $stateParams.token;
      Authentication.confirmAccount(token).then(function(email) {
        vm.email = email;
      });
    }

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