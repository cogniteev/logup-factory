'use strict'

module.exports = function(grunt){

  require('load-grunt-tasks')(grunt);

  var buildConfig = {
    src: 'src',
    dist: 'dist'
  };

  grunt.initConfig({
    buildConfig: buildConfig,
    stylus: {
      compile: {
        options: {
          paths: [ '<%= buildConfig.src %>/styl' ],
          use: [ require('nib'), require('stylus-brandcolors'), require('stylus-mrmrscolors') ]
        },
        files: {
          '<%= buildConfig.dist %>/css/index.css': '<%= buildConfig.src %>/styl/index.styl'
        }
      }
    },
    copy: {
      bower: {
        files: [
          {
            expand: true,
            cwd: 'bower_components',
            src: [
              'underscore/underscore.js',
              'backbone/backbone.js',
              'jquery/dist/jquery.min.js',
              'jquery/dist/jquery.min.map',
              'requirejs/require.js',
              'requirejs-domready/domReady.js'
            ],
            dest: '<%= buildConfig.dist %>/js/lib',
            flatten: true
          },
          {
            expand: true,
            cwd: 'bower_components/fontawesome',
            src: [
              'css/font-awesome.min.css',
              'fonts/**/*'
            ],
            dest: '<%= buildConfig.dist %>'
          }
        ]
      },
      code: {
        expand: true,
        cwd: '<%= buildConfig.src %>/js',
        src: '**/*.js',
        dest: '<%= buildConfig.dist %>/js'
      }
    },
    clean: {
      dist: [
        '<%= buildConfig.dist %>/css',
        '<%= buildConfig.dist %>/js'
      ]
    },
    watch: {
      styl: {
        files: '<%= buildConfig.src %>/css/styl/**/*',
        tasks: [ 'stylus' ]
      },
      bower: {
        files: '<%= buildConfig.src %>/js/bower_components',
        tasks: [ 'copy:bower' ]
      }
    }
  });

  grunt.registerTask('default', [
    'clean:dist',
    'copy',
    'stylus'
  ]);
};
