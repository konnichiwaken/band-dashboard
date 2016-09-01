/**
* EditAccountController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('EditAccountController', EditAccountController);

  EditAccountController.$inject = ['$http', '$stateParams'];

  /**
  * @namespace EditAccountController
  */
  function EditAccountController($http, $stateParams) {
    var vm = this;

    activate();

    function activate() {
      $http.get('/api/v1/accounts/' + $stateParams.account + '/').success(function(response) {
        vm.account = response;
      });
    }
  }
})();
