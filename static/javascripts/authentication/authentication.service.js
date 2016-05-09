/**
* Authentication
* @namespace band-dash.authentication
*/
(function () {
  'use strict';

  angular
    .module('band-dash.authentication')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http', 'Snackbar'];

  /**
  * @namespace Authentication
  * @returns {Factory}
  */
  function Authentication($cookies, $http, Snackbar) {
    /**
    * @name Authentication
    * @desc The Factory to be returned
    */
    var Authentication = {
      register: register,
      login: login,
      logout: logout,
      getAuthenticatedAccount: getAuthenticatedAccount,
      isAuthenticated: isAuthenticated,
      setAuthenticatedAccount: setAuthenticatedAccount,
      unauthenticate: unauthenticate
    };

    return Authentication;

    ////////////////////

    /**
    * @name register
    * @desc Try to register a new user
    * @param {string} email The email entered by the user
    * @param {string} password The password entered by the user
    * @param {string} username The username entered by the user
    * @param {string} section The section entered by the user
    * @param {string} instrument_number The instrument number entered by the user
    * @returns {Promise}
    * @memberOf band-dash.authentication.Authentication
    */
    function register(email, password, first_name, last_name, section, instrument_number) {
      return $http.post('/api/v1/accounts/', {
        email: email,
        password: password,
        first_name: first_name,
        last_name: last_name,
        band_member: {
          section: section,
          instrument_number: instrument_number
        }
      }).then(registerSuccessFn, registerErrorFn);

      /**
      * @name registerSuccessFn
      * @desc Log the new user in
      */
      function registerSuccessFn(data, status, headers, config) {
        Snackbar.show('Account created successfully');
      }

      /**
      * @name registerErrorFn
      * @desc Log that there was a failure when attempting to register a new user
      */
      function registerErrorFn(data, status, headers, config) {
        Snackbar.error('Couldn\'t register');
      }
    }

    /**
     * @name login
     * @desc Try to log in with email `email` and password `password`
     * @param {string} email The email entered by the user
     * @param {string} password The password entered by the user
     * @returns {Promise}
     * @memberOf band-dash.authentication.Authentication
     */
    function login(email, password) {
      return $http.post('/api/v1/auth/login/', {
        email: email,
        password: password
      }).then(loginSuccessFn, loginErrorFn);

      /**
       * @name loginSuccessFn
       * @desc Set the authenticated account and redirect to index
       */
      function loginSuccessFn(data, status, headers, config) {
        Authentication.setAuthenticatedAccount(data.data);
        window.location = '/attendance/members/all';
      }

      /**
       * @name loginErrorFn
       * @desc Log that there was a login failure
       */
      function loginErrorFn(data, status, headers, config) {
        Snackbar.error('Couldn\'t log in with supplied credentials');
      }
    }

    /**
     * @name logout
     * @desc Try to log the user out
     * @returns {Promise}
     * @memberOf band-dash.authentication.Authentication
     */
    function logout() {
      return $http.post('/api/v1/auth/logout/')
        .then(logoutSuccessFn, logoutErrorFn);

      /**
       * @name logoutSuccessFn
       * @desc Unauthenticate and redirect to index with page reload
       */
      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();
        window.location = '/';
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Error when logging out" to the console
       */
      function logoutErrorFn(data, status, headers, config) {
        Snackbar.error('Can\'t log out');
      }
    }

    /**
     * @name getAuthenticatedAccount
     * @desc Return the currently authenticated account
     * @returns {object|undefined} Account if authenticated, else `undefined`
     * @memberOf thinkster.authentication.Authentication
     */
    function getAuthenticatedAccount() {
      var authenticatedAccount = $cookies.getObject('authenticatedAccount');
      if (!authenticatedAccount) {
        return;
      }

      return authenticatedAccount;
    }

    /**
     * @name isAuthenticated
     * @desc Check if the current user is authenticated
     * @returns {boolean} True is user is authenticated, else false.
     * @memberOf band-dash.authentication.Authentication
     */
    function isAuthenticated() {
      return !!$cookies.get('authenticatedAccount');
    }

    /**
     * @name setAuthenticatedAccount
     * @desc Stringify the account object and store it in a cookie
     * @param {Object} user The account object to be stored
     * @returns {undefined}
     * @memberOf band-dash.authentication.Authentication
     */
    function setAuthenticatedAccount(account) {
      $cookies.putObject('authenticatedAccount', account);
    }

    /**
     * @name unauthenticate
     * @desc Delete the cookie where the user object is stored
     * @returns {undefined}
     * @memberOf band-dash.authentication.Authentication
     */
    function unauthenticate() {
      $cookies.remove('authenticatedAccount');
    }
  }
})();
