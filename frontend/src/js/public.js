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
      'click a.logout': 'logout'
    },
    extractFormData: function(form){
      var data = {};
      $(form).serializeArray().forEach(function(input){
        if (input.name === 'email') {
          data[input.name] = input.value.trim();
        } else {
          data[input.name] = input.value;
        }
      });
      return data;
    },
    login: function(e){
      var data = this.extractFormData(e.currentTarget)
        , action = $(e.currentTarget).attr('action');

      e.preventDefault();
      if (data.email.length > 0 && data.password.length > 0) {
        $.ajax({
          url: action,
          data: data,
          method: 'POST',
          context: this,
          success: function(res){
            var $el = $(e.currentTarget);
            if (res.error) {
              if ($el.find('.error').length === 0) {
                $el.prepend('<p class="error">' + res.error + '</p>');
              } else {
                $el.find('.error').html(res.error);
              }
            } else {
              document.location.href = '/app';
            }
          },
          error: function(res){
            var message = 'Something went wrong';
            console.log(message);
          }
        });
      }
    },
    signup: function(e){
      var data = this.extractFormData(e.currentTarget)
        , action = $(e.currentTarget).attr('action');

      e.preventDefault();
      if (data.email.length > 0 && data.password.length > 0) {
        $.ajax({
          url: action,
          data: data,
          method: 'POST',
          context: this,
          success: function(res){
            var $el = $(e.currentTarget);
            if (res.error) {
              if ($el.find('.error').length === 0) {
                $el.prepend('<p class="error">' + res.error + '</p>');
              } else {
                $el.find('.error').html(res.error);
              }
            } else {
              document.location.href = '/login';
            }
          },
          error: function(res){
            var message = 'Something went wrong';
            console.log(message);
          }
        });
      }
    },
    forgotPassword: function(e){
      var data = this.extractFormData(e.currentTarget)
        , action = $(e.currentTarget).attr('action');

      e.preventDefault();
      if (data.email.length > 0) {
        $.ajax({
          url: action
          data: this.extractFormData(e.currentTarget),
          method: 'POST',
          context: this,
          success: function(res){
            var $el = $(e.currentTarget);
            if (res.error) {
              if ($el.find('.error').length === 0) {
                $el.prepend('<p class="error">' + res.error + '</p>');
              } else {
                $el.find('.error').html(res.error);
              }
            } else {
              $(e.currentTarget).html('form processed, check your emails');
            }
          },
          error: function(res){
            var message = 'Something went wrong';
            console.log(message);
          }
        });
      }
    },
    passwordReset: function(e){
      var data = this.extractFormData(e.currentTarget)
        , action = $(e.currentTarget).attr('action');

      e.preventDefault();
      if (data.password.length > 0) {
        $.ajax({
          url: action,
          data: this.extractFormData(e.currentTarget),
          method: 'POST',
          context: this,
          success: function(res){
            var $el = $(e.currentTarget);
            if (res.error) {
              if ($el.find('.error').length === 0) {
                $el.prepend('<p class="error">' + res.error + '</p>');
              } else {
                $el.find('.error').html(res.error);
              }
            } else {
              $(e.currentTarget).html('password was reset, redirecting to /login');
              setTimeout(function(){ document.location.href = '/login'; }, 3000);
            }
          },
          error: function(res){
            var message = 'Something went wrong';
            console.log(message);
          }
        });
      }
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
      var data = this.extractFormData(e.currentTarget)
        , action = $(e.currentTarget).attr('action');

      e.preventDefault();
      if (data.email.length > 0) {
        $.ajax({
          url: action,
          data: data,
          method: 'POST',
          context: this,
          success: function(res){
            var $el = $(e.currentTarget);
            if (res.error) {
              if ($el.find('.error').length === 0) {
                $el.prepend('<p class="error">' + res.error + '</p>');
              } else {
                $el.find('.error').html(res.error);
              }
            } else {
              $(e.currentTarget).html('successfully registered to beta access');
            }
          },
          error: function(res){
            var message = 'Something went wrong';
            console.log(message);
          }
        });
      }
    }
  });
  return new Toolbelt();
});
