/**
* NavbarController
* @namespace band-dash.layout
*/
(function () {
  'use strict';

  angular
    .module('band-dash.layout')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['$scope', 'Authentication'];

  /**
  * @namespace NavbarController
  */
  function NavbarController($scope, Authentication) {
    var vm = this;

    vm.logout = logout;

    /**
    * @name logout
    * @desc Log the user out
    * @memberOf band-dash.layout.NavbarController
    */
    function logout() {
      Authentication.logout();
    }
  }
})();
