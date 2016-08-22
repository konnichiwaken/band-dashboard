(function () {
  'use strict';

  angular
    .module('band-dash.authentication', ['ngCookies'])
    .run(run);

  function run(PermissionStore, RoleStore, Authentication, $filter) {
    RoleStore
      .defineRole('director', function() {
        if (Authentication.isAuthenticated()) {
          var account = Authentication.getAuthenticatedAccount();
          if (account.is_registered) {
            for (var i = 0; i < account.roles.length; i++) {
              var role = account.roles[i];
              if ($filter('lowercase')(role) === 'director') {
                return true;
              }
            }
          }
        }

        return false;
      });

    RoleStore
      .defineRole('president', function() {
        if (Authentication.isAuthenticated()) {
          var account = Authentication.getAuthenticatedAccount();
          if (account.is_registered) {
            for (var i = 0; i < account.roles.length; i++) {
              var role = account.roles[i];
              if ($filter('lowercase')(role) === 'president') {
                return true;
              }
            }
          }
        }

        return false;
      });

    RoleStore
      .defineRole('secretary', function() {
        if (Authentication.isAuthenticated()) {
          var account = Authentication.getAuthenticatedAccount();
          if (account.is_registered) {
            for (var i = 0; i < account.roles.length; i++) {
              var role = account.roles[i];
              if ($filter('lowercase')(role) === 'secretary') {
                return true;
              }
            }
          }
        }

        return false;
      });

    PermissionStore
      .definePermission('isAuthenticated', function() {
        return Authentication.isAuthenticated();
      });

    PermissionStore
      .definePermission('isRegistered', function() {
        var account = Authentication.getAuthenticatedAccount();
        if (account) {
          return account.is_registered;
        } else {
          return false;
        }
      });
  }
})();
