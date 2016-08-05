/**
* BandController
* @namespace band-dash.members
*/
(function () {
  'use strict';

  angular
    .module('band-dash.members')
    .controller('BandController', BandController);

  BandController.$inject = ['$location', '$scope', 'Members', 'Snackbar'];

  /**
  * @namespace BandController
  */
  function BandController($location, $scope, Members, Snackbar) {
    var vm = this;

    vm.createBand = createBand;

    /**
    * @name createBand
    * @desc Create a band
    * @memberOf band-dash.members.BandController
    */
    function createBand() {
      Members.createBand(vm.identifier).then(createBandSuccessFn, createBandErrorFn);

      /**
      * @name createBandTypeSuccessFn
      * @desc Log that event type has been created successfully
      */
      function createBandSuccessFn(data, status, headers, config) {
        Snackbar.show('Band created successfully');
        vm.identifier = null;
      }

      /**
      * @name createBandTypeErrorFn
      * @desc Log error to the console
      */
      function createBandErrorFn(data, status, headers, config) {
        Snackbar.error("Can't create band");
      }
    }
  }
})();
