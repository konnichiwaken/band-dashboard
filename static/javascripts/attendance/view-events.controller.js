/**
* AllEventsController
* @namespace band-dash.attendance
*/
(function () {
  'use strict';

  angular
    .module('band-dash.attendance')
    .controller('AllEventsController', AllEventsController);

  AllEventsController.$inject = ['$location', '$scope', '$http'];

  /**
  * @namespace AllEventsController
  */
  function AllEventsController($location, $scope, $http) {
    var vm = this;

    activate()

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf band-dash.attendance.AllEventsController
    */
    function activate() {
      $http.get('/api/v1/attendance/event/').success(function(response) {
        vm.events = response;
      });
    }
  }
})();
