/**
* BandController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('BandController', BandController);

  BandController.$inject = ['$location', '$scope', 'Members'];

  /**
  * @namespace BandController
  */
  function BandController($location, $scope, Members) {
    var vm = this;

    vm.createBand = createBand;

    /**
    * @name createBand
    * @desc Create a band
    * @memberOf band-dash.members.BandController
    */
    function createBand() {
      Members.createBand(vm.identifier);
    }
  }
})();
