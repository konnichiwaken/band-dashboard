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
      createAccounts: createAccounts,
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
    * @name createAccounts
    * @desc Try to create a number of accounts
    * @param {array} accounts The accounts to create
    * @returns {Promise}
    * @memberOf band-dash.authentication.Authentication
    */
    function createAccounts(accounts) {
      return $http.post('/api/v1/create_accounts/', {
        accounts: accounts,
      }).then(createAccountsSuccessFn, createAccountsErrorFn);

      /**
      * @name createAccountsSuccessFn
      * @desc Log the new user in
      */
      function createAccountsSuccessFn(data, status, headers, config) {
        Snackbar.show('Accounts created successfully');
      }

      /**
      * @name createAccountsErrorFn
      * @desc Log that there was a failure when attempting to register a new user
      */
      function createAccountsErrorFn(data, status, headers, config) {
        Snackbar.error('Couldn\'t create accounts');
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
