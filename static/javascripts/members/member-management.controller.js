/**
* MemberManagementController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('MemberManagementController', MemberManagementController);

  MemberManagementController.$inject = ['$http'];

  /**
  * @namespace MemberManagementController
  */
  function MemberManagementController($http) {
    var vm = this;

    activate();

    function activate() {
      $http.get('/api/v1/accounts/').success(function(response) {
        vm.accounts = response;
      });
    }
  }
})();
