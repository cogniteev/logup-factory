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
      'submit form.beta-access': 'requestBetaAccess',
      'click button.logout': 'logout'
    },
    extractFormData: function(form){
      var formData = {};
      $(form).serializeArray().forEach(function(input){
        formData[input.name] = input.value;
      });
      return formData;
    },
    login: function(e){
      e.preventDefault();
      $.ajax({
        url: '/login',
        data: this.extractFormData(e.currentTarget),
        method: 'POST',
        context: this,
        success: function(data){
          if (data.error) {
            //
          } else {
            document.location.href = '/app';
          }
        },
        error: function(res){
          var message = 'Something went wrong';
          console.log(message);
        }
      });
    },
    signup: function(e){
      e.preventDefault();
      $.ajax({
        url: '/signup',
        data: this.extractFormData(e.currentTarget),
        method: 'POST',
        context: this,
        success: function(res){
          if (res.error) {
            // show error
          } else {
            document.location.href = '/login';
          }
        },
        error: function(res){
          var message = 'Something went wrong';
          console.log(message);
        }
      });
    },
    forgotPassword: function(e){
      e.preventDefault();
      $.ajax({
        url: '/forgot-password',
        data: this.extractFormData(e.currentTarget),
        method: 'POST',
        context: this,
        success: function(res){
          if (res.error) {
            // show error
          } else {
            // notify user something happened
          }
        },
        error: function(res){
          var message = 'Something went wrong';
          console.log(message);
        }
      });
    },
    passwordReset: function(e){
      e.preventDefault();
      $.ajax({
        url: '/password-reset',
        data: this.extractFormData(e.currentTarget),
        method: 'POST',
        context: this,
        success: function(res){
          if (res.error) {
            // show error
          } else {
            // notify user something happened
          }
        },
        error: function(res){
          var message = 'Something went wrong';
          console.log(message);
        }
      });
    },
    logout: function(e){
      e.preventDefault();
      $.ajax({
        url: '/logout',
        method: 'GET',
        context: this,
        success: function(res){
          if (res.error) {
            // show error
          } else {
            document.location.href = '/';
          }
        },
        error: function(res){
          var message = 'Something went wrong';
          console.log(message);
        }
      });
    },
    requestBetaAccess: function(e){
      e.preventDefault();
      $.ajax({
        url: '/request-beta-access',
        method: 'POST',
        context: this,
        success: function(res){
          if (res.error) {
            // show error
          } else {
            // notify user something happened
          }
        },
        error: function(res){
          var message = 'Something went wrong';
          console.log(message);
        }
      });
    }
  });
  return new Toolbelt();
});
