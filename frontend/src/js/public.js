requirejs.config({
  baseUrl: '/js/lib',
  shim: {
    jquery: { exports: 'jQuery' },
    underscore: { exports: '_' },
    backbone: {
      deps: [ 'underscore', 'jquery' ],
      exports: 'Backbone'
    }
  },
  paths: {
    jquery: 'jquery.min'
  }
});

requirejs([
  'underscore',
  'jquery',
  'backbone',
  'domReady!'
], function(_, $, Backbone){
  var Toolbelt = Backbone.View.extend({
    el: 'body',
    events: {
      'submit form.login': 'login',
      'submit form.signup': 'signup',
      'submit form.forgot-password': 'forgotPassword',
      'submit form.password-reset': 'passwordReset',
      'click button.logout': 'logout'
    },
    login: function(e){
      e.preventDefault();
      console.log('login');
    },
    signup: function(e){
      e.preventDefault();
      console.log('signup');
    },
    forgotPassword: function(e){
      e.preventDefault();
      console.log('forgotPassword');
    },
    passwordReset: function(e){
      e.preventDefault();
      console.log('passwordReset');
    },
    logout: function(e){
      e.preventDefault();
      console.log('logout');
    }
  });
  return new Toolbelt();
});
